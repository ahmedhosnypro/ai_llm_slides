#!/usr/bin/env python3
"""Wave-5 cascade crops for slide_052 — PIL crop + margin + LANCZOS + pre-check.
Regions: 1 parse-seed (class_Picture, estimated default) + 6 judge-supplement
(from 10_visual_judge/slide_052/judge/round1_transcript.md defect list).
"""
import json, os
from PIL import Image

RUN = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314"
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg"
OUT = os.path.join(RUN, "11_cascade/slide_052/crops")

REGIONS = [
    # id, class, x0,y0,x1,y1 (frame px), provenance, note
    ("crop01", "picture", 720, 380, 960, 540, "parse-seed",
     "class_Picture origin tokens (0.9443,0.9586)->(906.5,517.6); origin-only block, estimated default region anchored at border/letterbox junction; visually corrected at crop-judge step"),
    ("crop02", "upper_boxes", 350, 160, 885, 300, "judge-supplement",
     "round1 F3/F4: five upper 3D boxes stacked Encode/Decoder/Attention + five Q circles y254 (judge px)"),
    ("crop03", "lower_boxes", 350, 335, 885, 425, "judge-supplement",
     "round1 F4: five lower masked boxes stacked Masked/Multi-Head/Self Attention"),
    ("crop04", "left_kv_y", 40, 150, 345, 290, "judge-supplement",
     "round1 F1/F2: K circle (309,176-199), V circle (307,228-250), Y tags x85/163/239 y247-263, token enclosure"),
    ("crop05", "encoder_inputs", 40, 295, 330, 530, "judge-supplement",
     "round1 F1/F5: Transformer Encoder box, I/feel/Sick inputs, SOS=Start Of Sentence legend"),
    ("crop06", "word_boxes", 340, 430, 885, 530, "judge-supplement",
     "round1 F5: Word and Position Encoding bar + SOS/Je/me/sens/malade word boxes"),
    ("crop07", "badge", 800, 20, 960, 120, "judge-supplement",
     "round1 F1: yellow badge 52 (858-893, 56-84) + top-right chrome corner"),
]

MARGIN = 0.04
im = Image.open(SRC)
W, H = im.size
assert (W, H) == (960, 540), (W, H)
manifest = []
for cid, cls, x0, y0, x1, y1, prov, note in REGIONS:
    mx = int((x1 - x0) * MARGIN); my = int((y1 - y0) * MARGIN)
    cx0 = max(0, x0 - mx); cy0 = max(0, y0 - my)
    cx1 = min(W, x1 + mx); cy1 = min(H, y1 + my)
    crop = im.crop((cx0, cy0, cx1, cy1))
    cw, ch = crop.size
    scale = 3.0
    up_w, up_h = int(round(cw * scale)), int(round(ch * scale))
    while up_w > 1664 or up_h > 2048:
        scale = round(scale - 0.1, 2)
        up_w, up_h = int(round(cw * scale)), int(round(ch * scale))
    up = crop.resize((up_w, up_h), Image.LANCZOS)
    d = os.path.join(OUT, f"{cid}_{cls}")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "crop.png")
    up.save(p, "PNG")
    # objective pre-check
    chk = Image.open(p); px = chk.convert("L")
    stat = px.getextrema()
    ok = chk.size[0] >= 480 and stat[0] < stat[1]
    manifest.append({
        "id": cid, "class": cls, "level": 1, "provenance": prov, "note": note,
        "box_frame_px": [cx0, cy0, cx1, cy1],
        "box_src_region_requested": [x0, y0, x1, y1],
        "crop_px": [up_w, up_h], "scale": scale,
        "transform": f"frame_x = crop_x/{scale} + {cx0}; frame_y = crop_y/{scale} + {cy0}",
        "png": p, "precheck_ok": bool(ok), "precheck": {"dims": chk.size, "gray_extrema": stat},
    })
    print(cid, cls, "crop", (cw, ch), "->", (up_w, up_h), "scale", scale, "precheck_ok", ok)

with open(os.path.join(RUN, "11_cascade/slide_052/manifest.json"), "w") as f:
    json.dump({"slide": "slide_052", "frame": [960, 540], "source": SRC,
               "crops": manifest}, f, indent=2)
print("manifest written:", len(manifest), "crops")
