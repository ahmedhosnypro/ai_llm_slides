#!/usr/bin/env python3
"""Stage 15: lighter-threshold ASCII maps to catch thin math strokes."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
lum = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3.0

def amap(x0, x1, y0, y1, thr, label):
    print(f'--- {label} x{x0}..{x1} y{y0}..{y1} thr{thr} ---')
    print('     ' + ''.join(str((x//10)%10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = ''.join('#' if lum[y, x] < thr else '.' for x in range(x0, x1))
        print(f'{y:4d} {row}')

amap(236, 300, 290, 342, 195, 'EQ1 sum region + right (1px rows)')
amap(236, 350, 346, 398, 195, 'EQ2 sum region + right (1px rows)')
