#!/usr/bin/env python3
"""ASCII structure maps + subtitle color profile + robust fill medians."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def classify(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R - (G + B) / 2 > 55: return 'R'          # red
    if B - (R + G) / 2 > 55: return 'B'          # blue
    if R > 225 and G > 225 and 150 < B < 220: return 'Y'   # yellow chip
    if G > R + 6 and G > B + 6 and G > 195: return 'G'     # light green
    if R < 110 and G < 110 and B < 110: return 'D'         # dark
    if R > 150 and G > 100 and B > 100 and R > G + 12 and R > B + 12: return 'M'  # mauve
    if R > 200 and G > 200 and B > 200: return '.'         # white-ish
    if abs(R-G) < 20 and abs(G-B) < 20 and 200 < R < 245: return ','  # gray panel
    return '?'

print('=== MATRIX ASCII (x 440..690 step 5, y 195..405 step 4) ===')
print('    ' + ''.join(str((440 + i*5) // 100 % 10) for i in range(51)))
for y in range(195, 406, 4):
    line = ''
    for x in range(440, 695, 5):
        line += classify(a[y, x])
    print(f'{y:3d} {line}')

print()
print('=== SUBTITLE COLUMN PROFILE (y 84..106, x 255..600): dominant ink class per column ===')
for x in range(255, 601, 3):
    col = a[84:107, x]
    classes = Counter(classify(px) for px in col)
    ink = {k: v for k, v in classes.items() if k in 'RBDM'}
    tot = sum(ink.values())
    if tot >= 2:
        dom = max(ink.items(), key=lambda kv: kv[1])
        print(f'  x={x}: {dict(ink)} dom={dom[0]}')

print()
print('=== subtitle sample pixels y=93..99, x=330..360 (the gap region) ===')
for x in range(330, 362, 4):
    print(f'  x={x}:', [tuple(a[y, x]) for y in (90, 94, 98)])

print()
print('=== ROBUST FILL MEDIANS ===')
def med(y0, y1, x0, x1, label):
    z = a[y0:y1, x0:x1].reshape(-1, 3)
    print(f'  {label}: median rgb {tuple(int(v) for v in np.median(z, axis=0))} n={len(z)}')
med(232, 250, 600, 660, 'mauve upper tri (clean band)')
med(300, 315, 490, 520, 'green lower tri (clean band)')
med(216, 226, 462, 476, 'chip r0c0 (yellow+digit)')
med(373, 381, 463, 474, 'chip r4c0 yellow')
med(155, 165, 425, 435, 'tag0 fill (green tag)')
med(290, 300, 355, 370, 'row chip fill')
med(140, 150, 855, 875, 'eq box interior white')
print()
print('=== digit "0" core color (darkest px in digit bboxes) ===')
for (x0, x1, y0, y1) in [(463, 474, 214, 227), (508, 519, 252, 266), (555, 566, 292, 307)]:
    z = a[y0:y1, x0:x1].reshape(-1, 3)
    lum = z.sum(axis=1)
    i = lum.argmin()
    print(f'  digit@({x0},{y0}): darkest {tuple(z[i])}  p10 lum {np.percentile(lum,10):.0f}')
print()
print('=== -inf glyph core color ===')
for (x0, x1, y0, y1) in [(501, 527, 212, 230), (592, 618, 249, 268)]:
    z = a[y0:y1, x0:x1].reshape(-1, 3)
    redness = z[:, 0] - (z[:, 1] + z[:, 2]) / 2
    i = redness.argmax()
    print(f'  -inf@({x0},{y0}): reddest {tuple(z[i])}')
print()
print('=== statement text line1: exact right edge (blue ink cols, y 425..445, x 550..700) ===')
bluem = (b - (r + g) / 2 > 55)
for x in range(540, 720, 5):
    n = bluem[425:446, x].sum()
    if n: print(f'  x={x}: n={n}')
print()
print('=== title L1 gap check: ink cols y 58..78, x 250..620 (find word gaps) ===')
redm = (r - (g + b) / 2 > 55)
cols = [x for x in range(250, 625) if redm[58:79, x].sum() > 0]
runs = []
start = prev = cols[0]
for x in cols[1:]:
    if x > prev + 1:
        runs.append((start, prev)); start = x
    prev = x
runs.append((start, prev))
print('  L1 ink col runs:', runs)
print()
print('=== L2 ink col runs (red|blue, y 84..106, x 250..600) ===')
cols2 = [x for x in range(250, 605) if (redm[84:107, x] | bluem[84:107, x]).sum() > 0]
runs2 = []
start = prev = cols2[0]
for x in cols2[1:]:
    if x > prev + 1:
        runs2.append((start, prev)); start = x
    prev = x
runs2.append((start, prev))
print('  L2 ink col runs:', runs2)
