#!/usr/bin/env python3
"""Targeted 2px-cell ASCII maps of small regions in slide_011.jpg."""
import numpy as np
from PIL import Image
import sys

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im).astype(float)

def classify(px):
    r, g, b = px
    if r < 110 and g < 110 and b < 110: return "D"
    if r > 120 and r - g > 150 and r - b > 120: return "R"      # strong red
    if r > 200 and g > 200 and b < 130: return "Y"
    if r > 225 and 120 < g < 205 and 50 < b < 150: return "O"
    if b > 150 and b - r > 50 and r < 140: return "U"           # blue
    if 150 < r < 220 and abs(r - g) < 12 and abs(g - b) < 12: return "G"
    if r > 180 and b - r > 14: return "L"
    if r > 222 and r - b > 9 and g - b > 3: return "B"
    if r > 228 and abs(r - g) < 7 and abs(b - g) < 9: return "P"
    if r > 238: return "W"
    return "."

def region(x0, y0, x1, y1, cell=2, label=""):
    print(f"\n===== {label} x[{x0},{x1}] y[{y0},{y1}] cell={cell} =====")
    hdr = "     "
    for cx in range(x0, x1, cell):
        hdr += str((cx // 10) % 10)
    print(hdr)
    for cy in range(y0, y1, cell):
        row = f"{cy:4d} "
        for cx in range(x0, x1, cell):
            c = a[cy:cy+cell, cx:cx+cell].reshape(-1, 3).mean(axis=0)
            row += classify(c)
        print(row)

which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all", "a"): region(480, 100, 960, 172, 2, "A: above yellow block (arrows + o labels)")
if which in ("all", "b"): region(40, 440, 480, 540, 2, "B: below orange block (lines + x labels + Encoder + strip)")
if which in ("all", "c"): region(100, 218, 490, 310, 2, "C: encoder sub-block + attention box + fan lines")
if which in ("all", "d"): region(480, 270, 960, 372, 2, "D: decoder sub-block + self-loops + label")
if which in ("all", "e"): region(430, 200, 560, 480, 2, "E: center red arrow + pink curves")
