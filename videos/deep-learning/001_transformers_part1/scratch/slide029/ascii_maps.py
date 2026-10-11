#!/usr/bin/env python3
"""ASCII pixel-class maps of slide-029 delta regions (I cannot see images)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)

def classify(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r > 130 and r - g > 60 and r - b > 60: return "R"          # red ink
    if r > 225 and g > 150 and g < 230 and g - b > 25 and r - b > 40: return "O"  # orange fill
    if b > 130 and b - r > 55 and b - g > 45: return "B"          # blue ink
    if 130 < r < 210 and g < 130 and b > 130 and b - g > 40: return "M"  # magenta/purple
    if r > 235 and g > 235 and b > 235: return "w"                # white
    if b >= g - 2 and g > r + 4 and b > 230: return "c"           # pale cyan
    if r > 240 and g > 220 and b < 215: return "y"                # yellow
    if r < 100 and g < 100 and b < 100: return "k"                # black
    if r > 180 and g > 120 and b < 140 and r - b > 60: return "o"  # darker orange/tan
    return "."

def show(x0, y0, x1, y1, step=2, label=""):
    print(f"== {label} x{x0}..{x1} y{y0}..{y1} (step {step}; 1 char = {step}px) ==")
    hdr = "     " + "".join(str((x0 + i * step) // 100 % 10) for i in range(0, (x1 - x0) // step))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join(classify(A[y, x0 + i * step]) for i in range(0, (x1 - x0) // step))
        print(f"y{y:3d} {row}")

# callout 1 + 2 band
show(255, 135, 540, 195, 2, "CALLOUT1")
show(600, 135, 880, 195, 2, "CALLOUT2")
# query box + Q badge + strip top
show(90, 405, 560, 540, 2, "QUERY AREA")
# result box
show(540, 415, 900, 530, 2, "RESULT BOX")
# K badge
show(140, 320, 195, 365, 1, "K BADGE")
# V badge
show(725, 320, 775, 365, 1, "V BADGE")
