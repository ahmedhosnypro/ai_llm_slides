#!/usr/bin/env python3
"""Slide 033 pass W4: true peach-panel edges + fixed label bboxes + runs."""
from PIL import Image
import numpy as np

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]

# gray-panel mask (E9E9E7 family) vs peach mask (F7E2CD family)
gray = (np.abs(A - np.array((233, 233, 231))).sum(axis=2) <= 21)
peach = (np.abs(A - np.array((247, 226, 205))).sum(axis=2) <= 27)

print("== gray vs peach fraction per column (rows 150..500) ==")
for x in list(range(40, 100, 4)) + list(range(860, 925, 4)):
    print(f"  x={x}: gray {gray[150:500, x].mean():.2f} peach {peach[150:500, x].mean():.2f}")
print("== gray vs peach fraction per row (cols 150..850) ==")
for y in list(range(44, 140, 6)) + list(range(500, 540, 6)):
    print(f"  y={y}: gray {gray[y, 150:850].mean():.2f} peach {peach[y, 150:850].mean():.2f}")

# peach panel edges: first/last col/row where SOLID peach (>=60% of span)
colfrac = peach[150:500].mean(axis=0)
rowfrac = peach[:, 150:850].mean(axis=1)
cols = np.where(colfrac > 0.5)[0]
rows = np.where(rowfrac > 0.5)[0]
print(f"\nSOLID peach columns: {cols.min()}..{cols.max()}")
print(f"SOLID peach rows: {rows.min()}..{rows.max()}")

# does a maroon/dark border surround the peach panel?
print("\n== peach panel border scan ==")
x0, x1, y0, y1 = cols.min(), cols.max(), rows.min(), rows.max()
for y in (y0 - 3, y0 - 2, y0 - 1, y0, y0 + 1):
    print(f"  top y={y} x500: {tuple(A[y, 500])}")
for x in (x0 - 3, x0 - 2, x0 - 1, x0, x0 + 1):
    print(f"  left x={x} y300: {tuple(A[300, x])}")

red = (R - G > 45) & (R - B > 30) & (R > 120)
sub = red[220:400, 196:262]
ys, xs = np.nonzero(sub)
bands = []
if len(ys):
    ys_u = np.unique(ys)
    s = p = ys_u[0]
    for v in ys_u[1:]:
        if v <= p + 3:
            p = v
        else:
            bands.append((s, p)); s = p = v
    bands.append((s, p))
print("\n== K label red bboxes (x196..262) ==")
for (a, b) in bands:
    sel = (ys >= a) & (ys <= b)
    print(f"  y {a+220}..{b+220}: x {xs[sel].min()+196}..{xs[sel].max()+196} n={sel.sum()}")

sub = red[220:400, 736:800]
ys, xs = np.nonzero(sub)
bands = []
if len(ys):
    ys_u = np.unique(ys)
    s = p = ys_u[0]
    for v in ys_u[1:]:
        if v <= p + 3:
            p = v
        else:
            bands.append((s, p)); s = p = v
    bands.append((s, p))
print("== V label red bboxes (x736..800) ==")
for (a, b) in bands:
    sel = (ys >= a) & (ys <= b)
    print(f"  y {a+220}..{b+220}: x {xs[sel].min()+736}..{xs[sel].max()+736} n={sel.sum()}")

sred = (R - G > 30) & (R - B > 18) & (R > 140)
print("== long red horizontal runs (len>=12) ==")
for y in range(220, 540):
    row = sred[y]
    x = 40
    while x < 930:
        if row[x]:
            x2 = x
            while x2 < 930 and (row[x2] or (x2 + 4 < 930 and row[x2:x2 + 5].any())):
                x2 += 1
            if x2 - x >= 12:
                print(f"  y={y}: x {x}..{x2-1} (len {x2-x})")
            x = x2
        else:
            x += 1

print("== long red vertical runs (len>=10) ==")
for x in range(40, 930):
    col = sred[:, x]
    y = 40
    while y < 539:
        if col[y]:
            y2 = y
            while y2 < 539 and (col[y2] or (y2 + 4 < 539 and col[y2:y2 + 5].any())):
                y2 += 1
            if y2 - y >= 10:
                print(f"  x={x}: y {y}..{y2-1} (len {y2-y})")
            y = y2
        else:
            y += 1

g = (G - R > 14) & (G - B > 4) & (G > 90) & (R < 190)
print("== loose green horizontal runs (len>=8) ==")
for y in range(40, 540):
    row = g[y]
    x = 40
    while x < 930:
        if row[x]:
            x2 = x
            while x2 < 930 and (row[x2] or (x2 + 5 < 930 and row[x2:x2 + 6].any())):
                x2 += 1
            if x2 - x >= 8:
                print(f"  y={y}: x {x}..{x2-1} (len {x2-x})")
            x = x2
        else:
            x += 1
