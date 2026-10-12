#!/usr/bin/env python3
"""Forensics pass 1 for slide_045.jpg (960x540, 1px=1pt): find bordered boxes,
title band, and global structure."""
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("size", W, H)

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 120) & (R - G > 55) & (R - B > 55)
blue = (B > 90) & (B - R > 45) & (B - G > 30)
dark = (R < 120) & (G < 120) & (B < 150)  # text ink-ish
black = (R < 60) & (G < 60) & (B < 60)

# horizontal runs of red/blue (box borders): rows where count is large
def runs(mask, axis, minlen):
    out = []
    if axis == 0:  # per-row
        for y in range(H):
            xs = np.where(mask[y])[0]
            if len(xs) > minlen:
                # longest contiguous run
                d = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1)
                seg = max(d, key=len)
                if len(seg) > minlen:
                    out.append((y, seg[0], seg[-1], len(seg)))
    else:
        for x in range(W):
            ys = np.where(mask[:, x])[0]
            if len(ys) > minlen:
                d = np.split(ys, np.where(np.diff(ys) > 3)[0] + 1)
                seg = max(d, key=len)
                if len(seg) > minlen:
                    out.append((x, seg[0], seg[-1], len(seg)))
    return out

print("\n== RED horizontal rows (>=120 px run) ==")
prev = None
for y, x0, x1, n in runs(red, 0, 120):
    if prev is None or y - prev > 2:
        print(f"y={y} x{x0}..{x1} n={n}")
    prev = y

print("\n== BLUE horizontal rows (>=80 px run) ==")
prev = None
for y, x0, x1, n in runs(blue, 0, 80):
    if prev is None or y - prev > 2:
        print(f"y={y} x{x0}..{x1} n={n}")
    prev = y

print("\n== RED vertical cols (>=60 px run) ==")
prev = None
for x, y0, y1, n in runs(red, 1, 60):
    if prev is None or x - prev > 2:
        print(f"x={x} y{y0}..{y1} n={n}")
    prev = x

print("\n== BLUE vertical cols (>=40 px run) ==")
prev = None
for x, y0, y1, n in runs(blue, 1, 40):
    if prev is None or x - prev > 2:
        print(f"x={x} y{y0}..{y1} n={n}")
    prev = x
