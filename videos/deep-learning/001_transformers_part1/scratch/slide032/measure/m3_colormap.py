# m3_colormap.py — coarse ASCII map of color families, 8px cells
import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = a.shape[:2]
CELL = 8
def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    sat = mx - mn
    if mx > 235 and sat < 18: return "."   # white
    if mx > 205 and sat < 22: return ","   # light gray (panel E8E8E6 / band)
    if sat < 30 and mx <= 205 and mx > 140: return ":"  # mid gray
    if mx < 110: return "#"                # dark ink
    if r > 150 and g < 110 and b < 110: return "R"  # red
    if r > 180 and g > 120 and b < 120 and r-b > 70: return "O"  # orange
    if r > 170 and g < 130 and b > 130: return "M"  # magenta/pink
    if r > 200 and g > 170 and b > 130 and r-b > 40: return "Y"  # yellow/cream
    if b > 130 and b-r > 40 and b-g > 30: return "B"  # blue
    if g > 120 and g-r > 40 and g-b > 30: return "G"  # green
    return "?"
rows = []
for cy in range(0, H, CELL):
    line = []
    for cx in range(0, W, CELL):
        blk = a[cy:cy+CELL, cx:cx+CELL].reshape(-1,3)
        med = np.median(blk, axis=0)
        line.append(classify(med))
    rows.append("".join(line))
hdr = "    " + "".join(str((i//CELL*CELL)//100 % 10) if (i//CELL*CELL) % 100 < CELL else " " for i in range(0, W, CELL))
print("cols: each char = 8px; x = col*8, y = row*8")
for i, r in enumerate(rows):
    print(f"{i*CELL:3d} {r}")
