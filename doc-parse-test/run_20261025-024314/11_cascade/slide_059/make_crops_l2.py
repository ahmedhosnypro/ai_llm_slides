#!/usr/bin/env python3
"""Wave-5 cascade level-2 sub-crops for slide_059 (recursion on level-1 crop parses)."""
import json
import os

from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))  # .../11_cascade/slide_059
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                   "videos", "deep-learning", "002_transformers_part2",
                                   "unique_slides", "slide_059.jpg"))
OUT = os.path.join(HERE, "crops")

# (id, dir_name, frame box, scale, parent, trigger)
REGIONS = [
    ("crop06", "crop06_labels_row_l2", (415, 48, 615, 80), 3.0, "crop01",
     "crop01 parse: IC1/IC2/IC3 cluster still carries stray leading glyph; labels-row isolated for clean re-read"),
    ("crop07", "crop07_circles_l2", (410, 85, 625, 140), 3.0, "crop01",
     "crop01 parse: only 2 of 3 in-circle Softmax+Sigma pairs resolved; circles cluster isolated"),
    ("crop08", "crop08_xrow_left_l2", (195, 402, 470, 450), 3.0, "crop02",
     "crop02 parse: Xl/Xj garbles for first labels; left half isolated at higher zoom"),
    ("crop09", "crop09_xrow_tail_l2", (560, 402, 870, 450), 3.0, "crop02",
     "crop02 parse: O fragment + N-tails unresolved; tail zone isolated"),
    ("crop10", "crop10_yrow_left_l2", (195, 208, 470, 262), 3.0, "crop03",
     "crop03 parse: Yd garble for first label; left half isolated at higher zoom"),
    ("crop11", "crop11_yrow_tail_l2", (560, 208, 870, 262), 3.0, "crop03",
     "crop03 parse: YNz/YNI N-tails unresolved; tail zone isolated"),
    ("crop12", "crop12_annot_lower_l2", (51, 320, 299, 525), 2.0, "crop05",
     "crop05 parse describes only the top stack of the annotation column; lower half isolated"),
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
        "id": cid, "dir": name, "parent": parent, "level": 2, "trigger": trigger,
        "plan_box_frame_px": list(box), "crop_box_frame_px": list(mbox),
        "scale": scale, "size_px": list(up.size), "mean_rgb": round(mean, 1),
        "precheck_ok": ok,
        "transform": "frame_x = crop_x/%g + %d ; frame_y = crop_y/%g + %d" % (scale, mbox[0], scale, mbox[1]),
    })

print(json.dumps(results, indent=1))
exit(0 if all(r["precheck_ok"] for r in results) else 1)
