#!/usr/bin/env python3
"""Slide 038 — m10: disambiguate top-row label/arrow/bar stack; bar widths; X->block arrows; plus circles."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

print("== raw rows 249..300 at column-2 label center x=278 and bar-left x=266 ==")
for y in range(249, 301):
    print(f"  y={y} slide_y={invy(y)} x278={tuple(img[y,278])} x266={tuple(img[y,266])} x290={tuple(img[y,290])}")

print("== top bar horizontal extent: non-white cols in y 262..272 ==")
ink = (R < 200) | (G < 200) | (B < 200)
seg = ink[262:272, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 4 and not inr:
        s = i; inr = True
    elif v <= 4 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  top bar blobs:", [(a, b, b - a) for a, b in runs])

print("== mid bar horizontal extent: non-white cols in y 356..366 ==")
seg = ink[356:366, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 4 and not inr:
        s = i; inr = True
    elif v <= 4 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  mid bar blobs:", [(a, b, b - a) for a, b in runs])

print("== X bar horizontal extent: non-white cols in y 470..479 ==")
seg = ink[470:479, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 4 and not inr:
        s = i; inr = True
    elif v <= 4 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  X bar blobs:", [(a, b, b - a) for a, b in runs])

print("== top bar sub-cell colors at y=266 (col2 bar x 262..296) ==")
for x in range(262, 297, 2):
    print(f"  x={x}: {tuple(img[266, x])}", end="")
print()
print("== X bar sub-cell colors at y=474 (col2 bar) ==")
for x in range(262, 297, 2):
    print(f"  x={x}: {tuple(img[474, x])}", end="")
print()

print("== blue arrows X->block: window y 451..468, blobs ==")
blue = (B > 130) & (R < 90) & (G < 90)
seg = blue[451:468, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 1 and not inr:
        s = i; inr = True
    elif v <= 1 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  X->blk blobs:", [(a, b) for a, b in runs])

print("== blue arrows block->mid: window y 402..414 (just above navy top 401) ==")
seg = blue[402:414, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 1 and not inr:
        s = i; inr = True
    elif v <= 1 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  blk->Y blobs:", [(a, b) for a, b in runs])

print("== plus circles: rows 330..352 at col1 x195..212 raw ==")
for y in range(330, 353, 2):
    print(f"  y={y}: " + " ".join(f"{tuple(img[y,x])}" for x in range(196, 213, 4)))

print("== navy block text band: white pixels inside navy rows 401..450 ==")
white = (R > 200) & (G > 200) & (B > 200)
seg = white[405:447, 170:880]
prof = seg.sum(axis=1)
for i, v in enumerate(prof):
    if v > 5: print(f"  row {i+405}: {v}")

print("== caption text rows 494..508: red text inside yellow highlight ==")
red = (R > 120) & (G < 110) & (B < 110)
seg = red[494:508, 265:560]
prof = seg.sum(axis=1)
print("  red rows:", {i + 494: int(v) for i, v in enumerate(prof) if v > 2})
colprof = seg.sum(axis=0)
cols = np.where(colprof > 0)[0]
if len(cols): print(f"  red x {cols.min()+265}..{cols.max()+265} -> slide {invx(cols.min()+265)}..{invx(cols.max()+265)}")

print("== annotations: ink rows x 60..160, y 360..470 with color classification ==")
for y in range(360, 472):
    row = img[y, 60:160]
    ink_ = (row[:, 0] < 200) | (row[:, 1] < 200) | (row[:, 2] < 200)
    n = ink_.sum()
    if n > 2:
        rr = row[ink_][:, 0].mean(); gg = row[ink_][:, 1].mean(); bb = row[ink_][:, 2].mean()
        col = "blue" if bb > rr and bb > 100 else ("orange" if rr > 150 and gg > 60 and gg < 150 else ("red" if rr > 120 and gg < 110 else f"({rr:.0f},{gg:.0f},{bb:.0f})"))
        print(f"  y={y} n={n} {col}")
