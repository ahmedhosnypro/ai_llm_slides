#!/usr/bin/env python3
"""Slide 043 probe C: ASCII maps of arrow regions + left-stack right region."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def cls(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    if r > 150 and g < 110 and b < 110 and r - g > 50 and r - b > 40: return "R"   # strong red
    if r > 140 and r - g > 25 and r - b > 15 and g < 190: return "r"               # washed red/pink
    if r > 110 and g < 70 and b > 110 and b - g > 80: return "M"                   # magenta
    if g > 140 and r < 190 and b < 110 and g - b > 60: return "G"                  # green
    if r > 200 and g > 180 and b < 130: return "Y"                                 # yellow
    if r > 170 and 70 <= g < 180 and b < 110: return "O"                           # orange
    if 80 < r < 180 and 110 < g < 200 and b > 160: return "B"                      # bluegray
    if r < 100 and g < 100 and b < 140: return "K"                                 # dark
    return "."

def dump(x0, x1, y0, y1, step=2, tag=""):
    print(f"--- {tag} x{x0}..{x1} y{y0}..{y1} step {step} ---")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join(cls(a[y, x]) for x in range(x0, x1, step))
        print(f"y{y:4d} {row}")

# v-arrow + label region
dump(605, 675, 160, 320, 2, "V-ARROW+LABEL")
# h-arrow region below right block
dump(645, 830, 300, 355, 2, "H-ARROW")
# diagonal arrow + label
dump(790, 905, 220, 410, 3, "D-ARROW")
