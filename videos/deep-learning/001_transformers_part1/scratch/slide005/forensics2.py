#!/usr/bin/env python3
"""Forensics 2: per-cell fill classification for the 5 stacks, gray bars, title, misc."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def near(px, target, tol=28):
    return all(abs(int(px[i]) - target[i]) <= tol for i in range(3))

PALETTE = {
    "FFFFCC": (255, 255, 204), "FFCC99": (255, 204, 153), "99FFFF": (153, 255, 255),
    "FFCCFF": (255, 204, 255), "CCFFCC": (204, 255, 204), "WHITE": (255, 255, 255),
    "BFBFBF": (191, 191, 191), "F2F2F2": (242, 242, 242), "E9E9E7": (233, 233, 231),
}

def classify(px):
    best, bd = None, 10**9
    for name, t in PALETTE.items():
        d = sum((int(px[i]) - t[i]) ** 2 for i in range(3))
        if d < bd:
            best, bd = name, d
    return best

STACKS = [(163, 244), (308, 390), (456, 537), (598, 679), (737, 818)]
NAMES = ["Words Vectors", "1st FM", "2nd FM", "3rd FM", "4th FM"]

# 1) vertical extent of stacks: use a column through stack interiors, find where
#    outlines/fills change from background. Use x = mid of stack 1.
for (x0, x1), nm in zip(STACKS, NAMES):
    xm = (x0 + x1) // 2
    col = im[:, xm]
    # rows where pixel is NOT panel-gray/white (i.e., cell fill or outline ink)
    rows = []
    for y in range(140, 500):
        px = col[y]
        is_bg = near(px, (233, 233, 231), 14) or near(px, (255, 255, 255), 10)
        if not is_bg:
            rows.append(y)
    if rows:
        print(f"{nm}: interior col x={xm} non-bg rows {rows[0]}..{rows[-1]}  count={len(rows)}")

# 2) row-scan: find horizontal cell boundaries via outline rows across stack 1 width
x0, x1 = STACKS[0]
strip = im[:, x0+3:x1-3]
rowink = []
for y in range(150, 480):
    row = strip[y]
    n_red = sum(1 for px in row if px[0] > 140 and px[1] < 110 and px[2] < 110)
    rowink.append((y, n_red))
print("\nstack1 red-outline rows (red count > 20):")
print([(y, n) for y, n in rowink if n > 20])

# 3) classify each cell center for each stack
print("\n--- per-cell center classification (rows found next) ---")
# first get cell boundaries from outline rows of stack 1
bnd = [y for y, n in rowink if n > 20]
