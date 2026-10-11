#!/usr/bin/env python3
"""m6: ASCII class map of the inset region so the layout can be read
programmatically (2x2 px cells)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
im = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)

def classify(p):
    r, g, b = p
    if r < 120 and g < 120 and b < 120:
        return "K"                      # dark ink (text/arrows/borders)
    if g > r + 20 and g > b + 10 and g < 210 and r < 160:
        return "G"                      # green border
    if abs(r - 194) < 40 and abs(g - 187) < 40 and abs(b - 220) < 40:
        return "L"                      # lavender
    if abs(r - 207) < 35 and abs(g - 233) < 30 and abs(b - 208) < 35:
        return "s"                      # soft light green (SoftMax)
    if r > 240 and g > 240 and b > 235:
        return "W"                      # white
    if r > 230 and 195 < g < 235 and 170 < b < 215:
        return "P"                      # peach canvas
    if r > 245 and g > 235 and 130 < b < 190:
        return "Y"                      # pale yellow
    if abs(r - 153) < 45 and abs(g - 122) < 45 and abs(b - 140) < 45:
        return "m"                      # mauve/dark rose
    return "."

X0, X1, Y0, Y1 = 792, 930, 108, 322
hdr = "     " + "".join(str((x // 10) % 10) for x in range(X0, X1, 2))
print(hdr)
for y in range(Y0, Y1, 2):
    row = []
    for x in range(X0, X1, 2):
        c = classify(im[y, x])
        c2 = classify(im[y + 1, x + 1])
        # prefer the more "informative" class of the 2x2 block
        pri = "KGLsWYPm."
        ch = c if pri.index(c) <= pri.index(c2) else c2
        row.append(ch)
    print(f"{y:4d} " + "".join(row))
