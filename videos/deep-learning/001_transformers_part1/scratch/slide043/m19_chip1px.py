#!/usr/bin/env python3
"""1px color runs for chip rows."""
import numpy as np
from PIL import Image
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
def cls(c):
    r,g,b=c
    if r>245 and g>245 and b>245: return 'W'
    if abs(r-233)<12 and abs(g-233)<12 and abs(b-231)<14: return 'G'
    if abs(r-241)<12 and abs(g-139)<18 and abs(b-150)<18: return 'S'
    if g>140 and g-r>30 and g-b>20 and r<200: return 'e'   # green dash
    if r>240 and g<160 and b<160: return 'p'   # pale pink cell
    if r>240 and g>240 and b>190: return 'C'   # pale cream
    if r<90 and g<90 and b<90: return 'K'
    if r>140 and g<110 and b<110: return 'R'
    if abs(r-51)<45 and abs(g-102)<45 and abs(b-204)<45: return 'B'
    if abs(r-222)<28 and abs(g-184)<28 and abs(b-135)<32: return 'T'
    if abs(r-238)<30 and abs(g-130)<40 and abs(b-238)<30: return 'V'
    return '?'
for Y in [326, 330, 334, 338, 342]:
    prev=None; out=''
    for x in range(96, 260):
        c = cls(a[Y,x])
        if c!=prev: out += f"{x}{c}"; prev=c
    print(f"y={Y}: {out}")
print()
for X in [130, 140, 160, 200, 300, 310]:
    prev=None; out=''
    for y in range(318, 440):
        c = cls(a[y,X])
        if c!=prev: out += f"{y}{c}"; prev=c
    print(f"x={X}: {out}")
