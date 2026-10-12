#!/usr/bin/env python3
"""Slide 030: p10 glyph cores (darkest decile) for contested tokens."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
lum = im.mean(axis=2)

def p10(x0, y0, x1, y1, label, maxlum=140):
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    l = lum[y0:y1, x0:x1].reshape(-1)
    m = l < maxlum
    if m.sum() < 8:
        print(f"{label}: too few"); return
    px = reg[m]
    k = max(1, len(px) // 10)
    idx = np.argsort(px.sum(axis=1))[:k]
    print(f"{label}: n={int(m.sum())} p10median={tuple(np.median(px[idx], axis=0).astype(int))}")

print("--- references ---")
p10(127, 398, 231, 415, "REF black lv r2")
p10(250, 481, 460, 500, "REF navy Independent")
p10(513, 148, 773, 160, "REF navy remember id1")
p10(503, 410, 562, 427, "REF red rv r2")
print("--- matrix 2x2 cells ---")
p10(303, 353, 370, 376, "mx r1c1 cos(wd)")
p10(388, 353, 448, 376, "mx r1c2 sin(wd)")
p10(305, 401, 366, 421, "mx r2c1 sin(wd)")
p10(384, 401, 449, 421, "mx r2c2 cos(wd)")
print("--- deriv matrix-terms ---")
p10(429, 249, 494, 267, "L1 cos(wd)")
p10(587, 249, 647, 267, "L1 sin(wd)")
p10(434, 295, 499, 312, "L2 cos(wd)")
p10(582, 295, 649, 312, "L2 sin(wd)")
print("--- deriv red terms ---")
p10(366, 249, 420, 267, "L1 sin(wt)")
p10(520, 295, 574, 312, "L2 sin(wt)")
print("--- vecbox ---")
p10(261, 69, 330, 88, "v1 r1 sin(wt)")
p10(250, 152, 358, 175, "v2 r1 Sin(w(t+d))")
