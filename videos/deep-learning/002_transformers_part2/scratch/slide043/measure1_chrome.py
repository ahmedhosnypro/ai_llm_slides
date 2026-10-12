#!/usr/bin/env python3
"""Slide 043 — chrome landmark fit + first-pass ink census (P3 pattern member).
Pattern refit per frame per qa/slide042/worker_report.md convention #1."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# --- red border mask (LOOSE, chroma-proof per 042 lesson: r>150, r-g>30)
red_loose = (r > 150) & (r - g > 30) & (r - b > 30)

# vertical border columns: count red in each column within y 100..400 (clear band)
colcount = red_loose[100:400, :].sum(axis=0)
cands = [x for x in range(W) if colcount[x] > 200]
print('border col candidates:', cands)

# horizontal border rows: count red in each row within x 150..850
rowcount = red_loose[:, 150:850].sum(axis=1)
rcands = [y for y in range(H) if rowcount[y] > 400]
print('border row candidates:', rcands)

# --- badge: yellow fill FDFD96 loose mask (high r,g, low-ish b)
yellow = (r > 200) & (g > 200) & (b > 100) & (b < 200)
ys, xs = np.where(yellow[30:130, 820:960])
if len(xs):
    print('badge yellow bbox x', xs.min() + 820, xs.max() + 820, 'y', ys.min() + 30, ys.max() + 30,
          'center', (xs.min() + xs.max()) / 2 + 820, (ys.min() + ys.max()) / 2 + 30)

# --- purple ring 6A5ACD
purple = (abs(r - 106) < 45) & (abs(g - 90) < 45) & (abs(b - 205) < 55) & (b - r > 40)
ys, xs = np.where(purple[30:130, 820:960])
if len(xs):
    print('badge purple ring bbox x', xs.min() + 820, xs.max() + 820, 'y', ys.min() + 30, ys.max() + 30,
          'center', (xs.min() + xs.max()) / 2 + 820, (ys.min() + ys.max()) / 2 + 30)

# --- title: red text in top band y 60..130, x 100..850 (strict red text mask)
red_text = (r > 150) & (r - g > 80) & (r - b > 80)
ys, xs = np.where(red_text[60:130, 100:850])
if len(xs):
    print('title ink bbox x', xs.min() + 100, xs.max() + 100, 'y', ys.min() + 60, ys.max() + 60,
          'cx', (xs.min() + xs.max()) / 2 + 100)

# --- global luminance-dip map of dark ink to find major blocks
lum = 0.299 * r + 0.587 * g + 0.114 * b
dark = lum < 120
print('--- dark ink row profile (x 60..900) ---')
for y0 in range(0, 540, 20):
    row = dark[y0:y0 + 20, 60:900].sum()
    print(f'y{y0:3d}..{y0+20:3d} dark_px={row}')
