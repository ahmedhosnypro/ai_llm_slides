#!/usr/bin/env python3
"""Slide 030: core color comparison for contested tokens (references: black lv, red rv, navy Independent)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
lum = im.mean(axis=2)

def core(x0, y0, x1, y1, label, lo=20, hi=130):
    """Median of stroke-body pixels (lum in [lo,hi]) - the true ink tone."""
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    l = lum[y0:y1, x0:x1].reshape(-1)
    m = (l >= lo) & (l <= hi)
    if m.sum() < 10:
        print(f"{label}: too few ({int(m.sum())})"); return
    px = reg[m]
    print(f"{label}: n={int(m.sum())} median={tuple(np.median(px, axis=0).astype(int))} p25={tuple(np.percentile(px, 25, axis=0).astype(int))}")

print("--- references ---")
core(127, 398, 231, 415, "REF black: lv r2 cos(w(t+d))")
core(503, 410, 562, 427, "REF red: rv r2 cos(wt)")
core(250, 481, 460, 500, "REF navy: Independent text")
core(513, 148, 773, 160, "REF navy: remember id1")
core(633, 410, 828, 428, "REF navy: note L2")
print("--- contested: deriv matrix-terms ---")
core(429, 249, 494, 267, "L1 cos(wd)")
core(587, 249, 647, 267, "L1 sin(wd)")
core(434, 295, 499, 312, "L2 cos(wd)")
core(582, 295, 649, 312, "L2 sin(wd)")
print("--- contested: matrix 2x2 cells ---")
core(303, 353, 370, 376, "mx r1c1 cos(wd)")
core(388, 353, 448, 376, "mx r1c2 sin(wd)")
core(305, 401, 366, 421, "mx r2c1 sin(wd)")
core(384, 401, 449, 421, "mx r2c2 cos(wd)")
print("--- contested: red vector terms ---")
core(366, 249, 420, 267, "L1 sin(wt)")
core(519, 249, 579, 267, "L1 cos(wt)")
print("--- v1 red cells (vecbox) ---")
core(261, 69, 330, 88, "v1 r1 sin(wt)")
core(261, 114, 330, 138, "v1 r2 cos(wt)")
print("--- labels/captions ---")
core(102, 88, 232, 102, "label1")
core(98, 444, 299, 458, "caption1")
core(634, 361, 838, 376, "note header red")
print("--- brace/brackets ---")
core(272, 447, 470, 468, "brace")
core(242, 60, 245, 137, "v1 red bracket stroke")
core(279, 352, 282, 431, "mx blue bracket stroke")
core(484, 352, 487, 431, "rv red bracket stroke")
core(120, 353, 122, 430, "lv black bracket stroke")
print("--- deriv black halves (ref) ---")
core(103, 249, 192, 267, "L1 sin(w(t+d))")
core(217, 249, 314, 267, "L1 sin(wt +wd)")
