#!/usr/bin/env python3
"""Slide 044 — regional disambiguation pass 2. Skeleton per 043 measure4/5 conventions."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

def bbox(mask, x0, y0, x1, y1, label):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) == 0:
        print(f'{label}: EMPTY in ({x0},{y0})..({x1},{y1})')
        return None
    print(f'{label}: x {xs.min()+x0}..{xs.max()+x0}  y {ys.min()+y0}..{ys.max()+y0}  n={len(xs)}')
    return (xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0)

red_strict = (r > 150) & (r - g > 80) & (r - b > 80)
red_loose = (r > 150) & (r - g > 30) & (r - b > 30)
blue = (b > 120) & (b - r > 40) & (b - g > 30)
navy = (b > 100) & (b - r > 20) & (b - g > 20) & (r < 120) & (g < 120)
mag = (r > 150) & (b > 150) & (g < 120) & (r - g > 60) & (b - g > 60)
sal = (r > 200) & (r - g > 50) & (g - b > 10) & (g > 70)
green = (g > 130) & (g - r > 40) & (g - b > 40)
yellowy = (r > 200) & (g > 190) & (b < 120)
bluegray = (abs(r - 112) < 40) & (abs(g - 144) < 40) & (abs(b - 175) < 45) & (b - r > 25)
dark = lum < 120

print('== CHROME borders (clean bands) ==')
# left border: below the left cube (y430..505)
colcount = red_loose[430:505, :].sum(axis=0)
print('left-border cols (y430..505, cnt>30):', [x for x in range(W) if colcount[x] > 30])
rowcount = red_loose[:, 60:890].sum(axis=1)
print('border rows cnt>400:', [y for y in range(H) if rowcount[y] > 400])
# right border rows below cubes
colc2 = red_loose[430:505, 850:960].sum(axis=0)
print('right-border cols (y430..505, x850+):', [(x+850, int(colc2[x])) for x in range(110) if colc2[x] > 20])

print('== TITLE (red text top band) ==')
bbox(red_strict, 100, 40, 850, 95, 'title red ink')
# per-column red to see word gaps (y40..95)
cols = red_strict[40:95, :].sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if cols[x] > 0 and not inrun:
        start = x; inrun = True
    elif cols[x] == 0 and inrun:
        if x - start > 2: runs.append((start, x - 1))
        inrun = False
print('title word runs:', runs[:30])

print('== HEADER (blue, x40..300) ==')
bbox(blue, 40, 60, 300, 200, 'header blue')
rows = blue[:, 40:300].sum(axis=1)
bands = []
inb = False
for y in range(H):
    if rows[y] > 2 and not inb: s0 = y; inb = True
    elif rows[y] <= 2 and inb:
        if y - s0 > 3: bands.append((s0, y - 1))
        inb = False
print('header blue row bands:', bands)

print('== NAVY top bands (cube tops) ==')
bbox(navy, 250, 70, 920, 200, 'navy band region')
print('== MAGENTA cubes ==')
bbox(mag, 0, 0, W, H, 'all magenta')
# column profile of magenta to split the three magenta-bearing cubes
mcols = mag.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if mcols[x] > 0 and not inrun: start = x; inrun = True
    elif mcols[x] == 0 and inrun:
        if x - start > 3: runs.append((start, x - 1))
        inrun = False
print('magenta col runs:', runs)
print('== SALMON (left front + GN orange part) ==')
bbox(sal, 0, 100, 320, 450, 'left salmon block')
scols = sal.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if scols[x] > 0 and not inrun: start = x; inrun = True
    elif scols[x] == 0 and inrun:
        if x - start > 2: runs.append((start, x - 1))
        inrun = False
print('salmon col runs:', runs)

print('== GREEN ==')
bbox(green, 0, 60, W, 480, 'all green')
gcols = green.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if gcols[x] > 0 and not inrun: start = x; inrun = True
    elif gcols[x] == 0 and inrun:
        if x - start > 2: runs.append((start, x - 1))
        inrun = False
print('green col runs:', runs)
print('== YELLOW (cube top rows, not badge) ==')
bbox(yellowy, 0, 60, W, 480, 'all yellowy y60..480')
print('== BLUEGRAY strips ==')
bbox(bluegray, 0, 60, W, 480, 'all bluegray')
print('== DARK (text boxes + oval) ==')
bbox(dark, 560, 430, 920, 515, 'oval dark fill')
bbox(dark, 40, 360, 930, 515, 'bottom band dark')
