#!/usr/bin/env python3
"""Slide 043 — precise: true-red vs orange, callout box, seams, green box, text bands."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

true_red = (r > 140) & (r - g > 60) & (r - b > 60) & (g < b + 35)   # red text/arrows only
orange   = (r > 180) & (r - g > 60) & (g > b + 40)
magenta  = (r > 150) & (b > 150) & (g < 80)
blue     = (b > 120) & (b - r > 60) & (b - g > 40)                   # blue text
green_t  = (g > 100) & (g - r > 40) & (g - b > 40)                   # green border/text
cream    = (r > 245) & (g > 245) & (b > 200) & (b < 248)
white    = (r > 245) & (g > 245) & (b > 248)
black    = lum < 90

def bbox(mask, y0, y1, x0, x1, label, minpx=6):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) < minpx:
        print(f'{label}: NONE'); return None
    print(f'{label}: x {xs.min()+x0}..{xs.max()+x0}  y {ys.min()+y0}..{ys.max()+y0}  n={len(xs)}')
    return (xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0)

print('=== CALLOUT BOX ===')
bbox(cream, 100, 400, 250, 700, 'cream fill')
# red border: true_red rows/cols with long runs in callout window
for y in range(110, 370):
    xs = np.where(true_red[y, 300:680])[0]
    if len(xs) > 250: print(f'  true_red row y{y}: x {xs.min()+300}..{xs.max()+300} n={len(xs)}')
for x in range(300, 680):
    ys2 = np.where(true_red[110:370, x])[0]
    if len(ys2) > 100: print(f'  true_red col x{x}: y {ys2.min()+110}..{ys2.max()+110} n={len(ys2)}')

print('=== SEAM SCANS (pixel rows through front-band mids) ===')
print('left y=200:', [tuple(a[200, x]) for x in range(112, 208, 4)])
print('right y=178:', [tuple(a[178, x]) for x in range(666, 804, 4)])

print('=== STACK TOP BANDS (above magenta) + right receding slices ===')
bbox(orange, 100, 190, 100, 340, 'left orange (top bands + right face)')
for name, m in [('navyish', (r < 90) & (b < 130) & (lum < 90)),
                ('yellow', (r > 200) & (g > 200) & (b < 120)),
                ('green_c', (g > 130) & (g - r > 30) & (g - b > 30))]:
    bbox(m, 100, 195, 60, 350, f'left top {name}')

print('=== right stack slices (x 800..920, y 100..350) ===')
for name, m in [('orange', orange), ('magenta', magenta),
                ('lightblue', (b > 150) & (b - r > 30) & (g > 120)),
                ('navyish', (r < 90) & (b < 130) & (lum < 90)),
                ('green_c', (g > 130) & (g - r > 30) & (g - b > 30)),
                ('yellow', (r > 200) & (g > 200) & (b < 120))]:
    bbox(m, 100, 350, 795, 940, f'right slice {name}')

print('=== RED ARROWS + LABELS (true_red, right diagram zone) ===')
bbox(true_red, 100, 360, 590, 950, 'all true_red right zone')
# per-row to separate elements
prev = None
for y in range(150, 360):
    xs = np.where(true_red[y, 590:950])[0]
    if len(xs) > 2:
        rng = (xs.min()+590, xs.max()+590)
        if prev is None or y - prev > 3:
            print(f'  y{y}: x {rng[0]}..{rng[1]} n={len(xs)}')
        prev = y

print('=== GREEN BOTTOM BOX ===')
for y in range(340, 520):
    xs = np.where(green_t[y, 40:920])[0]
    if len(xs) > 300: print(f'  green row y{y}: x {xs.min()+40}..{xs.max()+40} n={len(xs)}')
for x in range(40, 920):
    ys2 = np.where(green_t[340:520, x])[0]
    if len(ys2) > 60: print(f'  green col x{x}: y {ys2.min()+340}..{ys2.max()+340} n={len(ys2)}')

print('=== BOTTOM BOX TEXT BANDS (y 400..500) ===')
for y in range(400, 500):
    xsb = np.where(blue[y, 60:900])[0]
    xsr = np.where(true_red[y, 60:900])[0]
    xsk = np.where(black[y, 60:900])[0]
    msg = []
    if len(xsb) > 3: msg.append(f'BLUE x{xsb.min()+60}..{xsb.max()+60} n={len(xsb)}')
    if len(xsr) > 3: msg.append(f'RED x{xsr.min()+60}..{xsr.max()+60} n={len(xsr)}')
    if len(xsk) > 3: msg.append(f'BLACK x{xsk.min()+60}..{xsk.max()+60} n={len(xsk)}')
    if msg: print(f'  y{y}: ' + ' | '.join(msg))
