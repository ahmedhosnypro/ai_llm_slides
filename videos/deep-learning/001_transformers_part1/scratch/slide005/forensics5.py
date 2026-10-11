#!/usr/bin/env python3
"""Forensics 5: precise per-cell fills, outline rows per stack, element bboxes."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

STACKS = [("Words Vectors", 163, 244), ("1st FM", 308, 390), ("2nd FM", 456, 537),
          ("3rd FM", 598, 679), ("4th FM", 737, 818)]

def avg(y0, y1, x0, x1):
    return tuple(round(v, 1) for v in im[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0))

# 1) outline rows per stack: rows where many pixels across the stack width are
#    "outline-like" (darker than panel gray, low saturation-ish)
print("=== outline rows per stack (row mean < 215 and > 60 non-white-ish px) ===")
bounds = {}
for nm, x0, x1 in STACKS:
    strip = im[150:500, x0+4:x1-4]
    rows = []
    for i in range(strip.shape[0]):
        rowpx = strip[i]
        dark = ((rowpx[:, 0] < 215) | (rowpx[:, 1] < 215) | (rowpx[:, 2] < 215)).sum()
        if dark > (x1 - x0) * 0.5:
            rows.append(150 + i)
    # collapse consecutive
    runs = []
    s = p = None
    for y in rows:
        if s is None:
            s = p = y
        elif y == p + 1:
            p = y
        else:
            runs.append((s + p) / 2); s = p = y
    if s is not None:
        runs.append((s + p) / 2)
    bounds[nm] = runs
    print(f"{nm}: {len(runs)} lines: {[round(v,1) for v in runs]}")
    if len(runs) > 1:
        pitches = [round(runs[i+1]-runs[i],1) for i in range(len(runs)-1)]
        print(f"   pitches: {pitches}")

# 2) per-cell fill classification using stack-1 boundaries for all stacks
print("\n=== per-cell fill (5x5 avg at cell center) ===")
b1 = bounds["Words Vectors"]
top, bot = b1[0], b1[-1]
ncell = len(b1) - 1
pitch = (bot - top) / ncell
print(f"stack1: top {top:.1f} bot {bot:.1f} ncell {ncell} pitch {pitch:.2f}")
for nm, x0, x1 in STACKS:
    print(f"--- {nm} (x{x0}-{x1}) ---")
    fills = []
    for ci in range(ncell):
        cy = int(top + pitch * (ci + 0.5))
        cx = (x0 + x1) // 2
        a = avg(cy - 2, cy + 3, cx - 4, cx + 5)
        fills.append(a)
        print(f"  cell {ci+1:2d} (y{top+pitch*ci:.0f}-{top+pitch*(ci+1):.0f}): {a}")
