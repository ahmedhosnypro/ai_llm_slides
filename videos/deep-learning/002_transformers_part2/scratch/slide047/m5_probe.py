#!/usr/bin/env python3
"""m5_probe.py — precise probes: chrome landmarks, borders, badge, container, bars."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

print('--- point probes ---')
for (x, y) in [(20,300),(35,300),(44,300),(50,300),(60,300),(80,300),(100,300),(480,20),(480,35),(480,44),(480,50),(480,55),(920,300),(925,300),(930,300),(940,300),(950,300),(958,300),(480,510),(480,515),(480,518),(300,492),(700,492)]:
    print(f'({x:3d},{y:3d}) = {tuple(A[y,x])}')

print()
print('--- red-ish (r>140, g<110, b<110) column counts, y 40..516 ---')
redm = (R > 140) & (G < 110) & (B < 110)
for x in list(range(35, 75)) + list(range(895, 950)):
    c = int(redm[40:517, x].sum())
    if c > 50: print(f'x={x}: {c}')

print()
print('--- red-ish row counts, x 40..950 ---')
for y in list(range(35, 60)) + list(range(505, 522)):
    c = int(redm[y, 40:950].sum())
    if c > 100: print(f'y={y}: {c}')

print()
print('--- badge zone: scan y 50..95, x 860..925 for yellow (r>230,g>210,b<180) and purple ring ---')
yel = (R > 225) & (G > 205) & (B < 190)
pur = (abs(R-106) < 50) & (abs(G-90) < 45) & (abs(B-205) < 55)
ys, xs = np.where(yel[50:95, 855:930])
if len(xs): print('yellow bbox in badge zone: x', xs.min()+855, xs.max()+855, 'y', ys.min()+50, ys.max()+50, 'n=', len(xs))
ys, xs = np.where(pur[45:100, 850:935])
if len(xs): print('purple bbox: x', xs.min()+850, xs.max()+850, 'y', ys.min()+45, ys.max()+45, 'n=', len(xs))
print('badge center probe (893,71):', tuple(A[71,893]), '(893,55):', tuple(A[55,893]), '(893,88):', tuple(A[88,893]), '(876,71):', tuple(A[71,876]), '(910,71):', tuple(A[71,910]))

print()
print('--- plum bar bounds ---')
plum = (R>95)&(R<170)&(G<85)&(B>60)&(B<135)
ys, xs = np.where(plum[400:480, :])
print('plum bbox: x', xs.min(), xs.max(), 'y', ys.min()+400, ys.max()+400)

print()
print('--- container fill bounds (tan/orange 200<r<250,140<g<205,80<b<150) ---')
tan = (R>195)&(R<252)&(G>135)&(G<208)&(B>70)&(B<155)
colc = tan[100:460,:].sum(axis=0)
xs = np.where(colc > 200)[0]
print('container cols:', xs.min(), xs.max())
rowc = tan[:, 200:800].sum(axis=1)
ys = np.where(rowc > 200)[0]
print('container rows:', ys.min(), ys.max())

print()
print('--- LN bars: saturated orange (r>225, 120<g<185, b<95) row counts x 180..880 ---')
lno = (R>225)&(G>115)&(G<190)&(B<100)
lr = lno[:, 180:880].sum(axis=1)
for y in range(84, 480):
    if lr[y] > 250: print(f'y={y}: {int(lr[y])}')
