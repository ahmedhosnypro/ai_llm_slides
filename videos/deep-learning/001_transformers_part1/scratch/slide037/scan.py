#!/usr/bin/env python3
"""Scan rows/cols of slide_037.jpg: print color runs to map box boundaries."""
import numpy as np
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def hexof(px):
    return f"{px[0]:02X}{px[1]:02X}{px[2]:02X}"

def runs(vals, min_run=4):
    """collapse consecutive similar colors into runs"""
    out = []
    start = 0
    for i in range(1, len(vals) + 1):
        if i == len(vals) or not np.all(np.abs(vals[i] - vals[start]).max() <= 12):
            if i - start >= min_run:
                c = vals[(start + i) // 2]
                out.append((start, i - 1, hexof(c)))
            start = i
    return out

import sys
mode = sys.argv[1] if len(sys.argv) > 1 else "row"
v = int(sys.argv[2]) if len(sys.argv) > 2 else 0
if mode == "row":
    vals = a[v, :, :]
    r = runs(vals)
    print(f"row y={v}:")
    for (s, e, hx) in r:
        if e - s >= 3:
            print(f"  x[{s:3d},{e:3d}] w={e-s+1:3d} {hx}")
else:
    vals = a[:, v, :]
    r = runs(vals)
    print(f"col x={v}:")
    for (s, e, hx) in r:
        if e - s >= 3:
            print(f"  y[{s:3d},{e:3d}] h={e-s+1:3d} {hx}")
