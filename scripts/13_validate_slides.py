#!/usr/bin/env python3
"""
13_validate_slides.py — Per slide: validate the vision analysis with glm-5.3 (text-only).

glm-5.3 receives the extracted analysis JSON and checks it for:
  - required fields present and non-empty
  - internal consistency (title matches verbatim text, layout regions cover elements)
  - precision (no vague quantifiers like "several"/"some" where counts are needed)
  - PowerPoint-recreation readiness (the recreation_brief + layout suffice to rebuild it)
It returns a corrected FINAL JSON (same schema + "validation" block). Output:
    analysis/slide_XXX_final.json, analysis/slides_final.json, analysis/summary.md

Environment:
    IR_BASE_URL  (default http://localhost:17844/v1 — the local IronRouter dist)
    IR_API_KEY   (default: read from <project>/.analyze-image-key)
    IR_TEXT_MODEL (default "glm-5.3")

Usage:
    python3 13_validate_slides.py <analysis_dir> [--slides 10]
"""

import argparse
import glob
import json
import os
import re
import sys
import time

import openai

VALIDATION_PROMPT = """\
You are a strict QA reviewer for presentation content extraction. You are given the JSON \
analysis of ONE slide (extracted from a course video by a vision model). You CANNOT see the \
image — your job is to validate the JSON itself as the single source of truth for later \
recreating this slide in PowerPoint.

Check and fix:
1. SCHEMA: every required field present and non-empty: slide_title, verbatim_text.bullets, \
layout.arrangement, layout.regions, visual_elements, colors, recreation_brief. Fill any \
missing field with your best reconstruction from the other fields (never leave null/empty \
unless truly absent from the source).
2. CONSISTENCY: title/subtitle must agree with bullets and labels; layout.regions must cover \
every element mentioned in visual_elements and verbatim_text; the recreation_brief must \
reference the same texts and elements (no contradictions, no invented content).
3. PRECISION: replace vague quantifiers ("several", "some", "many", "a few", "various") with \
exact counts from the JSON; make every sentence concretely actionable for a slide builder.
4. RECREATABILITY: rewrite recreation_brief as an ordered, numbered checklist where each step \
places one element: exact text, position, color, and shape/chart type. Someone following it \
must reproduce the slide without asking questions.
5. Do NOT invent facts not derivable from the JSON. If something is genuinely marked [?], keep \
the marker and list it in validation.uncertain_items.

Respond with a SINGLE valid JSON object (no markdown fences, no commentary):
{
  "slide_title": ..., "subtitle_or_header": ..., "verbatim_text": ..., "layout": ...,
  "visual_elements": ..., "imagery": ..., "colors": ..., "typography_notes": ...,
  "animation_state": ...,
  "recreation_brief": "<the rewritten numbered checklist>",
  "validation": {
    "verdict": "<PASS | PASS_WITH_FIXES | FAIL>",
    "fixes_applied": ["<each concrete fix>"],
    "uncertain_items": ["<anything marked [?] or unverifiable>"],
    "recreatability_score_1_to_10": <number>
  }
}

SLIDE ANALYSIS JSON TO VALIDATE:
"""


def extract_json(text: str) -> dict:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    else:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            text = text[start : end + 1]
    return json.loads(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis_dir")
    parser.add_argument("--slides", type=int, default=10)
    parser.add_argument("--model", default=os.environ.get("IR_TEXT_MODEL", "glm-5.3"))
    args = parser.parse_args()

    base_url = os.environ.get("IR_BASE_URL", "http://localhost:17844/v1")
    api_key = os.environ.get("IR_API_KEY")
    if not api_key:
        key_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".analyze-image-key")
        if os.path.exists(key_file):
            api_key = open(key_file).read().strip()
    if not api_key:
        sys.exit("IR_API_KEY env var required (or create .analyze-image-key in the project root)")

    analysis_dir = os.path.abspath(args.analysis_dir)
    raw_files = sorted(glob.glob(os.path.join(analysis_dir, "slide_*_raw.json")))[: args.slides]
    if not raw_files:
        sys.exit(f"no slide_*_raw.json in {analysis_dir} — run 12_analyze_slides.py first")

    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    finals = []
    for rf in raw_files:
        out_file = rf.replace("_raw.json", "_final.json")
        if os.path.exists(out_file):
            print(f"{os.path.basename(rf)}: already validated, skipping")
            finals.append(json.load(open(out_file)))
            continue
        raw = json.load(open(rf))
        print(f"{os.path.basename(rf)}: validating with {args.model} ...", flush=True)
        t0 = time.time()
        try:
            resp = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": VALIDATION_PROMPT + json.dumps(raw, indent=1)}],
                max_tokens=16000,
                temperature=0.1,
                stream=True,  # streaming avoids the upstream gateway's 60s non-streaming cut
            )
            parts = []
            for chunk in resp:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    parts.append(chunk.choices[0].delta.content)
            parsed = extract_json("".join(parts))
            parsed["_meta"] = raw.get("_meta", {})
            parsed["_meta"]["validated_by"] = args.model
            parsed["_meta"]["validation_elapsed_s"] = round(time.time() - t0, 1)
            with open(out_file, "w") as f:
                json.dump(parsed, f, indent=2)
            v = parsed.get("validation", {})
            print(f"  -> {os.path.basename(out_file)} verdict={v.get('verdict')} "
                  f"score={v.get('recreatability_score_1_to_10')} ({time.time()-t0:.0f}s)")
            finals.append(parsed)
        except Exception as e:
            print(f"  FAILED: {e}")

    with open(os.path.join(analysis_dir, "slides_final.json"), "w") as f:
        json.dump(finals, f, indent=2)

    # human-readable summary
    lines = ["# Slide Validation Summary\n",
             "| Slide | Title | Verdict | Score | Uncertain |",
             "|---|---|---|---|---|"]
    for p in finals:
        v = p.get("validation", {})
        lines.append(
            f"| {p.get('_meta', {}).get('frame', '?')} "
            f"| {(p.get('slide_title') or '')[:50]} "
            f"| {v.get('verdict', '?')} "
            f"| {v.get('recreatability_score_1_to_10', '?')} "
            f"| {len(v.get('uncertain_items', []))} |")
    with open(os.path.join(analysis_dir, "summary.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nfinal results: {os.path.join(analysis_dir, 'slides_final.json')}")
    print(f"summary:       {os.path.join(analysis_dir, 'summary.md')}")


if __name__ == "__main__":
    main()
