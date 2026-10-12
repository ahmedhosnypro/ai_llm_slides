#!/usr/bin/env python3
"""measure4: coarse ASCII maps to locate squares/labels/arrows/headers precisely"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

def classify(px):
    r, g, b = px
    if r > 235 and g > 235 and b > 235: return "."   # white
    s = abs(r-233)+abs(g-233)+abs(b-231)
    if s <= 40: return " "                            # panel gray
    if r > 200 and g > 170 and b > 120: return ","    # peach-ish
    if b > 90 and r < 90 and g < 90: return "B"       # blue
    if r > 80 and g < 80 and b < 90: return "R"       # dark red
    if r > 150 and 90 < g < 190 and b < 140: return "O"  # orange
    if g > 90 and r < 120 and b < 130: return "G"     # green
    if r < 100 and g < 100 and b < 100: return "#"    # black ink
    return "-"

def amap(name, x0, y0, x1, y1, sx=3, sy=3):
    print(f"=== {name} x{x0}..{x1} y{y0}..{y1} (cell {sx}x{sy}; col marks every 10 cells = 30px) ===")
    hdr = "     " + "".join(str((x0 + c * sx) // 100 % 10) if (c % 10 == 0) else " " for c in range((x1 - x0) // sx + 1))
    print(hdr)
    for y in range(y0, y1, sy):
        row = "".join(classify(a[y, x]) for x in range(x0, x1, sx))
        print(f"{y:4d} {row}")

# Left panel INPUT container
amap("L-INPUT", 150, 125, 265, 470)
