#!/usr/bin/env python3
"""Downsampled color-code map of slide_026 frame (96x54 chars, each = 10x10 px)."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def classify(c):
    r, g, b = c
    if r > 246 and g > 246 and b > 246: return '.'   # white
    if abs(r-233) < 10 and abs(g-233) < 10 and abs(b-231) < 12: return ','  # panel gray E9E9E7
    if r < 60 and g < 60 and b < 60: return '#'       # black/dark ink
    if r > 150 and g < 90 and b < 90: return 'R'      # red
    if r > 100 and g < 80 and b < 80: return 'r'      # dark red/maroon
    if b > 150 and r < 120 and g > 120: return 'B'    # cyan-blue
    if b > 130 and r < 100 and g < 110: return 'b'    # navy/blue
    if r > 190 and 110 < g < 190 and b < 150 and r-b > 60: return 'O'  # orange
    if g > 150 and r < 180 and b < 150 and g-r > 20 and g-b > 20: return 'G'  # green
    if 200 < r < 245 and 210 < g < 245 and 180 < b < 220 and g-b > 15: return 'g'  # light green DFEECD
    if abs(r-g) < 14 and abs(g-b) < 14 and 150 < r < 210: return 'm'  # mid gray BFBFBF
    if 210 <= r <= 246 and 210 <= g <= 246 and 210 <= b <= 246: return '-'  # light gray
    if r > 200 and g > 200 and b < 160: return 'Y'    # yellow
    return '?'

for gy in range(0, H, 10):
    row = ''
    for gx in range(0, W, 10):
        # sample 4 px in the cell, majority
        votes = {}
        for dy in (2, 6):
            for dx in (2, 6):
                if gx+dx < W and gy+dy < H:
                    k = classify(px[gx+dx, gy+dy])
                    votes[k] = votes.get(k, 0) + 1
        row += max(votes, key=votes.get)
    print(f"{gy:3d} {row}")
print("     " + ''.join(str((gx//10) % 10) for gx in range(0, W, 10)))
