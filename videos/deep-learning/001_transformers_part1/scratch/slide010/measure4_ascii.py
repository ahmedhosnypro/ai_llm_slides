#!/usr/bin/env python3
"""Pass 4 (slide010): 3px-resolution ASCII maps of the whole content area.

Adapted from scratch/slide009/measure8_ascii.py. Charset:
  R strong red | r reddish/pink | K dark | W white | G green-ish
  Y yellow (decoder container) | O peach (encoder container) | L lavender
  B blue-ish ink | g light-green fill | . panel gray | (space) other light
"""
from PIL import Image
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_010.jpg"
bi = np.asarray(Image.open(IM).convert("RGB"), dtype=np.int16)

def cls(r, g, b):
    if r > 150 and g < 100 and b < 100: return "R"
    if r - g > 35 and r - b > 30 and r > 140: return "r"
    if r < 120 and g < 120 and b < 120: return "K"
    if r > 242 and g > 242 and b > 242: return "W"
    if r > 230 and g > 230 and b < 190 and g > 200: return "Y"   # decoder yellow FDFF85/FAEC69
    if r > 235 and 175 < g < 230 and 150 < b < 205: return "O"  # peach F8D5AD
    if 200 < r < 245 and 200 < g < 245 and b > 228: return "L"  # lavender D9D9F3
    if r < 130 and g < 130 and b > 150: return "B"              # blue ink 2222CC
    if g - r > 12 and g - b > 8: return "G"
    if 225 <= r <= 242 and 225 <= g <= 242 and 215 <= b <= 235: return "."
    return " "

def dump(x0, x1, y0, y1, step=3):
    print(f"===== map x{x0}..{x1} y{y0}..{y1} step={step} =====")
    hdr = "     " + "".join(str(((x0 + x * step) // 10) % 10) for x in range((x1 - x0) // step))
    print(hdr)
    for yy in range(y0, y1, step):
        row = []
        for xx in range(x0, x1, step):
            reg = bi[yy:yy + step, xx:xx + step].reshape(-1, 3)
            m = reg.mean(axis=0)
            row.append(cls(m[0], m[1], m[2]))
        print(f"y{yy:3d} " + "".join(row))

dump(480, 925, 110, 300, 3)      # decoder + right attention box
