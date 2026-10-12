#!/usr/bin/env python3
"""measure6_mine — frame-diff bands (27 vs 28) + calibrated chip centers (both frames).
Chips: greenish-union (fill+border+text) binary-closed blobs, 40<=w<=90, 15<=h<=60.
Centers reported in frame px and slide pt (fx = 18.63 + 0.96123*sx ; fy = 0.95556*sy)."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
CXf, CYf = 578.0, 284.0

def chips_of(name):
    A = np.asarray(Image.open(f"{BASE}/unique_slides/{name}.jpg").convert("RGB")).astype(int)
    r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    green = ((g - r) > 22) & ((g - b) > 18) & (g > 110)
    green = ndi.binary_closing(green, structure=np.ones((7, 7)))
    lab, n = ndi.label(green)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 600:
            continue
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if not (40 <= w <= 95 and 15 <= h <= 62):
            continue
        cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        ang = float(np.degrees(np.arctan2(CYf - cy, cx - CXf)) % 360)
        out.append({"ang": round(ang, 1), "frame": [round(cx, 1), round(cy, 1)],
                    "slide": [round((cx - 18.63) / 0.96123, 2), round(cy / 0.95556, 2)],
                    "wh": [int(w), int(h)], "n": int(len(xs))})
    out.sort(key=lambda c: c["ang"])
    return out

c27, c28 = chips_of("slide_027"), chips_of("slide_028")

A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_027.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
d = (np.abs(A - B).sum(axis=2) > 90)
def bands(counts, thr, gap=8):
    idx = np.nonzero(counts > thr)[0]
    res = []
    if len(idx):
        s = p = idx[0]
        for v in idx[1:]:
            if v - p > gap:
                res.append([int(s), int(p)]); s = v
            p = v
        res.append([int(s), int(p)])
    return res
diff = {"npx": int(d.sum()), "col_bands": bands(d.sum(axis=0), 6), "row_bands": bands(d.sum(axis=1), 6)}
print(json.dumps({"chips27": c27, "chips28": c28, "diff27v28": diff}, indent=1))
