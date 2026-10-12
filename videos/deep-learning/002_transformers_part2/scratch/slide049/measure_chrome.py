#!/usr/bin/env python3
"""Measure slide_049.jpg chrome landmarks -> frame->slide mapping.

Fits the affine mapping (scale + offset) from the four chrome landmarks:
panel left/right border columns, top border row, bottom border stroke row,
plus badge yellow-bbox center cross-check (target slide coords 42, 919, 45, 540
per shared_patterns/house_chrome.js; badge center (893,71) d36).
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("frame size:", W, "x", H)

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# red border pixels: strong red, low green/blue (C00000 core -> JPEG halo widened)
red = (r > 120) & (g < 90) & (b < 90) & (r - g > 70) & (r - b > 70)

# ---- column profile of red border pixels (full height) ----
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
# candidate vertical border lines: columns with tall red runs
tall = np.where(colcount > 200)[0]
print("tall red columns (>200px):", tall.tolist())
wide = np.where(rowcount > 400)[0]
print("wide red rows (>400px):", wide.tolist())

# Left border: first cluster of tall columns; right border: last cluster
def clusters(vals, gap=3):
    out = []
    cur = [vals[0]]
    for v in vals[1:]:
        if v - cur[-1] <= gap:
            cur.append(v)
        else:
            out.append(cur); cur = [v]
    out.append(cur)
    return out

if len(tall):
    cl = clusters(tall)
    print("column clusters:", [(c[0], c[-1], int(colcount[c].max())) for c in cl][:12])
if len(wide):
    rw = clusters(wide)
    print("row clusters:", [(c[0], c[-1], int(rowcount[c].max())) for c in rw][:12])

# ---- badge: yellow pixels (FDFD96-ish: high r,g mid; low blue) top-right ----
yellow = (r > 200) & (g > 200) & (b < 190) & (abs(r - g) < 40) & (b - r < -20)
ys, xs = np.where(yellow)
if len(xs):
    # restrict to top-right quadrant
    m = (xs > W * 0.8) & (ys < H * 0.25)
    if m.sum():
        bx0, bx1, by0, by1 = xs[m].min(), xs[m].max(), ys[m].min(), ys[m].max()
        print("badge yellow bbox: x %d..%d  y %d..%d  center (%.1f, %.1f)  d=%.1f" %
              (bx0, bx1, by0, by1, (bx0 + bx1) / 2, (by0 + by1) / 2, (bx1 - bx0 + by1 - by0) / 2))

# ---- purple ring pixels (6A5ACD) near badge ----
purple = (abs(r - 106) < 60) & (abs(g - 90) < 60) & (abs(b - 205) < 50) & (b - r > 40) & (b - g > 40)
ys2, xs2 = np.where(purple)
if len(xs2):
    m2 = (xs2 > W * 0.8) & (ys2 < H * 0.25)
    if m2.sum():
        print("badge purple-ring bbox: x %d..%d y %d..%d" % (xs2[m2].min(), xs2[m2].max(), ys2[m2].min(), ys2[m2].max()))

# ---- sample colors along horizontal scanline through panel top area ----
for yy in [40, 43, 45, 48, 52, 60]:
    row = a[yy]
    # find transitions from white to gray/red
    s = []
    prev = None
    for xx in range(0, 120):
        px = tuple(row[xx])
        k = 'W' if min(px) > 235 else ('R' if px[0] - max(px[1], px[2]) > 60 else ('G' if abs(px[0]-233)<15 and abs(px[1]-233)<15 else '?'))
        if k != prev:
            s.append((xx, k, px))
            prev = k
    print("row", yy, s[:10])
