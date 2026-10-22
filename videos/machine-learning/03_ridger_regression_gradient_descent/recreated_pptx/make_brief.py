#!/usr/bin/env python3
"""Assemble a build-worker dispatch brief for one slide of deck 03.

Usage: python3 make_brief.py NNN [--out PATH]

Reads FLEET_BRIEF_TEMPLATE.md + slide_dependencies.json + the slide's
analysis/slide_NNN_final.json and prints the complete dispatch prompt with the
DEPS line and CONTENT LINES substituted. Brief content lines come from the
slide's OWN final JSON (never another deck's, never memory).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))            # recreated_pptx/
NS = os.path.dirname(HERE)                                    # the video namespace
ROOT = os.path.dirname(os.path.dirname(NS))                    # project root


def content_lines(final):
    lines = []
    title = final.get("slide_title", "")
    sub = final.get("subtitle_or_header") or ""
    lines.append(f"Title: {title}" + (f" | header/subtitle: {sub}" if sub else ""))
    layout = final.get("layout", {})
    if isinstance(layout, dict):
        arr = layout.get("arrangement") or layout.get("description") or json.dumps(layout)[:400]
        lines.append(f"Layout: {arr}")
    elif layout:
        lines.append(f"Layout: {str(layout)[:400]}")
    ves = final.get("visual_elements", [])
    if isinstance(ves, list):
        for ve in ves[:4]:
            t = ve.get("type", "element") if isinstance(ve, dict) else str(ve)
            desc = ""
            if isinstance(ve, dict):
                desc = ve.get("description") or ve.get("data") or ve.get("content") or ""
                desc = str(desc)[:220]
            lines.append(f"Visual element: {t} — {desc}")
    elif ves:
        lines.append(f"Visual elements: {str(ves)[:400]}")
    vt = final.get("verbatim_text", {})
    if isinstance(vt, dict):
        counts = ", ".join(f"{k}={len(v)}" if isinstance(v, list) else k
                           for k, v in vt.items() if v)
        if counts:
            lines.append(f"Verbatim text blocks: {counts}")
    val = final.get("validation", {})
    if val:
        lines.append(f"Validation: verdict={val.get('verdict')} "
                     f"score={val.get('recreatability_score_1_to_10')} "
                     f"uncertain={val.get('uncertain_items')}")
        fixes = val.get("fixes") or []
        for f in list(fixes)[:6]:
            lines.append(f"VALIDATOR FIX: {str(f)[:220]}")
    imagery = final.get("imagery")
    if imagery:
        lines.append(f"Imagery: {str(imagery)[:220]}")
    return lines


def deps_line(nnn):
    deps = json.load(open(os.path.join(NS, "slide_dependencies.json")))
    edges = deps.get("edges", {})
    parents = edges.get(str(nnn)) or edges.get(nnn) or []
    special = deps.get("special", {}).get(str(nnn)) or deps.get("special", {}).get(nnn)
    if not parents:
        return "root — no dependencies; build free."
    pl = " + ".join(f"slide_{int(p):03d}" for p in parents)
    line = (f"child of {pl}: import the certified component "
            f"`recreated_pptx/build/components/slide_{'_and_'.join(f'{int(p):03d}' for p in parents)}.js` "
            f"(renderBase + per-block exports with skip/only); never copy-paste; "
            f"your parent is certified — its pixels are law; child-local fixes only "
            f"(copy-then-modify), never edit the parent component.")
    if special:
        line += f" SPECIAL (founder): {special}"
    return line


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: make_brief.py NNN [--out PATH]")
    nnn = int(sys.argv[1])
    sid = f"{nnn:03d}"
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]

    final = json.load(open(os.path.join(NS, "analysis", f"slide_{sid}_final.json")))
    template = open(os.path.join(HERE, "FLEET_BRIEF_TEMPLATE.md")).read()

    # The template is: orchestrator header --- BRIEF BODY --- dispatch-law footer.
    # Assemble only the middle section.
    body = template.split("---")[1]
    body = body.replace("NNN", sid)
    body = body.replace(
        'DEPS: <"root — no dependencies; build free." | "child of M: import the certified\ncomponent `recreated_pptx/build/components/slide_MMM.js` (renderBase + per-block\nexports with skip/only); never copy-paste; your parent is certified — its\npixels are law; child-local fixes only (copy-then-modify), never edit the\nparent component. Special note for 13: inherit 12\'s table PATTERN, redraw at\n13\'s measured position with 13\'s numbers. Special note for 17: chain 12→13→17\ncomposes transitively.">',
        "DEPS: " + deps_line(nnn))
    cl = "\n".join(f"  - {l}" for l in content_lines(final))
    body = body.replace(
        "CONTENT LINES: <3-6 lines from the slide's own final JSON + frame: title,\nlayout regions, key visual elements (tables/equations/graphs with their\nvalues), any founder/AGENTS.md notes. Workers verify against the spec anyway —\nthese are orientation, not authority.>",
        "CONTENT LINES (orientation only — the final JSON + frame are authority):\n" + cl)

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            f.write(body)
        print(f"brief banked: {out_path}")
    else:
        print(body)


if __name__ == "__main__":
    main()
