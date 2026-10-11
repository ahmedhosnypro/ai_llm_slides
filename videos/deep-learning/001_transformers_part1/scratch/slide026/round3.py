#!/usr/bin/env python3
"""Round 3: pills bbox, glyph block medians, node hunt, Y-box, side lines."""
import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def med(name, x0, y0, x1, y1):
    reg = A[y0:y1, x0:x1].reshape(-1, 3)
    m = np.median(reg, axis=0).astype(int)
    print(f"{name:30s} ({x0},{y0})-({x1},{y1}) #{m[0]:02X}{m[1]:02X}{m[2]:02X} {tuple(m)}")

print("== pills: pale-yellow mask bbox per zone ==")
t = np.array([252, 250, 214])
for nm, (x0, x1) in {"Sim": (240, 380), "Prob": (420, 520), "WSum": (570, 700)}.items():
    sub = A[150:196, x0:x1]
    m = (np.abs(sub - t).sum(axis=2) <= 45)
    ys, xs = np.where(m)
    if len(xs):
        print(f"  {nm}: x{x0+xs.min()}..{x0+xs.max()} y{150+ys.min()}..{150+ys.max()} n={len(xs)}")
        med(f"  {nm} fill", x0 + xs.min() + 2, 150 + int(np.median(ys)) - 1, x0 + xs.min() + 6, 150 + int(np.median(ys)) + 1)
    else:
        print(f"  {nm}: none")

print("\n== pill text ink (dark px in pill zones) ==")
for nm, (x0, x1) in {"Sim": (240, 380), "Prob": (420, 520), "WSum": (570, 700)}.items():
    sub = A[150:196, x0:x1]
    m = sub.sum(axis=2) < 400
    ys, xs = np.where(m)
    if len(xs):
        print(f"  {nm} text: x{x0+xs.min()}..{x0+xs.max()} y{150+ys.min()}..{150+ys.max()} n={len(xs)}")

print("\n== left-stack row1 block medians (y243..250) ==")
for x0 in range(60, 140, 8):
    med(f"  L1 x{x0}", x0, 243, x0 + 8, 250)

print("\n== strip glyph1 medians (y489..501) ==")
for x0 in range(185, 290, 8):
    med(f"  S1 x{x0}", x0, 489, x0 + 8, 501)

print("\n== right-stack row1 medians (y243..250) ==")
for x0 in range(764, 845, 8):
    med(f"  R1 x{x0}", x0, 243, x0 + 8, 250)

print("\n== node hunt: darkest pixel per column in x492..762 at each line row ==")
for y in (246, 287, 328, 372):
    prof = []
    for x in range(492, 762, 2):
        seg = A[y - 3:y + 4, x]
        i = np.argmin(seg.sum(axis=1))
        v = seg[i].sum()
        prof.append(v)
    arr = np.array(prof)
    dark = [(492 + 2 * i, int(arr[i])) for i in range(len(arr)) if arr[i] < 560]
    print(f"  y={y}: dark cols {dark[:40]}")

print("\n== vertical traces x500..770, y150..197 (into Sigma) ==")
sub = A[150:197, 500:770]
m = (np.abs(sub - np.array([230, 120, 110])).sum(axis=2) <= 260) & (sub.sum(axis=2) < 620)
colsum = m.sum(axis=0)
cols = [500 + i for i in range(len(colsum)) if colsum[i] >= 4]
print("  columns with red ink:", cols)

print("\n== Y-box column scans ==")
for x in (556, 560, 566, 580, 590):
    col = A[108:200, x]
    s = []
    for y in range(0, 92):
        r, g, b = col[y]
        if abs(r - 247) + abs(g - 227) + abs(b - 206) > 55:
            s.append(f"y{108+y}:#{r:02X}{g:02X}{b:02X}")
    print(f"  x={x}: {' '.join(s[:26])}")

print("\n== side vertical lines ==")
for nm, (x, y) in {"L38": (38, 430), "L50": (50, 430), "R919": (919, 430), "R867": (867, 430),
                   "L38b": (38, 400), "L50b": (50, 470), "R919b": (919, 400)}.items():
    c = A[y, x]
    print(f"  {nm:6s} ({x},{y}) #{c[0]:02X}{c[1]:02X}{c[2]:02X} {tuple(c)}")

print("\n== dashed curve hunt left zone (x55..175, y390..478): any ink cols ==")
sub = A[390:478, 55:175]
m = (np.abs(sub - np.array([247, 227, 206])).sum(axis=2) > 70)
colsum = m.sum(axis=0)
runs, s = [], None
for i, v in enumerate(colsum):
    if v >= 2 and s is None: s = i
    if v < 2 and s is not None: runs.append((55 + s, 55 + i - 1)); s = None
if s is not None: runs.append((55 + s, 55 + len(colsum) - 1))
print("  ink col runs:", runs)
# same for right zone
sub = A[380:490, 845:918]
m = (np.abs(sub - np.array([247, 227, 206])).sum(axis=2) > 70)
m2 = (np.abs(sub - np.array([233, 233, 231])).sum(axis=2) > 60)
mm = m & m2
colsum = mm.sum(axis=0)
runs, s = [], None
for i, v in enumerate(colsum):
    if v >= 2 and s is None: s = i
    if v < 2 and s is not None: runs.append((845 + s, 845 + i - 1)); s = None
if s is not None: runs.append((845 + s, 845 + len(colsum) - 1))
print("  right-zone ink col runs (non-peach non-gray):", runs)

print("\n== softmax entry arrows zone (x345..458, y196..403): red-ish ink ==")
sub = A[196:403, 345:458]
m = (sub[:, :, 0] - sub[:, :, 1] > 40) & (sub[:, :, 0] > 150)
ys, xs = np.where(m)
if len(xs):
    print(f"  n={len(xs)} x{345+xs.min()}..{345+xs.max()} y{196+ys.min()}..{196+ys.max()}")
    # cluster by row bands
    rowsum = np.bincount(ys, minlength=207)
    bands = [(196 + i, int(rowsum[i])) for i in range(207) if rowsum[i] >= 3]
    print("  row bands:", bands[:30])

print("\n== W label exact ink (blue-ish) x490..515, y222..370 ==")
sub = A[222:370, 490:515]
m = (sub[:, :, 2] - sub[:, :, 0] > 40)
L, n = ndimage.label(m)
for i, sl in enumerate(ndimage.find_objects(L)):
    mm = L[sl] == i + 1
    if mm.sum() < 6: continue
    print(f"  W-label blob x{490+sl[1].start}..{490+sl[1].stop-1} y{222+sl[0].start}..{222+sl[0].stop-1} n={int(mm.sum())}")
