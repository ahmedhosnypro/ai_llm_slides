#!/usr/bin/env python3
"""Slide 043 — complete arrow scans + stack layer vscans."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)

mR = lambda p: (p[:, 0] > 140) & (p[:, 0] - p[:, 1] > 60) & (p[:, 0] - p[:, 2] > 60) & (p[:, 1] < p[:, 2] + 35)

def runs(mask_1d, base, label):
    out, start = [], None
    for i, v in enumerate(mask_1d):
        if v and start is None: start = i
        if not v and start is not None:
            out.append((start + base, i - 1 + base)); start = None
    if start is not None: out.append((start + base, len(mask_1d) - 1 + base))
    return out

print('=== FULL vertical-arrow/label zone x595..680, every row y160..350 (n>=1) ===')
for y in range(160, 351):
    rs = runs(mR(a[y, 595:680]), 595, '')
    if rs: print(f'  y{y}: {rs}')

print('=== horizontal-arrow zone x630..830 y300..350 ===')
for y in range(300, 351):
    rs = runs(mR(a[y, 630:830]), 630, '')
    if rs: print(f'  y{y}: {rs}')

print('=== diagonal-arrow/label zone x770..900 y200..330 ===')
for y in range(200, 331):
    rs = runs(mR(a[y, 770:900]), 770, '')
    if rs: print(f'  y{y}: {rs}')

print('=== stack vscans ===')
def vscan(x, y0, y1, mask_fn, label):
    m = mask_fn(a[y0:y1, x])
    print(f'{label} x={x}: {runs(m, y0, "")}')

mM = lambda p: (p[:, 0] > 150) & (p[:, 2] > 150) & (p[:, 1] < 80)
mN = lambda p: (p[:, 0] < 110) & (p[:, 1] < 110) & (p[:, 2] < 150) & (p[:, 2] >= p[:, 0])
mO = lambda p: (p[:, 0] > 180) & (p[:, 0] - p[:, 1] > 60) & (p[:, 1] > p[:, 2] + 40)
mY = lambda p: (p[:, 0] > 200) & (p[:, 1] > 200) & (p[:, 2] < 130)
mg = lambda p: (p[:, 1] > 120) & (p[:, 1] - p[:, 0] > 30) & (p[:, 1] - p[:, 2] > 30)
mL = lambda p: (p[:, 2] > 150) & (p[:, 2] - p[:, 0] > 25) & (p[:, 1] > 110)
mDR = lambda p: (p[:, 0] > 150) & (p[:, 0] - p[:, 1] > 80) & (p[:, 1] < 110) & (p[:, 2] < 110)  # dark red/orange face

for x in (240, 290, 312):
    vscan(x, 95, 345, mO, 'left orange')
    vscan(x, 95, 345, mN, 'left navy ')
    vscan(x, 95, 345, mY, 'left yellow')
    vscan(x, 95, 345, mg, 'left green ')
for x in (215, 222):
    vscan(x, 150, 345, mDR, 'left red-face band')
for x in (800, 808, 825, 843, 860):
    vscan(x, 95, 325, mN, 'right navy')
    vscan(x, 95, 325, mO, 'right orange')
    vscan(x, 95, 325, mY, 'right yellow')
    vscan(x, 95, 325, mL, 'right lblue')
    vscan(x, 95, 325, mg, 'right green')
print('samples:', [(x, tuple(a[180, x])) for x in (795, 800, 805, 810, 815, 820, 826, 830)],
      [(x, tuple(a[150, x])) for x in (840, 845, 850, 856, 862)],
      [(x, tuple(a[110, x])) for x in (750, 780, 800, 820, 840, 855)])
