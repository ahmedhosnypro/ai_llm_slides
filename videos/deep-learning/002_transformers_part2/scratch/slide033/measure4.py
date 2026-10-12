#!/usr/bin/env python3
"""slide033 measure-4: row/column profiles per region -> exact box extents."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = a.shape
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556

def classify(px):
    r, g, b = px
    if r > 238 and g > 238 and b > 235: return "white"
    if r > 225 and g > 215 and 160 < b < 228 and r - b > 18: return "cream"
    if r > 226 and 165 < g < 225 and 140 < b < 195 and r - b > 55: return "orange"
    if 150 < r < 215 and g > 165 and 130 < b < 205 and g - b > 25 and g - r > 8: return "green"
    if r < 150 and g > 130 and b < g - 20: return "greenDk"
    if b > 200 and b - r > 12 and g > 200: return "ltblue"
    if r > 120 and g < 75 and b < 75: return "red"
    if r < 110 and g < 110 and b < 110: return "black"
    if 170 < r < 230 and g < 90 and b < 90: return "maroon"
    if b > 130 and r < 110 and b - r > 45: return "blue"
    return f"({r},{g},{b})"

def row_profile(x0, x1, y0, y1, label):
    print(f"=== ROW PROFILE {label} (x {x0}..{x1}) ===")
    runs = []
    cur = None
    for y in range(y0, y1 + 1):
        strip = a[y, x0:x1 + 1]
        med = tuple(int(v) for v in np.median(strip, axis=0))
        c = classify(med)
        if cur and cur[0] == c:
            cur[2] = y
        else:
            if cur: runs.append(cur)
            cur = [c, y, y]
    if cur: runs.append(cur)
    for c, ys, ye in runs:
        if ye - ys >= 0:
            print(f"  y {ys:3d}..{ye:3d} (h{ye-ys+1:3d}) {c:8s} slideY[{MAPY(ys):.1f}..{MAPY(ye):.1f}] in[{MAPY(ys)/72:.3f}..{MAPY(ye)/72:.3f}]")

def col_profile(y0, y1, x0, x1, label):
    print(f"=== COL PROFILE {label} (y {y0}..{y1}) ===")
    runs = []
    cur = None
    for x in range(x0, x1 + 1):
        strip = a[y0:y1 + 1, x]
        med = tuple(int(v) for v in np.median(strip, axis=0))
        c = classify(med)
        if cur and cur[0] == c:
            cur[2] = x
        else:
            if cur: runs.append(cur)
            cur = [c, x, x]
    if cur: runs.append(cur)
    for c, xs, xe in runs:
        print(f"  x {xs:3d}..{xe:3d} (w{xe-xs+1:3d}) {c:8s} slideX[{MAPX(xs):.1f}..{MAPX(xe):.1f}] in[{MAPX(xs)/72:.3f}..{MAPX(xe)/72:.3f}]")

# sin/cos terms column interior
row_profile(330, 396, 100, 535, "sin/cos terms col")
# vector pairs column interior
row_profile(226, 250, 100, 535, "vector pairs col")
# index column interior
row_profile(262, 306, 100, 535, "index col")
# horizontal extents of the three columns + pair box at a few key rows
col_profile(150, 175, 55, 430, "row 150-175 (pair-1 area)")
col_profile(430, 440, 55, 430, "row 430-440 (gap area)")
col_profile(480, 500, 55, 430, "row 480-500 (pair-5 area)")
