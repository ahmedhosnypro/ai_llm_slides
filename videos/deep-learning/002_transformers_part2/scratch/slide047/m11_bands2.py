#!/usr/bin/env python3
"""m11_bands2.py — exact cell bands, arrows, FFN dots, boxes, badge for slide_047."""
from PIL import Image
import numpy as np
from collections import Counter

F47 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A = np.asarray(Image.open(F47).convert('RGB')).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
SY = 0.955556
sy = lambda fy: fy / SY

print('== 1. output row band: classify x=199 and x=211 (cell segments, off-label) y 48..96 ==')
for x in (199, 211):
    prev = None
    for y in range(48, 97):
        px = A[y, x]
        r, g, b = px
        if r > 243 and g > 243 and b > 243: c = 'white'
        elif abs(r - 233) < 12 and abs(g - 233) < 12 and abs(b - 231) < 12: c = 'panel'
        elif r > 240 and g > 235 and 180 < b < 235: c = 'paleY'
        elif g > r and g > 150 and b < 160: c = 'greenish'
        elif r > 240 and 190 < g < 235 and 170 < b < 225: c = 'pinkish'
        elif r + g + b < 500: c = 'dark'
        else: c = f'other{tuple(px)}'
        if c != prev:
            print(f'  x={x} y={y}: {c} {tuple(px)}')
            prev = c

print('== 2. X row band: same at x=199/211, y 470..520 ==')
for x in (199, 211):
    prev = None
    for y in range(470, 521):
        px = A[y, x]
        r, g, b = px
        if r > 243 and g > 243 and b > 243: c = 'white'
        elif abs(r - 233) < 12 and abs(g - 233) < 12 and abs(b - 231) < 12: c = 'panel'
        elif r > 240 and g > 235 and 180 < b < 235: c = 'paleY'
        elif g > r and g > 150 and b < 160: c = 'greenish'
        elif b > r + 20 and b > 100: c = 'blueish'
        elif r > 240 and 190 < g < 235 and 170 < b < 225: c = 'pinkish'
        elif r + g + b < 500: c = 'dark'
        else: c = f'other{tuple(px)}'
        if c != prev:
            print(f'  x={x} y={y}: {c} {tuple(px)}')
            prev = c

