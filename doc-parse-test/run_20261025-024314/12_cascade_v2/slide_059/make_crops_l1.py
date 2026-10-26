#!/usr/bin/env python3
"""Level-1 region crops for slide_059 cascade_v2 (6 regions, prechecked)."""
import json
import os

from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg"
OUT = os.path.join(HERE, "crops")
FRAME_W, FRAME_H = 960, 540

# (id, dir_name, plan box, scale, provenance, targets, trigger)
REGIONS = [
    ("crop01", "crop01_softmax_cluster", (400, 40, 645, 135), 3.0,
     "judge-supplement", [5, 6, 9, 10, 11],
     "wave-4 CROP PLAN: C1/C2/C3+Sigma+in-circle Softmax cluster (arbitrated HIGH defects)"),
    ("crop02", "crop02_xrow_labels", (195, 402, 870, 450), 2.0,
     "judge-supplement", [12, 13, 14, 15, 16, 17, 18, 19],
     "wave-4 CROP PLAN: input-row X0..X_N-1 subscript labels (GT-gap)"),
    ("crop03", "crop03_yrow_labels", (195, 208, 870, 262), 2.0,
     "judge-supplement", [20, 21, 22, 23, 24, 25, 26, 27],
     "wave-4 CROP PLAN: output-row Y0..Y_N-1 subscript labels (GT-gap)"),
    ("crop04", "crop04_pooled_row", (380, 138, 645, 175), 3.0,
     "judge-supplement", [],
     "wave-4 CROP PLAN + mission hint: pooled 20-cell table row wholly unreported by full-frame parse (register M3)"),
    ("crop05", "crop05_annotation_stack", (60, 130, 290, 510), 2.0,
     "judge-supplement", [36, 37, 38, 39, 40, 41, 42, 43, 44, 45],
     "register M4 + judge A8 band correction: left stacked-annotation column"),
    ("crop06", "crop06_class_picture_est", (720, 405, 960, 540), 3.0,
     "parse-class-block", [35],
     "full-frame parse call05_t9k class_Picture origin (0.9443,0.9586)=(906.5,517.6) px, origin-only -> estimated default quadrant cell"),
]


def clamp_box(b):
    x0, y0, x1, y1 = b
    return (max(0, x0), max(0, y0), min(FRAME_W, x1), min(FRAME_H, y1))


im = Image.open(SRC)
results = []
for cid, name, box, scale, prov, targets, trigger in REGIONS:
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
        "class": name.split("_", 1)[1], "level": 1,
        "plan_box_frame_px": list(box), "box_frame_px": list(mbox),
        "estimated": cid == "crop06",
        "margin_applied": "+4% of box dims per side, clamped",
        "scale": scale, "resample": "LANCZOS", "size_px": list(up.size),
        "mean_rgb": round(mean, 1), "precheck_ok": ok,
        "provenance": prov, "targets_gt": targets, "trigger": trigger,
        "transform": f"frame_x = crop_x/{scale:g} + {mbox[0]} ; frame_y = crop_y/{scale:g} + {mbox[1]}",
    })

with open(os.path.join(HERE, "crops_l1_precheck.json"), "w") as f:
    json.dump(results, f, indent=1)
print(json.dumps(results, indent=1))
exit(0 if all(r["precheck_ok"] for r in results) else 1)
