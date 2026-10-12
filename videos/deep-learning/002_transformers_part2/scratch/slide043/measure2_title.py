#!/usr/bin/env python3
"""Slide 043 — refine landmarks, title extent, and element census."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red_loose = (r > 150) & (r - g > 30) & (r - b > 30)
red_text = (r > 150) & (r - g > 80) & (r - b > 80)

colcount = red_loose[100:400, :].sum(axis=0)
for x in (57, 58, 59, 60, 899, 900, 901, 902, 903):
    print(f'col {x}: red_loose={colcount[x]}')
rowcount = red_loose[:, 150:850].sum(axis=1)
for y in (41, 42, 43, 44, 45, 515, 516, 517, 518):
    print(f'row {y}: red_loose={rowcount[y]}')

# title band: red text rows 50..140, x 100..900 — per-row extents
print('--- title red-text per-row extents (x100..900) ---')
for y in range(50, 140):
    xs = np.where(red_text[y, 100:900])[0]
    if len(xs) > 3:
        print(f'y{y}: x {xs.min()+100}..{xs.max()+100} n={len(xs)}')
