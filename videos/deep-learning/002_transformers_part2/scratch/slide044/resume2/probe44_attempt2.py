#!/usr/bin/env python3
"""Slide 044 attempt-2 adjudication probes (orig side): F1 left Channels label,
F2 FV arrow/label vs red rect, F3 layer banner border (+ GN/INST box controls)."""
import numpy as np
from PIL import Image

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
orig = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
r0, g0, b0 = orig[:,:,0], orig[:,:,1], orig[:,:,2]

redL  = (r0 > 150) & (r0-g0 > 30) & (r0-b0 > 30)          # loose red (chroma-destroyed borders)
redS  = (r0 > 150) & (g0 < 90) & (b0 < 90)                # strict red text
darkL = (0.299*r0 + 0.587*g0 + 0.114*b0) < 120            # dark ink

def rowprof(mask, x0, x1, y0, y1, label):
    print(f'-- {label} rows y{y0}..{y1} x{x0}..{x1} --')
    for y in range(y0, y1):
        xs = np.where(mask[y, x0:x1])[0]
        if len(xs) > 0:
            print(f'  y{y}: x {xs.min()+x0}..{xs.max()+x0} n={len(xs)}')

def colprof(mask, x0, x1, y0, y1, label):
    print(f'-- {label} cols x{x0}..{x1} y{y0}..{y1} --')
    for x in range(x0, x1):
        ys = np.where(mask[y0:y1, x])[0]
        if len(ys) > 0:
            print(f'  x{x}: y {ys.min()+y0}..{ys.max()+y0} n={len(ys)}')

print('===== F1: left Channels label hunt (any ink between arrow y441 and LY box) =====')
rowprof(redL | darkL, 55, 250, 442, 466, 'any-ink')
print('  -- strict red only --')
rowprof(redS, 55, 250, 442, 466, 'red-strict')
print('  -- above arrow y412..427 --')
rowprof(redL | darkL, 55, 250, 412, 427, 'any-ink-above')
print('  -- arrow zone full detail y424..445 (red loose) --')
rowprof(redL, 55, 250, 424, 445, 'red-loose')

print('===== F2: FV arrow/label true x (orig red, x600..700, y135..370) =====')
colprof(redL, 600, 700, 135, 370, 'FV red cols')
print('  -- red rows in x630..700 --')
rowprof(redL, 630, 700, 135, 200, 'FV red rows top')

print('===== F3: box borders (orig) =====')
def hline(y, x0, x1, label):
    n = int((redL[y, x0:x1]).sum()); d = int((darkL[y, x0:x1]).sum())
    xs = np.where(redL[y, x0:x1])[0]
    ext = f'{xs.min()+x0}..{xs.max()+x0}' if len(xs) else '-'
    print(f'  {label} y{y}: redL n={n} ext {ext} | darkL n={d}')
print(' LAYER box (x62..906 y455..501):')
for y in (453,454,455,456,457,458, 499,500,501,502,503): hline(y, 100, 700, 'LY')
def vline(x, y0, y1, label):
    n = int((redL[y0:y1, x]).sum()); d = int((darkL[y0:y1, x]).sum())
    print(f'  {label} x{x}: redL n={n} | darkL n={d}')
for x in (60,61,62,63,64,65, 903,904,905,906,907): vline(x, 460, 495, 'LY-side')
print(' GN box (x259..449 y371..444) control:')
for y in (369,370,371,372,373, 442,443,444,445,446): hline(y, 262, 446, 'GN')
for x in (257,258,259,260,261, 447,448,449,450,451): vline(x, 375, 440, 'GN-side')
print(' INST box (x468..865 y363..441) control:')
for y in (361,362,363,364,365, 439,440,441,442,443): hline(y, 470, 740, 'IN')
for x in (466,467,468,469,470, 863,864,865,866,867): vline(x, 367, 436, 'IN-side')
print('  (INST right side probe avoids oval x740..882? oval overlaps x740..882 — probe far right col 903..907 too)')
for x in (880,890,900,903,905): vline(x, 367, 436, 'IN-right')

print('===== sample colors =====')
for (x, y, lbl) in [(380,175,'GN salmon top zone'), (310,175,'GN magenta top zone'),
                    (500,195,'IN top zone'), (100,230,'left front top zone'),
                    (500,456,'LY top border row'), (500,371,'GN top border row'),
                    (500,363,'IN top border row'), (350,456,'LY top border LHS'),
                    (122,450,'left-chan gap zone'), (122,447,'left-chan gap zone2')]:
    print(f'  orig({x},{y}) {lbl}: {tuple(int(v) for v in orig[y,x])}')
