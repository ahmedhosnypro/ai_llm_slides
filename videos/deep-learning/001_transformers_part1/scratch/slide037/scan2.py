#!/usr/bin/env python3
"""Finer region scans with configurable step + ink masks."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def hexof(px):
    return f"{int(px[0]):02X}{int(px[1]):02X}{int(px[2]):02X}"

def runs(vals, min_run=3, tol=14):
    out = []
    start = 0
    for i in range(1, len(vals) + 1):
        if i == len(vals) or not np.all(np.abs(vals[i] - vals[start]).max() <= tol):
            if i - start >= min_run:
                c = np.median(vals[start + 1:i - 1], axis=0) if i - start > 3 else vals[start]
                out.append((start, i - 1, hexof(c)))
            start = i
    return out

mode = sys.argv[1]
v = int(sys.argv[2])
step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
if mode == "row":
    vals = a[v, ::step, :]
    print(f"row y={v} (step {step}):")
    for (s, e, hx) in runs(vals):
        if e - s >= 2:
            print(f"  x[{s*step:3d},{e*step:3d}] w={(e-s+1)*step:3d} {hx}")
else:
    vals = a[::step, v, :]
    print(f"col x={v} (step {step}):")
    for (s, e, hx) in runs(vals):
        if e - s >= 2:
            print(f"  y[{s*step:3d},{e*step:3d}] h={(e-s+1)*step:3d} {hx}")
