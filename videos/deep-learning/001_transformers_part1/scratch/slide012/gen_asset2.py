#!/usr/bin/env python3
"""Measure pass 6: iterative refined bounds for all highlight boxes; then regenerate
the baked asset with the CORRECT rects."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
a = np.asarray(Image.open(f"{VID}/unique_slides/slide_012.jpg").convert("RGB")).astype(float)
page = Image.open(f"{VID}/scratch/slide012/page300-01.png").convert("RGB")
pa = np.asarray(page).astype(float).copy()

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
pinkm = (r - g > 40) & (b - g > 40) & (r > 190) & (b > 185)
tanm = (r - b > 35) & (r > 220) & (g > 140) & (g < 240) & (b > 100) & (b < 225) & (g - b > 12)

def yband(mask, x0, x1, y0, y1, frac=0.5):
    f = mask[y0:y1, x0:x1].mean(axis=1)
    idx = np.where(f > frac)[0]
    return (y0 + int(idx.min()), y0 + int(idx.max())) if len(idx) else None

def xspan(mask, y0, y1, x0, x1, frac=0.5):
    f = mask[y0:y1 + 1, x0:x1].mean(axis=0)
    idx = np.where(f > frac)[0]
    return (x0 + int(idx.min()), x0 + int(idx.max())) if len(idx) else None

print("== refined boxes ==")
rects = {}
for name, (wx0, wx1, wy0, wy1) in {
    "vaswani": (255, 345, 168, 192), "shazeer": (378, 468, 168, 192),
    "parmar": (487, 592, 168, 192), "uszkoreit": (602, 708, 168, 192),
    "jones": (245, 352, 228, 252), "kaiser": (563, 657, 228, 252),
}.items():
    # seed y-band from a central column slice, then x-span, then refine y on the x-span
    by = yband(pinkm, (wx0 + wx1) // 2 - 20, (wx0 + wx1) // 2 + 20, wy0, wy1, 0.4)
    bx = xspan(pinkm, by[0], by[1], wx0, wx1, 0.5)
    by2 = yband(pinkm, bx[0] + 5, bx[1] - 5, wy0 - 6, wy1 + 6, 0.5)
    rects[name] = (bx, by2)
    print(f"  {name}: x[{bx[0]},{bx[1]}] y[{by2[0]},{by2[1]}]")

ty = yband(tanm, 400, 540, 46, 92, 0.5)
tx = xspan(tanm, ty[0] + 2, ty[1] - 2, 320, 615, 0.5)
ty2 = yband(tanm, tx[0] + 10, tx[1] - 10, 44, 94, 0.5)
print(f"  title: x[{tx[0]},{tx[1]}] y[{ty2[0]},{ty2[1]}]")

# date band: column profile to find left/right, row profile for top/bottom
bx = xspan(tanm, 220, 280, 86, 150, 0.5)
by = yband(tanm, bx[0] + 8, bx[1] - 8, 170, 325, 0.5)
print(f"  date band: x[{bx[0]},{bx[1]}] y[{by[0]},{by[1]}]")
# raw col medians at band mid to see left edge precisely
for x in range(93, 104):
    print(f"    x={x} y230 median: {np.median(a[225:235, x], axis=0).astype(int)}")

# ---------- mapping ----------
SX, OX = 0.28909, 97.13
SY, OY = 0.28480, -60.52
f2p_x = lambda fx: (fx - OX) / SX
f2p_y = lambda fy: (fy - OY) / SY

def bake(fx0, fx1, fy0, fy1, alpha, color, name):
    x0, x1 = int(round(f2p_x(fx0))), int(round(f2p_x(fx1)))
    y0, y1 = int(round(f2p_y(fy0))), int(round(f2p_y(fy1)))
    x0c, y0c = max(0, x0), max(0, y0)
    x1c, y1c = min(pa.shape[1], x1), min(pa.shape[0], y1)
    reg = pa[y0c:y1c, x0c:x1c]
    pa[y0c:y1c, x0c:x1c] = alpha * np.array(color) + (1 - alpha) * reg
    print(f"  baked {name}: page x[{x0},{x1}] y[{y0},{y1}]")

ALPHA_TAN, COL_TAN = 0.275, (233, 109, 0)
ALPHA_PINK, COL_PINK = 0.52, (226, 86, 230)

print("== baking (corrected rects) ==")
bake(tx[0], tx[1] + 1, ty2[0], ty2[1] + 1, ALPHA_TAN, COL_TAN, "title")
for name, (bx_, by_) in rects.items():
    bake(bx_[0], bx_[1] + 1, by_[0], by_[1] + 1, ALPHA_PINK, COL_PINK, name)
# date band: bake if fully right of page x0 (frame 97.1); else shape
print(f"  date band left edge frame x={bx[0]} (page edge at frame 97.1)")

PAD_L = 13
x0, x1, y0, y1 = -PAD_L, 2419, 397, 2054
canvas = np.full((y1 - y0, x1 - x0, 3), 255.0)
sx0 = max(0, x0)
canvas[:, sx0 - x0:, :] = pa[y0:y1, sx0:x1]
Image.fromarray(canvas.astype(np.uint8)).save(f"{VID}/recreated_pptx/build/assets/slide012_page1.png")
print(f"== asset saved, {canvas.shape[1]}x{canvas.shape[0]}")
