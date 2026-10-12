#!/usr/bin/env python3
"""Slide 043 — disambiguated census: red TEXT vs orange cubes, cream callout,
magenta fronts, green box, bottom text bands."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# 042 disambiguation masks
red_text = (r > 150) & (r - g > 60) & (r - b > 60) & (g < b + 35)   # red TEXT only
orange   = (r > 200) & (r - g > 60) & (g > b + 40)                   # FF7F00 faces
magenta  = (r > 150) & (b > 150) & (g < 80)                          # CC00CC fronts
cream    = (r > 235) & (g > 235) & (b > 190) & (b < 235)             # FFFDE0 callout fill

def bbox(mask, y0, y1, x0, x1, label, minpx=6):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) < minpx:
        print(f'{label}: NONE in window')
        return None
    bx0, bx1 = xs.min() + x0, xs.max() + x0
    by0, by1 = ys.min() + y0, ys.max() + y0
    print(f'{label}: x {bx0}..{bx1}  y {by0}..{by1}  (w {bx1-bx0}, h {by1-by0}, n={len(xs)})')
    return (bx0, by0, bx1, by1)

print('=== TITLE (red text, y 40..100) ===')
t = bbox(red_text, 40, 100, 100, 900, 'title')

print('=== CREAM CALLOUT (y 100..400) ===')
c = bbox(cream, 100, 400, 250, 700, 'cream fill')

print('=== MAGENTA (fronts, y 100..450) ===')
bbox(magenta, 100, 450, 60, 460, 'left-stack magenta')
bbox(magenta, 100, 450, 600, 920, 'right-stack magenta')

print('=== ORANGE (y 100..450) ===')
bbox(orange, 100, 450, 60, 460, 'left-stack orange')
bbox(orange, 100, 450, 600, 920, 'right-stack orange')

print('=== red text below title (y 100..470) — per-element probe ===')
bbox(red_text, 100, 470, 250, 700, 'red text in callout window')
bbox(red_text, 100, 470, 600, 940, 'red text/arrows right window')
bbox(red_text, 100, 470, 60, 300, 'red text left window')

# bottom box: green border (00AA00-ish: g high, r,b low)
green_border = (g > 120) & (g - r > 40) & (g - b > 40)
print('=== GREEN (border of bottom box + green text) ===')
ys, xs = np.where(green_border[380:540, 40:920])
if len(xs):
    print(f'green all: x {xs.min()+40}..{xs.max()+40}  y {ys.min()+380}..{ys.max()+380} n={len(xs)}')
# per-row green to find border lines vs text
for y in range(380, 540):
    xs = np.where(green_border[y, 40:920])[0]
    if len(xs) > 200:
        print(f'  green row y{y}: x {xs.min()+40}..{xs.max()+40} n={len(xs)}')
