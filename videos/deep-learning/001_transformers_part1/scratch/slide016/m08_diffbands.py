#!/usr/bin/env python3
"""Spatial diff analysis 16 vs 17: which bands/regions actually differ."""
import numpy as np
from PIL import Image

A = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg").convert("RGB")).astype(int)
d = np.abs(A - B).max(axis=2)

print("-- diff>24 by 20px row bands (x560-920) --")
for y0 in range(95, 540, 20):
    band = d[y0:y0+20, 560:920]
    print(f"  y{y0:3d}-{y0+19:3d}: {(band>24).mean()*100:5.1f}%")
print("\n-- diff>24 by 20px col bands (y104-523) --")
for x0 in range(560, 920, 20):
    band = d[104:524, x0:x0+20]
    print(f"  x{x0:3d}-{x0+19:3d}: {(band>24).mean()*100:5.1f}%")
# the highlight region of 16 vs 17
print("\n-- 16's yellow highlight bbox (r>235,g>235,b<130) minus callout zone --")
r, g, b = A[:,:,0], A[:,:,1], A[:,:,2]
yel = (r > 235) & (g > 235) & (b < 130)
ys, xs = np.where(yel[:, 560:925])
print(f"   diag-zone yellow: x{xs.min()+560}-{xs.max()+560} y{ys.min()}-{ys.max()} n={len(xs)}")
