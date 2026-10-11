#!/usr/bin/env python3
"""Slide 030: per-box border rectangles via contiguous-run analysis."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
blue = (B > 90) & (B - R > 40) & (B - G > 40)
green = (G > 90) & (G - R > 30) & (G - B > 30)

def longest_run(v):
    best = cur = 0; s = e = -1; cs = 0
    for i, x in enumerate(v):
        if x: cur += 1
        else:
            if cur > best: best, s, e = cur, cs, i - 1
            cur = 0; cs = i + 1
    if cur > best: best, s, e = cur, cs, len(v) - 1
    return best, s, e

def box_borders(name, x0, y0, x1, y1):
    sub = blue[y0:y1, x0:x1]
    print(f"== {name} window x{x0}..{x1} y{y0}..{y1}")
    for r in range(sub.shape[0]):
        run, s, e = longest_run(sub[r])
        if run > 100: print(f"  row y={y0+r}: run {run} x {x0+s}..{x0+e}")
    for c in range(sub.shape[1]):
        run, s, e = longest_run(sub[:, c])
        if run > 60: print(f"  col x={x0+c}: run {run} y {y0+s}..{y0+e}")

box_borders("vector box", 70, 40, 390, 245)
box_borders("remember box", 455, 90, 860, 200)
box_borders("derivation box", 70, 228, 680, 335)
box_borders("matrix box", 70, 320, 640, 510)
box_borders("green box (green mask)", 600, 330, 900, 485)

# probe anomalies
for (x, y) in [(280, 130), (280, 160), (471, 140), (502, 140), (616, 280), (653, 280), (616, 400)]:
    print(f"px({x},{y}) = {tuple(im[y, x])}")
