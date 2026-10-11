#!/usr/bin/env python3
"""ASCII structure map of slide_016.jpg diagram zone (3px cells)."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
H, W = IM.shape[:2]

def cls(p):
    r, g, b = p
    if r > 235 and g > 235 and b > 235: return "W"          # white canvas
    if abs(r-233) < 14 and abs(g-233) < 14 and abs(b-231) < 14: return "G"  # gray panel
    if r > 240 and 218 < g < 242 and 200 < b < 230: return "P"  # peach panel F8E8D8
    if 190 < r < 215 and g > 240 and 205 < b < 235: return "D"  # dec panel C8F8E0
    if 190 < r < 215 and 155 < g < 180 and 120 < b < 145: return "T"  # tan CCA884
    if 140 < r < 200 and 145 < g < 195 and 95 < b < 145: return "O"   # olive/B0B888/98B088
    if 180 < r < 205 and 230 < g < 250 and 205 < b < 230: return "L"  # light green C0F0D8
    if r < 110 and g < 110 and b < 110: return "K"            # dark ink
    if b > r + 40 and b > g + 30 and b > 110: return "B"      # blue
    if r > 130 and g < 90 and b < 90: return "R"              # red
    if r > 220 and g > 220 and b < 120: return "Y"            # yellow
    if g > r + 30 and g > b + 30: return "F"                  # frame green stroke
    return "."

print("    " + "".join(str((X // 10) % 10) for X in range(560, 925, 3)))
for y in range(95, 540, 3):
    row = []
    for x in range(560, 925, 3):
        # mode of 3x3 cell
        cell = IM[y:y+3, x:x+3].reshape(-1, 3)
        from collections import Counter
        c = Counter(map(tuple, cell)).most_common(1)[0][0]
        row.append(cls(c))
    print(f"{y:3d} " + "".join(row))
