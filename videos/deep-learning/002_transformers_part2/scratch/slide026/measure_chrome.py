#!/usr/bin/env python3
"""Measure slide_026.jpg chrome landmarks -> frame->slide mapping (per slide_002.js method).
Frame: 960x540 (approx). Playlist chrome in TRUE slide coords (960x540, 1px=1pt):
  panel left 42, right 918, top 45, bottom-border 538-539; badge center (893,71) d36.
Output: affine map frame->slide from 4 chrome landmarks (border lines + badge).
"""
from PIL import Image
import numpy as np, json, sys

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
W, H = img.size
a = np.asarray(img).astype(int)
print(f"frame size: {W}x{H}")

r, g, b = a[..., 0], a[..., 1], a[..., 2]

# red border mask: C00000 ~ (192,0,0); allow JPEG noise
red = (r > 130) & (g < 90) & (b < 90)

# Panel border: vertical red lines. Find columns with long red runs
col_counts = red.sum(axis=0)
row_counts = red.sum(axis=1)
# print top candidate columns/rows
cols = np.argsort(col_counts)[::-1][:20]
rows = np.argsort(row_counts)[::-1][:20]
print("top red cols:", sorted([(int(c), int(col_counts[c])) for c in cols]))
print("top red rows:", sorted([(int(rw), int(row_counts[rw])) for rw in rows]))

# badge: yellow FDFD96 ~ (253,253,150) with purple ring 6A5ACD
yellow = (r > 200) & (g > 200) & (b > 100) & (b < 200)
ys, xs = np.nonzero(yellow)
if len(xs):
    print(f"yellow bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  center ({(xs.min()+xs.max())/2},{(ys.min()+ys.max())/2}) n={len(xs)}")
