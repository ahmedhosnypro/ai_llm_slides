#!/usr/bin/env python3
"""V/K panel 4px maps + surgical scanlines + note/emphasis zooms."""
from PIL import Image
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def cls(c):
    r, g, b = c
    if r > 238 and g > 238 and b > 238: return "."
    if r < 90 and g < 90 and b < 90: return "#"
    if r < 160 and b > 120 and b - r > 50 and g < 120: return "N"
    if r < 160 and r - g > 45 and r - b > 45 and g < 110: return "r"
    if r < 160 and g - r > 20 and g - b > 20 and g > 70: return "v"
    if r > 130 and r-g > 55 and r-b > 55: return "R"
    if b > 120 and b-r > 55 and b-g > 35: return "B"
    if g > 105 and g-r > 30 and g-b > 30: return "G"
    if r > 225 and 150 < g < 218 and 160 < b < 235 and r-g > 18: return "k"
    if r > 233 and 210 < g < 245 and 180 < b < 230: return "P"
    if 130 < r < 215 and 130 < g < 218 and b > 195 and b-r > 20: return "w"
    if r < 220 and g > 200 and g-r > 12 and g-b > 8: return "g"
    if r > 225 and g > 210 and b < 165: return "Y"
    return "-"

def region(x0, y0, x1, y1, cell=4, step=4):
    print("     " + "".join(str(((x0 + i*cell)//10) % 10) if ((x0+i*cell) % 50 < cell) else " " for i in range((x1-x0)//cell)))
    for y in range(y0, y1, step):
        row = []
        for x in range(x0, x1, cell):
            cnt = Counter()
            for dy in range(cell):
                for dx in range(cell):
                    cnt[cls(px[min(x+dx, W-1), min(y+dy, H-1)])] += 1
            row.append(cnt.most_common(1)[0][0])
        print(f"{y:4d} " + "".join(row))

def runs(y, x0, x1):
    out = []; prev = None; start = x0
    for x in range(x0, x1):
        c = cls(px[x, y])
        if c != prev:
            if prev is not None: out.append((prev, start, x-1))
            prev = c; start = x
    out.append((prev, start, x1-1))
    return out

def show(label, rs, minlen=1):
    print(f"{label}: " + " ".join(f"{c}{a}-{b}" for (c, a, b) in rs if b-a+1 >= minlen))

print("=== V PANEL x465..900 y95..305 ===")
region(465, 95, 900, 305)
print("\n=== K PANEL x50..470 y300..540 ===")
region(50, 300, 470, 540)
print("\n=== scanlines ===")
show("y305", runs(305, 440, 700))
show("y285", runs(285, 430, 700))
show("y325 (callout2)", runs(325, 690, 935))
show("y355 (callout3)", runs(355, 430, 700))
show("y400 (emphasis)", runs(400, 630, 930))
show("y470 (notebox)", runs(470, 480, 930))
show("y500 (notebox)", runs(500, 480, 930))
show("y215 (V =)", runs(215, 780, 900))
show("y400 (K =)", runs(400, 370, 470))
