#!/usr/bin/env python3
"""Slide 038 — m16: surgical probes. Cell borders, mid-bar colors, bar right end,
annotation true bboxes, subscript digit shapes."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

print("== top-bar dark border cols (rows 262..275, count of dark px per col) ==")
dark = (R < 150) & (G < 150) & (B < 150)
seg = dark[262:275, 150:890]
colprof = seg.sum(axis=0)
strokes = [c + 150 for c in range(len(colprof)) if colprof[c] >= 8]
print("  border cols:", strokes)

print("== X-bar dark border cols (rows 469..481) ==")
seg = dark[469:481, 150:890]
colprof = seg.sum(axis=0)
strokes = [c + 150 for c in range(len(colprof)) if colprof[c] >= 8]
print("  border cols:", strokes)

print("== mid-bar: raw colors rows 352..370 at col2 x 262..296 ==")
for y in range(352, 371, 2):
    print(f"  y={y}: " + " ".join(f"{tuple(img[y, x])}" for x in range(262, 297, 3)))

print("== mid-bar dark border cols (rows 354..367) ==")
seg = dark[354:367, 150:890]
colprof = seg.sum(axis=0)
strokes = [c + 150 for c in range(len(colprof)) if colprof[c] >= 7]
print("  border cols:", strokes)

print("== gray bar right end: rows 299..317, cols 860..900 raw ==")
for x in range(860, 901, 2):
    print(f"  x={x}: {tuple(img[305, x])} {tuple(img[318, x])}")

print("== gray bar left end: cols 165..185 raw ==")
for x in range(165, 186, 2):
    print(f"  x={x}: {tuple(img[305, x])}")

print("== col1 top subscript raw grid (x 204..218, y 262..277) ==")
for y in range(262, 278):
    row = ""
    for x in range(204, 219):
        r, g, b = img[y, x]
        if r > 200 and g > 200 and b > 200: row += "."
        elif r < 120 and g < 100: row += "#"
        elif r > 150 and g < 150: row += "+"
        else: row += "-"
    print(f"  y={y}: {row}")

print("== col8 top tail subscript raw grid (x 838..858, y 262..277) ==")
for y in range(262, 278):
    row = ""
    for x in range(838, 859):
        r, g, b = img[y, x]
        if r > 200 and g > 200 and b > 200: row += "."
        elif r < 120 and g < 100: row += "#"
        elif r > 150 and g < 150: row += "+"
        else: row += "-"
    print(f"  y={y}: {row}")

print("== col7 top tail label full grid (x 752..790, y 262..277) ==")
for y in range(262, 278):
    row = ""
    for x in range(752, 791):
        r, g, b = img[y, x]
        if r > 200 and g > 200 and b > 200: row += "."
        elif r < 120 and g < 100: row += "#"
        elif r > 150 and g < 150: row += "+"
        else: row += "-"
    print(f"  y={y}: {row}")

print("== annotations true bboxes (x window 72..168 to skip borders) ==")
blue = (B > 110) & (R < 110) & (G < 110)
orange = (R > 150) & (G > 60) & (G < 160) & (B < 90) & (R - B > 90)
red = (R > 110) & (R < 220) & (G < 110) & (B < 110)
for name, mask, y0, y1 in (("blue", blue, 362, 398), ("orange", orange, 412, 442), ("red", red, 448, 484)):
    seg2 = mask[y0:y1, 72:168]
    rows = np.where(seg2.sum(axis=1) > 2)[0]
    if not len(rows): print(f"  {name}: none"); continue
    groups, cur = [], [rows[0]]
    for r in rows[1:]:
        if r - cur[-1] <= 3: cur.append(r)
        else: groups.append(cur); cur = [r]
    groups.append(cur)
    for g in groups:
        band = seg2[g[0]:g[-1]+1]
        cols = np.where(band.sum(axis=0) > 0)[0]
        print(f"  {name}: y {g[0]+y0}..{g[-1]+y0} x {cols.min()+72}..{cols.max()+72}"
              f" -> slide y {invy(g[0]+y0)}..{invy(g[-1]+y0)} x {invx(cols.min()+72)}..{invx(cols.max()+72)}")

print("== top-row label ink extents per column (red mask, y 260..276) ==")
seg3 = red[260:276, 150:890]
colprof = seg3.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 1 and not inr: s = i; inr = True
    elif v <= 1 and inr:
        if i - s >= 2: runs.append((s + 150, i + 150))
        inr = False
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] <= 4: merged[-1] = (merged[-1][0], b)
    else: merged.append((a, b))
print("  label blobs:", [(a, b, b - a) for a, b in merged])
print("  slide:", [(round(invx(a), 1), round(invx(b), 1)) for a, b in merged])
