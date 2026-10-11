#!/usr/bin/env python3
"""Legend internals; right-side W chip cluster; bottom query row."""
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
def cls(c):
    r,g,b=c
    if r>245 and g>245 and b>245: return 'W'
    if abs(r-233)<12 and abs(g-233)<12 and abs(b-231)<14: return 'G'
    if g>180 and r<230 and b<230 and g-r>10 and g-b>10: return 'n'  # pale green legend
    if r>230 and g>200 and b<130: return 'y'  # yellow
    if r<90 and g<90 and b<90: return 'K'
    if r>140 and g<110 and b<110: return 'R'
    if abs(r-51)<50 and abs(g-102)<50 and abs(b-204)<50: return 'B'
    return '?'
print("== legend rows ==")
for Y in range(440, 540, 4):
    prev=None; out=''
    for x in range(700, 960):
        c = cls(a[Y,x])
        if c!=prev: out += f'{x}{c}'; prev=c
    print(f'y={Y}: {out[:400]}')
