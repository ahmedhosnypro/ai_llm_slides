#!/usr/bin/env python3
"""Slide 043 — fine scanlines: stack bands, red band, callout border, arrows, labels."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(mask_1d, base, label):
    out, start = [], None
    for i, v in enumerate(mask_1d):
        if v and start is None: start = i
        if not v and start is not None:
            out.append((start + base, i - 1 + base)); start = None
    if start is not None: out.append((start + base, len(mask_1d) - 1 + base))
    print(f'{label}: {out}')

def hscan(y, x0, x1, mask_fn, label):
    runs(mask_fn(a[y, x0:x1]), x0, f'{label} y={y}')

def vscan(x, y0, y1, mask_fn, label):
    runs(mask_fn(a[y0:y1, x]), y0, f'{label} x={x}')

mM = lambda p: (p[:, 0] > 150) & (p[:, 2] > 150) & (p[:, 1] < 80)
mN = lambda p: (p[:, 0] < 110) & (p[:, 1] < 110) & (p[:, 2] < 150) & (p[:, 2] >= p[:, 0])
mO = lambda p: (p[:, 0] > 180) & (p[:, 0] - p[:, 1] > 60) & (p[:, 1] > p[:, 2] + 40)
mY = lambda p: (p[:, 0] > 200) & (p[:, 1] > 200) & (p[:, 2] < 130)
mg = lambda p: (p[:, 1] > 120) & (p[:, 1] - p[:, 0] > 30) & (p[:, 1] - p[:, 2] > 30)
mL = lambda p: (p[:, 2] > 150) & (p[:, 2] - p[:, 0] > 25) & (p[:, 1] > 110)
mR = lambda p: (p[:, 0] > 140) & (p[:, 0] - p[:, 1] > 60) & (p[:, 0] - p[:, 2] > 60) & (p[:, 1] < p[:, 2] + 35)

print('=== LEFT STACK top bands (h-scans) ===')
for y in (107, 113, 120, 130, 140, 148, 158, 168, 174):
    hscan(y, 105, 345, mN, ' navy')
    hscan(y, 105, 345, mY, 'yellow')
    hscan(y, 105, 345, mg, ' green')
    hscan(y, 105, 345, mO, 'orange')
print('--- left front/red/right scans ---')
for y in (185, 200, 250, 300, 330):
    hscan(y, 105, 345, mM, 'magenta')
    hscan(y, 105, 345, mR, '  red')
    hscan(y, 105, 345, mO, 'orange')
print('samples red band:', [tuple(a[250, x]) for x in (206, 210, 215, 220, 226, 230)])
print('samples orange slab:', [tuple(a[250, x]) for x in (235, 250, 270, 290, 310, 325)])
print('samples navy top:', [tuple(a[112, x]) for x in (190, 220, 250, 280)])
print('samples yellow band:', [tuple(a[131, x]) for x in (195, 205, 215, 225)])
print('samples green band:', [tuple(a[166, x]) for x in (135, 150, 170, 190, 205)])

print('=== RIGHT STACK scans ===')
for y in (100, 112, 126, 140, 152, 162):
    hscan(y, 720, 900, mN, ' navy')
    hscan(y, 720, 900, mO, 'orange')
    hscan(y, 720, 900, mY, 'yellow')
    hscan(y, 720, 900, mL, ' lblue')
for y in (200, 250, 300):
    hscan(y, 655, 900, mM, 'magenta')
    hscan(y, 655, 900, mg, ' green')
    hscan(y, 655, 900, mO, 'orange')
    hscan(y, 655, 900, mY, 'yellow')
    hscan(y, 655, 900, mL, ' lblue')
vscan(700, 90, 330, mM, 'right front vscan x700 M')
vscan(700, 90, 330, mN, 'right front vscan x700 N')
print('samples right lblue:', [tuple(a[200, x]) for x in (846, 852, 858, 864)])
print('samples right yellow?', [tuple(a[130, x]) for x in (840, 845, 850, 855, 860)])

print('=== CALLOUT border + edges ===')
print('top border y170..175 @x450:', [tuple(a[y, 450]) for y in range(168, 178)])
print('bottom border y262..268 @x450:', [tuple(a[y, 450]) for y in range(260, 270)])
print('left border x330..336 @y220:', [tuple(a[220, x]) for x in range(328, 338)])
print('right border x613..620 @y220:', [tuple(a[220, x]) for x in range(611, 621)])
vscan(340, 165, 280, mR, 'callout left border red? x340')
hscan(173, 325, 625, mR, 'callout top border red? y173')

print('=== VERTICAL ARROW fine scan x620..670, y165..320 ===')
for y in range(165, 321, 2):
    runs(mR(a[y, 620:670]), 620, f'  y{y}')

print('=== HORIZONTAL ARROW + label y310..345 ===')
for y in range(310, 346):
    runs(mR(a[y, 630:830]), 630, f'  y{y}')

print('=== DIAGONAL ARROW + labels x780..900 y230..320 ===')
for y in range(230, 321, 2):
    runs(mR(a[y, 780:900]), 780, f'  y{y}')
