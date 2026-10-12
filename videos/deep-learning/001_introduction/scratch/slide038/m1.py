#!/usr/bin/env python3
"""Slide 038 forensics pass 1: global bands, box borders, title ink."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]
print(f"frame {W}x{H}")

reddish = (r > 120) & (g < 110) & (b < 110)
blue = (b > 130) & (b - r > 40) & (b - g > 30)
dark = (r < 110) & (g < 110) & (b < 110)

print("--- row profile: non-white/non-gray ink count per row (0..H) ---")
notbg = ~((abs(r - 232) < 20) & (abs(g - 232) < 20) & (abs(b - 232) < 20)) & ~(r > 235) & ~(g > 235) & ~(b > 235)
for y in range(H):
    c = notbg[y].sum()
    if c > 200:
        print(f"y={y} n={c}")

print("--- reddish rows with >300 px (rules/borders) ---")
for y in range(H):
    c = reddish[y].sum()
    if c > 300:
        xs = np.nonzero(reddish[y])[0]
        print(f"y={y} n={c} x {xs.min()}..{xs.max()}")

print("--- blue rows with >200 px (formula box border) ---")
for y in range(H):
    c = blue[y].sum()
    if c > 200:
        xs = np.nonzero(blue[y])[0]
        print(f"y={y} n={c} x {xs.min()}..{xs.max()}")

print("--- blue cols with >60 px ---")
for x in range(W):
    c = blue[:, x].sum()
    if c > 60:
        ys = np.nonzero(blue[:, x])[0]
        print(f"x={x} n={c} y {ys.min()}..{ys.max()}")

print("--- reddish cols with >80 px (diagram box sides) ---")
for x in range(W):
    c = reddish[:, x].sum()
    if c > 80:
        ys = np.nonzero(reddish[:, x])[0]
        print(f"x={x} n={c} y {ys.min()}..{ys.max()}")

print("--- reddish cols with 30..80 px in y 60..110 (title candidates) ---")
tit = reddish[55:115]
for x in range(W):
    c = tit[:, x].sum()
    if c > 25:
        ys = np.nonzero(tit[:, x])[0] + 55
        print(f"x={x} n={c} y {ys.min()}..{ys.max()}")
