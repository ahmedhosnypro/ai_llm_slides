#!/usr/bin/env python3
"""m1_chrome.py — fit slide_041.jpg's frame->slide mapping from its four chrome landmarks.

Landmarks (true slide coords from house_chrome.js law):
  panel left 42, right 918(+1 border -> inner edge 919), top 45, bottom-border rows 538-539
  badge circle d36 centered (893,71)
Frame side (zoomed-out ~0.958 capture + black letterbox below): find red border lines
and the yellow badge bbox in frame px, fit frame_x = a + b*slide_x, frame_y = c + d*slide_y.
"""
from PIL import Image
import numpy as np, json

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# red border ink: strong red, low green/blue (C00000-ish, allow JPEG noise)
red = (R > 120) & (G < 90) & (B < 90)
ys, xs = np.where(red)
print('red ink bbox: x', xs.min(), xs.max(), ' y', ys.min(), ys.max(), ' count', len(xs))

# vertical border lines: columns with long vertical red runs
colcount = red.sum(axis=0)
cand_cols = [x for x in range(W) if colcount[x] > 100]
print('candidate border columns (>100 red px):', cand_cols)

rowcount = red.sum(axis=1)
cand_rows = [y for y in range(H) if rowcount[y] > 100]
print('candidate border rows (>100 red px):', cand_rows)

# badge: yellow fill (FDFD96-ish: high R,G mid, low-ish B) in top-right quadrant
yellow = (R > 200) & (G > 200) & (B < 190) & (np.arange(W)[None, :] > 700)
ys2, xs2 = np.where(yellow)
if len(xs2):
    print('badge yellow bbox: x', xs2.min(), xs2.max(), ' y', ys2.min(), ys2.max(),
          ' center', (xs2.min() + xs2.max()) / 2, (ys2.min() + ys2.max()) / 2, ' count', len(xs2))

# purple ring (6A5ACD) check
purple = (np.abs(R - 0x6A) < 45) & (np.abs(G - 0x5A) < 45) & (np.abs(B - 0xCD) < 45) & (np.arange(W)[None, :] > 700)
ys3, xs3 = np.where(purple)
if len(xs3):
    print('purple ring bbox: x', xs3.min(), xs3.max(), ' y', ys3.min(), ys3.max(),
          ' center', (xs3.min() + xs3.max()) / 2, (ys3.min() + ys3.max()) / 2, ' count', len(xs3))

# black letterbox rows (full-width dark)
dark = (R < 60) & (G < 60) & (B < 60)
darkrow = dark.sum(axis=1)
lb = [y for y in range(H) if darkrow[y] > 700]
print('letterbox rows (>700 dark px):', lb[:5], '...', lb[-5:] if lb else None)
