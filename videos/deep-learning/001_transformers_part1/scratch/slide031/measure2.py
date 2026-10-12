#!/usr/bin/env python3
"""Coarse color-class map + targeted edge scans for slide_031.jpg."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def classify(c):
    r, g, b = c
    if r > 240 and g > 240 and b > 240: return "."        # white
    if r > 235 and g > 215 and 180 < b < 225: return "P"  # peach FCE4CF
    if abs(r-245) < 25 and abs(g-184) < 30 and abs(b-208) < 30: return "k"  # pink F5B8D0
    if abs(r-242) < 20 and abs(g-185) < 25 and abs(b-198) < 25: return "r"  # rose F2B9C6
    if abs(r-185) < 25 and abs(g-194) < 25 and abs(b-242) < 25: return "w"  # periwinkle B9C2F2
    if abs(r-199) < 22 and abs(g-232) < 20 and abs(b-199) < 22: return "g"  # light green C7E8C7
    if r > 235 and g > 225 and b < 150: return "Y"        # yellow
    if r > 150 and g < 110 and b < 110 and r-g > 70: return "R"  # red
    if b > 140 and b-r > 60 and b-g > 50: return "B"      # blue
    if g > 110 and g-r > 50 and g-b > 40: return "G"      # green
    if r < 100 and g < 100 and b < 100: return "#"        # dark ink
    if r < 210 and g < 210 and b < 210: return "-"        # gray/mid ink
    return " "

print("   " + "".join(str((x//10) % 10) for x in range(0, W, 10)))
for y in range(0, H, 10):
    row = []
    for x in range(0, W, 10):
        # dominant class in the 10x10 cell (skip ' ' and '.')
        from collections import Counter
        cnt = Counter()
        for dy in range(0, 10, 2):
            for dx in range(0, 10, 2):
                cnt[classify(px[min(x+dx, W-1), min(y+dy, H-1)])] += 1
        # priority order: strong classes first
        for ch in "#RBYGwgrkP-.":
            if cnt[ch] >= 6:
                row.append(ch); break
        else:
            row.append(cnt.most_common(1)[0][0] if cnt else " ")
    print(f"{y:3d} " + "".join(row))
