#!/usr/bin/env python3
"""Run-length scans + point samples for slide_031.jpg."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def cls(c):
    r, g, b = c
    if r > 238 and g > 238 and b > 238: return "."
    if r > 130 and r-g > 55 and r-b > 55: return "R"
    if b > 120 and b-r > 55 and b-g > 35: return "B"
    if g > 105 and g-r > 30 and g-b > 30: return "G"
    if r < 115 and g < 115 and b < 115: return "#"
    if r > 225 and 150 < g < 218 and 160 < b < 235 and r-g > 18: return "k"
    if r > 233 and 210 < g < 245 and 180 < b < 230: return "P"
    if 130 < r < 215 and 130 < g < 218 and b > 195 and b-r > 20: return "w"
    if r < 220 and g > 200 and g-r > 12 and g-b > 8: return "g"
    return "-"

def runs(y, x0, x1):
    out = []
    prev = None; start = x0
    for x in range(x0, x1):
        c = cls(px[x, y])
        if c != prev:
            if prev is not None: out.append((prev, start, x-1))
            prev = c; start = x
    out.append((prev, start, x1-1))
    return out

def vruns(x, y0, y1):
    out = []
    prev = None; start = y0
    for y in range(y0, y1):
        c = cls(px[x, y])
        if c != prev:
            if prev is not None: out.append((prev, start, y-1))
            prev = c; start = y
    out.append((prev, start, y1-1))
    return out

def show(label, rs, minlen=1):
    parts = [f"{c}{a}-{b}" for (c, a, b) in rs if b-a+1 >= minlen]
    print(f"{label}: " + " ".join(parts))

print("== Q panel scanlines (x57..467) ==")
for y in [98, 110, 120, 134, 150, 170, 180, 195, 205, 220, 250, 262, 280, 290]:
    show(f"y={y}", runs(y, 55, 470), 2)
print("\n== Q vertical runs ==")
for x in [70, 90, 130, 190, 250, 300, 360, 395, 420, 440, 460]:
    show(f"x={x}", vruns(x, 96, 302), 2)

print("\n== point samples ==")
pts = [
 ("matrix text r1c1", 233, 134), ("matrix text r1c2", 266, 134), ("matrix text r1c3", 313, 134), ("matrix text r1c4", 349, 134),
 ("matrix cell fill r1c1", 240, 130), ("matrix gap col", 262, 150), ("matrix bg row", 250, 148),
 ("clusterA", 188, 180), ("clusterA2", 192, 182),
 ("= sign", 393, 202), ("= sign2", 395, 210),
 ("capsule cell1 fill Q", 85, 150), ("capsule cell1 text", 88, 152),
 ("X2 label", 120, 200), ("X2 label2", 128, 195),
 ("outcap cell1 fill", 430, 150), ("outcap cell1 text", 432, 135),
 ("outcap outline right", 450, 200),
 ("W_Q label", 180, 250),
]
for lbl, x, y in pts:
    print(f"  {lbl} ({x},{y}): {px[x,y]}")

print("\n== dark ink under Q capsule (y168..190, x60..215) ==")
for y in range(166, 196):
    n = sum(1 for x in range(60, 215) if cls(px[x, y]) == "#")
    if n: print(f"  y={y}: {n}", end=";")
print()
