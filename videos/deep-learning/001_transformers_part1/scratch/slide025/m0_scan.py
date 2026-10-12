#!/usr/bin/env python3
"""Coarse structure scan of slide_025.jpg (960x540, 1px=1pt).
Prints color-classified run maps on selected scanlines to locate the panels,
architecture, bubble, highlight, and dashed lines."""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"size {W}x{H}")


def classify(p):
    r, g, b = p
    if r > 235 and g > 235 and b > 235:
        return "."  # white
    if abs(r - 233) < 18 and abs(g - 233) < 18 and abs(b - 231) < 18:
        return "g"  # panel gray E9E9E7
    if r > 150 and g < 90 and b < 90:
        return "R"  # red
    if r < 150 and g > 110 and b < 110 and g > r + 30:
        return "G"  # green
    if r > 200 and g > 190 and b < 130:
        return "Y"  # yellow
    if 180 < r < 245 and 150 < g < 215 and 100 < b < 180 and r > b:
        return "t"  # tan / peach family
    if 130 < r < 200 and 100 < g < 180 and 150 < b < 230 and b > g:
        return "L"  # lavender/purple family
    if r < 120 and g < 120 and b < 120:
        return "k"  # dark ink
    return "?"


def scanrow(y):
    runs = []
    cur = None
    start = 0
    row = [classify(im[y, x]) for x in range(W)]
    for x, c in enumerate(row + ["END"]):
        if c != cur:
            if cur is not None and x - start >= 2:
                runs.append((start, x - 1, cur))
            cur = c
            start = x
    print(f"y={y}: " + " ".join(f"{a}-{b}{c}" for a, b, c in runs if c != "." or b - a > 12))


def scancol(x):
    runs = []
    cur = None
    start = 0
    col = [classify(im[y, x]) for y in range(H)]
    for y, c in enumerate(col + ["END"]):
        if c != cur:
            if cur is not None and y - start >= 2:
                runs.append((start, y - 1, cur))
            cur = c
            start = y
    print(f"x={x}: " + " ".join(f"{a}-{b}{c}" for a, b, c in runs if c != "." or b - a > 12))


for y in [15, 30, 45, 60, 90, 110, 135, 150, 165, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 535]:
    scanrow(y)
print("---cols---")
for x in [10, 30, 45, 60, 100, 140, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 500, 520, 550, 570, 600, 630, 660, 690, 720, 750, 780, 810, 840, 870, 900, 920, 940, 950]:
    scancol(x)
