#!/usr/bin/env python3
"""m1_map.py — coarse ASCII map of 002:37 frame: 4x4 blocks classified by dominant color."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
img = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = img.shape

def cls_block(block):
    r, g, b = block[..., 0].mean(), block[..., 1].mean(), block[..., 2].mean()
    # dominant color classification with priority
    def d(rgb): return abs(r-rgb[0])+abs(g-rgb[1])+abs(b-rgb[2])
    if r > 238 and g > 238 and b > 238: return "."   # white
    if d((231, 233, 230)) < 14: return ","            # gray panel E9E9E7-ish
    if d((251, 229, 214)) < 30: return "P"            # peach panel
    if d((206, 255, 224)) < 30: return "M"            # mint panel
    if d((232, 163, 61)) < 55: return "O"             # orange
    if d((201, 166, 107)) < 55: return "T"            # tan
    if d((46, 125, 50)) < 90 or d((27, 114, 63)) < 90: return "G"  # green border
    if d((204, 0, 0)) < 90 or (r > 120 and g < 90 and b < 90): return "R"  # red
    if d((216, 160, 184)) < 50: return "V"            # mauve
    if d((179, 157, 219)) < 50: return "L"            # lavender
    if d((255, 241, 118)) < 60: return "Y"            # yellow
    if d((165, 214, 167)) < 50: return "S"            # soft green
    if d((248, 187, 208)) < 50: return "K"            # pink
    if r < 70 and g < 70 and b < 70: return "#"       # dark ink
    return " "

print("    " + "".join(f"{x//100%10}" if x % 100 == 0 else ("|" if (x//20)*20 == x else " ") for x in range(0, W, 4)))
for y in range(0, H, 4):
    row = []
    for x in range(0, W, 4):
        row.append(cls_block(img[y:y+4, x:x+4]))
    print(f"{y:3d} " + "".join(row))
