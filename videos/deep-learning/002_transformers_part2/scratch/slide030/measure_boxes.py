#!/usr/bin/env python3
"""Slide 030: find the 5 content boxes' borders precisely."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# blue-ish border pixels (0000CC core; JPEG-darkened navy possible)
blue = (B > 90) & (B - R > 40) & (B - G > 40)
green = (G > 90) & (G - R > 30) & (G - B > 30)
red = (R > 100) & (R - G > 50) & (R - B > 40)

def bbox_of(mask, x0, y0, x1, y1, min_run=60):
    sub = mask[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) > min_run)[0]
    cols = np.where(sub.sum(axis=0) > min_run)[0]
    if not len(rows) or not len(cols):
        return None
    return (x0 + int(cols[0]), y0 + int(rows[0]), x0 + int(cols[-1]), y0 + int(rows[-1]))

# search windows (frame px) around each expected box, looking for long horizontal blue runs
print("== blue horizontal strokes (rows where blue run-count high) ==")
brow = blue.sum(axis=1)
bcol = blue.sum(axis=0)
rows_hit = [(y, int(brow[y])) for y in range(40, 520) if brow[y] > 80]
print("blue rows:", rows_hit)
cols_hit = [(x, int(bcol[x])) for x in range(40, 920) if bcol[x] > 40]
print("blue cols:", cols_hit)
grn = bbox_of(green, 560, 300, 920, 500)
print("green note box bbox:", grn)
