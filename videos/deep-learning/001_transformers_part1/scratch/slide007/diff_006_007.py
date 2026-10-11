#!/usr/bin/env python3
"""slide007 delta verification: pixel-diff slide_006.jpg vs slide_007.jpg.
Verifies the dispatch claim: 7 = 6's composition + delta (callout box, its connector,
'(Challenges)' title line) and nothing removed/moved/resized."""
from PIL import Image, ImageChops
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
a = np.asarray(Image.open(f"{BASE}/slide_006.jpg").convert("RGB")).astype(int)
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)
print("shapes:", a.shape, b.shape)

d = np.abs(a - b).sum(axis=2)  # per-pixel L1
mask = d > 60  # significant difference
ys, xs = np.nonzero(mask)
print(f"diff pixels (>60 L1): {mask.sum()}")
if len(ys):
    print("overall diff bbox: x", xs.min(), "-", xs.max(), " y", ys.min(), "-", ys.max())

# cluster diff rows into bands
rows = np.nonzero(mask.sum(axis=1) > 3)[0]
bands = []
if len(rows):
    start = prev = rows[0]
    for r in rows[1:]:
        if r - prev > 4:
            bands.append((start, prev)); start = r
        prev = r
    bands.append((start, prev))
print("\ndiff row-bands (y ranges) with column extents:")
for (y0, y1) in bands:
    sub = mask[y0:y1 + 1]
    cols = np.nonzero(sub.sum(axis=0) > 0)[0]
    print(f"  y {y0:3d}..{y1:3d}  x {cols.min():3d}..{cols.max():3d}  px={int(sub.sum())}")

# check REMOVAL: pixels where 006 has dark ink but 007 is light (content removed)
dark6 = (a.sum(axis=2) < 400)
light7 = (b.sum(axis=2) > 500)
removed = dark6 & light7
print("\n'ink in 006 but gone in 007' pixels:", int(removed.sum()))
if removed.sum():
    rys, rxs = np.nonzero(removed)
    print("  removal bbox: x", rxs.min(), "-", rxs.max(), "y", rys.min(), "-", rys.max())
# check SHIFT: ink in 007 at coords where 006 had ink of different color in same neighborhood
