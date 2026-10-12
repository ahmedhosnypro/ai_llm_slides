#!/usr/bin/env python3
"""Measure slide_027.jpg chrome landmarks -> frame->slide mapping.

Video 002's capture is zoomed out (~0.958 scale, see build/slide_002.js header).
Fit frame_x = a + b*slide_x ; frame_y = c*slide_y from four chrome landmarks:
panel left/right/top border + bottom border rows (chrome: 42, 919, 45, 540)
and cross-check with the badge circle bbox center (chrome: (893,71) d36).
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
).convert("RGB")).astype(int)
H, W, _ = im.shape
print("frame size:", W, H)

r, g, b = im[..., 0], im[..., 1], im[..., 2]
# red border C00000-ish: strong red, low green/blue
red = (r > 120) & (g < 90) & (b < 90) & (r - g > 60) & (r - b > 60)

# --- vertical border lines: columns with many red pixels in top half
colcount = red[:300, :].sum(axis=0)
cand = [x for x in range(W) if colcount[x] > 150]
print("left/right border candidate cols:", cand[:6], cand[-6:] if cand else [])

# --- horizontal border lines: rows with many red pixels
rowcount = red[:, :].sum(axis=1)
cand_r = [y for y in range(H) if rowcount[y] > 300]
print("top/bottom border candidate rows:", cand_r[:6], cand_r[-6:] if cand_r else [])

# --- badge: yellow FDFD96-ish blob in top-right quadrant
yel = (r > 220) & (g > 220) & (b > 110) & (b < 200)
ys, xs = np.where(yel)
if len(xs):
    m = (xs > 700) & (ys < 200)
    bx, by = xs[m], ys[m]
    print("badge bbox: x %d..%d (cx %.1f, w %d)  y %d..%d (cy %.1f, h %d)" % (
        bx.min(), bx.max(), (bx.min()+bx.max())/2, bx.max()-bx.min()+1,
        by.min(), by.max(), (by.min()+by.max())/2, by.max()-by.min()+1))

# bottom black letterbox bar rows
dark = (r < 40) & (g < 40) & (b < 40)
darkrows = [y for y in range(H) if dark[y, :].sum() > 700]
print("letterbox rows:", darkrows[:8])
