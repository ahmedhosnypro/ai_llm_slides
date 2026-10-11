#!/usr/bin/env python3
"""1px map of decoder y195..330 + fill samples between lines."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def cls(px):
    r, g, b = px
    if r < 120 and g < 120 and b < 120: return '#'
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
    if 150 <= r <= 215 and 140 <= g <= 205 and 60 <= b <= 150 and abs(r-g) < 30: return 'O'
    if r > 240 and g > 240 and b > 240: return ' '
    return '?'

x0, x1 = 740, 850
print(f"decoder x{x0}..{x1} y195..330 step1")
hdr = '     ' + ''.join(str((x0+i)//100 % 10) if (x0+i) % 20 == 0 else ' ' for i in range(x1-x0+1))
hdr2 = '     ' + ''.join(str((x0+i)//10 % 10) if (x0+i) % 20 == 0 else ' ' for i in range(x1-x0+1))
print(hdr); print(hdr2)
for y in range(195, 331):
    print(f"{y:3d}  {''.join(cls(A[y, x]) for x in range(x0, x1+1))}")
