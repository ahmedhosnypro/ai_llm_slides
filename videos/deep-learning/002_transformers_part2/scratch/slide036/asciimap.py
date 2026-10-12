#!/usr/bin/env python3
"""ASCII map of slide_036.jpg: classify each 8px cell by dominant color family.
Classes tuned for this slide: R red ink, B blue ink, N navy banner, f cream panel,
P pink cell, L light-yellow cell, Y bright yellow (badge/caption hl), g green, m maroon."""
import numpy as np
from PIL import Image
from collections import Counter

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape

def cls(y, x):
    r, g, b = a[y, x]
    if r < 70 and g < 70 and b < 70: return "K"
    if r > 140 and g < 100 and b < 100: return "R"
    if 90 <= r <= 200 and g < 70 and b < 70: return "m"   # maroon/dark red
    if b > 120 and r < 90 and g < 90 and b >= 170: return "B"  # bright blue (arrows/dots)
    if b > 100 and r < 80 and g < 80 and b < 170: return "N"   # navy
    if r > 200 and g > 200 and b < 110: return "Y"        # bright yellow
    if r > 235 and g > 200 and 120 < b < 235: return "L"  # light yellow cell
    if r > 225 and g > 225 and b > 225: return "."        # white
    if r > 235 and 195 < b < 240 and g > 235: return "f"  # cream fill
    if r > 225 and 120 <= g <= 185 and b > 175: return "P"  # pink cell
    if g > 120 and r < 110 and b < 130: return "g"        # green
    if abs(r-233) < 14 and abs(g-233) < 14 and abs(b-231) < 16: return "E"  # gray panel
    return " "

CELL = 8
rows, cols = H // CELL, W // CELL
hdr = "    " + "".join(str((c * CELL) // 100 % 10) for c in range(cols))
print(hdr)
for ri in range(rows):
    y = ri * CELL + CELL // 2
    line = []
    for ci in range(cols):
        x = ci * CELL + CELL // 2
        blk = [cls(y + dy, x + dx) for dy in (-2, 0, 2) for dx in (-2, 0, 2)]
        line.append(Counter(blk).most_common(1)[0][0])
    print(f"{y:3d} " + "".join(line))
