#!/usr/bin/env python3
"""Slide 038 — defbox lines (fixed), chrome right border, diagram panel top, vector rows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

blue = (B > 110) & (R < 110) & (G < 110)
red = (R > 110) & (G < 110) & (B < 110)

print("== defbox text bands (fixed) ==")
seg = blue[95:250, 97:860]
counts = seg.sum(axis=1)
in_band = False
for y in range(95, 250):
    c = counts[y - 95]
    if c > 3 and not in_band:
        y0 = y; in_band = True
    elif c <= 3 and in_band:
        band = blue[y0:y, 97:860]
        cols = np.where(band.sum(axis=0) > 0)[0]
        print(f"  band y {y0}..{y-1} x {cols.min()+97}..{cols.max()+97}"
              f" -> slide y {invy(y0)}..{invy(y-1)} x {invx(cols.min()+97)}..{invx(cols.max()+97)}  (h {y-y0})")
        in_band = False

print("== defbox top/bottom border rows (any blue row with count>200 in x 97..860) ==")
for y in range(95, 250):
    c = blue[y, 97:860].sum()
    if c > 200:
        print("  row", y, c)

print("== chrome right border probe (cols 880..915, rows 60..500) ==")
for x in range(880, 916):
    f_ = red[60:500, x].mean()
    if f_ > 0.3:
        print("  col", x, f"frac={f_:.2f}", "-> slide x", invx(x))

print("== diagram panel top row (rows 238..262, x 100..850) ==")
for y in range(238, 263):
    c = red[y, 100:850].sum()
    if c > 300:
        print("  row", y, c, "-> slide y", invy(y))
