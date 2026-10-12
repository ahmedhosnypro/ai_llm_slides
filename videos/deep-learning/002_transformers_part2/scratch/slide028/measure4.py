#!/usr/bin/env python3
"""slide_028 measurement pass 4 — targeted local-window measurement of the 8 heads
and 8 labels around their expected polar positions, plus a corrected spoke scan with
raw pixel profiles for the suspicious rays (270/300/330)."""
import numpy as np
from PIL import Image
import json

A = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = A.shape[:2]
CXf, CYf = 578.0, 284.0  # measured fill center (pass 3)
CXs, CYs = 581.0, 297.2
def to_frame(xs_, ys_): return (18.63 + 0.96123 * xs_, 0.95556 * ys_)
def to_slide(fx, fy): return ((fx - 18.63) / 0.96123, fy / 0.95556)
def polar_f(deg, r_slide):
    xs_, ys_ = CXs + r_slide * np.cos(np.radians(deg)), CYs - r_slide * np.sin(np.radians(deg))
    return to_frame(xs_, ys_)

out = {}

# ---------- heads: local window around polar((k+1)*30, 224.5), margin +-20 slide pt ----------
print("== heads (orange mask, local window) ==")
heads = []
for k in range(8):
    fx, fy = polar_f((k + 1) * 30, 224.5)
    x0, x1 = int(fx) - 22, int(fx) + 23
    y0, y1 = int(fy) - 22, int(fy) + 23
    sub = A[y0:y1, x0:x1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (sr > 160) & ((sr - sg) > 80) & ((sg - sb) > 40)
    n = int(m.sum())
    if n:
        ys, xs = np.where(m)
        cx, cy = x0 + xs.mean(), y0 + ys.mean()
        sxx, syy = to_slide(cx, cy)
        pred = (CXs + 224.5 * np.cos(np.radians((k + 1) * 30)), CYs - 224.5 * np.sin(np.radians((k + 1) * 30)))
        print(f" head{k}: n={n} centroid slide ({sxx:.1f},{syy:.1f}) d_polar=({sxx-pred[0]:+.1f},{syy-pred[1]:+.1f})")
        heads.append({"k": k, "n": n, "slide": [round(sxx, 1), round(syy, 1)],
                      "d_polar": [round(sxx - pred[0], 1), round(syy - pred[1], 1)]})
    else:
        print(f" head{k}: NO orange ink in window around frame ({fx:.0f},{fy:.0f})")
        heads.append({"k": k, "n": 0})
out["heads"] = heads

# ---------- labels: local window around polar((2k+1)*15, 255), generous margin ----------
print("\n== labels (red mask, local window, orange excluded) ==")
labels = []
for k in range(8):
    fx, fy = polar_f((2 * k + 1) * 15, 255)
    x0, x1 = int(fx) - 30, int(fx) + 31
    y0, y1 = int(fy) - 22, int(fy) + 23
    sub = A[y0:y1, x0:x1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (sr > 150) & ((sr - sg) > 55) & (sg < 185) & ((sb - sg) > -15)
    n = int(m.sum())
    if n:
        ys, xs = np.where(m)
        cx, cy = x0 + xs.mean(), y0 + ys.mean()
        sxx, syy = to_slide(cx, cy)
        pred = (CXs + 255 * np.cos(np.radians((2 * k + 1) * 15)), CYs - 255 * np.sin(np.radians((2 * k + 1) * 15)))
        print(f" label{k}: n={n} centroid slide ({sxx:.1f},{syy:.1f}) d_polar=({sxx-pred[0]:+.1f},{syy-pred[1]:+.1f})")
        labels.append({"k": k, "n": n, "slide": [round(sxx, 1), round(syy, 1)],
                       "d_polar": [round(sxx - pred[0], 1), round(syy - pred[1], 1)]})
    else:
        print(f" label{k}: NO red ink in window around frame ({fx:.0f},{fy:.0f})")
        labels.append({"k": k, "n": 0})
out["labels"] = labels

# ---------- corrected spoke scan with pixel dumps ----------
print("\n== spoke rays: raw luminance dips along r 30..245 ==")
for deg in (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330):
    dips = []
    for rr_ in np.arange(30, 246, 1.0):
        x = CXf + rr_ * np.cos(np.radians(deg)); y = CYf - rr_ * np.sin(np.radians(deg))
        xi, yi = int(round(x)), int(round(y))
        if not (0 <= xi < W and 0 <= yi < H): continue
        c = A[yi, xi]
        d = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        if d > 45: dips.append(round(rr_))
    # compress to ranges
    rngs = []
    for v in dips:
        if rngs and v - rngs[-1][1] <= 2: rngs[-1][1] = v
        else: rngs.append([v, v])
    print(f" {deg:3d}deg: {len(dips):3d} dips  ranges {rngs[:14]}")
out["spoke_dips"] = {deg: len([1]) for deg in ()}

json.dump(out, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide028/measure4.json", "w"), indent=1)
print("\nsaved measure4.json")