print('== 3. X-row cells horizontal structure at y=499 (segment borders) ==')
row = A[499]
segs = []
prev = None
for x in range(180, 240):
    px = row[x]
    key = tuple((px // 24) * 24 + 12)
    if key != prev:
        segs.append((x, tuple(px)))
        prev = key
print(segs)

print('== 4. output-row cells horizontal structure at y=80 ==')
row = A[80]
segs = []
prev = None
for x in range(180, 240):
    px = row[x]
    key = tuple((px // 24) * 24 + 12)
    if key != prev:
        segs.append((x, tuple(px)))
        prev = key
print(segs)

print('== 5. FFN unit boxes: vertical borders + dot rows ==')
band = A[233:256, :]
# orange border mask (ED7D31-ish washed: r>200, 100<g<190, b<130) vs unit fill (248,184,104)
bor = ((R[233:256] > 195) & (G[233:256] < 195) & (B[233:256] < 135) &
       (R[233:256] - B[233:256] > 80)).sum(axis=0)
cand = [x for x in range(130, 900) if bor[x] >= 12]
groups = []
for x in cand:
    if groups and x - groups[-1][1] <= 2: groups[-1][1] = x
    else: groups.append([x, x])
print('vertical border cols:', groups)
# green dots: green mask in 232..245
gm = ((G[232:246] > R[232:246]) & (G[232:246] > 140) & (B[232:246] < 150)).sum(axis=0)
gc = [x for x in range(130, 900) if gm[x] >= 2]
ggroups = []
for x in gc:
    if ggroups and x - ggroups[-1][1] <= 2: ggroups[-1][1] = x
    else: ggroups.append([x, x])
print('green dot clusters (row1):', ggroups)
gm2 = ((G[246:258] > R[246:258]) & (G[246:258] > 140) & (B[246:258] < 150)).sum(axis=0)
print('green clusters (row2):', [x for x in range(130, 900) if gm2[x] >= 2][:40])
# magenta dots: r high, b high, g mid
mm = ((R[238:256] > 190) & (B[238:256] > 130) & (G[238:256] < 180) & (B[238:256] > G[238:256])).sum(axis=0)
mc = [x for x in range(130, 900) if mm[x] >= 2]
mgroups = []
for x in mc:
    if mgroups and x - mgroups[-1][1] <= 2: mgroups[-1][1] = x
    else: mgroups.append([x, x])
print('magenta dot clusters:', mgroups)

print('== 6. zone2 arrows vertical extent at col2 (x=278): blue/lavender rows ==')
for y in range(462, 500):
    px = A[y, 278]
    if px[2] > px[0] + 15 or px.sum() < 400:
        print(f'  y={y}: {tuple(px)}')

print('== 7. LN bar text ink extent (top bar): dark px rows/cols in 104..128 ==')
dm = (A[104:128, 150:880].sum(axis=2) < 480)
rows = dm.sum(axis=1)
print('dark rows:', [(104 + i, int(n)) for i, n in enumerate(rows) if n > 3])
cols = dm.sum(axis=0)
xs = [150 + i for i, n in enumerate(cols) if n > 0]
print('ink x extent:', min(xs), max(xs))

print('== 8. FFN header text ink extent (212..226) ==')
dm = (A[210:228, 150:880].sum(axis=2) < 480)
cols = dm.sum(axis=0)
xs = [150 + i for i, n in enumerate(cols) if n > 0]
rows = dm.sum(axis=1)
print('ink x extent:', min(xs), max(xs), 'rows:', [(210 + i, int(n)) for i, n in enumerate(rows) if n > 3])

print('== 9. Block Output / Input boxes: border rect detection ==')
red = (R > 140) & (G < 90) & (B < 90)
for y0, y1, lab in ((50, 95, 'BlockOutput'), (472, 520, 'BlockInput')):
    sub = red[y0:y1, 45:190]
    colcnt = sub.sum(axis=0)
    rowcnt = sub.sum(axis=1)
    vcols = [45 + i for i, n in enumerate(colcnt) if n > 8]
    hrows = [y0 + i for i, n in enumerate(rowcnt) if n > 8]
    print(f'{lab}: vertical border cols {vcols}, horizontal border rows {hrows}')

print('== 10. vertical title ink bands (red mask, x 80..140) ==')
sub = red[100:510, 78:140]
rowcnt = sub.sum(axis=1)
bands = []
inb = False
for i, n in enumerate(rowcnt):
    if n > 2 and not inb:
        start = 100 + i; inb = True
    elif n <= 2 and inb:
        bands.append((start, 100 + i - 1)); inb = False
if inb: bands.append((start, 509))
print('title ink row bands:', bands)
colcnt = sub.sum(axis=0)
print('title col extent:', [78 + i for i, n in enumerate(colcnt) if n > 2][:5], '...',
      [78 + i for i, n in enumerate(colcnt) if n > 2][-5:])

print('== 11. badge ==')
yel = (R > 225) & (G > 225) & (B < 205)
sub = yel[40:110, 850:935]
ys, xs = np.where(sub)
print('badge bbox x', 850 + xs.min(), 850 + xs.max(), 'y', 40 + ys.min(), 40 + ys.max(),
      'center', (850 + (xs.min() + xs.max()) / 2, 40 + (ys.min() + ys.max()) / 2))

print('== 12. orange curves: presence at col1-26 (x~155) top+bottom units ==')
for y0, y1, lab in ((96, 165, 'top unit'), (303, 378, 'bottom unit')):
    m = ((R[y0:y1, 145:175] > 200) & (G[y0:y1, 145:175] < 190) & (B[y0:y1, 145:175] < 130)).sum(axis=1)
    nz = [y0 + i for i, n in enumerate(m) if n >= 2]
    print(f'{lab} curve x145-175 rows: {nz[:6]}...{nz[-6:] if len(nz) > 6 else ""} n={len(nz)}')

print('== 13. green arrows bands at col2 (x=278): greenish px ==')
gmask = (G > R) & (G > 130) & (B < 150)
for y0, y1, lab in ((126, 145, 'top green (LN->plus)'), (296, 315, 'post-LN->?'), (340, 355, 'bottom green'), (100, 115, 'in top bar')):
    cols = gmask[y0:y1].sum(axis=0)
    xs = [x for x in range(150, 890) if cols[x] >= 2]
    groups = []
    for x in xs:
        if groups and x - groups[-1][1] <= 3: groups[-1][1] = x
        else: groups.append([x, x])
    print(f'{lab} y{y0}-{y1}: {len(groups)} clusters', groups[:10])
