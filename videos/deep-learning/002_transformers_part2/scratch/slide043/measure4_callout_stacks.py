#!/usr/bin/env python3
"""Slide 043 — deep probes: callout fill/border, stack grids, green box, text bands."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def sample(x, y, label):
    print(f'{label} ({x},{y}): {tuple(a[y, x])}')

# --- callout fill color probe (grid of samples in x 350..650, y 150..340)
print('--- callout interior samples ---')
for (x, y) in [(360,160),(420,200),(500,250),(580,300),(640,330),(300,250),(560,150),(450,320)]:
    sample(x, y, 'callout?')

# where does the cream mask actually hit? column histogram
cream = (r > 235) & (g > 235) & (b > 190) & (b < 235)
ys, xs = np.where(cream[100:400, 250:700])
import collections
colh = collections.Counter((xs + 250) // 20 * 20)
print('cream col hist:', sorted(colh.items())[:30])

# --- find the callout box border: red stroke mask (strict) around x 250..700 y 100..400
red_any = (r > 140) & (r - g > 60) & (r - b > 60)
print('--- red border rows/cols (callout window, long runs) ---')
for y in range(100, 400):
    xs = np.where(red_any[y, 250:700])[0]
    if len(xs) > 300:
        print(f'  red row y{y}: x {xs.min()+250}..{xs.max()+250} n={len(xs)}')
for x in range(250, 700):
    ys2 = np.where(red_any[100:400, x])[0]
    if len(ys2) > 150:
        print(f'  red col x{x}: y {ys2.min()+100}..{ys2.max()+100} n={len(ys2)}')

# --- left stack grid seams: magenta mask per row/col counts
mag = (r > 150) & (b > 150) & (g < 80)
print('--- left stack magenta col profile (x110..210) ---')
for x in range(110, 212, 2):
    print(f'x{x}: {mag[176:339, x].sum()}', end='  ')
print()
print('--- left stack magenta row profile (y174..340) ---')
for y in range(174, 341, 2):
    print(f'y{y}: {mag[y, 110:210].sum()}', end='  ')
print()
print('--- right stack magenta col profile (x660..805) ---')
for x in range(660, 806, 3):
    print(f'x{x}: {mag[153:315, x].sum()}', end='  ')
print()
print('--- right stack magenta row profile (y150..316) ---')
for y in range(150, 317, 2):
    print(f'y{y}: {mag[y, 660:805].sum()}', end='  ')
print()
