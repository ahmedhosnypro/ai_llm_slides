#!/usr/bin/env python3
"""High-res ASCII maps of slide_031.jpg regions (4px cells, dominant class)."""
from PIL import Image
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def classify(c):
    r, g, b = c
    if r > 238 and g > 238 and b > 238: return "."   # white
    if r > 233 and 210 < g < 243 and 180 < b < 228: return "P"  # peach
    if r > 225 and 150 < g < 215 and 165 < b < 235 and r-g > 25: return "k"  # pink/rose family
    if 130 < r < 210 and 130 < g < 215 and b > 195 and b-r > 25: return "w"  # periwinkle family
    if r < 215 and g > 200 and b < 235 and g-r > 20: return "G"  # light green family
    if r > 225 and g > 210 and b < 165: return "Y"   # yellow
    if r > 130 and r-g > 55 and r-b > 55: return "R"  # red
    if b > 120 and b-r > 55 and b-g > 35: return "B"  # blue
    if g > 105 and g-r > 30 and g-b > 30: return "V"  # green (strong)
    if r < 115 and g < 115 and b < 115: return "#"    # dark
    return "-"

def region(x0, y0, x1, y1, cell=4):
    hdr = "     " + "".join(str(((x0 + i*cell)//10) % 10) if ((x0+i*cell) % 50 < cell) else " " for i in range((x1-x0)//cell))
    print(hdr)
    for y in range(y0, y1, cell):
        row = []
        for x in range(x0, x1, cell):
            cnt = Counter()
            for dy in range(cell):
                for dx in range(cell):
                    cnt[classify(px[min(x+dx, W-1), min(y+dy, H-1)])] += 1
            best = cnt.most_common()
            ch = best[0][0]
            # prefer ink classes when tied-ish
            row.append(ch)
        print(f"{y:4d} " + "".join(row))

print("=== Q PANEL x50..470 y96..305 (4px) ===")
region(50, 96, 470, 305)
