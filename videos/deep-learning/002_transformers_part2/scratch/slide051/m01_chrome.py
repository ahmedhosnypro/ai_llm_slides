#!/usr/bin/env python3
"""m01_chrome.py — chrome landmarks for slide_051.jpg (960x540).
Derive the frame->slide mapping from the four chrome border landmarks
(panel left/right/top borders + bottom border), exactly as slide_002.js did.
"""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape
print("size", W, H)

# White canvas: near-white pixels
white = (np.abs(im - 255).max(axis=2) <= 6)
# Gray panel E9E9E7 = (233,233,231)
gray = (np.abs(im - np.array([233, 233, 231])).max(axis=2) <= 4)

# Column profile of white (canvas) — canvas spans full slide width in theory
col_white = white.sum(axis=0)
row_white = white.sum(axis=1)
# find leftmost/rightmost columns where white count is large (canvas)
thresh = 0.5 * H
cols = np.where(col_white > thresh)[0]
rows = np.where(row_white > 0.3 * W)[0]
print("white canvas cols:", cols.min(), cols.max(), " rows:", rows.min(), rows.max())

# Gray panel: find largest run of columns with many gray pixels
col_gray = gray.sum(axis=0)
row_gray = gray.sum(axis=1)
gcols = np.where(col_gray > 0.5 * H)[0]
grows = np.where(row_gray > 0.3 * W)[0]
print("gray panel cols:", (gcols.min(), gcols.max()) if len(gcols) else None,
      " rows:", (grows.min(), grows.max()) if len(grows) else None)

# Red border C00000 pixels (the thin red frame on panel left/right/top)
red = (im[:, :, 0] > 120) & (im[:, :, 1] < 80) & (im[:, :, 2] < 80)
col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
# vertical borders = columns with many red pixels
rcols = np.where(col_red > 100)[0]
rrows = np.where(row_red > 100)[0]
print("red vertical border cols:", rcols.tolist())
print("red horizontal border rows:", rrows.tolist())

# Badge: FDFD96-ish yellow circle near top-right (frame-space)
badge = (np.abs(im - np.array([253, 253, 150])).max(axis=2) <= 40)
ys, xs = np.where(badge)
if len(xs):
    sel = (xs > 700) & (ys < 150)
    if sel.any():
        print("badge bbox (frame): x", xs[sel].min(), xs[sel].max(), " y", ys[sel].min(), ys[sel].max(),
              " center", (xs[sel].min() + xs[sel].max()) / 2, (ys[sel].min() + ys[sel].max()) / 2)

# bottom black strip (letterbox)?
blackrow = ((im.max(axis=2) < 40).sum(axis=1))
brs = np.where(blackrow > 0.8 * W)[0]
print("full-black rows:", (brs.min(), brs.max()) if len(brs) else None)
