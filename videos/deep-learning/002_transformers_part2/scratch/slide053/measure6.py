#!/usr/bin/env python3
"""Final measurement pass: raw borders, colors, exact text bboxes, tag shape, diagonal."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def s(fx): return (fx - 18.45) / 0.95991
def sy(fy): return (fy + 0.29) / 0.95600
def S(fx0, fx1, fy0, fy1):
    return f'slide x {s(fx0):.1f}..{s(fx1):.1f} (w {s(fx1)-s(fx0):.1f}) y {sy(fy0):.1f}..{sy(fy1):.1f} (h {sy(fy1)-sy(fy0):.1f})'

print('=== A. matrix top border raw rows y 198..205 at x 480..482, 560..562, 640..642 ===')
for y in range(198, 206):
    print(f'  y={y}:', [tuple(a[y, x]) for x in (480, 481, 560, 561, 640, 641)])

print('=== B. matrix bottom border rows y 383..389 at x 480,560,640 ===')
for y in range(383, 390):
    print(f'  y={y}:', [tuple(a[y, x]) for x in (480, 560, 640)])

print('=== C. diagonal probes (expect dark line on green/mauve boundary) ===')
for (px, py) in [(487, 238), (495, 241), (530, 258), (560, 281), (600, 311), (640, 342), (520, 250), (660, 372)]:
    print(f'  ({px},{py}):', tuple(a[py, px]))

print('=== D. border color cores ===')
print('  container top border:', [tuple(a[y, 500]) for y in (109, 110, 111, 112)])
print('  statement top border:', [tuple(a[y, 400]) for y in (416, 417, 418, 419, 420)])
print('  statement bottom border:', [tuple(a[y, 400]) for y in (505, 506, 507, 508)])
print('  statement left border:', [tuple(a[460, x]) for x in (63, 64, 65, 66)])
print('  eq box border top:', [tuple(a[y, 800]) for y in (124, 125, 126, 127)])
print('  matrix left border:', [tuple(a[300, x]) for x in (445, 446, 447, 448)])
print('  arrow fill:', tuple(a[297, 310]), tuple(a[296, 305]), tuple(a[300, 315]))
print('  title red core:', tuple(a[68, 270]), tuple(a[70, 310]), tuple(a[67, 590]))
print('  subtitle red core:', tuple(a[95, 270]), tuple(a[95, 390]))
print('  subtitle blue core:', tuple(a[95, 480]), tuple(a[95, 520]), tuple(a[95, 560]))
print('  softmax label red:', tuple(a[114, 740]), tuple(a[115, 760]))
print('  eq ink color:', tuple(a[157, 830]), tuple(a[170, 815]), tuple(a[155, 745]))
print('  chip yellow:', tuple(a[220, 465]), tuple(a[258, 510]), tuple(a[378, 600]))
print('  chip outline:', [tuple(a[214, x]) for x in (465, 466, 467, 468)])
print('  zero navy:', tuple(a[220, 468]), tuple(a[299, 468]), tuple(a[339, 468]))
print('  minf red:', tuple(a[220, 515]), tuple(a[258, 560]), tuple(a[300, 605]))
print('  green chip fill:', tuple(a[220, 365]), tuple(a[258, 370]), tuple(a[375, 380]))
print('  tag green fill:', tuple(a[170, 470]), tuple(a[170, 520]), tuple(a[175, 610]))
print('  mauve fill:', tuple(a[240, 620]), tuple(a[260, 630]), tuple(a[300, 650]), tuple(a[230, 600]))
print('  lower green fill:', tuple(a[300, 490]), tuple(a[350, 520]), tuple(a[370, 560]), tuple(a[330, 470]))

print('=== E. exact text bboxes ===')
redm = (r - (g + b) / 2 > 55)
bluem = (b - (r + g) / 2 > 55)
darkm = (r < 110) & (g < 110) & (b < 110)

def bb(mask, x0, x1, y0, y1, label):
    z = np.zeros_like(mask); z[y0:y1, x0:x1] = True
    ys, xs = np.where(mask & z)
    if len(xs) == 0:
        print(f'  {label}: EMPTY'); return
    print(f'  {label}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}  {S(xs.min(), xs.max(), ys.min(), ys.max())}')

bb(redm, 200, 700, 55, 80, 'L1 title red')
bb(bluem | redm, 200, 700, 82, 106, 'L2 subtitle all')
bb(redm, 200, 460, 82, 106, 'L2 red part')
bb(bluem, 200, 700, 82, 106, 'L2 blue part')
bb(redm, 700, 930, 100, 124, 'Softmax label')
bb(bluem, 60, 900, 424, 446, 'stmt line1 blue text (excl borders x 68..873)')
bb(redm | darkm, 68, 873, 464, 487, 'expl line2 (red+navy)')
bb(redm | darkm, 68, 873, 487, 506, 'expl line3 (red+navy)')
bb(redm, 68, 873, 464, 487, 'expl line2 red only')
bb(redm, 68, 873, 487, 506, 'expl line3 red only')
bb(darkm, 68, 873, 464, 487, 'expl line2 navy only')
bb(darkm, 68, 873, 487, 506, 'expl line3 navy only')
bb(redm, 340, 445, 210, 232, 'chip r0 SOS text')
bb(redm, 340, 445, 248, 270, 'chip r1 Je text')
bb(redm, 340, 445, 286, 310, 'chip r2 me text')
bb(redm, 340, 445, 324, 352, 'chip r3 sens text')
bb(redm, 340, 445, 364, 390, 'chip r4 malade text')

print('=== F. tag0 ASCII shape (x 415..490, y 125..208, downsample 3) ===')
green = (g > r + 6) & (g > b + 6) & (g > 195) & (r > 150)
for y in range(125, 208, 3):
    line = ''
    for x in range(415, 492, 3):
        line += '#' if green[y, x] else '.'
    print(f'  y{y:3d} {line}')

print('=== G. tag red-text diagonals: tag1 (Je) and tag4 (malade) text pixel scatter ===')
for label, (x0, x1) in [('tag1', (455, 505)), ('tag4', (590, 650))]:
    z = np.zeros_like(redm); z[125:206, x0:x1] = True
    ys, xs = np.where(redm & z)
    if len(xs):
        print(f'  {label}: n={len(xs)} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}')
        for i in range(0, min(len(xs), 400), 25):
            print(f'     ({xs[i]},{ys[i]})', end='')
        print()

print('=== H. matrix border row counts, red only, rows 199..204 & 383..388, x 450..675 ===')
for y in list(range(199, 205)) + list(range(383, 389)):
    n = redm[y, 450:675].sum()
    xs = np.where(redm[y, 450:675])[0]
    rng = f'{xs.min()+450}..{xs.max()+450}' if len(xs) else '-'
    print(f'  row {y}: red n={n} x {rng}')

print('=== I. cursor gap check: right border col 677, rows 270..300 dark/blue ===')
for y in range(268, 302, 2):
    print(f'  y={y}:', tuple(a[y, 677]), tuple(a[y, 680]), tuple(a[y, 690]))
