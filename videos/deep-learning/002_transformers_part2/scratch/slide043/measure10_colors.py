#!/usr/bin/env python3
"""Slide 043 — final samples: bright-quartile colors, pencil icon, green line, navy top."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def bright_quartile(y0, y1, x0, x1, ch, label):
    reg = a[y0:y1, x0:x1]
    flat = reg.reshape(-1, 3)
    idx = np.argsort(flat[:, ch])[int(len(flat) * 0.97)]
    print(f'{label}: bright-q({ch}) = {tuple(flat[idx])}, mean-top5% = {tuple(flat[np.argsort(flat[:, ch])[-max(1,len(flat)//20):]].mean(axis=0).astype(int))}')

print('--- bright quartiles ---')
bright_quartile(198, 222, 800, 817, 1, 'right green')
bright_quartile(198, 222, 819, 834, 0, 'right orange')
bright_quartile(198, 222, 836, 851, 0, 'right yellow')
bright_quartile(198, 222, 853, 870, 2, 'right lblue')
bright_quartile(110, 125, 740, 850, 2, 'right navy top')
bright_quartile(126, 140, 836, 852, 0, 'right yellow top y126')
bright_quartile(120, 130, 265, 315, 0, 'left orange top')
bright_quartile(200, 330, 246, 316, 0, 'left orange main')
bright_quartile(200, 330, 204, 245, 0, 'left red band')
bright_quartile(196, 336, 114, 203, 0, 'left magenta front')
bright_quartile(170, 310, 668, 798, 0, 'right magenta front')
bright_quartile(160, 176, 128, 212, 1, 'left green band')
bright_quartile(124, 139, 190, 235, 0, 'left yellow band')
bright_quartile(105, 121, 187, 278, 2, 'left navy band')
bright_quartile(368, 380, 84, 807, 2, 'bottom L1 blue')
bright_quartile(180, 192, 342, 523, 0, 'callout L1 red')
bright_quartile(243, 254, 396, 576, 1, 'callout L4 green')

print('--- pencil icon zone: dark pixels x332..420, y230..267 ---')
lum = (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])
for y in range(230, 268, 2):
    xs = np.where(lum[y, 332:420] < 150)[0]
    if len(xs): print(f'  y{y}: x {[(x+332) for x in xs[:12]]}{"..." if len(xs) > 12 else ""} n={len(xs)}')

print('--- green line L4 precise (g>90, g-r>25, g-b>25) ---')
mG = (a[:, :, 1] > 90) & (a[:, :, 1] - a[:, :, 0] > 25) & (a[:, :, 1] - a[:, :, 2] > 25)
for y in range(238, 268):
    xs = np.where(mG[y, 380:600])[0]
    if len(xs) > 2: print(f'  y{y}: x {xs.min()+380}..{xs.max()+380} n={len(xs)}')

print('--- L3 blue precise ---')
mB = (a[:, :, 2] > 120) & (a[:, :, 2] - a[:, :, 0] > 60) & (a[:, :, 2] - a[:, :, 1] > 40)
for y in range(220, 240):
    xs = np.where(mB[y, 340:620])[0]
    if len(xs) > 2: print(f'  y{y}: x {xs.min()+340}..{xs.max()+340} n={len(xs)}')

print('--- right stack top: navy vs olive rows (samples) ---')
for y in (94, 98, 103, 108, 116, 122, 128, 134, 142, 150, 158, 163):
    print(f'  y{y}:', [tuple(a[y, x]) for x in (750, 790, 820)])

print('--- left stack above front (x140..200) ---')
for y in (140, 150, 160, 170, 178, 184):
    print(f'  y{y}:', [tuple(a[y, x]) for x in (130, 150, 170, 190, 200)])
