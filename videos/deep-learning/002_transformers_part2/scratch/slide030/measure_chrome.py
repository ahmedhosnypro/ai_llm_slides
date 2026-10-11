#!/usr/bin/env python3
"""Slide 030: measure chrome landmarks + fit frame->slide mapping (cf. slide_002/032)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
print(f"frame {W}x{H}")
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# red-ish border pixels (C00000 core allows JPEG spread)
red = (R > 120) & (G < 70) & (B < 70)
# count red per column / row in the border zones
col_counts = red.sum(axis=0)
row_counts = red.sum(axis=1)
# vertical border strokes: columns with big red counts
cand_cols = [x for x in range(W) if col_counts[x] > 200]
cand_rows = [y for y in range(H) if row_counts[y] > 200]
print("red-heavy columns:", cand_cols)
print("red-heavy rows:", cand_rows)

# letterbox: near-black full-width rows at the bottom
dark = (R < 40) & (G < 40) & (B < 40)
dark_rows = [y for y in range(H) if dark[y].sum() > 700]
print("near-black full-width rows:", dark_rows[:10], "...", dark_rows[-10:] if len(dark_rows) > 10 else "")

# badge: yellow blob top-right (yellow: R high, G high, B low)
yellow = (R > 200) & (G > 200) & (B < 160)
ys, xs = np.where(yellow[30:120, 800:960])
if len(xs):
    print(f"badge yellow bbox frame x {xs.min()+800}..{xs.max()+800} y {ys.min()+30}..{ys.max()+30} center ({(xs.min()+xs.max())/2+800:.1f},{(ys.min()+ys.max())/2+30:.1f})")
else:
    print("no yellow badge blob found in 800..960 x 30..120")

# purple ring pixels near badge
purple = (B > 150) & (R > 80) & (R < 160) & (G < 120)
ys2, xs2 = np.where(purple[30:120, 800:960])
if len(xs2):
    print(f"badge purple-ring bbox x {xs2.min()+800}..{xs2.max()+800} y {ys2.min()+30}..{ys2.max()+30}")
