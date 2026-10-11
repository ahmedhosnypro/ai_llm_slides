#!/usr/bin/env python3
"""PIL forensics on slide_026.jpg (960x540, 1px = 1pt = 1/72 in).
Masks each spec color (tolerance) and prints per-color bounding boxes + counts,
plus row/col profiles for the major boxes."""
import sys, json
from PIL import Image
import numpy as np

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W, _ = A.shape

def mask_bbox(target, tol, name):
    t = np.array(target)
    m = (np.abs(A - t).sum(axis=2) <= tol)
    n = int(m.sum())
    out = {"name": name, "target": list(target), "count": n}
    if n > 0:
        ys, xs = np.where(m)
        out.update({"x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max())})
        # column and row profiles (runs of >=8 px) to split multiple blobs
        cols = np.where(m.sum(axis=0) >= 8)[0]
        rows = np.where(m.sum(axis=1) >= 8)[0]
        def runs(idx):
            if len(idx) == 0: return []
            r, s, p = [], idx[0], idx[0]
            for v in idx[1:]:
                if v > p + 6:
                    r.append((int(s), int(p))); s = v
                p = v
            r.append((int(s), int(p)))
            return r
        out["col_runs"] = runs(cols)
        out["row_runs"] = runs(rows)
    print(json.dumps(out))

COLORS = [
    ((251, 229, 214), 30, "peach_canvas_FBE5D6"),
    ((200, 179, 156), 40, "tan_C8B39C"),
    ((223, 166, 223), 45, "plum_DFA6DF"),
    ((197, 224, 245), 35, "lightblue_C5E0F5"),
    ((226, 239, 218), 30, "lightgreen_E2EFDA"),
    ((255, 255, 153), 40, "yellow_FFFF99"),
    ((255, 153, 204), 45, "pink_FF99CC"),
    ((217, 179, 255), 45, "lavender_D9B3FF"),
    ((0, 176, 80), 60, "green_00B050"),
    ((146, 208, 80), 40, "green92_D0_92D050"),
    ((255, 0, 0), 90, "red_FF0000"),
    ((0, 51, 204), 70, "blue_0033CC"),
    ((255, 255, 0), 60, "yellow_FFFF00"),
    ((255, 0, 255), 80, "magenta_FF00FF"),
    ((192, 0, 0), 60, "darkred_C00000"),
    ((253, 253, 150), 40, "badge_FDFD96"),
]

for t, tol, name in COLORS:
    mask_bbox(t, tol, name)
