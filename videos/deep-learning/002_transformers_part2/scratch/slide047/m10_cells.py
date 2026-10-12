#!/usr/bin/env python3
"""m10_cells.py — run-length color analysis across strip rows."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)

def hue(r, g, b):
    if r > 243 and g > 243 and b > 238: return 'WHITE'
    if 225 < r < 245 and 225 < g < 245 and 225 < b < 245 and max(r,g,b)-min(r,g,b) < 12: return 'PANEL'
    if r > 235 and g > 240 and 150 < b < 235: return 'yellowpale'
    if r > 240 and g > 235 and b < 150: return 'YELLOW'
    if r > 225 and g > 205 and b > 180 and g < 240: return 'pinkpale'
    if r > 225 and 200 < g < 245 and 225 < b < 252 and b >= g: return 'BLUEpale'
    if r > 235 and 140 < g < 210 and 150 < b < 230: return 'PINK'
    if b > 200 and r < 215 and g > 130: return 'CYAN'
    if r < 165 and g > 175 and b < 165: return 'GREEN'
    if 165 < r < 225 and g > 175 and b < 175: return 'greenpale'
    if r > 150 and g < 110 and b < 110: return 'RED'
    if 130 < r < 220 and 60 < g < 135 and b < 90: return 'dkorange'
    if r > 205 and 120 < g < 195 and 75 < b < 160: return 'ORANGE'
    if 95 < r < 175 and g < 95 and 55 < b < 145: return 'PLUM'
    if 150 < r < 235 and 150 < g < 235 and 150 < b < 235 and max(r,g,b)-min(r,g,b) < 30: return 'GRAY'
    return f'?({r},{g},{b})'

def rle(y, x0=130, x1=910):
    out = []
    cur = None; start = x0
    for x in range(x0, x1):
        r, g, b = A[y, x]
        h = hue(r, g, b)
        if h != cur:
            if cur is not None: out.append((start, x - 1, cur))
            cur = h; start = x
    out.append((start, x1 - 1, cur))
    return [o for o in out if o[1] - o[0] >= 3]

for y in [66, 68, 490, 494, 182, 186, 288, 392]:
    print(f'--- y={y} ---')
    for s, e, h in rle(y):
        print(f'  x{s:3d}..{e:3d} ({e-s+1:2d}px) {h}')
