#!/usr/bin/env python3
"""Level-2 sub-crops for slide_059 cascade_v2 (recursion on level-1 crop parses)."""
import json
import os

from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg"
OUT = os.path.join(HERE, "crops")
FRAME_W, FRAME_H = 960, 540

# (id, dir_name, plan box, scale, parent, trigger)
REGIONS = [
    ("crop07", "crop07_labels_row_l2", (415, 48, 615, 80), 3.0, "crop01",
     "call01: IC1/IC2/IC3 leading-glyph garble persists, C3 absent; labels row isolated (wave-4 A1: fx 438-599, fy 55-71)"),
    ("crop08", "crop08_circles_l2", (410, 85, 625, 140), 3.0, "crop01",
     "call01: only 2 of 3 in-circle Softmax+Sigma pairs resolved; circles cluster isolated (register M2/A10: cx 440/513/585)"),
    ("crop09", "crop09_xrow_left_l2", (195, 402, 470, 450), 3.0, "crop02",
     "call02: Xl/Xj head garbles + Xx/O mid-row fragments; head half isolated (wave-2 m3: heads X0..X3 fx 217-455)"),
    ("crop10", "crop10_xrow_mid_l2", (470, 402, 640, 450), 3.0, "crop02",
     "call02: O fragment at X4/X5 slots; mid window isolated (heads X4@509, X5@582)"),
    ("crop11", "crop11_yrow_tail_l2", (560, 208, 870, 262), 3.0, "crop03",
     "call03: YNz/YNI tail garbles; tail zone isolated (register B2: Y_N-2 fx 760-777, Y_N-1 fx 836-853)"),
    ("crop12", "crop12_yrow_head_l2", (215, 210, 375, 262), 3.0, "crop03",
     "call03: Yd head garble; hypothesis = annotation-column bleed at fx<215 (wave-4 A8 stacks end fx~270); tighter box starts at label origin 217"),
    ("crop13", "crop13_annot_lower_l2", (51, 320, 299, 525), 2.0, "crop05",
     "call05: only 1 of 5 annotation stacks read (Single vector...); lower half isolated (register M4: 3/3/2/2-line stacks)"),
]


def clamp_box(b):
    x0, y0, x1, y1 = b
    return (max(0, x0), max(0, y0), min(FRAME_W, x1), min(FRAME_H, y1))


im = Image.open(SRC)
results = []
for cid, name, box, scale, parent, trigger in REGIONS:
    x0, y0, x1, y1 = box
    mx = int(round((x1 - x0) * 0.04))
    my = int(round((y1 - y0) * 0.04))
    mbox = clamp_box((x0 - mx, y0 - my, x1 + mx, y1 + my))
    up = im.crop(mbox).resize(
        (int(round((mbox[2] - mbox[0]) * scale)), int(round((mbox[3] - mbox[1]) * scale))),
        Image.LANCZOS)
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    up.save(os.path.join(d, "slide_059.png"))
    stat = ImageStat.Stat(up)
    mean = sum(stat.mean) / len(stat.mean)
    ok = up.size[0] >= 480 and up.size[0] <= 1664 and up.size[1] <= 2048 and mean > 0
    results.append({
        "id": cid, "dir": f"crops/{name}", "png": f"crops/{name}/slide_059.png",
        "class": name.split("_", 1)[1].rsplit("_l2", 1)[0], "level": 2, "parent": parent,
        "plan_box_frame_px": list(box), "box_frame_px": list(mbox),
        "estimated": False,
        "margin_applied": "+4% of box dims per side, clamped",
        "scale": scale, "resample": "LANCZOS", "size_px": list(up.size),
        "mean_rgb": round(mean, 1), "precheck_ok": ok,
        "provenance": "recursive-level2", "trigger": trigger,
        "transform": f"frame_x = crop_x/{scale:g} + {mbox[0]} ; frame_y = crop_y/{scale:g} + {mbox[1]}",
    })

with open(os.path.join(HERE, "crops_l2_precheck.json"), "w") as f:
    json.dump(results, f, indent=1)
print(json.dumps([{k: r[k] for k in ("id", "size_px", "mean_rgb", "precheck_ok", "box_frame_px")} for r in results], indent=1))
exit(0 if all(r["precheck_ok"] for r in results) else 1)
