#!/usr/bin/env python3
"""Pass 8: 4px-resolution ASCII map of the backprop panel (x485..925, y310..500)."""
from PIL import Image
import numpy as np

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0].astype(int), bi[:,:,1].astype(int), bi[:,:,2].astype(int)

def cls(r, g, b):
    if r > 150 and g < 100 and b < 100: return "R"   # strong red
    if r - g > 35 and r - b > 30 and r > 140: return "r"  # reddish/pink
    if r < 120 and g < 120 and b < 120: return "K"   # dark/black
    if r > 242 and g > 242 and b > 242: return "W"   # white
    if g - r > 12 and g - b > 8: return "G"          # green-ish
    if 226 <= r <= 240 and 226 <= g <= 238 and 214 <= b <= 226: return "."  # panel warm gray
    if 228 <= r <= 238 and 228 <= g <= 238 and 228 <= b <= 238: return "p"  # panel cool gray
    return " "

print("    " + "".join(str((485 + x*4) // 10 % 10) for x in range(110)))
for y0 in range(310, 500, 4):
    row = []
    for x0 in range(485, 925, 4):
        reg = bi[y0:y0+4, x0:x0+4].reshape(-1, 3)
        m = reg.mean(axis=0)
        row.append(cls(m[0], m[1], m[2]))
    print(f"y{y0:3d} " + "".join(row))
