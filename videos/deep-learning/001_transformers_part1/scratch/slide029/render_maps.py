#!/usr/bin/env python3
"""Render-space ASCII maps + ink measurements for the delta regions."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
R = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide029/render_1.png").convert("RGB"), dtype=np.int16)
print("render size:", R.shape)

def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r > 130 and r - g > 60 and r - b > 60: return "R"
    if r > 225 and 150 < g < 235 and g - b > 20 and r - b > 40: return "O"
    if b > 120 and b - r > 50 and b - g > 40: return "B"
    if 120 < r < 225 and g < 150 and b > 130 and b - g > 35: return "M"
    if r > 240 and g > 240 and b > 240: return "w"
    if r > 200 and 170 < g < 230 and 120 < b < 200: return "T"
    if r > 235 and g > 205 and b < 190: return "y"
    return "."

def show(x0, y0, x1, y1, step, label):
    print(f"== {label} x{x0}..{x1} y{y0}..{y1} step {step} ==")
    print("     " + "".join(str((x0 + i * step) // 100 % 10) for i in range(0, (x1 - x0) // step)))
    for y in range(y0, y1, step):
        print(f"y{y:4d} " + "".join(cls(R[y, x0 + i * step]) for i in range(0, (x1 - x0) // step)))

# title + subtitle bands (render): y 100..230, x 150..1900
show(150, 100, 1900, 232, 8, "TITLE/SUBTITLE BAND")
# Values tan box area (render): frame x748..850 y180..226 -> render 1558..1771, 375..471
show(1540, 370, 1790, 480, 3, "VALUES BOX AREA")
# query box area: frame x95..250 y405..470 -> render 198..521, 844..979
show(190, 840, 530, 985, 4, "QUERY BOX AREA")
