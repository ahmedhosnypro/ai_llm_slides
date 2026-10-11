#!/usr/bin/env python3
"""Measure slide_003.jpg: chrome border landmarks -> frame->slide mapping, then
title/subtitle ink boxes mapped to TRUE slide coordinates (pts, 1px=1pt at 960x540).

Slide 002's mapping precedent (certified build):
  frame_x = 18.63 + 0.96123 * slide_x ; frame_y = 0.95556 * slide_y
Landmarks (slide 002): frame panel left 59, right 902, top 43, bottom-border 516
<-> slide chrome 42, 919, 45, 540.
"""
import numpy as np
from PIL import Image
import json, sys

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"frame size: {W}x{H}")

R, G, B = a[..., 0], a[..., 1], a[..., 2]

# --- 1. locate the red border (C00000-ish: strong red, low green/blue) ---
red = (R > 120) & (R - G > 60) & (R - B > 60)

# Panel left/right border: columns with many red pixels (vertical strokes)
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
# print columns with high counts
cols = [c for c in range(W) if colcount[c] > 200]
rows = [r for r in range(H) if rowcount[r] > 200]
print("red-dominant columns (>200px):", cols)
print("red-dominant rows (>200px):", rows)

def runs(v):
    """group consecutive indices into runs, return list of (start,end,center)"""
    out = []
    if not v:
        return out
    s = p = v[0]
    for x in v[1:]:
        if x == p + 1:
            p = x
        else:
            out.append((s, p, (s + p) / 2))
            s = p = x
    out.append((s, p, (s + p) / 2))
    return out

print("column runs:", runs(cols))
print("row runs:", runs(rows))

# --- 2. badge: yellow circle top-right (FDFD96-ish) ---
yellow = (R > 200) & (G > 200) & (B < 210) & (B < G - 25) & (B < R - 25)
ys, xs = np.nonzero(yellow)
if len(xs):
    # restrict to top-right quadrant
    m = (xs > W * 0.75) & (ys < H * 0.35)
    bx, by = xs[m], ys[m]
    print(f"yellow badge bbox: x {bx.min()}..{bx.max()} (cx {(bx.min()+bx.max())/2}), "
          f"y {by.min()}..{by.max()} (cy {(by.min()+by.max())/2}), d~{bx.max()-bx.min()+1}x{by.max()-by.min()+1}, n={len(bx)}")

# --- 3. black letterbox strip at bottom: rows fully dark ---
dark = (R < 40) & (G < 40) & (B < 40)
darkrowfrac = dark.sum(axis=1) / W
black_rows = [r for r in range(H) if darkrowfrac[r] > 0.9]
print("near-fully-black rows:", runs(black_rows) if black_rows else "none")

# --- 4. blue title/subtitle ink (1C1CC8-ish royal blue) ---
blue = (B > 110) & (B - R > 60) & (B - G > 60) & (R < 120)
ys, xs = np.nonzero(blue)
print(f"blue ink pixel count: {len(xs)}")
if len(xs):
    print(f"blue ink overall bbox: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
    # row histogram to separate the two lines
    rowh = np.zeros(H, dtype=int)
    for y in ys:
        rowh[y] += 1
    bands = []
    inband = False
    for y in range(H):
        if rowh[y] > 0 and not inband:
            s = y; inband = True
        elif rowh[y] == 0 and inband:
            bands.append((s, y - 1)); inband = False
    if inband:
        bands.append((s, H - 1))
    bands = [b for b in bands if b[1] - b[0] >= 3]
    print("blue ink row bands (>=4px tall):", bands)
    for (y0, y1) in bands:
        m2 = (ys >= y0) & (ys <= y1)
        bx2, by2 = xs[m2], ys[m2]
        print(f"  band y{y0}..{y1}: x {bx2.min()}..{bx2.max()} (w {bx2.max()-bx2.min()+1}, cx {(bx2.min()+bx2.max())/2:.1f})")
