#!/usr/bin/env python3
"""slide033 measure-6: ASCII structure map of the left columns + pair box region."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)

def ch(px):
    r, g, b = px
    if r > 246 and g > 246 and b > 246: return "."      # white
    if 222 < r <= 246 and 222 < g <= 246 and 222 < b <= 246: return " "  # bg E8E8E8
    if r > 228 and g > 205 and 150 < b < 215 and r - b > 25 and g - b > 18: return "c"  # cream
    if r > 215 and 165 < g < 225 and 120 < b < 180 and r - b > 55: return "o"  # lt orange
    if r > 200 and 110 < g <= 175 and b < 130 and r - b > 80: return "O"  # dk orange
    if 140 < r < 215 and g > 175 and 120 < b < 200 and g - b > 20 and g - r > 15: return "g"  # lt green
    if r < 140 and g > 130 and g - r > 30 and g - b > 40: return "G"  # dk green
    if r > 115 and g < 80 and b < 80: return "R"        # red C00000
    if 150 < r < 215 and g < 95 and b < 95: return "M"  # maroon
    if r < 115 and g < 115 and b < 115: return "k"      # black/dark
    if b > 200 and g > 200 and b - r > 10: return "b"   # lt blue
    if b > 120 and r < 110 and b - r > 40: return "B"   # blue
    if r > 200 and g > 200 and b > 150 and b < 215: return "y"  # pale yellow
    return ":"

print("    " + "".join(str((x // 10) % 10) for x in range(210, 345, 2)))
for y in range(112, 520, 2):
    row = "".join(ch(a[y, x]) for x in range(210, 345, 2))
    print(f"{y:3d} {row}")
