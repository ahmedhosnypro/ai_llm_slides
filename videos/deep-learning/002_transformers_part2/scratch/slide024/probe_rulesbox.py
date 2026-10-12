#!/usr/bin/env python3
"""Precisely probe the rules box border + fill in frame 24."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)

# horizontal scan across the box at a text-free row (frame y=358, between top border and line 1)
for y in (356, 358, 360):
    print(f"row {y}, x 50..90:", [f"{x}:{tuple(img[y,x])}" for x in range(54, 82, 3)])
# right side
for y in (356, 358, 360):
    print(f"row {y}, x 880..900:", [f"{x}:{tuple(img[y,x])}" for x in range(880, 898, 3)])
# vertical scan at x=400 (between texts)
print("col x=400, y 340..368:", [f"{y}:{tuple(img[y,400])}" for y in range(340, 369, 2)])
print("col x=400, y 490..520:", [f"{y}:{tuple(img[y,400])}" for y in range(490, 521, 2)])
# where does the bottom border sit? col x=200 and x=700
for x in (200, 700):
    print(f"col x={x}, y 496..516:", [f"{y}:{tuple(img[y,x])}" for y in range(496, 517, 2)])
# top border row: full-width blue count per row, y 335..365
b = img[..., 2]; r = img[..., 0]; g = img[..., 1]
blue = (b > 120) & (b > r + 40)
for y in range(335, 366):
    c = blue[y, 40:920].sum()
    if c > 20:
        print(f"top-ish border row y={y}: blue count {c}")
# left/right border cols: blue count per col, y 350..510
for x in range(40, 930):
    c = blue[350:510, x].sum()
    if c > 80:
        print(f"border col x={x}: blue count {c}")
