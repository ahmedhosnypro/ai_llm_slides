#!/usr/bin/env python3
"""Verification probe (read-only): is x615 a full-height cursor line, and where is the
original callout's right border? Settles the peer's x331..644.5 box vs x333..615."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

print('--- x613..617 column profile OUTSIDE the callout rows (cursor test) ---')
for x in (613, 614, 615, 616, 617):
    above = lum[60:165, x]
    below = lum[275:350, x]
    print(f'x{x}: above-box rows lum<215: {(above < 215).sum()}/105, mean {above.mean():.0f}; below-box lum<215: {(below < 215).sum()}/75, mean {below.mean():.0f}')

print('--- full-height scan: any column with a long pale dip? x600..660, y50..510 ---')
for x in range(600, 661):
    col = lum[50:510, x]
    dips = (col < 215).sum()
    if dips > 200:
        print(f'x{x}: {dips}/460 rows lum<215')

print('--- callout right border: samples at y200, y230, y250 across x605..660 ---')
for y in (200, 230, 250):
    row = [(x, tuple(a[y, x])) for x in range(605, 661, 5)]
    print(f'y{y}: {row}')

print('--- cream fill extent at y200/y230 (r>245,g>245,200<b<248) ---')
cream = (a[:, :, 0] > 245) & (a[:, :, 1] > 245) & (a[:, :, 2] > 200) & (a[:, :, 2] < 248)
for y in (200, 230):
    xs = np.where(cream[y, 330:660])[0]
    if len(xs):
        print(f'y{y}: cream x {xs.min()+330}..{xs.max()+330} n={len(xs)}')

print('--- RENDER comparison: cream extent + border position in render_1.png ---')
r = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide043/render_1.png').convert('RGB')
ra = np.asarray(r).astype(int)
rc = (ra[:, :, 0] > 245) & (ra[:, :, 1] > 245) & (ra[:, :, 2] > 200) & (ra[:, :, 2] < 248)
# render is 2001x1125 at 150dpi; frame px -> render px: *2000/960
for y in (200, 230):
    ry = int(y * 2000 / 960)
    xs = np.where(rc[ry, 600:1450])[0]
    if len(xs):
        print(f'rend y{ry} (frame y{y}): cream x {(xs.min()+600)*0.48:.0f}..{(xs.max()+600)*0.48:.0f} fp  n={len(xs)}')
