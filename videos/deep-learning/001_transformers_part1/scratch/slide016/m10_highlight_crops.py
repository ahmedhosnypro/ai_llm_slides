#!/usr/bin/env python3
"""Highlight region: yellowish mask + red dash positions; crop generation for vision."""
import numpy as np
from PIL import Image
from collections import deque

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg"
IM = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:,:,0], IM[:,:,1], IM[:,:,2]

# yellowish incl. blends over peach/tan/olive
yel = (r > 225) & (g > 195) & (b < 170) & ((r - b) > 70) & ((g - b) > 50)
sub = yel[240:335, 660:800]
ys, xs = np.where(sub)
print(f"yellowish(660-800,240-335): x{xs.min()+660}-{xs.max()+660} y{ys.min()+240}-{ys.max()+240} n={len(xs)}")
# column profile
for x in range(660, 800, 4):
    col = yel[240:335, x]
    idx = np.where(col)[0]
    if len(idx) > 3:
        print(f"  x={x}: y {idx.min()+240}-{idx.max()+240} n={len(idx)}")
# row profile
for y in range(240, 335, 4):
    row = yel[y, 660:800]
    idx = np.where(row)[0]
    if len(idx) > 3:
        print(f"  y={y}: x {idx.min()+660}-{idx.max()+660} n={len(idx)}")

# red dash pixels around the highlight
red = (r > 140) & (g < 110) & (b < 110)
print("\nred pixels in x660-800 y240-340 (grouped by rows):")
for y in range(240, 340):
    idx = np.where(red[y, 660:800])[0]
    if len(idx):
        # group consecutive
        groups = []
        s = p = idx[0]
        for i in idx[1:]:
            if i == p + 1: p = i
            else: groups.append((s+660, p+660)); s = p = i
        groups.append((s+660, p+660))
        print(f"  y={y}: {groups}")

# red dash columns (left/right edges)
print("\nred pixel columns x660-800 over y240-340:")
for x in range(660, 800):
    idx = np.where(red[240:340, x])[0]
    if len(idx) > 2:
        print(f"  x={x}: n={len(idx)} y{idx.min()+240}-{idx.max()+240}")

# --- generate vision crops ---
import os
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide016/crops"
os.makedirs(OUT, exist_ok=True)
src = Image.open(SRC).convert("RGB")
CROPS = {
    "dec_bottom": (735, 395, 895, 530, 3),
    "dec_lower":  (735, 318, 895, 412, 3),
    "dec_upper":  (735, 195, 895, 325, 2),
    "dec_top":    (735, 100, 895, 200, 3),
    "enc_bottom": (575, 400, 735, 530, 3),
    "enc_container": (590, 260, 735, 415, 2),
    "highlight":  (665, 240, 800, 335, 3),
}
for name, (x0, y0, x1, y1, up) in CROPS.items():
    c = src.crop((x0, y0, x1, y1))
    c = c.resize(((x1-x0)*up, (y1-y0)*up), Image.LANCZOS)
    c.save(f"{OUT}/{name}.png")
    print(f"crop {name}: ({x0},{y0})-({x1},{y1}) x{up} -> {c.size}")
