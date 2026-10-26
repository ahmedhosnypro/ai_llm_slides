#!/usr/bin/env python3
"""Wave-5 cascade auto-crop for slide_059: judge-supplement regions -> PNG crops."""
import json
import os
import sys

from PIL import Image, ImageStat

RUN = os.path.dirname(os.path.abspath(__file__))  # .../11_cascade/slide_059
SRC = os.path.abspath(os.path.join(RUN, "..", "..", "..", "..",
                                   "videos", "deep-learning", "002_transformers_part2",
                                   "unique_slides", "slide_059.jpg"))
OUT = os.path.join(RUN, "crops")

# (id, dir_name, frame box fx0,fy0,fx1,fy1, scale) — boxes from 10_visual_judge/
# slide_059/judge/round1_transcript.md CROP PLAN (+ crop05 from register M4 band).
REGIONS = [
    ("crop01", "crop01_softmax_cluster", (400, 40, 645, 135), 3.0),
    ("crop02", "crop02_xrow_labels", (195, 402, 870, 450), 2.0),
    ("crop03", "crop03_yrow_labels", (195, 208, 870, 262), 2.0),
    ("crop04", "crop04_pooled_row", (380, 138, 645, 175), 3.0),
    ("crop05", "crop05_annotation_stack", (60, 130, 290, 510), 2.0),
]
FRAME_W, FRAME_H = 960, 540


def clamp_box(b):
    x0, y0, x1, y1 = b
    return (max(0, x0), max(0, y0), min(FRAME_W, x1), min(FRAME_H, y1))


im = Image.open(SRC)
results = []
for cid, name, box, scale in REGIONS:
    x0, y0, x1, y1 = box
    mx = int(round((x1 - x0) * 0.04))
    my = int(round((y1 - y0) * 0.04))
    mbox = clamp_box((x0 - mx, y0 - my, x1 + mx, y1 + my))
    crop = im.crop(mbox)
    w, h = crop.size
    up = crop.resize((int(round(w * scale)), int(round(h * scale))), Image.LANCZOS)
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    png = os.path.join(d, "crop.png")
    up.save(png)
    stat = ImageStat.Stat(up)
    mean = sum(stat.mean) / len(stat.mean)
    ok = up.size[0] >= 480 and up.size[1] > 0 and mean > 0 and up.size[0] <= 1664 and up.size[1] <= 2048
    results.append({
        "id": cid, "dir": name, "plan_box_frame_px": list(box),
        "crop_box_frame_px": list(mbox), "scale": scale,
        "size_px": list(up.size), "mean_rgb": round(mean, 1),
        "precheck_ok": ok,
        "transform": "frame_x = crop_x/%g + %d ; frame_y = crop_y/%g + %d" % (scale, mbox[0], scale, mbox[1]),
    })

print(json.dumps(results, indent=1))
bad = [r for r in results if not r["precheck_ok"]]
sys.exit(1 if bad else 0)
