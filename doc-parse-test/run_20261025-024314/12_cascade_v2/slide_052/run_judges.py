#!/usr/bin/env python3
"""Sequential vision-gateway judges for slide_052 cascade v2 crops (max 1 in-flight)."""
import json
import subprocess
import sys
import time

TREE = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/12_cascade_v2/slide_052"
AI = "/home/ahmed/Projects/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"

PNG = {}
for _rows in ("crops/prep_rows.json", "crops/prep_rows_l2.json", "crops/prep_rows_l3.json"):
    for _r in json.load(open(f"{TREE}/{_rows}")):
        PNG[_r["id"]] = _r["png"]

JUDGES = [
    ("crop01", "Crop of slide 052 (frame 960x540), box frame-px (794,462)-(960,540), upscale 3x. doc-parse read the single string: 'nalade'. Tasks: (1) transcribe ALL visible text with approximate crop-px positions; (2) classify the parse string 'nalade': REAL (visible on image) or NOT-IN-GT (not on image) - if the visible text is actually 'malade' or a fragment of it, say so; (3) is there any standalone picture/image content in this region (the full-frame parser claimed a class_Picture region near frame (906.5,517.6))? End with 'JUDGE VERDICT: <one line>'."),
    ("crop02", "Crop of slide 052 (frame 960x540), box frame-px (307,149)-(929,306), upscale 2x. doc-parse read: 'October 1', 'Ende Decoder Attention', 'Encode Decoder Attention' x4. Tasks: (1) transcribe ALL visible text with approximate crop-px positions; (2) is there ANY text reading 'October 1' anywhere in this crop? (3) how many blue 3D box stacks are visible and what is the exact first label line of each ('Encode', 'Ende', or 'Encoder')? (4) how many blue Q circles with white Q are visible below the boxes, at what crop-px positions? (5) any red K or green V circles visible? End with 'JUDGE VERDICT: <one line>'."),
    ("crop05", "Crop of slide 052 (frame 960x540), box frame-px (28,280)-(342,540), upscale 3x. doc-parse read: 'Transformer Encoder', 'feel', 'Sick', 'SOS = Start Of Sentence'. Tasks: (1) transcribe ALL visible text with approximate crop-px positions; (2) is the single letter 'I' visible inside a small white input box with red border? (3) list each input box and its word; (4) is the legend text exactly 'SOS = Start Of Sentence'? End with 'JUDGE VERDICT: <one line>'."),
    ("crop06", "Crop of slide 052 (frame 960x540), box frame-px (794,22)-(960,113), upscale 3x. doc-parse read: '52'. Tasks: (1) transcribe ALL visible text with crop-px positions; (2) what number is printed in the yellow circular badge? End with 'JUDGE VERDICT: <one line>'."),
    ("crop08", "Crop of slide 052 (frame 960x540), box frame-px (30,236)-(310,287), upscale 3x. doc-parse read: 'Ya', 'Y2'. Tasks: (1) transcribe ALL visible text with crop-px positions; (2) how many red Y tags are visible, at what crop-px x positions, and what does each glyph actually read (plain 'Y', 'Ya', 'Y0', 'Y1', 'Y2')? End with 'JUDGE VERDICT: <one line>'."),
    ("crop09", "Crop of slide 052 (frame 960x540), box frame-px (164,150)-(326,280), upscale 3x. doc-parse read: 'Y1', 'Y2'. Tasks: (1) transcribe ALL visible text/glyphs with crop-px positions; (2) is there a red circle containing the letter K? at what position? (3) is there a green circle containing the letter V? at what position? (4) how many red Y tags are inside this box and what do they read? End with 'JUDGE VERDICT: <one line>'."),
    ("crop10", "Crop of slide 052 (frame 960x540), box frame-px (39,225)-(201,295), upscale 3x. doc-parse read: 'Ya', 'Y'. Tasks: (1) transcribe ALL visible text with crop-px positions; (2) how many red Y tags are visible, at what x positions, and which one (if any) is a plain clean 'Y' with no extra characters? End with 'JUDGE VERDICT: <one line>'."),
    ("crop12", "Crop of slide 052 (frame 960x540), box frame-px (484,165)-(906,305), upscale 3x. doc-parse read only: 'Encode Decoder Attention' x3 (no Q). Tasks: (1) transcribe ALL visible text with crop-px positions; (2) how many blue Q circles with white Q are visible in this crop, at what crop-px positions? (3) how many 3-line box stacks are visible and do all read Encode/Decoder/Attention? End with 'JUDGE VERDICT: <one line>'."),
    ("crop13", "Crop of slide 052 (frame 960x540), box frame-px (692,331)-(898,429), upscale 3x. doc-parse read: 'Masked', 'M-Head', 'Multi-Head', 'Self Attention'. Tasks: (1) transcribe ALL visible text with crop-px positions; (2) is this the 5th masked attention box and what is its actual stacked label (expected 3 lines: Masked / Multi-Head / Self Attention)? (3) is the word 'Masked' rendered in yellow? End with 'JUDGE VERDICT: <one line>'."),
    ("crop14", "Crop of slide 052 (frame 960x540), box frame-px (164,152)-(326,228), upscale 3x. doc-parse read the garbled string: 'Int-head Sell on Block'. Tasks: (1) transcribe ALL visible text with crop-px positions; (2) is the visible text actually the tail of the callout 'Masked Multi-head Self Attention Block' that enters this box from the left? (3) is there a red circle containing the letter K anywhere in this crop, at what position? End with 'JUDGE VERDICT: <one line>'."),
    ("crop15", "Crop of slide 052 (frame 960x540), box frame-px (164,208)-(326,272), upscale 3x. doc-parse read: NOTHING (empty). Tasks: (1) transcribe ALL visible text/glyphs with crop-px positions; (2) is there a green circle containing the letter V, at what position? (3) any other letters or circles? End with 'JUDGE VERDICT: <one line>'."),
    ("crop16", "Crop of slide 052 (frame 960x540), box frame-px (32,423)-(248,482), upscale 3x. doc-parse read only: 'feel'. Tasks: (1) transcribe ALL visible text with crop-px positions; (2) how many small input boxes are visible and what does each contain (expected words: I, feel, Sick)? End with 'JUDGE VERDICT: <one line>'."),
]


def main():
    import os
    results = []
    for cid, prompt in JUDGES:
        out = f"{TREE}/judges/{cid}_judge.md"
        if os.path.exists(out) and os.path.getsize(out) > 0:
            print(f"{cid} SKIP (already banked)", flush=True)
            continue
        png = PNG[cid]
        err = f"{TREE}/judges/{cid}_judge.stderr.log"
        ts = time.time()
        with open(out, "w") as fo, open(err, "w") as fe:
            rc = subprocess.call(
                [sys.executable, AI, "analysis", png, "-p", prompt],
                stdout=fo, stderr=fe, timeout=600,
            )
        wall = time.time() - ts
        results.append((cid, rc, wall))
        print(f"{cid} exit={rc} wall={wall:.1f}s", flush=True)
    fails = [r for r in results if r[1] != 0]
    print(f"DONE {len(results)} judges, {len(fails)} failures")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
