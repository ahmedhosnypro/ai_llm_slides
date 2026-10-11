#!/usr/bin/env python3
"""Detect rectangles (long red/blue horizontal runs) and vertical borders in slide_039 frame."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 120 and r - g > 50 and r - b > 50
def blueish(p):
    r, g, b = p
    return b > 110 and b - r > 60 and b - g > 40

# long horizontal red runs per row (>= 200 px)
def runs_in_row(y, pred, minlen):
    out = []
    x = 62
    while x <= 899:
        if pred(px[x, y]):
            x0 = x
            while x <= 899 and pred(px[x, y]): x += 1
            if x - x0 >= minlen: out.append((x0, x - 1))
        else:
            x += 1
    return out

hred = {yy: runs_in_row(yy, reddish, 200) for yy in range(47, 514)}
hblue = {yy: runs_in_row(yy, blueish, 200) for yy in range(47, 514)}

print("RED horiz runs >=200px:")
for y, rs in sorted(hred.items()):
    if rs: print(" ", y, rs)
print("BLUE horiz runs >=200px:")
for y, rs in sorted(hblue.items()):
    if rs: print(" ", y, rs)

# vertical red runs (>= 25 px) per column -> box left/right borders
vruns = {}
for x in range(62, 900):
    y = 47
    while y <= 513:
        if reddish(px[x, y]):
            y0 = y
            while y <= 513 and reddish(px[x, y]): y += 1
            if y - y0 >= 25:
                vruns.setdefault(x, []).append((y0, y - 1))
        else:
            y += 1
print("RED vert runs >=25px (col: [runs]):")
for x, rs in sorted(vruns.items()):
    print(" ", x, rs)
