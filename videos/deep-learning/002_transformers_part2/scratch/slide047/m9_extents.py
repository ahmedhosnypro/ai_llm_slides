#!/usr/bin/env python3
"""m9_extents.py — x-extents of bars, containers, text bands, rows."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def dark_extent(y, thr=200, x0=60, x1=910):
    row = A[y]
    xs = [x for x in range(x0, x1) if row[x][0] < thr or row[x][2] < thr - 30]
    if xs: print(f'y={y}: dark x {xs[0]}..{xs[-1]} n={len(xs)}')
    else: print(f'y={y}: none')

print('--- LN bar 1 (fill darker than container): rows y112..126, dark-ish r<225 ---')
for y in [110, 113, 116, 118, 120, 123, 126]:
    row = A[y]
    xs = [x for x in range(140, 900) if row[x][0] < 215 and row[x][1] < 165]
    if xs: print(f'y={y}: text x {xs[0]}..{xs[-1]} n={len(xs)}')

print('--- LN bar edges: scan y=120 vs y=134 for fill transition ---')
for y in [100, 104, 116, 130, 134, 140]:
    row = A[y]
    xs = [x for x in range(130, 905) if abs(int(row[x][0]) - 235) > 18 and abs(int(row[x][1]) - 176) > 18]
    print(f'y={y}: nonfill n={len(xs)}', (xs[0], xs[-1]) if xs else '')

print('--- LN bar 2 text ---')
for y in [320, 324, 328, 331, 334]:
    row = A[y]
    xs = [x for x in range(140, 900) if row[x][0] < 215 and row[x][1] < 165]
    if xs: print(f'y={y}: text x {xs[0]}..{xs[-1]} n={len(xs)}')

print('--- FFN header text (y214..227) ---')
for y in [214, 218, 220, 224, 227]:
    row = A[y]
    xs = [x for x in range(140, 900) if row[x][0] < 190 and row[x][2] < 120]
    if xs: print(f'y={y}: dark x {xs[0]}..{xs[-1]} n={len(xs)}')

print('--- FFN box borders: y=206 and y=264 dark extent ---')
for y in [205, 206, 264, 265]:
    row = A[y]
    xs = [x for x in range(130, 910) if row[x][0] < 190 and row[x][1] < 120]
    if xs: print(f'y={y}: border x {xs[0]}..{xs[-1]} n={len(xs)}')

print('--- dashed container 1: dash marks at y=96 and y=165 ---')
for y in [95, 96, 97, 164, 165, 166, 167]:
    row = A[y]
    xs = [x for x in range(130, 905) if row[x][0] < 210 and row[x][1] < 160]
    if xs: print(f'y={y}: dashes n={len(xs)}', xs[:8], '...', xs[-8:] if len(xs) > 8 else '')

print('--- dashed container 2: dashes at y~303?/313/377 ---')
for y in [303, 304, 312, 313, 376, 377, 378, 379]:
    row = A[y]
    xs = [x for x in range(130, 905) if row[x][0] < 210 and row[x][1] < 160]
    if xs: print(f'y={y}: dashes n={len(xs)}', xs[:8], '...', xs[-8:] if len(xs) > 8 else '')

print('--- vertical title: red text in x80..120, rows y120..515 ---')
red = (R > 120) & (G < 90) & (B < 90)
sub = red[100:520, 78:124]
ys, xs = np.where(sub)
if len(ys): print('title text bbox: x', xs.min() + 78, xs.max() + 78, 'y', ys.min() + 100, ys.max() + 100, 'n=', len(ys))

print('--- Block Output box: red border around x58..175, y44..80 ---')
sub2 = red[40:85, 50:180]
ys, xs = np.where(sub2)
if len(ys): print('BlockOutput red bbox: x', xs.min() + 50, xs.max() + 50, 'y', ys.min() + 40, ys.max() + 40, 'n=', len(ys))
print('--- Block Input box: red border y478..515, x50..180 ---')
sub3 = red[470:518, 50:180]
ys, xs = np.where(sub3)
if len(ys): print('BlockInput red bbox: x', xs.min() + 50, xs.max() + 50, 'y', ys.min() + 470, ys.max() + 470, 'n=', len(ys))

print('--- MHA bar text (white) extent: y=440..448, white px in plum bar ---')
wt = (R > 200) & (G > 170) & (B > 170)
sub4 = wt[432:455, 170:890]
ys, xs = np.where(sub4)
if len(ys): print('MHA white-text bbox: x', xs.min() + 170, xs.max() + 170, 'y', ys.min() + 432, ys.max() + 432, 'n=', len(ys))

print('--- strip rows: exact top/bottom via dark horizontal strokes at col1 x172..250 ---')
for y in range(44, 92):
    seg = A[y, 172:250]
    dk = int(((seg[:, 0] < 190) & (seg[:, 1] < 150)).sum())
    if dk > 20: print(f'top-row stroke y={y}: {dk}')
print()
for y in range(476, 520):
    seg = A[y, 172:250]
    dk = int(((seg[:, 0] < 190) & (seg[:, 1] < 150)).sum())
    if dk > 20: print(f'bottom-row stroke y={y}: {dk}')
print()
for y in range(170, 200):
    seg = A[y, 172:250]
    dk = int(((seg[:, 0] < 190) & (seg[:, 1] < 150)).sum())
    if dk > 20: print(f'rowA stroke y={y}: {dk}')
print()
for y in range(280, 300):
    seg = A[y, 172:250]
    dk = int(((seg[:, 0] < 190) & (seg[:, 1] < 150)).sum())
    if dk > 20: print(f'rowB stroke y={y}: {dk}')
print()
for y in range(382, 402):
    seg = A[y, 172:250]
    dk = int(((seg[:, 0] < 190) & (seg[:, 1] < 150)).sum())
    if dk > 20: print(f'rowC stroke y={y}: {dk}')
