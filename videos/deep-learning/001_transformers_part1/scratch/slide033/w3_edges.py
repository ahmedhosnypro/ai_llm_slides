#!/usr/bin/env python3
"""Slide 033 pass W3: edge pixel sampling + widget/label precise bboxes."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)

print("== panel left edge: rows y=300, y=100, cols x=34..48 ==")
for y in (100, 300, 500):
    print(f" y={y}: " + " ".join(f"x{x}:{tuple(A[y,x])}" for x in range(34, 49, 2)))
print("== panel top edge: x=500, rows y=38..52 ==")
print("  " + " ".join(f"y{y}:{tuple(A[y,500])}" for y in range(38, 53)))
print("== panel right edge: y=300, x=912..930 ==")
print("  " + " ".join(f"x{x}:{tuple(A[300,x])}" for x in range(912, 931, 2)))
print("== panel bottom edge: x=500, rows y=530..539 ==")
print("  " + " ".join(f"y{y}:{tuple(A[y,500])}" for y in range(530, 540)))
print("== badge area cols x=870..920 at y=71 ==")
print("  " + " ".join(f"x{x}:{tuple(A[71,x])}" for x in range(868, 921, 4)))
print("== above panel top: x=500, y=30..41 ==")
print("  " + " ".join(f"y{y}:{tuple(A[y,500])}" for y in range(30, 42, 2)))

# ---- left container: row bands via red X labels + widget cell maps -------------
print("\n== left container rows: red-ink columns in x60..140 ==")
red = (A[:, :, 0] - A[:, :, 1] > 45) & (A[:, :, 0] - A[:, :, 2] > 30) & (A[:, :, 0] > 120)
sub = red[220:400, 60:140]
rows = np.where(sub.sum(axis=1) > 2)[0] + 220
print("  red rows:", rows.tolist())

# ---- K labels: red bboxes per band in x200..260 -------------------------------
print("\n== K label bboxes (red ink x196..262) ==")
sub = red[220:400, 196:262]
ys, xs = np.nonzero(sub)
if len(ys):
    bands = []
    ys_u = np.unique(ys)
    s = p = ys_u[0]
    for v in ys_u[1:]:
        if v <= p + 3:
            p = v
        else:
            bands.append((s, p)); s = p = v
    bands.append((s, p))
    for (a, b) in bands:
        m = sub[(ys >= a) & (ys <= b)]
        xs_sel = xs[(ys >= a) & (ys <= b)]
        print(f"  band y {a+220}..{b+220}: x {xs_sel.min()+196}..{xs_sel.max()+196}  n={m.sum()}")

# ---- V labels: red bboxes x736..800 --------------------------------------------
print("\n== V label bboxes (red ink x736..800) ==")
sub = red[220:400, 736:800]
ys, xs = np.nonzero(sub)
if len(ys):
    bands = []
    ys_u = np.unique(ys)
    s = p = ys_u[0]
    for v in ys_u[1:]:
        if v <= p + 3:
            p = v
        else:
            bands.append((s, p)); s = p = v
    bands.append((s, p))
    for (a, b) in bands:
        xs_sel = xs[(ys >= a) & (ys <= b)]
        print(f"  band y {a+220}..{b+220}: x {xs_sel.min()+736}..{xs_sel.max()+736}  n={((ys>=a)&(ys<=b)).sum()}")

# ---- red horizontal lines: long runs per row (soft mask) -----------------------
print("\n== long red/orange horizontal runs (len>=12), y 220..540 ==")
sred = (A[:, :, 0] - A[:, :, 1] > 30) & (A[:, :, 0] - A[:, :, 2] > 18) & (A[:, :, 0] > 140)
for y in range(220, 540):
    row = sred[y]
    x = 40
    while x < 930:
        if row[x]:
            x2 = x
            while x2 < 930 and (row[x2] or (x2 + 4 < 930 and row[x2:x2+5].any())):
                x2 += 1
            if x2 - x >= 12:
                print(f"  y={y}: x {x}..{x2-1} (len {x2-x})")
            x = x2
        else:
            x += 1

# ---- red vertical runs (len>=10), x 40..930 ------------------------------------
print("\n== long red vertical runs (len>=10) ==")
for x in range(40, 930):
    col = sred[:, x]
    y = 40
    while y < 539:
        if col[y]:
            y2 = y
            while y2 < 539 and (col[y2] or (y2 + 4 < 539 and col[y2:y2+5].any())):
                y2 += 1
            if y2 - y >= 10:
                print(f"  x={x}: y {y}..{y2-1} (len {y2-y})")
            y = y2
        else:
            y += 1

# ---- loose green full-slide scan: dashed container borders + connectors --------
print("\n== loose green: long horizontal runs (len>=8) ==")
g = (A[:, :, 1] - A[:, :, 0] > 14) & (A[:, :, 1] - A[:, :, 2] > 4) & (A[:, :, 1] > 90) & (A[:, :, 0] < 190)
for y in range(40, 540):
    row = g[y]
    x = 40
    while x < 930:
        if row[x]:
            x2 = x
            while x2 < 930 and (row[x2] or (x2 + 5 < 930 and row[x2:x2+6].any())):
                x2 += 1
            if x2 - x >= 8:
                print(f"  y={y}: x {x}..{x2-1} (len {x2-x})")
            x = x2
        else:
            x += 1
