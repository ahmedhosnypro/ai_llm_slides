#!/usr/bin/env python3
"""Probe title glyph extents per column (loose red) to pin cap-top and baseline."""
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_050.jpg"
im = Image.open(FR).convert("RGB")
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 90 and r - max(g, b) > 50

def is_redcore(c):
    r, g, b = c
    return r > 140 and g < 80 and b < 80

# row profile over the title band
print("row profile (x 235..715): y, loose_count, core_count")
for y in range(262, 312):
    lo = sum(1 for x in range(235, 716) if is_red(px[x, y]))
    co = sum(1 for x in range(235, 716) if is_redcore(px[x, y]))
    if lo or co:
        print(f"  y={y}: loose={lo} core={co}")

# per-column (ymin, ymax) with loose red for selected columns
print("per-column extents (loose):")
for x in list(range(238, 260, 2)) + [300, 400, 480, 495, 500, 600, 660, 680, 690, 695, 700, 705, 709]:
    ys = [y for y in range(255, 315) if is_red(px[x, y])]
    if ys:
        print(f"  x={x}: y {min(ys)}..{max(ys)}")

# gap profile: which x-columns have any ink (loose) -> word gaps
cols = []
for x in range(230, 720):
    n = sum(1 for y in range(255, 315) if is_red(px[x, y]))
    cols.append((x, n))
runs = []
cur = None
for x, n in cols:
    if n > 0:
        if cur is None:
            cur = [x, x]
        else:
            cur[1] = x
    else:
        if cur is not None:
            runs.append(tuple(cur))
            cur = None
if cur:
    runs.append(tuple(cur))
print("ink runs (column spans):", runs)
