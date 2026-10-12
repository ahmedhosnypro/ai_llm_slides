#!/usr/bin/env python3
"""Slide 043 — bottom-box full text scan, line-3 tail colors, callout border/fill map."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

true_red = (r > 140) & (r - g > 60) & (r - b > 60) & (g < b + 35)
blue     = (b > 120) & (b - r > 60) & (b - g > 40)
black    = (lum < 80) & ~blue & ~true_red

print('=== BOTTOM BOX TEXT full scan y360..500 ===')
for y in range(360, 500):
    xsb = np.where(blue[y, 60:900])[0]
    xsr = np.where(true_red[y, 60:900])[0]
    xsk = np.where(black[y, 60:900])[0]
    msg = []
    if len(xsb) > 3: msg.append(f'BLUE x{xsb.min()+60}..{xsb.max()+60} n={len(xsb)}')
    if len(xsr) > 3: msg.append(f'RED x{xsr.min()+60}..{xsr.max()+60} n={len(xsr)}')
    if len(xsk) > 3: msg.append(f'BLK x{xsk.min()+60}..{xsk.max()+60} n={len(xsk)}')
    if msg: print(f'  y{y}: ' + ' | '.join(msg))

print('=== line-3 tail pixel samples (x715..835, y476..490) ===')
for y in (478, 481, 484):
    print(f'y{y}:', [tuple(a[y, x]) for x in range(716, 836, 8)])

print('=== line-1 start samples (x84..140, y392..406) ===')
for y in (394, 397, 400):
    print(f'y{y}:', [tuple(a[y, x]) for x in range(84, 145, 6)])

print('=== CALLOUT BORDER scan (true_red, thin, x300..680 y150..350) ===')
for y in range(150, 350):
    xs = np.where(true_red[y, 300:680])[0]
    if len(xs) > 100: print(f'  row y{y}: x {xs.min()+300}..{xs.max()+300} n={len(xs)}')
for x in range(300, 680):
    ys2 = np.where(true_red[150:350, x])[0]
    if len(ys2) > 60: print(f'  col x{x}: y {ys2.min()+150}..{ys2.max()+150} n={len(ys2)}')

print('=== CALLOUT FILL MAP (samples every 20px, x330..620 y180..320) ===')
for y in range(180, 321, 20):
    row = []
    for x in range(330, 621, 20):
        px = a[y, x]
        row.append('C' if (px[0] > 245 and px[1] > 245 and 200 < px[2] < 248) else
                   ('W' if (px[0] > 245 and px[1] > 245 and px[2] > 248) else
                    ('G' if px[1] > px[0] and px[1] > px[2] else
                     ('K' if lum[y, x] < 100 else '.'))))
    print(f'y{y}: {"".join(row)}')

print('=== CALLOUT TEXT BANDS (inside x330..640, y175..325) ===')
for y in range(175, 326):
    xsr = np.where(true_red[y, 330:640])[0]
    xsb = np.where(blue[y, 330:640])[0]
    xsk = np.where(black[y, 330:640])[0]
    grn = (g > 100) & (g - r > 30) & (g - b > 30)
    xsg = np.where(grn[y, 330:640])[0]
    msg = []
    if len(xsr) > 3: msg.append(f'RED x{xsr.min()+330}..{xsr.max()+330} n={len(xsr)}')
    if len(xsb) > 3: msg.append(f'BLUE x{xsb.min()+330}..{xsb.max()+330} n={len(xsb)}')
    if len(xsk) > 3: msg.append(f'BLK x{xsk.min()+330}..{xsk.max()+330} n={len(xsk)}')
    if len(xsg) > 3: msg.append(f'GRN x{xsg.min()+330}..{xsg.max()+330} n={len(xsg)}')
    if msg: print(f'  y{y}: ' + ' | '.join(msg))
