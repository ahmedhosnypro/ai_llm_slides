#!/usr/bin/env python3
"""ASCII map of slide_011.jpg: 4px cells classified by mean color."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im).astype(float)
H, W = a.shape[:2]
CELL = 4
h2, w2 = H // CELL, W // CELL

def classify(px):
    r, g, b = px
    if r > 120 and r - g > 60 and r - b > 60: return "R"          # red
    if b > 150 and b - r > 50 and r < 130: return "U"             # blue
    if r > 200 and g > 200 and b < 130: return "Y"                # yellow
    if r > 225 and 120 < g < 205 and 50 < b < 150: return "O"     # orange
    if r < 110 and g < 110 and b < 110: return "D"                # dark/text
    if 150 < r < 218 and abs(r - g) < 12 and abs(g - b) < 12: return "G"   # gray BFBFBF
    if r > 180 and b - r > 14: return "L"                          # lavender tint
    if r > 222 and r - b > 9 and g - b > 3: return "B"             # beige tint
    if r > 225 and abs(r - g) < 6 and abs(b - g) < 8: return "P"   # panel E9E9E7-ish light neutral
    if r > 238: return "W"                                         # white
    return "."

print("   " + "".join(str((x * CELL // 100) % 10) for x in range(w2)))
for cy in range(h2):
    row = []
    for cx in range(w2):
        cell = a[cy*CELL:(cy+1)*CELL, cx*CELL:(cx+1)*CELL].reshape(-1, 3).mean(axis=0)
        row.append(classify(cell))
    print(f"{cy*CELL:3d} " + "".join(row))
