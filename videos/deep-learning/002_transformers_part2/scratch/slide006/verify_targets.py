#!/usr/bin/env python3
"""Verify L1 p-descender + L4/L5 right edge in the ORIGINAL with fine thresholds."""
from PIL import Image
import numpy as np

a = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg").convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
blue = (B - R > 30) & (B - G > 30) & (B > 100)   # looser

# L1 rows 158..170 (below the 161 cut): where is ink?
for y in range(158, 172):
    xs = np.where(blue[y, 100:500])[0]
    if len(xs): print(f"L1 frame y={y}: n={len(xs)} x {xs.min()+100}..{xs.max()+100}")

# L4 right edge: cols near 310..325, rows 269..283
print("\nL4 right-edge columns (loose mask):")
for x in range(305, 325):
    n = int(blue[269:284, x].sum())
    if n: print(f"  x={x}: n={n}")
print("L4 with loose mask, full bbox:")
ys, xs = np.where(blue[267:286, 100:340])
print("  x %d..%d y %d..%d" % (xs.min()+100, xs.max()+100, ys.min()+267, ys.max()+267))

print("\nL5 right-edge columns (loose mask):")
for x in range(450, 470):
    n = int(blue[309:324, x].sum())
    if n: print(f"  x={x}: n={n}")
ys, xs = np.where(blue[307:326, 100:480])
print("L5 loose bbox: x %d..%d y %d..%d" % (xs.min()+100, xs.max()+100, ys.min()+307, ys.max()+307))

# L1 loose bbox + right edge
ys, xs = np.where(blue[145:170, 100:500])
print("\nL1 loose bbox: x %d..%d y %d..%d" % (xs.min()+100, xs.max()+100, ys.min()+145, ys.max()+145))

# title right edge loose
red = (R - G > 30) & (R - B > 30) & (R > 90)
ys, xs = np.where(red[60:110, 200:700])
print("TITLE loose bbox: x %d..%d y %d..%d" % (xs.min()+200, xs.max()+200, ys.min()+60, ys.max()+60))
