#!/usr/bin/env python3
"""Stage 12: column-wise dark-ink profile per equation band (10px buckets) + baseline rows."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3.0
dark = lum < 150

def S(fx, fy): return ((fx-18.63)/0.96123, fy/0.95556)

def colscan(y0, y1, x0, x1, label, bucket=8):
    print(f'== {label} (y{y0}..{y1}) ==')
    for xa in range(x0, x1, bucket):
        sub = dark[y0:y1, xa:xa+bucket]
        ys, xs = np.where(sub)
        if len(xs) == 0:
            print(f'  x {xa}-{xa+bucket}: .')
            continue
        ya, yb = y0+ys.min(), y0+ys.max()
        print(f'  x {xa}-{xa+bucket}: ink y {ya}..{yb} n={len(xs):3d}   slide_y {S(0,ya)[1]:.1f}..{S(0,yb)[1]:.1f}')

colscan(285, 342, 155, 350, 'EQ1 full band')
colscan(333, 398, 155, 410, 'EQ2 full band')
colscan(390, 452, 155, 335, 'EQ3 full band')
colscan(446, 484, 155, 385, 'EQ4 full band')
# header bands
colscan(208, 232, 148, 530, 'INPUT line')
colscan(252, 276, 148, 350, 'OUTPUT line')
# title band
colscan(60, 95, 255, 420, 'TITLE left half')
