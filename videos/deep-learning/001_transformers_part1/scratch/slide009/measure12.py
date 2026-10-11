#!/usr/bin/env python3
"""Pass 12: resolve (1) the blue curve's full path (loose bluish mask),
(2) pink row: rects at green centers vs midpoints + red arrows between."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(F).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0].astype(int), bi[:,:,1].astype(int), bi[:,:,2].astype(int)

print("== (1) BLUE CURVE: loose bluish (Bl-R>14, Bl-G>8, Bl>135, R<225) full trace ==")
bluish = (Bl - R > 14) & (Bl - G > 8) & (Bl > 135) & (R < 225)
sub = np.zeros_like(bluish); sub[150:345, 380:960] = bluish[150:345, 380:960]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 8:
        ys, xs = sl
        res.append((area, xs.start, ys.start, xs.stop, ys.stop))
res.sort(reverse=True)
for area, x0, y0, x1, y1 in res[:20]:
    print(f"  area={area:5d} x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0})")
# trace the biggest curve comp row by row
if res:
    big = res[0]
    m = (lab == np.argmax([ (lab[sl]==i+1).sum() for i,sl in enumerate(ndimage.find_objects(lab)) if (sl[1].start,sl[0].start)==(big[1],big[2]) ])+1) if False else None
# simpler: trace bluish in the band y300..330
print("  row trace y298..340 (x-runs of bluish, x480..930):")
for y in range(298, 341, 2):
    row = np.where(bluish[y, 480:930])[0]
    if len(row) >= 2:
        runs = []
        s = row[0]; p = row[0]
        for v in row[1:]:
            if v - p > 4: runs.append((s+480, p+480)); s = v
            p = v
        runs.append((s+480, p+480))
        print(f"    y{y}: {runs}")
print("  col trace: bluish above panel y290..313, per-x bands:")
win = bluish[288:314, 480:930]
colsum = win.sum(axis=0)
runs = []; s = None
for i, v in enumerate(colsum):
    if v >= 2 and s is None: s = i
    elif v < 2 and s is not None:
        if i - s >= 1: runs.append((s+480, i+480, int(colsum[s:i].max())))
        s = None
print(f"    {runs[:30]}")

print("== (2) PINK ROW: colors at green centers vs midpoints, y413..418 ==")
gcenters = [531, 566, 600, 638, 673, 707.5, 742, 780, 818, 856, 894]
mids = [548.5, 583, 619, 655.5, 690, 725, 761, 799, 837, 875]
print("  at green centers:")
for cx in gcenters:
    c = bi[413:419, int(cx)-2:int(cx)+3].reshape(-1,3).mean(axis=0)
    print(f"    x{cx:.0f}: ({c[0]:.0f},{c[1]:.0f},{c[2]:.0f})", end="")
print()
print("  at midpoints:")
for cx in mids:
    c = bi[413:419, int(cx)-2:int(cx)+3].reshape(-1,3).mean(axis=0)
    print(f"    x{cx:.0f}: ({c[0]:.0f},{c[1]:.0f},{c[2]:.0f})", end="")
print()
print("  pinkish col runs y408..424 fine (min count 2, gap tol 2):")
pinkish = (R - G > 18) & (R > 190) & (G > 140) & (G < 235) & (Bl > 120)
cols = pinkish[408:424, 500:920].sum(axis=0)
runs = []; s = None; last = None
for i, v in enumerate(cols):
    if v >= 2:
        if s is None: s = i
        last = i
    elif s is not None and i - last > 2:
        runs.append((s+500, last+500)); s = None
if s is not None: runs.append((s+500, last+500))
print(f"    {runs}")
print("  red-ish (arrow) col runs y408..424 (R-G>40, R<200):")
redish = (R - G > 40) & (R > 110) & (R < 210) & (G < 130)
cols = redish[408:424, 500:920].sum(axis=0)
runs = []; s = None; last = None
for i, v in enumerate(cols):
    if v >= 1:
        if s is None: s = i
        last = i
    elif s is not None and i - last > 3:
        runs.append((s+500, last+500)); s = None
if s is not None: runs.append((s+500, last+500))
print(f"    {runs}")

print("== (2b) NABLA-ROW GAPS: red arrow shapes (y374..396, per gap) ==")
gaps = [(542,555),(581,594),(618,632),(656,670),(694,704),(729,739),(763,773),(798,811),(836,846),(871,881)]
for gx0, gx1 in gaps:
    reg = bi[374:397, gx0:gx1]
    m = (reg[:,:,0].astype(int) - reg[:,:,1] > 30) & (reg[:,:,0] > 120)
    ys, xs = np.where(m)
    if len(ys):
        print(f"    gap {gx0}..{gx1}: red n={len(ys)} x{gx0+xs.min()}..{gx0+xs.max()+1} y{374+ys.min()}..{374+ys.max()+1}")
    else:
        print(f"    gap {gx0}..{gx1}: none")
