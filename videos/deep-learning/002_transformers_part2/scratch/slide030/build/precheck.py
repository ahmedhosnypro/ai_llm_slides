#!/usr/bin/env python3
"""Slide 030: pre-checks (matrix box top border, clean caption extents, id2 right edge)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)

# 1) matrix box top border: horizontal blue line, x100..600, rows 330..360
for y in range(330, 362):
    c = int(blum[y, 100:600].sum())
    if c > 100:
        print(f"matrix top border candidate row {y}: {c}")

# 2) captions clean of the brace (brace x272..469 y447..467)
ys, xs = np.where(redm[438:462, 95:270])
print(f"caption1 clean: x {xs.min()+95}..{xs.max()+95} y {ys.min()+438}..{ys.max()+438}")
ys, xs = np.where(redm[438:466, 472:620])
print(f"caption2 clean: x {xs.min()+472}..{xs.max()+472} y {ys.min()+438}..{ys.max()+438}")

# 3) remember id2 right edge, band clear of the box bottom border (rows 184+)
ys, xs = np.where(blum[164:182, 505:845])
print(f"id2 clean: x {xs.min()+505}..{xs.max()+505} y {ys.min()+164}..{ys.max()+164}")

# 4) v2 r1/r2 exact lefts (prefix starts) and matrix lv cells
for label, (x0, x1, y0, y1) in [("v2r1", (240, 360, 150, 178)), ("v2r2", (240, 360, 193, 218))]:
    ys, xs = np.where(((R < 110) & (G < 110) & (B < 110))[y0:y1, x0:x1])
    print(f"{label}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
