#!/usr/bin/env python3
"""Measure slide_035.jpg original frame: chrome landmarks -> frame->slide mapping,
badge cross-check, and content ink bboxes (title red, blue body lines).
Follows the slide_002 measurement approach (frame zoomed ~0.958, letterbox below)."""
from PIL import Image
import numpy as np

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_035.jpg"
im = Image.open(P).convert("RGB")
W, H = im.size
print(f"frame size: {W}x{H}")
a = np.asarray(im).astype(int)

R, G, B = a[..., 0], a[..., 1], a[..., 2]

# ---- red border ink (C00000 ~ (192,0,0)): strong red, low G, low B
red = (R > 130) & (G < 90) & (B < 90)
# ---- gray panel E9E9E7 ~ (233,233,231)
gray = (abs(R - 233) < 12) & (abs(G - 233) < 12) & (abs(B - 231) < 14)
# ---- white canvas
white = (R > 245) & (G > 245) & (B > 245)
# ---- blue body text (#1A1AB8 ~ (26,26,184)): strong blue, low R, low G
blue = (B > 120) & (R < 110) & (G < 110)
# ---- yellow badge FDFD96
yellow = (R > 220) & (G > 215) & (B < 190)

# ---- letterbox strip (black rows at bottom)
row_dark = ((R < 60) & (G < 60) & (B < 60)).sum(axis=1)
dark_rows = [y for y in range(H) if row_dark[y] > W * 0.8]
print("dark(>80% width) rows:", dark_rows[:5], "...", dark_rows[-5:] if dark_rows else "none")

# ---- gray panel extents (per row/col counts) — restrict to non-dark rows
gray_cols = gray.sum(axis=0)
gray_rows = gray.sum(axis=1)
gcols = [x for x in range(W) if gray_cols[x] > 30]
grows = [y for y in range(H) if gray_rows[y] > 30]
print(f"gray panel cols: {gcols[0]}..{gcols[-1]}  rows: {grows[0]}..{grows[-1]}")

# ---- red border landmarks: leftmost/rightmost red col with long vertical run,
# topmost red row with long horizontal run
red_cols = red.sum(axis=0)
red_rows = red.sum(axis=1)
rcols = [x for x in range(W) if red_cols[x] > 50]
rrows = [y for y in range(H) if red_rows[y] > 50]
print(f"red long-run cols: {rcols[:6]}...{rcols[-6:]}")
print(f"red long-run rows: {rrows[:6]}...{rrows[-6:]}")

# ---- badge: yellow bbox
ys, xs = np.where(yellow)
if len(xs):
    print(f"badge yellow bbox: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  center ({(xs.min()+xs.max())/2},{(ys.min()+ys.max())/2})")
    # numeral ink inside badge (dark pixels within yellow bbox)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    sub = a[by0:by1 + 1, bx0:bx1 + 1]
    dark = (sub[..., 0] < 120) & (sub[..., 1] < 120) & (sub[..., 2] < 120)
    dys, dxs = np.where(dark)
    if len(dxs):
        print(f"  numeral ink bbox (abs): x {bx0+dxs.min()}..{bx0+dxs.max()}  y {by0+dys.min()}..{by0+dys.max()}")

# ---- red title ink: red pixels with long-ish horizontal extent above the body area.
# Title should be the big red text block between border top and list area.
red_ys, red_xs = np.where(red)
# Split red ink by rows: cluster into bands
rows_with_red = sorted(set(red_ys))
bands = []
if rows_with_red:
    start = prev = rows_with_red[0]
    for y in rows_with_red[1:]:
        if y - prev > 3:
            bands.append((start, prev))
            start = y
        prev = y
    bands.append((start, prev))
print("red ink row-bands (start,end,height):")
for (y0, y1) in bands:
    m = (red_ys >= y0) & (red_ys <= y1)
    if m.sum() > 40:
        print(f"  y {y0}..{y1} h={y1-y0+1} px_count={m.sum()} x {red_xs[m].min()}..{red_xs[m].max()}")

# ---- blue ink bands
blue_ys, blue_xs = np.where(blue)
rows_with_blue = sorted(set(blue_ys))
bbands = []
if rows_with_blue:
    start = prev = rows_with_blue[0]
    for y in rows_with_blue[1:]:
        if y - prev > 4:
            bbands.append((start, prev))
            start = y
        prev = y
    bands_ = bbands
    bbands.append((start, prev))
print("blue ink row-bands (start,end,height,x-extent,px_count):")
for (y0, y1) in bbands:
    m = (blue_ys >= y0) & (blue_ys <= y1)
    if m.sum() > 20:
        # x-extent may include multiple words per line; print column histogram clusters
        xs_line = np.sort(blue_xs[m])
        # cluster columns with gap > 12
        clusters = []
        cs = cp = xs_line[0]
        for x in xs_line[1:]:
            if x - cp > 12:
                clusters.append((cs, cp))
                cs = x
            cp = x
        clusters.append((cs, cp))
        print(f"  y {y0}..{y1} h={y1-y0+1} n={m.sum()} clusters={clusters}")
