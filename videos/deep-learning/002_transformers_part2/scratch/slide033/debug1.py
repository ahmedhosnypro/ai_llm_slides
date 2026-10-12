#!/usr/bin/env python3
"""slide033 debug: where did title/subtitle/defs text land in render_1?"""
import numpy as np
from PIL import Image
from scipy import ndimage

ra = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide033/render_1.png").convert("RGB")).astype(int)
H, W, _ = ra.shape
RPT = 72 / 150.0
r, g, b = ra[..., 0], ra[..., 1], ra[..., 2]

print("render", W, "x", H)
# strong red ink rows (exclude chrome border rows)
red = (r > 130) & (g < 95) & (b < 95)
red[:92, :] = False
rows = red.sum(axis=1)
print("red ink rows (slide pt):")
y = 0
while y < H:
    if rows[y] > 6:
        y2 = y
        while y2 < H - 1 and rows[y2 + 1] > 6:
            y2 += 1
        xs = np.where(red[y:y2 + 1].any(axis=0))[0]
        print(f"  pt y {y*RPT:.1f}..{y2*RPT:.1f} x {xs.min()*RPT:.1f}..{xs.max()*RPT:.1f} (px rows {y}..{y2})")
        y = y2 + 1
    else:
        y += 1

navy = (b > 100) & (r < 100) & (b - r > 40)
rows = navy.sum(axis=1)
print("navy ink rows (slide pt):")
y = 0
while y < H:
    if rows[y] > 6:
        y2 = y
        while y2 < H - 1 and rows[y2 + 1] > 6:
            y2 += 1
        xs = np.where(navy[y:y2 + 1].any(axis=0))[0]
        print(f"  pt y {y*RPT:.1f}..{y2*RPT:.1f} x {xs.min()*RPT:.1f}..{xs.max()*RPT:.1f}")
        y = y2 + 1
    else:
        y += 1

# subtitle: any dark ink rows in y 60..110 pt
dark = (r < 150) & (g < 150) & (b < 160)
sub = dark[125:250, 100:1800]
rows = sub.sum(axis=1)
print("dark ink rows in y60..110pt x30..270pt:")
for y in range(sub.shape[0]):
    if rows[y] > 10:
        xs = np.where(sub[y].any(axis=0))[0]
        print(f"  pt y {(y+125)*RPT:.1f} n={rows[y]} x {(xs.min()+100)*RPT:.1f}..{(xs.max()+100)*RPT:.1f}")
