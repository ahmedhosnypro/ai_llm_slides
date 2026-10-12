#!/usr/bin/env python3
"""Slide 043 left stack fine scan: exact boundaries along cube-row midlines."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def runs_row(y, x0, x1, tol=28):
    """segment row by color change"""
    out, start = [], x0
    prev = a[y, x0]
    for x in range(x0 + 1, x1):
        cur = a[y, x]
        if abs(int(cur[0]) - int(prev[0])) + abs(int(cur[1]) - int(prev[1])) + abs(int(cur[2]) - int(prev[2])) > tol * 3:
            r, g, b = prev
            out.append((start, x - 1, f"#{r:02X}{g:02X}{b:02X}"))
            start = x
        prev = cur
    r, g, b = prev
    out.append((start, x1 - 1, f"#{r:02X}{g:02X}{b:02X}"))
    return [(s, e, c) for s, e, c in out if e - s >= 1]

def runs_col(x, y0, y1, tol=28):
    out, start = [], y0
    prev = a[y0, x]
    for y in range(y0 + 1, y1):
        cur = a[y, x]
        if abs(int(cur[0]) - int(prev[0])) + abs(int(cur[1]) - int(prev[1])) + abs(int(cur[2]) - int(prev[2])) > tol * 3:
            r, g, b = prev
            out.append((start, y - 1, f"#{r:02X}{g:02X}{b:02X}"))
            start = y
        prev = cur
    r, g, b = prev
    out.append((start, y1 - 1, f"#{r:02X}{g:02X}{b:02X}"))
    return [(s, e, c) for s, e, c in out if e - s >= 1]

print("LEFT stack row-midline scans (cube rows ~188..211, 219..243, 250..274, 281..305, 312..337):")
for y in [195, 200, 226, 232, 257, 263, 288, 294, 319, 325]:
    print(f"y={y}:", runs_row(y, 105, 350))
print()
print("LEFT stack col scans through slice columns:")
for x in [220, 235, 255, 270, 285, 300, 310]:
    print(f"x={x} y95..345:", runs_col(x, 95, 346))
