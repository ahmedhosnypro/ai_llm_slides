#!/usr/bin/env python3
"""Pass 4: strict-black cube/arrow, label surroundings, meme edges, red-copy extent."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

black = (r < 90) & (g < 90) & (b < 90)
red = (r > 120) & (g < 110) & (b < 110)

print("== 1. cube strict-black (x 700..920, y 200..500) ==")
ys, xs = np.where(black[200:500, 700:920])
print(f"  cube ink x {700+xs.min()}..{700+xs.max()}, y {200+ys.min()}..{200+ys.max()}, n={len(xs)}")
rowb = black[200:500, 700:920].sum(axis=1)
print("  row runs>4:", runs([int(200+y) for y in np.where(rowb > 4)[0]])[:18])
colb = black[200:500, 700:920].sum(axis=0)
print("  col runs>4:", runs([int(700+x) for x in np.where(colb > 4)[0]])[:18])

print("== 2. apex probe: strict-black rows 215..270 detail (x 700..900) ==")
for y in range(215, 272, 3):
    xs = np.where(black[y, 700:900])[0]
    print(f"  y={y}: {runs([int(700+x) for x in xs])[:8]}")

print("== 3. label surroundings: is label on white? ==")
for (x, y) in [(752, 238), (755, 245), (790, 236), (810, 247), (840, 240), (848, 246),
               (750, 228), (750, 256), (855, 232), (855, 252), (745, 220), (745, 265),
               (800, 225), (800, 260), (770, 222)]:
    print(f"  ({x},{y}): {tuple(im[y, x])}")

print("== 4. red copy (strict, excl label box x745..860 y228..256): right/top extent ==")
redt = (r - g > 45) & (r - b > 45) & (r > 110)
m = redt.copy()
m[228:257, 740:865] = False   # label zone
m[485:, :] = False             # bottom stroke
ys, xs = np.where(m[200:480, 620:890])
print(f"  red-copy visible ink x {620+xs.min()}..{620+xs.max()}, y {200+ys.min()}..{200+ys.max()}, n={len(xs)}")
colr = m[200:480, 620:890].sum(axis=0)
print("  col runs>2:", runs([int(620+x) for x in np.where(colr > 2)[0]])[:12])
rowr = m[200:480, 620:890].sum(axis=1)
print("  row runs>2:", runs([int(200+y) for y in np.where(rowr > 2)[0]])[:12])

print("== 5. meme edges precise ==")
# top edge between header words: cols 137, 213, 293
nonwhite = (r < 249) | (g < 249) | (b < 249)
for x in [120, 137, 213, 293, 310]:
    ys = [y for y in range(195, 260) if nonwhite[y, x]]
    print(f"  col {x} (195..260): {runs(ys)[:6]}")
# bottom edge: cols 100,200,300 rows 430..500
for x in [100, 200, 300, 320]:
    ys = [y for y in range(425, 500) if nonwhite[y, x]]
    print(f"  col {x} (425..500): {runs(ys)[:8]}")
# left/right edges at rows 300, 380, 430
for y in [255, 300, 380, 430]:
    xs = [x for x in range(70, 360) if nonwhite[y, x]]
    rr = runs(xs)
    print(f"  row {y}: {rr[:4]}")

print("== 6. arrow strict-black (x 600..820, y 320..480) ==")
ys, xs = np.where(black[320:480, 600:820])
print(f"  arrow ink x {600+xs.min()}..{600+xs.max()}, y {320+ys.min()}..{320+ys.max()}, n={len(xs)}")
rowa = black[320:480, 600:820].sum(axis=1)
print("  row runs>0:", runs([int(320+y) for y in np.where(rowa > 0)[0]])[:20])
cola = black[320:480, 600:820].sum(axis=0)
print("  col runs>0:", runs([int(600+x) for x in np.where(cola > 0)[0]])[:20])

print("== 7. yellow Third D (wider window) ==")
yel = (r > 200) & (g > 170) & (b < 150)
ys, xs = np.where(yel[350:500, 600:900])
print(f"  yellow x {600+xs.min()}..{600+xs.max()}, y {350+ys.min()}..{350+ys.max()}, n={len(xs)}")

print("== 8. blue copy right edge vs arrow left: row scans ==")
for y in [360, 390, 410, 430, 445]:
    xs = [x for x in range(600, 760) if (r[y, x] < 249 or g[y, x] < 249 or b[y, x] < 249)]
    print(f"  row {y} nonwhite 600..760: {runs(xs)[:6]}")

print("== 9. matrix bracket cols detail (red, y 286..441) ==")
colr = red[280:445, 100:320].sum(axis=0)
print("  col runs>2:", runs([int(100+x) for x in np.where(colr > 2)[0]])[:20])
rowr = red[280:445, 100:320].sum(axis=1)
print("  row runs>2:", runs([int(280+y) for y in np.where(rowr > 2)[0]])[:20])
