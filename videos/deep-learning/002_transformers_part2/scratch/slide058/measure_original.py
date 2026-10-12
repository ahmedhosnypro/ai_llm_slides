#!/usr/bin/env python3
"""Measure slide_058.jpg chrome landmarks + title ink, fit frame->slide mapping."""
from PIL import Image
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_058.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[..., 0], im[..., 1], im[..., 2]

# ---- red border strokes (C00000-ish): strong red, low green/blue
red = (R > 120) & (G < 80) & (B < 80)

# vertical strokes: columns with many red px
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
cols = [x for x in range(W) if colcount[x] > 300]
rows = [y for y in range(H) if rowcount[y] > 300]
print("red-heavy columns:", cols)
print("red-heavy rows:", rows)

# top border stroke: rows with wide red span in upper area
for y in range(0, 80):
    span = red[y].sum()
    if span > 500:
        print("top stroke row", y, "span", span)

# bottom border stroke: rows in 490..540 with wide red span
for y in range(480, H):
    span = red[y].sum()
    if span > 200:
        print("bottom-area red row", y, "span", span)

# ---- badge: yellow fill cluster (FDFD96-ish)
yellow = (R > 200) & (G > 200) & (B < 180) & (abs(R - G) < 40)
ys, xs = np.nonzero(yellow)
if len(xs):
    print("yellow bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(),
          "center", (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2, "n", len(xs))

# ---- black strip: rows where nearly all pixels are dark
dark = (R < 60) & (G < 60) & (B < 60)
for y in range(H):
    frac = dark[y].mean()
    if frac > 0.5:
        print("dark row", y, "frac", round(frac, 3))
