#!/usr/bin/env python3
"""m8_fine.py — fine ASCII map of a region: python3 m8_fine.py x0 x1 y0 y1 [bwx bhy]"""
from PIL import Image
import numpy as np
import sys

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]

x0, x1, y0, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
bwx = int(sys.argv[5]) if len(sys.argv) > 5 else 4
bhy = int(sys.argv[6]) if len(sys.argv) > 6 else 2

def cls(r, g, b):
    if r > 243 and g > 243 and b > 240: return '.'
    if 220 < r < 245 and 220 < g < 245 and 215 < b < 242 and abs(r-g) < 8 and abs(g-b) < 12: return 'D'  # gray panel E9E9E7
    if r > 225 and g > 205 and b > 195 and g <= b + 40 and r >= g: return 'l'   # pale pink/white box
    if r > 228 and g > 222 and 150 < b < 235: return 'y'   # cream/pale yellow
    if r > 215 and g > 185 and b < 155: return 'Y'         # yellow
    if r > 228 and 140 < g < 220 and 135 < b < 228 and b > g - 30: return 'p'  # pink
    if b > 185 and r < 210 and 120 < g < 220: return 'c'   # cyan
    if r < 140 and g > 110 and b < 140: return 'g'         # green
    if r > 150 and g < 110 and b < 110: return 'r'         # red
    if r > 190 and 115 < g < 200 and 75 < b < 150: return 'o'  # orange fill
    if 135 < r < 215 and 55 < g < 125 and b < 75: return 'O'   # dark orange border
    if 95 < r < 170 and g < 85 and 60 < b < 140: return 'P'    # plum
    if 85 < r < 150 and g < 80 and 120 < b < 200: return 'U'   # purple
    if abs(r-g) < 25 and abs(g-b) < 25 and 100 < r < 220: return 'w'  # gray
    if r < 60 and g < 60 and b < 60: return 'K'
    return '?'

hdr = '     '
for x in range(x0, x1, bwx):
    hdr += str((x // 10) % 10)
print(hdr)
for by in range(y0, y1, bhy):
    row = ''
    for bx in range(x0, x1, bwx):
        blk = A[by:by+bhy, bx:bx+bwx].reshape(-1, 3)
        r, g, b = blk[:, 0].mean(), blk[:, 1].mean(), blk[:, 2].mean()
        row += cls(r, g, b)
    print(f'{by:4d} {row}')
