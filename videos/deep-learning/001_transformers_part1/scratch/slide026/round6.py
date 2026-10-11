#!/usr/bin/env python3
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def cls(c):
    r, g, b = c
    if r < 160 and g < 160: return "k"                    # dark ink
    if r - g > 45 and r > 150: return "R"                  # red
    if r > 240 and g > 240 and b < 228: return "Y"         # yellow
    if b - r > 25 and b > 200: return "L"                  # lavender/blue
    if r > 225 and 120 < g < 215 and b > 185 and r - g > 25: return "P"  # pink
    if g - r > 15 and g - b > 5 and g > 200: return "m"    # mint/green light
    if g - r > 15 and g - b > 30: return "G"               # green strong
    if r > 240 and g > 240 and b > 240: return "w"         # white
    if abs(r-247)+abs(g-227)+abs(b-206) <= 40: return "."  # peach
    if abs(r-233)+abs(g-233)+abs(b-231) <= 22: return ","  # gray panel
    if r > 200 and g > 180 and b > 160 and r - b > 25: return "t"  # tan
    return "?"

def amap1(name, x0, x1, y0, y1):
    print(f"== {name} x{x0}..{x1-1} y{y0}..{y1-1} (1px) ==")
    for y in range(y0, y1):
        print(f"{y:3d} " + "".join(cls(A[y, x]) for x in range(x0, x1)))

amap1("NODE1 zone", 505, 565, 230, 266)
amap1("NODE4 zone", 595, 660, 356, 392)
amap1("Ybox+arrow", 538, 625, 112, 172)
amap1("glyph L1 row", 58, 148, 234, 258)
