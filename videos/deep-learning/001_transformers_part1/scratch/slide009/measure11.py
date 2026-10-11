#!/usr/bin/env python3
"""Pass 11: pink chain rects + connecting line; inter-row arrows; square widths;
whole-slide blue check; green box labels text."""
from PIL import Image
import numpy as np
from scipy import ndimage

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0].astype(int), bi[:,:,1].astype(int), bi[:,:,2].astype(int)

print("== WHOLE-SLIDE bluish comps (excluding callout/subtitle/badge zones) ==")
bluish = (Bl - R > 30) & (Bl - G > 15) & (Bl > 120)
lab, n = ndimage.label(bluish, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 15:
        ys, xs = sl
        print(f"  x{xs.start}..{xs.stop} y{ys.start}..{ys.stop} area={area}")

print("== PINK row: pinkish col runs y408..423 (gap tol 6) ==")
pinkish = (R - G > 22) & (R > 200) & (G > 150) & (G < 228)
cols = pinkish[408:424, 495:920].sum(axis=0)
runs = []
s = None; last = None
for i, v in enumerate(cols):
    if v >= 2:
        if s is None: s = i
        last = i
    elif s is not None and i - last > 6:
        runs.append((s + 495, last + 495)); s = None
if s is not None: runs.append((s + 495, last + 495))
print(f"  {len(runs)} runs:", [(a, b, b - a) for a, b in runs])
# sample pink fill color
print("  pink fill sample (547,415):", tuple(int(v) for v in bi[415, 547]),
      "| (583,415):", tuple(int(v) for v in bi[415, 583]),
      "| (727,415):", tuple(int(v) for v in bi[415, 727]))

print("== PINK connecting line: dark-ish px row band y408..424 outside rects ==")
darkline = (R < 190) & (G < 190) & (Bl < 190)
sub = np.zeros_like(darkline); sub[408:424, 495:920] = darkline[408:424, 495:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 10:
        ys, xs = sl
        print(f"  x{xs.start}..{xs.stop} y{ys.start}..{ys.stop} (w{xs.stop-xs.start} h{ys.stop-ys.start}) area={area}")

print("== BETWEEN pink and green (y424..462): anything non-panel? ==")
panel = (np.abs(R - 234) < 7) & (np.abs(G - 230) < 7) & (np.abs(Bl - 221) < 8)
other = ~panel
sub = np.zeros_like(other); sub[424:462, 500:915] = other[424:462, 500:915]
colsum = sub.sum(axis=0)
runs = []
s = None
for i, v in enumerate(colsum):
    if v >= 3 and s is None: s = i
    elif v < 3 and s is not None:
        if i - s >= 1: runs.append((s + 500, i + 500, int(colsum[s:i].max())))
        s = None
print(f"  non-panel col runs (n>=3 rows): {len(runs)}")
for a, b, m in runs[:30]:
    print(f"    x{a}..{b} peak={m}")

print("== SQUARE widths: border px at y373..374 and y393..395 ==")
for yy in (373, 374, 393, 394):
    row = bi[yy, 490:915]
    marks = [(490+i) for i in range(len(row)) if row[i].sum() < 645]
    # cluster
    cl = []
    for v in marks:
        if cl and v - cl[-1][-1] <= 3: cl[-1].append(v)
        else: cl.append([v])
    print(f"  y{yy}: clusters={[(c[0], c[-1]) for c in cl][:20]}")

print("== NABLA vertical extents at 12 centers (loose dark R<170) ==")
for k in range(12):
    cx = int(round(501.6 + 35.66 * k))
    win = bi[370:398, cx-14:cx+15]
    m = (win[:,:,0] < 170) & (win[:,:,1] < 170) & (win[:,:,2] < 170)
    ys, xs = np.where(m)
    if len(ys):
        print(f"  k={k} cx{cx}: ink x{cx-14+xs.min()}..{cx-14+xs.max()+1} y{370+ys.min()}..{370+ys.max()+1} (w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1}) n={len(ys)}")
    else:
        print(f"  k={k} cx{cx}: no ink (R<170)")

print("== GREEN labels: sample label ink color inside box k=0 (x526..538,y466..480) ==")
reg = bi[466:481, 524:540].reshape(-1,3)
dark = reg[(reg.sum(axis=1) < 420)]
print("  dark px mean:", dark.mean(axis=0) if len(dark) else "none", "n=", len(dark))
