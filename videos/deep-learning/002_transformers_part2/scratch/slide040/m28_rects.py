#!/usr/bin/env python3
"""m28: find ALL thin rect edges in the panel (eq1..eq4), eq4 rect right edge,
ellipse interior spatial map, L1 underline probe, L2 underline exact extent/color."""
import numpy as np
from PIL import Image

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg").convert("RGB")
a = np.asarray(F).astype(int)
lum = (a[:, :, 0]*299 + a[:, :, 1]*587 + a[:, :, 2]*114)//1000

print("== 1. long horizontal edges in panel (rows with runs>=60px of lum<225, x150..556) ==")
for y in range(206, 500):
    row = lum[y, 150:556] < 225
    # longest run
    best = 0; cur = 0; bs = None; s = 0
    for i, v in enumerate(row):
        if v:
            if cur == 0:
                s = i
            cur += 1
            if cur > best:
                best = cur; bs = s
        else:
            cur = 0
    if best >= 60:
        xs = np.where(row)[0]
        cols = a[y, 150:556][row]
        print(f"  y={y}: run {bs+150}..{bs+150+best-1} (len {best}) mean={cols.mean(axis=0).round(0)}")

print()
print("== 2. long vertical edges (cols with runs>=25px of lum<225, y206..500) ==")
for x in range(150, 557):
    col = lum[206:500, x] < 225
    best = 0; cur = 0; bs = None; s = 0
    for i, v in enumerate(col):
        if v:
            if cur == 0:
                s = i
            cur += 1
            if cur > best:
                best = cur; bs = s
        else:
            cur = 0
    if best >= 25:
        ys = np.where(col)[0]
        cols = a[206:500, x][col]
        print(f"  x={x}: run y {bs+206}..{bs+206+best-1} (len {best}) mean={cols.mean(axis=0).round(0)}")

print()
print("== 3. eq4 rect top/bottom full extent (rows 450..453, 473..476, x150..560) ==")
for y in [450, 451, 452, 453, 473, 474, 475, 476]:
    row = lum[y, 150:561] < 225
    xs = np.where(row)[0]
    if len(xs):
        # print run structure
        runs = []
        start = xs[0]; prev = xs[0]
        for v in xs[1:]:
            if v > prev + 2:
                runs.append((start + 150, prev + 150)); start = v
            prev = v
        runs.append((start + 150, prev + 150))
        big = [(r0, r1) for r0, r1 in runs if r1 - r0 >= 20]
        print(f"  y={y}: big runs {big}")

print()
print("== 4. ellipse interior spatial map x166..196 y450..478 ==")
def cls(x, y):
    r, g, b = a[y, x]
    L = lum[y, x]
    if L < 130: return "#"
    if r > 235 and g > 235 and b > 235: return "."
    if r > 200 and 140 < g < 220 and b < 170: return "T"   # tan
    if r > 200 and g < 150 and b < 120: return "O"          # orange ring
    if r > 150 and g < 130 and b < 130: return "r"          # red-ish
    return "?"
for y in range(450, 479):
    print(f"  {y:3d} " + "".join(cls(x, y) for x in range(166, 197)))

print()
print("== 5. L1 underline probe x500..840 y130..144 ==")
for y in range(130, 145):
    xs = np.where(lum[y, 500:841] < 200)[0]
    if len(xs):
        cols = a[y, 500:841][xs]
        print(f"  y={y}: n={len(xs)} x {xs.min()+500}..{xs.max()+500} mean={cols.mean(axis=0).round(0)}")

print()
print("== 6. L2 underline exact extent+color rows 156..158 x640..915 ==")
for y in [156, 157, 158]:
    row = lum[y, 640:916] < 210
    xs = np.where(row)[0]
    runs = []
    if len(xs):
        start = xs[0]; prev = xs[0]
        for v in xs[1:]:
            if v > prev + 3:
                runs.append((start + 640, prev + 640)); start = v
            prev = v
        runs.append((start + 640, prev + 640))
    print(f"  y={y}: runs {runs}")
    if len(xs):
        cols = a[y, 640:916][row]
        print(f"       mean={cols.mean(axis=0).round(0)} n={len(xs)}")

print()
print("== 7. L3 underline row 181 extent+color ==")
row = lum[181, 90:460] < 210
xs = np.where(row)[0]
cols = a[181, 90:460][row]
print(f"  y=181: x {xs.min()+90}..{xs.max()+90} n={len(xs)} mean={cols.mean(axis=0).round(0)}")

print()
print("== 8. eq3 rect edges: exact stroke rows/cols ==")
for x in [163, 164, 165]:
    col = lum[395:452, x] < 228
    print(f"  x={x}: dark rows {np.where(col)[0]+395}")
for y in [398, 399, 400]:
    row = lum[y, 150:300] < 228
    xs = np.where(row)[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+150}..{xs.max()+150} n={len(xs)} mean={a[y,150:300][row].mean(axis=0).round(0)}")
for x in [288, 289, 290]:
    col = lum[395:452, x] < 228
    print(f"  x={x}: dark rows {np.where(col)[0]+395}")

print()
print("== 9. eq4 rect left/right edge cols ==")
for x in [163, 164, 165, 548, 549, 550, 551, 552]:
    col = lum[448:478, x] < 228
    rows_ = np.where(col)[0]
    if len(rows_):
        print(f"  x={x}: dark rows y {rows_.min()+448}..{rows_.max()+448} n={len(rows_)}")
