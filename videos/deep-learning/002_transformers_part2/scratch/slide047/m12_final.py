#!/usr/bin/env python3
"""m12_final.py — remaining details: label/dot colors, boxes, header, house arrows."""
from PIL import Image
import numpy as np
from collections import Counter

F47 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
F46 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg'
A = np.asarray(Image.open(F47).convert('RGB')).astype(int)
A46 = np.asarray(Image.open(F46).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]

print('== 1. internal row label glyph colors (darkest px in label bands) ==')
for y0, y1, lab in ((174, 191, 'post-FFN label'), (280, 296, 'post-LN label'), (385, 401, 'out-attn label'), (61, 77, 'output label'), (493, 510, 'X label')):
    reg = A[y0:y1, 190:225].reshape(-1, 3)
    dk = reg[reg.sum(axis=1).argsort()[:14]]
    print(f'{lab}: darkest14 mean={dk.mean(axis=0).round(0)} min={dk.min(axis=0)}')

print('== 2. dot colors: output(blue), internal(purple?), X(green) at dot x=628/647 ==')
for cx in (628, 647):
    for cy, lab in ((67, 'out row'), (181, 'post-FFN'), (289, 'post-LN'), (391, 'out-attn'), (501, 'X row')):
        reg = A[cy - 4:cy + 4, cx - 3:cx + 4].reshape(-1, 3)
        dk = reg[reg.sum(axis=1).argsort()[:8]]
        print(f'  dot({cx},{cy}) {lab}: darkest8 mean={dk.mean(axis=0).round(0)}')

print('== 2b. frame_046 dot colors at same slide positions for comparison ==')
# 046 rows: final 67.3..84.8 center 76.05 -> frame 72.7; dots x slide 634.6 -> frame 628.2
for cy46, lab in ((73, '046 final row dot'), (286, '046 post-LN dot'), (500, '046 X dot')):
    reg = A46[cy46 - 4:cy46 + 4, 625:632].reshape(-1, 3)
    dk = reg[reg.sum(axis=1).argsort()[:8]]
    print(f'  {lab}: darkest8 mean={dk.mean(axis=0).round(0)}')

print('== 3. Block Output box: border rect via red-row/col run scan x60..190 y50..95 ==')
red = (R > 130) & (G < 100) & (B < 100)
for y in range(50, 96):
    xs = [x for x in range(55, 195) if red[y, x]]
    if len(xs) > 40:
        print(f'  long red row y={y}: {min(xs)}..{max(xs)} n={len(xs)}')
for x in range(55, 195):
    ys = [y for y in range(50, 96) if red[y, x]]
    if len(ys) > 12:
        print(f'  long red col x={x}: {min(ys)}..{max(ys)} n={len(ys)}')

print('== 4. Block Input box: same y480..518 ==')
for y in range(480, 519):
    xs = [x for x in range(55, 195) if red[y, x]]
    if len(xs) > 40:
        print(f'  long red row y={y}: {min(xs)}..{max(xs)} n={len(xs)}')
for x in range(55, 195):
    ys = [y for y in range(480, 518) if red[y, x]]
    if len(ys) > 10:
        print(f'  long red col x={x}: {min(ys)}..{max(ys)} n={len(ys)}')

print('== 5. FFN header: dark-ink column clusters (rows 211..224) ==')
dm = (A[211:224, 140:890].sum(axis=2) < 500)
cols = dm.sum(axis=0)
xs = [140 + i for i, n in enumerate(cols) if n > 0]
groups = []
for x in xs:
    if groups and x - groups[-1][1] <= 6: groups[-1][1] = x
    else: groups.append([x, x])
print('ink word clusters:', groups)

print('== 6. house arrow (FFN gap up) at col3 x=345..360, y=188..207: full profile ==')
for y in range(186, 208):
    print(f'  y={y}:', [tuple(A[y, x]) for x in (348, 351, 354, 357)])

print('== 7. zone1 house arrow col3 x=345..360 y=400..419 ==')
for y in range(400, 420):
    print(f'  y={y}:', [tuple(A[y, x]) for x in (348, 351, 354, 357)])

print('== 8. LN bar left/right edge x (top bar y=115, bottom y=325): first/last non-tan ==')
for y in (115, 325):
    row = A[y]
    xs = [x for x in range(125, 900) if abs(row[x][0] - 237) > 18 or abs(row[x][1] - 176) > 22 or abs(row[x][2] - 121) > 26]
    print(f'  y={y}: non-tan x {min(xs)}..{max(xs)} n={len(xs)} first-last details {tuple(row[min(xs)])} {tuple(row[max(xs)])}')

print('== 9. FFN box side borders? cols with dark px across rows 208..262 ==')
dm2 = (A[208:263, :].sum(axis=2) < 480)
colcnt = dm2.sum(axis=0)
edge = [x for x in range(120, 905) if colcnt[x] > 25]
print('tall dark cols:', edge)

print('== 10. vertical title: better mask bands ==')
tm = (R > 90) & (R - G > 35) & (R - B > 30) & (G < 130)
sub = tm[95:515, 70:150]
rowcnt = sub.sum(axis=1)
bands = []
inb = False
for i, n in enumerate(rowcnt):
    if n > 2 and not inb: start = 95 + i; inb = True
    elif n <= 2 and inb: bands.append((start, 95 + i - 1)); inb = False
if inb: bands.append((start, 514))
print('title bands:', bands)
colcnt2 = sub.sum(axis=0)
xs2 = [70 + i for i, n in enumerate(colcnt2) if n > 3]
print('title x extent:', min(xs2), max(xs2))

print('== 11. badge numeral ink (dark px inside badge circle) ==')
sub2 = A[56:85, 860:898]
dkm = (sub2.sum(axis=2) < 350)
ys3, xs3 = np.where(dkm)
if len(ys3): print('numeral ink bbox: x', 860 + xs3.min(), 860 + xs3.max(), 'y', 56 + ys3.min(), 56 + ys3.max())

print('== 12. X row / output row cell top+bottom edges across all cols (gray outline rows) ==')
# cell outline ~ (150,150,150)-ish on panel: scan rows 54..60 and 72..78 at x=340 (col3 gap-free zone)
for x in (340, 490, 770):
    print(f'  x={x}:', [(y, tuple(A[y, x])) for y in range(54, 62)], '...', [(y, tuple(A[y, x])) for y in range(72, 80)])

print('== 13. MHA bar exact top/bottom at x=500 ==')
print([ (y, tuple(A[y, 500])) for y in range(415, 424) ], '...', [ (y, tuple(A[y, 500])) for y in range(465, 473) ])
