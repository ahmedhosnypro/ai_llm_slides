#!/usr/bin/env python3
"""m02_borders.py — precise red border + badge landmarks for slide_051 frame."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
# red-ish: strong red dominance (border C00000 = (192,0,0), JPEG-soft)
red = (r > 110) & (r - g > 60) & (r - b > 60)

col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
print("columns with >=30 red px:", [int(c) for c in np.where(col_red >= 30)[0]])
print("rows with >=60 red px:", [int(rr) for rr in np.where(row_red >= 60)[0]])

# vertical border candidates: search columns 40..80 and 880..920, any redness
for band, lo, hi in [("left", 40, 90), ("right", 880, 920)]:
    sub = red[:, lo:hi]
    counts = sub.sum(axis=0)
    top = np.argsort(counts)[::-1][:6]
    print(f"{band} band top red cols:", [(int(lo + t), int(counts[t])) for t in sorted(top)])

# top border: rows 35..60
sub = red[35:60, :]
counts = sub.sum(axis=1)
top = np.argsort(counts)[::-1][:8]
print("top band top red rows:", [(int(35 + t), int(counts[t])) for t in sorted(top)])

# bottom: rows 505..525
sub = red[505:525, 60:900]
counts = sub.sum(axis=1)
top = np.argsort(counts)[::-1][:8]
print("bottom band top red rows:", [(int(505 + t), int(counts[t])) for t in sorted(top)])

# badge: yellow FDFD96 circle, search window x 840..910, y 40..105
badge = (np.abs(im - np.array([253, 253, 150])).max(axis=2) <= 45)
win = badge[40:110, 840:915]
ys, xs = np.where(win)
if len(xs):
    print("badge bbox: x", 840 + xs.min(), 840 + xs.max(), " y", 40 + ys.min(), 40 + ys.max(),
          " center", 840 + (xs.min() + xs.max()) / 2, 40 + (ys.min() + ys.max()) / 2)

# gray panel precise edges: gray E9E9E7
gray = (np.abs(im - np.array([233, 233, 231])).max(axis=2) <= 6)
colg = gray.sum(axis=0)
# first/last col where gray count > 200
gc = np.where(colg > 200)[0]
print("gray cols(>200):", int(gc.min()), int(gc.max()))
rowg = gray.sum(axis=1)
gr = np.where(rowg > 200)[0]
print("gray rows(>200):", int(gr.min()), int(gr.max()))
