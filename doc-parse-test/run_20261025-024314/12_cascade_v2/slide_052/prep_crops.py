#!/usr/bin/env python3
"""Crop prep for slide_052 cascade v2: PIL crop +4% margin clamped, LANCZOS
upscale 2-3x to >=480 px wide within 1664x2048, pre-check dims + nonzero mean."""
import json
import os
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg"
TREE = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/12_cascade_v2/slide_052"
FRAME_W, FRAME_H = 960, 540

# id, class, level, parent, provenance, requested(x0,y0,x1,y1), estimated, note
CROPS = [
    ("crop01", "picture", 1, None, "parse-seed", (800, 465, 960, 540), True,
     "class_Picture origin (0.9443,0.9586)->(906.5,517.6), origin-only -> estimated default box (register: confirmed-hallucination location; judge decides)"),
    ("crop02", "upper_boxes", 1, None, "judge-supplement", (330, 155, 906, 300), False,
     "5 upper 3D boxes stacked Encode/Decoder/Attention + 5 Q circles + residual bar title (judge-defect: 5x3 label grid shredded in full-frame parse)"),
    ("crop03", "lower_boxes", 1, None, "judge-supplement", (330, 300, 906, 425), False,
     "lower residual bar + 5 masked boxes stacked Masked/Multi-Head/Self Attention"),
    ("crop04", "wordrow", 1, None, "judge-supplement", (330, 430, 906, 530), False,
     "Word and Position Encoding purple bar + SOS/Je/me/sens/malade word boxes"),
    ("crop05", "leftpanel", 1, None, "judge-supplement", (40, 290, 330, 530), False,
     "Transformer Encoder box + I/feel/Sick input boxes + SOS=Start Of Sentence legend (judge-defect: GT9 missing from full frame)"),
    ("crop06", "badge", 1, None, "judge-supplement", (800, 25, 960, 110), False,
     "yellow badge 52 top-right (judge-defect: GT22 missing from full frame)"),
    ("crop07", "kv_q1", 1, None, "judge-supplement", (250, 150, 410, 290), False,
     "K circle (309,180) V circle (310,231) + leftmost Q + box1 left edge (judge-defect: GT18/GT19 missing)"),
    ("crop08", "y_row", 1, None, "judge-supplement", (40, 238, 300, 285), False,
     "3 Y tags x85/163/239 y247-263 + token enclosure top (judge-defect: GT21 missing)"),
]


def prep(crops):
    img = Image.open(SRC)
    assert img.size == (FRAME_W, FRAME_H), img.size
    out = []
    for cid, cls, level, parent, prov, req, estimated, note in crops:
        x0, y0, x1, y1 = req
        w, h = x1 - x0, y1 - y0
        mx, my = round(w * 0.04), round(h * 0.04)
        cx0, cy0 = max(0, x0 - mx), max(0, y0 - my)
        cx1, cy1 = min(FRAME_W, x1 + mx), min(FRAME_H, y1 + my)
        crop = img.crop((cx0, cy0, cx1, cy1))
        cw, ch = crop.size
        scale = 3 if 3 * cw <= 1664 and 3 * ch <= 2048 else 2
        assert scale * cw >= 480, (cid, cw, scale)
        assert scale * ch <= 2048, (cid, ch, scale)
        up = crop.resize((cw * scale, ch * scale), Image.LANCZOS)
        cdir = os.path.join(TREE, "crops", f"{cid}_{cls}")
        os.makedirs(cdir, exist_ok=True)
        png = os.path.join(cdir, "crop.png")
        up.save(png)
        g = up.convert("L")
        extrema = g.getextrema()
        precheck_ok = up.size[0] >= 480 and up.size[1] > 0 and extrema[0] != extrema[1]
        row = {
            "id": cid,
            "class": cls,
            "level": level,
            "parent": parent,
            "provenance": prov,
            "requested_region_frame_px": list(req),
            "box_frame_px": [cx0, cy0, cx1, cy1],
            "crop_px": list(up.size),
            "scale": scale,
            "transform": f"frame_x = crop_x/{scale} + {cx0}; frame_y = crop_y/{scale} + {cy0}",
            "png": png,
            "precheck_ok": precheck_ok,
            "precheck": {"dims": list(up.size), "gray_extrema": list(extrema)},
            "estimated": estimated,
            "note": note,
            "stop_reason": None,
            "stop_note": None,
        }
        out.append(row)
        print(json.dumps(row))
    return out


if __name__ == "__main__":
    rows = prep(CROPS)
    with open(os.path.join(TREE, "crops", "prep_rows.json"), "w") as f:
        json.dump(rows, f, indent=2)
    print(f"OK {len(rows)} crops", file=__import__('sys').stderr)
