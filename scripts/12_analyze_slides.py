#!/usr/bin/env python3
"""
12_analyze_slides.py — Per unique slide: vision analysis via IronRouter `images` model.

Produces analysis/slide_XXX_raw.json — a precise, structured description of the
slide's text content and visual presentation, good enough to recreate the slide
in PowerPoint without seeing the original.

Environment:
    IR_BASE_URL  (default http://localhost:17844/v1 — the local IronRouter dist)
    IR_API_KEY   (default: read from <project>/.analyze-image-key)
    IR_VISION_MODEL (default "images")

Usage:
    python3 12_analyze_slides.py <slides_dir> <analysis_out_dir> [--slides 10]
"""

import argparse
import base64
import json
import os
import re
import sys
import time

import openai

ANALYSIS_PROMPT = """\
You are a meticulous presentation-archaeologist AI. You are given ONE slide image from a \
Machine Learning course video. Your job: capture EVERYTHING on that slide with total \
fidelity, so the slide can be recreated later in PowerPoint by someone who has never seen it.

Respond with a SINGLE JSON object (no markdown fences, no commentary) with these fields:

{
  "slide_title": "<exact title text, verbatim>",
  "subtitle_or_header": "<exact subtitle/kicker text, verbatim, or null>",
  "verbatim_text": {
    "bullets": ["<each bullet, verbatim, exactly as written — preserve wording, order, emphasis>"],
    "labels": ["<every label, axis name, caption, footnote, watermark, slide number, annotation>"],
    "equations": ["<every equation/formula, transcribed exactly in plain text or LaTeX>"]
  },
  "layout": {
    "arrangement": "<precise spatial description: e.g. 'title top-left, two columns below: left column \
bullets, right column diagram; footer strip bottom-left with course logo'>",
    "regions": [
      {"name": "<region name>", "position": "<top/middle/bottom + left/center/right + rough % extents>",
       "content": "<what is in this region>"}
    ],
    "hierarchy": "<what dominates visually: size/weight/color ordering of the elements>"
  },
  "visual_elements": [
    {"type": "<diagram|chart|graph|table|flowchart|network|image|icon|highlight-box|arrow|other>",
     "description": "<precise description: for charts state chart type, axis names + ranges, series \
names, every readable data value/percentage; for diagrams state every node's text, arrows and their \
directions, grouping/containers; for tables state rows/columns and every cell text>",
     "colors": ["<approx hex of each distinct color used in this element>"],
     "position": "<where on the slide>"}
  ],
  "imagery": ["<every photo/icon/illustration: what it depicts, style, where it sits>"],
  "colors": {
    "background": "<approx hex>",
    "title_text": "<approx hex>",
    "body_text": "<approx hex>",
    "accents": ["<approx hex of accent/highlight colors>"]
  },
  "typography_notes": "<qualitative: serif vs sans, title vs body weight/size relations, any \
styling like all-caps, italics, numbered bullets>",
  "animation_state": "<if anything looks mid-build (e.g. bullet 3 of 5 revealed), say so>",
  "recreation_brief": "<numbered step-by-step instructions to recreate this slide in PowerPoint \
with full fidelity: exact texts to place, where, what shapes/charts to draw, what colors to use>"
}

RULES:
- Transcribe text VERBATIM — do not paraphrase, do not fix grammar, do not translate.
- Read ALL visible values on charts (numbers, percentages, axis ticks) — completeness beats brevity.
- Approximate hex colors from what you see (backgrounds, text, chart series).
- If a region is blurry/unreadable, transcribe your best guess wrapped in [?] markers.
- JSON must be valid and parseable. No trailing commas. Escape quotes properly."""


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
    parser.add_argument("slides_dir")
    parser.add_argument("analysis_out_dir")
    parser.add_argument("--slides", type=int, default=10)
    parser.add_argument("--from", dest="from_slide", type=int, default=1)
    parser.add_argument("--to", dest="to_slide", type=int, default=None)
    parser.add_argument("--model", default=os.environ.get("IR_VISION_MODEL", "images"))
    parser.add_argument("--max-tokens", type=int, default=16000)
    args = parser.parse_args()

    base_url = os.environ.get("IR_BASE_URL", "http://localhost:17844/v1")
    api_key = os.environ.get("IR_API_KEY")
    if not api_key:
        key_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".analyze-image-key")
        if os.path.exists(key_file):
            api_key = open(key_file).read().strip()
    if not api_key:
        sys.exit("IR_API_KEY env var required (or create .analyze-image-key in the project root)")

    slides_dir = os.path.abspath(args.slides_dir)
    out_dir = os.path.abspath(args.analysis_out_dir)
    os.makedirs(out_dir, exist_ok=True)

    index_path = os.path.join(slides_dir, "slides_index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else None

    slide_files = sorted(
        f for f in os.listdir(slides_dir) if f.lower().endswith((".jpg", ".jpeg"))
    )
    # Range filter BEFORE the --slides slice (slice default 10 would eat ranges otherwise).
    if args.from_slide > 1 or args.to_slide is not None:
        def _slide_num(name: str) -> int:
            m = re.match(r"slide_(\d+)\.jpe?g$", name, re.IGNORECASE)
            return int(m.group(1)) if m else 0
        slide_files = [f for f in slide_files
                       if _slide_num(f) >= args.from_slide
                       and (args.to_slide is None or _slide_num(f) <= args.to_slide)]
    slide_files = slide_files[: args.slides]

    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    ok, failed = 0, 0
    for fname in slide_files:
        out_file = os.path.join(out_dir, fname.replace(".jpg", "_raw.json"))
        if os.path.exists(out_file):
            print(f"{fname}: already analyzed, skipping")
            ok += 1
            continue
        with open(os.path.join(slides_dir, fname), "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        meta = next((s for s in (index or []) if s["image"] == fname), {})
        print(f"{fname}: analyzing with {args.model} ...", flush=True)
        t0 = time.time()
        try:
            resp = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": ANALYSIS_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ]}],
                max_tokens=args.max_tokens,
                temperature=0.1,
                stream=True,  # streaming avoids the upstream gateway's 60s non-streaming cut
            )
            parts, finish = [], None
            for chunk in resp:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    parts.append(chunk.choices[0].delta.content)
                if chunk.choices and chunk.choices[0].finish_reason:
                    finish = chunk.choices[0].finish_reason
            raw_text = "".join(parts)
            parsed = extract_json(raw_text)
            parsed["_meta"] = {"frame": fname, "model": args.model,
                               "source_timestamps": meta, "elapsed_s": round(time.time() - t0, 1)}
            with open(out_file, "w") as f:
                json.dump(parsed, f, indent=2)
            print(f"  -> {out_file} ({time.time()-t0:.0f}s, finish={finish})")
            ok += 1
        except Exception as e:
            failed += 1
            print(f"  FAILED: {e}")
    print(f"\ndone: {ok} analyzed, {failed} failed -> {out_dir}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
