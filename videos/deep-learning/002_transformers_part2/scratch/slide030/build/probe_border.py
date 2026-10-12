#!/usr/bin/env python3
"""Slide 030: precise chrome border landmarks in quiet zones -> frame->slide mapping."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# reddish stroke: red dominant, dark enough to be the C00000 border (not pale highlights)
red = (R > 110) & (R - G > 60) & (R - B > 60)

# LEFT border: scan columns 40..80 in quiet rows 300..400 (content boxes may reach there;
# choose rows where only the border is red). Print per-column red counts in that band.
for y0, y1, label in [(300, 400, "mid-left"), (450, 500, "low-left")]:
    cols = {}
    for x in range(40, 90):
        c = int(red[y0:y1, x].sum())
        if c > 0:
            cols[x] = c
    print(f"LEFT band rows {y0}-{y1}: {cols}")

# RIGHT border: columns 880..930 in rows 300..400
cols = {}
for x in range(880, 935):
    c = int(red[300:400, x].sum())
    if c > 0:
        cols[x] = c
print(f"RIGHT band rows 300-400: {cols}")

# TOP border: rows 30..60, columns 300..700 (quiet of content? remember box starts ~18%)
rows = {}
for y in range(30, 62):
    c = int(red[y, 300:700].sum())
    if c > 0:
        rows[y] = c
print(f"TOP cols 300-700: {rows}")

# BOTTOM border: rows 505..520, columns 300..700
rows = {}
for y in range(500, 522):
    c = int(red[y, 300:700].sum())
    if c > 0:
        rows[y] = c
print(f"BOTTOM cols 300-700: {rows}")

# darkest rows (letterbox)
dark = (R < 40) & (G < 40) & (B < 40)
dr = [y for y in range(H) if dark[y].sum() > 800]
print("letterbox full-black rows:", dr[0] if dr else None, "..", dr[-1] if dr else None)

# Fit mapping from candidate landmarks once found manually below
