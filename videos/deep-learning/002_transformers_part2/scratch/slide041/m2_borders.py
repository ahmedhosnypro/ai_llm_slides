#!/usr/bin/env python3
"""m2_borders.py — precise sub-profiles of the four chrome border lines + fit."""
from PIL import Image
import numpy as np

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
# reddish-ness: R strongly exceeds G and B (border C00000 over white/gray)
reddish = (R - G > 55) & (R - B > 55)

# top border: scan rows 30..60 for reddish count across x 100..850 (avoid badge/title)
for y in range(30, 61):
    c = reddish[y, 100:850].sum()
    if c > 20:
        print('top-border row cand y=%d count=%d mean=(%d,%d,%d)' % (
            y, c, R[y, 100:850][reddish[y, 100:850]].mean(),
            G[y, 100:850][reddish[y, 100:850]].mean(),
            B[y, 100:850][reddish[y, 100:850]].mean()))

# bottom border: rows 505..519
print('--- bottom')
for y in range(505, 520):
    c = reddish[y, 100:850].sum()
    print('y=%d reddish=%d' % (y, c))

# left border: columns 52..66, count over y 60..500
print('--- left')
for x in range(52, 67):
    c = reddish[60:500, x].sum()
    if c > 50:
        print('x=%d count=%d' % (x, c))

# right border: columns 895..908
print('--- right')
for x in range(895, 909):
    c = reddish[60:500, x].sum()
    if c > 50:
        print('x=%d count=%d' % (x, c))

# subpixel centers: weighted mean of reddish-ness over the 3 strongest columns/rows
def wcenter(profile_lo, profile_hi, axis_vals, weights):
    pass

# left subpixel
cols = {}
for x in range(54, 64):
    cols[x] = reddish[60:500, x].sum()
print('left col counts:', {k: int(v) for k, v in cols.items()})
# right subpixel
cols = {}
for x in range(896, 906):
    cols[x] = reddish[60:500, x].sum()
print('right col counts:', {k: int(v) for k, v in cols.items()})
# top subpixel
rows = {}
for y in range(38, 48):
    rows[y] = reddish[y, 100:850].sum()
print('top row counts:', {k: int(v) for k, v in rows.items()})
# bottom subpixel
rows = {}
for y in range(512, 519):
    rows[y] = reddish[y, 100:850].sum()
print('bottom row counts:', {k: int(v) for k, v in rows.items()})

# panel interior background sample (should be E9E9E7 -> frame-mapped)
print('bg sample at (200,400):', im[400, 200], ' (500,750):', im[300, 750], ' outside panel (20,20):', im[20, 20])
print('canvas below-left of panel (20,300):', im[300, 20])
print('letterbox sample (530,480):', im[530, 480])
