#!/usr/bin/env python3
"""Global color map for slide_031.jpg — downsampled classification (1 char per 8x8 block)."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def classify(c):
    r, g, b = c
    if r > 235 and g > 215 and b < 170: return "Y"          # yellow (highlight/emphasis)
    if r > 140 and r - g > 60 and r - b > 60: return "R"    # red (borders/text)
    if b > 140 and b - r > 60 and b - g > 40: return "B"    # blue
    if g > 110 and g - r > 35 and g - b > 35: return "G"    # green
    if abs(r - 245) < 20 and abs(g - 184) < 28 and abs(b - 205) < 30: return "p"  # pink capsule
    if abs(r - 242) < 18 and abs(g - 185) < 22 and abs(b - 198) < 22: return "r"  # rose matrix bg
    if abs(r - 185) < 24 and abs(g - 194) < 24 and abs(b - 242) < 24: return "v"  # periwinkle
    if abs(r - 199) < 20 and abs(g - 232) < 18 and abs(b - 199) < 20: return "m"  # mint green
    if abs(r - 252) < 10 and abs(g - 231) < 16 and abs(b - 205) < 24: return "a"  # peach/tan FCE4CF-ish
    if r > 244 and g > 244 and b > 244: return "."           # white
    if abs(r - 233) < 12 and abs(g - 233) < 12 and abs(b - 231) < 12: return "g"  # chrome gray
    if r < 110 and g < 110 and b < 110: return "#"           # dark ink
    return " "

for by in range(0, H, 8):
    row = []
    for bx in range(0, W, 8):
        votes = {}
        for dy in range(0, 8, 2):
            for dx in range(0, 8, 2):
                k = classify(px[bx + dx, by + dy])
                votes[k] = votes.get(k, 0) + 1
        row.append(max(votes, key=votes.get))
    print(f"{by:3d} " + "".join(row))
print("    " + "".join(str((x // 8) % 10) for x in range(0, W, 8)))
print("cols: 1 char = 8px; row label = y of block top")
