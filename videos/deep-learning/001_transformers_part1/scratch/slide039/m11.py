#!/usr/bin/env python3
"""m11.py — fine anatomy of left group (x125-268) and right group (x528-680)."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

def strip(y, x0, x1, min_run=2):
    row = a[y, x0:x1]
    peach = (np.abs(row[:, 0] - 240) < 14) & (np.abs(row[:, 1] - 224) < 14) & (np.abs(row[:, 2] - 200) < 16)
    out = []
    s = None
    for i in range(len(peach)):
        if not peach[i] and s is None: s = i
        elif peach[i] and s is not None:
            if i - s >= min_run:
                seg = row[s:i]
                m = seg.mean(axis=0).astype(int)
                out.append((x0 + s, x0 + i - 1, f"({m[0]},{m[1]},{m[2]})"))
            s = None
    print(f"y={y}:", " | ".join(f"[{c[0]}-{c[1]}]{c[2]}" for c in out))

print("=== LEFT GROUP x[125,268] ===")
for y in range(283, 408, 7):
    strip(y, 125, 268)
print("=== RIGHT GROUP x[528,680] ===")
for y in range(283, 418, 7):
    strip(y, 528, 680)
