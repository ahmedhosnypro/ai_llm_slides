#!/usr/bin/env python3
"""m13_last.py — title metrics, box texts, MHA bar extent, unit borders, dash extent."""
from PIL import Image
import numpy as np

F47 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F47).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
SY = 0.955556

print('== 1. vertical title: horizontal slices through letter bands ==')
for y in (180, 315, 390, 130):
    row = A[y]
    m = (row[:, 0] > 90) & (row[:, 0] - row[:, 1] > 35) & (row[:, 0] - row[:, 2] > 30) & (row[:, 1] < 130)
    xs = [x for x in range(50, 200) if m[x]]
    print(f'  y={y}: red x {min(xs) if xs else "-"}..{max(xs) if xs else "-"} n={len(xs)} sample={tuple(row[xs[len(xs)//2]]) if xs else "-"}')

print('== 2. Block Output box: white-fill bbox + border ==')
# white fill inside box: rows 58..88, x 60..190
wm = (R > 235) & (G > 225) & (B > 215)
sub = wm[55:95, 55:195]
ys, xs = np.where(sub)
print('  white bbox: x', 55 + xs.min(), 55 + xs.max(), 'y', 55 + ys.min(), 55 + ys.max())
# text ink (dark red) inside
tm = (R > 110) & (R - G > 40) & (R - B > 40)
sub = tm[55:95, 55:195]
ys, xs = np.where(sub)
print('  text ink bbox: x', 55 + xs.min(), 55 + xs.max(), 'y', 55 + ys.min(), 55 + ys.max())

print('== 3. Block Input box: same, rows 478..518 ==')
sub = wm[478:518, 55:195]
ys, xs = np.where(sub)
print('  white bbox: x', 55 + xs.min(), 55 + xs.max(), 'y', 478 + ys.min(), 478 + ys.max())
sub = tm[478:518, 55:195]
ys, xs = np.where(sub)
print('  text ink bbox: x', 55 + xs.min(), 55 + xs.max(), 'y', 478 + ys.min(), 478 + ys.max())

print('== 4. MHA bar x extent at y=430 ==')
plum = (R > 100) & (R < 165) & (G < 95) & (B > 55) & (B < 135)
xs = [x for x in range(100, 940) if plum[430, x]]
print('  plum x:', min(xs), '..', max(xs), 'n=', len(xs))
xs = [x for x in range(100, 940) if plum[460, x]]
print('  plum y=460 x:', min(xs), '..', max(xs), 'n=', len(xs))

print('== 5. unit vertical borders: orange-line cols in rows 233..254 (r-b>60, r>190, g<200) ==')
bor = ((R[233:254] > 190) & (G[233:254] < 200) & (R[233:254] - B[233:254] > 60) &
       (R[233:254] - G[233:254] > 25)).sum(axis=0)
cand = [x for x in range(130, 900) if bor[x] >= 10]
groups = []
for x in cand:
    if groups and x - groups[-1][1] <= 2: groups[-1][1] = x
    else: groups.append([x, x])
print('  border cols:', groups)

print('== 6. dash row x extent at y=96 (olive mask), excluding container border cols ==')
olive = (R[96] > 150) & (R[96] < 230) & (G[96] > 110) & (G[96] < 200) & (B[96] < 110) & (G[96] - B[96] > 40)
xs = [x for x in range(132, 893) if olive[x]]
print('  dash x:', min(xs), '..', max(xs), 'n=', len(xs), 'coverage', len(xs) / (893 - 132))

print('== 7. internal cells: border color at row edges (y=173/189, x=200..210) ==')
print('  y=173:', [tuple(A[173, x]) for x in range(196, 214, 3)])
print('  y=189:', [tuple(A[189, x]) for x in range(196, 214, 3)])
print('  y=230:', [tuple(A[230, x]) for x in range(196, 214, 3)])
print('  y=257:', [tuple(A[257, x]) for x in range(196, 214, 3)])

print('== 8. RELU label ink in unit 1 (rows 232..256, x 200..245): red-orange text ==')
tm2 = (R[232:256, 200:248] > 150) & (G[232:256, 200:248] < 140) & (B[232:256, 200:248] < 120)
ys, xs = np.where(tm2)
if len(ys):
    print('  RELU-ish ink bbox: x', 200 + xs.min(), 200 + xs.max(), 'y', 232 + ys.min(), 232 + ys.max(), 'n=', len(ys))

print('== 9. magenta dots: b-channel-high blobs in unit 1 rows 240..256 ==')
mm = (R[240:257, 165:245] > 180) & (B[240:257, 165:245] > 110) & (B[240:257, 165:245] > G[240:257, 165:245])
ys, xs = np.where(mm)
if len(ys):
    pts = sorted(set(zip((xs + 165).tolist(), (ys + 240).tolist())))
    xsu = sorted(set(p[0] for p in pts))
    print('  magenta x positions:', xsu, 'y range', min(p[1] for p in pts), max(p[1] for p in pts))

print('== 10. green dot y positions in unit 1 ==')
gm = (G[228:246, 165:245] > 120) & (G[228:246, 165:245] > R[228:246, 165:245]) & (B[228:246, 165:245] < 160)
ys, xs = np.where(gm)
if len(ys):
    print('  green y range:', 228 + ys.min(), 228 + ys.max(), 'x:', sorted(set((xs + 165).tolist())))
