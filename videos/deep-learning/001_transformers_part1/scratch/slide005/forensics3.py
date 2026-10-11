#!/usr/bin/env python3
"""Forensics 3: run-length encoding of key columns/rows; exact outline colors."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]

def rle_col(x, y0, y0f, y1f):
    print(f"--- column x={x} y{y0f}..{y1f} RLE ---")
    col = im[:, x]
    prev = None
    start = y0f
    for y in range(y0f, y1f):
        px = tuple(int(v) for v in col[y])
        key = (px[0] // 24, px[1] // 24, px[2] // 24)
        if key != prev:
            if prev is not None:
                print(f"  y{start}..{y-1} ({y-start}px) avg {tuple(int(v) for v in col[start:y].mean(axis=0))}")
            prev = key
            start = y
    print(f"  y{start}..{y1f-1} ({y1f-start}px) avg {tuple(int(v) for v in col[start:y1f].mean(axis=0))}")

def rle_row(y, x0f, x1f):
    print(f"--- row y={y} x{x0f}..{x1f} RLE ---")
    row = im[y]
    prev = None
    start = x0f
    for x in range(x0f, x1f):
        px = tuple(int(v) for v in row[x])
        key = (px[0] // 24, px[1] // 24, px[2] // 24)
        if key != prev:
            if prev is not None:
                print(f"  x{start}..{x-1} ({x-start}px) avg {tuple(int(v) for v in row[start:x].mean(axis=0))}")
            prev = key
            start = x
    print(f"  x{start}..{x1f-1} ({x1f-start}px) avg {tuple(int(v) for v in row[start:x1f].mean(axis=0))}")

# Words Vectors stack mid-column
rle_col(203, 0, 140, 500)
print()
# 1st Feature Map mid-column
rle_col(349, 0, 140, 500)
