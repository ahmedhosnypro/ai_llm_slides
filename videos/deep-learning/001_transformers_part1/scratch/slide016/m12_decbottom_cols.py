#!/usr/bin/env python3
"""1px column profiles through decoder bottom (x740-890, y400-528) to find box edges."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)

def cruns(x, y0, y1, tol=14):
    col = IM[y0:y1, x]
    out = []
    s = 0
    base = col[0]
    for i in range(1, len(col)):
        if np.abs(col[i] - col[s]).max() > tol:
            if i - s >= 2:
                m = col[s:i].mean(axis=0).astype(int)
                out.append((y0+s, y0+i-1, tuple(m)))
            s = i
    m = col[s:].mean(axis=0).astype(int)
    out.append((y0+s, y0+len(col)-1, tuple(m)))
    return out

for x in [746, 752, 760, 775, 790, 800, 812, 820, 830, 845, 860, 875]:
    print(f"\n-- col x={x}, y400-528 --")
    for a, b, c in cruns(x, 400, 528):
        print(f"   y{a:3d}-{b:3d} ({b-a+1:3d}) rgb({c[0]},{c[1]},{c[2]})")
