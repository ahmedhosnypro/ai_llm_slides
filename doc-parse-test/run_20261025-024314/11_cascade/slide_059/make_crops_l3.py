#!/usr/bin/env python3
"""Wave-5 cascade level-3 sub-crops for slide_059 (recursion on level-2 parses)."""
import json
import os

from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                   "videos", "deep-learning", "002_transformers_part2",
                                   "unique_slides", "slide_059.jpg"))
OUT = os.path.join(HERE, "crops")

REGIONS = [
    ("crop13", "crop13_xtail_l3", (715, 402, 870, 450), 3.0, "crop09",
     "crop09 parse: X/XN/XNd still mangled for N-tails; two-tail window isolated"),
    ("crop14", "crop14_yleft_tight_l3", (195, 208, 345, 262), 3.0, "crop10",
     "crop10 parse: Y_d/Y_i garbles + stray standalone 1 tokens; Y0/Y1 pair isolated"),
    ("crop15", "crop15_x12_zone_l3", (500, 402, 650, 450), 3.0, "crop08",
     "crop08 parse: middle tokens X3/X2/X3 garbled order; X1/X2 slots re-isolated"),
    ("crop16", "crop16_annot_table_l3", (51, 375, 299, 520), 2.0, "crop12",
     "crop12 parse: class_Chart ranked_table returned 2 of 5 stacks; chart region re-cropped"),
]
FRAME_W, FRAME_H = 960, 540


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
    up.save(os.path.join(d, "crop.png"))
    stat = ImageStat.Stat(up)
    mean = sum(stat.mean) / len(stat.mean)
    ok = up.size[0] >= 480 and mean > 0 and up.size[0] <= 1664 and up.size[1] <= 2048
    results.append({
        "id": cid, "dir": name, "parent": parent, "level": 3, "trigger": trigger,
        "plan_box_frame_px": list(box), "crop_box_frame_px": list(mbox),
        "scale": scale, "size_px": list(up.size), "mean_rgb": round(mean, 1),
        "precheck_ok": ok,
        "transform": "frame_x = crop_x/%g + %d ; frame_y = crop_y/%g + %d" % (scale, mbox[0], scale, mbox[1]),
    })

print(json.dumps(results, indent=1))
exit(0 if all(r["precheck_ok"] for r in results) else 1)
