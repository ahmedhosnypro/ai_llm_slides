#!/usr/bin/env python3
"""m11_final_geom.py — final geometry: bars, dashed containers, FFN, strips, curves."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def runs(m, min_len=1):
    out=[];i=0;n=len(m)
    while i<n:
        if m[i]:
            j=i
            while j<n and m[j]: j+=1
            if j-i>=min_len: out.append((i,j-1))
            i=j
        else: i+=1
    return out

# LN bar 1 top/bottom edge x-extent (dark orange horizontal lines)
for y in [101, 102, 103, 128, 129, 130]:
    row = A[y]
    m = (row[:,0] < 215) & (row[:,1] < 170) & (row[:,2] < 110)
    rr = runs(m, 30)
    print(f'bar1 edge y={y}:', rr)
for y in [312, 313, 314, 339, 340, 341]:
    row = A[y]
    m = (row[:,0] < 215) & (row[:,1] < 170) & (row[:,2] < 110)
    rr = runs(m, 30)
    print(f'bar2 edge y={y}:', rr)

# dashed container left/right verticals: dash pixels in x150..175 / x865..905 over y96..166 and y303..379
for (y0, y1, name) in [(96, 167, 'cont1'), (303, 380, 'cont2')]:
    for x0, x1, side in [(148, 178, 'left'), (862, 905, 'right')]:
        m = ((R[y0:y1, x0:x1] < 215) & (G[y0:y1, x0:x1] < 175) & (B[y0:y1, x0:x1] < 120)).sum(axis=0)
        xs = [x0 + i for i, c in enumerate(m) if c > 8]
        print(f'{name} {side}: dash columns {xs}')

# FFN box left/right verticals: dark px columns over y208..262
m = ((R[208:263, :] < 190) & (G[208:263, :] < 130)).sum(axis=0)
xs = [x for x in range(140, 910) if m[x] > 30]
print('FFN box verticals:', runs(np.array([1 if x in xs else 0 for x in range(910)]), 1)[:6], '...')
left = [x for x in xs if x < 250]; right = [x for x in xs if x > 820]
print('FFN left candidates:', left[:10], 'right:', right[:10])

# strip vertical strokes in top row: y60..72, dark-ish columns
m = ((R[58:74, :] < 205) & (G[58:74, :] < 175)).sum(axis=0)
xs = [x for x in range(160, 910) if m[x] >= 4]
print('top-row vertical strokes:', runs(np.array([1 if x in xs else 0 for x in range(910)]), 1))

# block-arrow zones: pale (white-washed) columns per zone
pale = (R > 228) & (G > 195) & (B > 165)
for (y0, y1, name) in [(192, 205, 'upIntoPostFFN'), (266, 280, 'upIntoFFN'), (402, 418, 'zone1'), (468, 480, 'zone2')]:
    cnt = pale[y0:y1, 150:900].sum(axis=0)
    xs = [150 + i for i, c in enumerate(cnt) if c >= 6]
    rr = runs(np.array([1 if x in xs else 0 for x in range(910)]), 1)
    rr = [(a, b) for a, b in rr if b - a >= 3]
    print(f'{name} y{y0}-{y1}: pale col clusters:', rr)

# red output arrows: y76..101 at col centers (already known); verify arrow tops
redm = (R > 140) & (G < 100) & (B < 100)
for y in [77, 82, 88, 94, 100]:
    row = redm[y]
    rr = [r for r in runs(row, 1) if 150 < r[0] < 900]
    print(f'red arrows y={y}:', rr)
