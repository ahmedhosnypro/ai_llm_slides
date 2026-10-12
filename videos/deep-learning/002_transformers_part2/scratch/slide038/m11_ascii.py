#!/usr/bin/env python3
"""Slide 038 — m11: ASCII hue map of column-2 strip (x 255..300) and col1 strip, rows 250..500."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

def cls(y, x):
    r, g, b = img[y, x]
    if r > 225 and g > 225 and b > 225: return "."   # white
    if r < 100 and g < 100 and b < 100: return "K"   # black/dark
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 30:
        if r > 180: return "w"  # light gray
        if r > 120: return "g"  # mid gray
        return "K"
    if r > 140 and g < 110 and b < 110: return "R"   # red
    if r > 150 and 60 < g < 160 and b < 90: return "O"  # orange
    if b > 120 and b - r > 40 and g < 110: return "B"  # dark blue
    if g > 120 and g - r > 30 and g - b > 30: return "G"  # green
    if r > 200 and g > 170 and b < 150: return "Y"   # yellow
    if r > 210 and 130 < g < 215 and 130 < b < 215: return "P"  # pink
    if g > 200 and r > 180 and b < 200: return "y"   # pale yellow/green
    if b > 200 and r > 180: return "p"               # pale blue/pink
    return "?"

def strip(x0, x1, y0, y1, step=1, label=""):
    print(f"== {label} x{x0}..{x1} y{y0}..{y1} (cols every {step}px) ==")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1 + 1, step))
    print(hdr)
    print("     " + "".join(str(x % 10) for x in range(x0, x1 + 1, step)))
    for y in range(y0, y1 + 1):
        print(f"y{y:03d} " + "".join(cls(y, x) for x in range(x0, x1 + 1, step)))

strip(255, 300, 250, 300, 1, "COL2 top area")
strip(190, 240, 250, 300, 1, "COL1 top area")
