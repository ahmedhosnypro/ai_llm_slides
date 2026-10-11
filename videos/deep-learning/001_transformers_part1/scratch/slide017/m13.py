#!/usr/bin/env python3
"""Full fine 2px maps of encoder + decoder panels with improved classifier."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def cls(px):
    r, g, b = px
    if r < 130 and g < 130 and b < 130: return '#'
    if r > 150 and g < 140 and b < 140 and r-g > 55: return 'R'
    if b > 130 and b-r > 50 and b-g > 30: return 'B'
    if r > 200 and g > 200 and b < 100: return 'Y'
    if r > 190 and 140 < g < 200 and 100 < b < 160 and r > g > b: return 'T'
    if 150 <= r <= 200 and 100 <= g <= 145 and 60 <= b <= 110 and r > g > b: return 'D'
    if 140 <= r <= 215 and 85 <= g <= 130 and 75 <= b <= 125 and r-g > 45 and abs(g-b) < 25: return 'C'
    if 130 <= r <= 225 and 80 <= g <= 160 and 150 <= b <= 240: return 'P'
    if 150 <= r <= 235 and 190 <= g <= 250 and 120 <= b <= 225 and g >= r: return 'L'
    if 235 < r and 225 < g and 195 < b: return '.'
    if 190 <= r <= 235 and g > 240 and 200 <= b <= 235: return 'g'
    if 225 < r and 225 < g and b < 100: return 'y'
    if 155 <= r <= 210 and 150 <= g <= 200 and 80 <= b <= 150 and abs(r-g) < 25: return 'O'
    if r > 240 and g > 240 and b > 240: return ' '
    return '?'

def amap(x0, x1, y0, y1, name, step=2):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1} step{step}")
    hdr = '     ' + ''.join(str((x0+i*step)//100 % 10) if (x0+i*step) % 20 < step else ' ' for i in range((x1-x0)//step+1))
    print(hdr)
    for y in range(y0, y1+1, step):
        line = []
        for x in range(x0, x1+1, step):
            c = Counter()
            for dy in range(step):
                for dx in range(step):
                    if y+dy <= 539 and x+dx <= 959:
                        c[cls(A[y+dy, x+dx])] += 1
            line.append(c.most_common(1)[0][0])
        print(f"{y:3d}  {''.join(line)}")

import sys
which = sys.argv[1] if len(sys.argv) > 1 else 'enc'
if which == 'enc':
    amap(576, 740, 255, 500, "ENCODER stack", 2)
else:
    amap(740, 900, 100, 340, "DECODER top", 2)
