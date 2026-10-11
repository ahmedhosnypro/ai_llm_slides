#!/usr/bin/env python3
"""Side-by-side classified 3px-grid maps: render vs original, diagram zone."""
import numpy as np
from PIL import Image
from collections import Counter
import sys

def cls(px):
    r, g, b = px
    if r < 120 and g < 120 and b < 120: return '#'
    if r > 150 and g < 140 and b < 140 and r-g > 55: return 'R'
    if b > 130 and b-r > 50 and b-g > 30: return 'B'
    if r > 200 and g > 200 and b < 100: return 'Y'
    if r > 190 and 140 < g < 200 and 100 < b < 160 and r > g > b: return 'T'
    if 150 <= r <= 205 and 100 <= g <= 150 and 60 <= b <= 115 and r > g > b: return 'D'
    if 140 <= r <= 215 and 85 <= g <= 135 and 75 <= b <= 125 and r-g > 40 and abs(g-b) < 25: return 'C'
    if 130 <= r <= 225 and 80 <= g <= 160 and 150 <= b <= 240: return 'P'
    if 150 <= r <= 235 and 190 <= g <= 250 and 120 <= b <= 225 and g >= r: return 'L'
    if 235 < r and 225 < g and 195 < b: return '.'
    if 190 <= r <= 235 and g > 240 and 200 <= b <= 235: return 'g'
    if 150 <= r <= 215 and 140 <= g <= 205 and 60 <= b <= 150 and abs(r-g) < 30: return 'O'
    if r > 240 and g > 240 and b > 240: return ' '
    return '?'

def gridmap(path):
    im = Image.open(path).convert('RGB').resize((960, 540), Image.LANCZOS)
    A = np.asarray(im).astype(int)
    rows = []
    for y0 in range(90, 537, 3):
        line = []
        for x0 in range(560, 957, 3):
            c = Counter()
            for dy in range(3):
                for dx in range(3):
                    c[cls(A[y0+dy, x0+dx])] += 1
            line.append(c.most_common(1)[0][0])
        rows.append((y0, ''.join(line)))
    return rows

which = sys.argv[1]
path = ('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/render_1.png'
        if which == 'render' else
        '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg')
print(f"===== {which} =====")
hdr = '     ' + ''.join(str((560 + i*3) // 100 % 10) if (560 + i*3) % 100 < 3 else ' ' for i in range(133))
print(hdr)
for y0, line in gridmap(path):
    print(f"{y0:3d}  {line}")
