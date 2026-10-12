#!/usr/bin/env python3
"""Slide 044 — chrome landmark fit + first-pass ink census (P3 pattern member #3).
Skeleton per scratch/slide043/measure1_chrome.py (certified pattern)."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red_loose = (r > 150) & (r - g > 30) & (r - b > 30)
colcount = red_loose[100:400, :].sum(axis=0)
cands = [x for x in range(W) if colcount[x] > 200]
print('border col candidates:', cands)
rowcount = red_loose[:, 150:850].sum(axis=1)
rcands = [y for y in range(H) if rowcount[y] > 400]
print('border row candidates:', rcands)

yellow = (r > 200) & (g > 200) & (b > 100) & (b < 200)
ys, xs = np.where(yellow[30:130, 820:960])
if len(xs):
    print('badge yellow bbox x', xs.min() + 820, xs.max() + 820, 'y', ys.min() + 30, ys.max() + 30,
          'center', (xs.min() + xs.max()) / 2 + 820, (ys.min() + ys.max()) / 2 + 30)
purple = (abs(r - 106) < 45) & (abs(g - 90) < 45) & (abs(b - 205) < 55) & (b - r > 40)
ys, xs = np.where(purple[30:130, 820:960])
if len(xs):
    print('badge purple ring bbox x', xs.min() + 820, xs.max() + 820, 'y', ys.min() + 30, ys.max() + 30)

red_text = (r > 150) & (r - g > 80) & (r - b > 80)
ys, xs = np.where(red_text[50:135, 100:850])
if len(xs):
    print('title ink bbox x', xs.min() + 100, xs.max() + 100, 'y', ys.min() + 50, ys.max() + 50,
          'cx', (xs.min() + xs.max()) / 2 + 100)

lum = 0.299 * r + 0.587 * g + 0.114 * b
dark = lum < 120
print('--- dark ink row profile (x 60..900) ---')
for y0 in range(0, 540, 20):
    print(f'y{y0:3d}..{y0+20:3d} dark_px={dark[y0:y0+20, 60:900].sum()}')

# blue ink census (header + blue emphasis)
blue = (b > 120) & (b - r > 40) & (b - g > 30)
print('--- blue ink row profile (x 40..900) ---')
for y0 in range(0, 540, 15):
    print(f'y{y0:3d}..{y0+15:3d} blue_px={blue[y0:y0+15, 40:900].sum()}')
# header blue bbox (top-left quadrant)
ys, xs = np.where(blue[80:180, 30:350])
if len(xs):
    print('header blue bbox x', xs.min() + 30, xs.max() + 30, 'y', ys.min() + 80, ys.max() + 80)

# magenta cubes
mag = (r > 150) & (b > 150) & (g < 120) & (r - g > 60) & (b - g > 60)
print('--- magenta row profile ---')
for y0 in range(0, 540, 15):
    print(f'y{y0:3d}..{y0+15:3d} mag_px={mag[y0:y0+15, :].sum()}')

# salmon/coral (left cube front)
sal = (r > 200) & (r - g > 50) & (g - b > 10) & (g > 70)
print('--- salmon row profile ---')
for y0 in range(0, 540, 15):
    print(f'y{y0:3d}..{y0+15:3d} sal_px={sal[y0:y0+15, :].sum()}')

# strict red (arrows/titles)
red_strict = (r > 150) & (r - g > 80) & (r - b > 80)
print('--- strict red row profile ---')
for y0 in range(0, 540, 15):
    print(f'y{y0:3d}..{y0+15:3d} red_px={red_strict[y0:y0+15, :].sum()}')

# black filled oval (Transformer choice): black fill with yellow text inside
blackfill = lum < 60
print('--- very dark fill row profile (x 600..900) ---')
for y0 in range(380, 540, 10):
    print(f'y{y0:3d}..{y0+10:3d} darkfill_px={blackfill[y0:y0+10, 600:900].sum()}')
