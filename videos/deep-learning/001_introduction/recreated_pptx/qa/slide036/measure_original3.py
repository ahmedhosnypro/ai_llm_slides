#!/usr/bin/env python3
"""Measure pass 3: precise geometry — slab quads per face, column outline, dashes,
filter, X, =, +, neuron, labels, arrows, question, equation, title lines."""
from PIL import Image
import numpy as np
from collections import Counter

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
lum = a.sum(axis=2) / 3

def modal(x0, y0, x1, y1, exclude_light=True):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    if exclude_light:
        sub = sub[sub.sum(axis=1) < 700]
    return Counter(map(tuple, sub)).most_common(5)

def ink_bbox(x0, y0, x1, y1, thresh=150, name=""):
    sub = lum[y0:y1, x0:x1]
    ys, xs = np.where(sub < thresh)
    if not len(xs):
        print(f"{name}: EMPTY"); return None
    bb = (x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()))
    print(f"{name}: x {bb[0]}..{bb[2]}  y {bb[1]}..{bb[3]}  ({bb[2]-bb[0]+1}x{bb[3]-bb[1]+1})")
    return bb

def colmask_bbox(x0, y0, x1, y1, target, tol, name=""):
    sub = a[y0:y1, x0:x1]
    d = np.abs(sub - np.array(target)).sum(axis=2)
    m = d < tol
    ys, xs = np.where(m)
    if not len(xs):
        print(f"{name}: EMPTY"); return None
    bb = (x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()))
    print(f"{name}: x {bb[0]}..{bb[2]}  y {bb[1]}..{bb[3]} ({bb[2]-bb[0]+1}x{bb[3]-bb[1]+1}) n={int(m.sum())}")
    return bb

print("== FACE COLORS (modal of flat interiors) ==")
print("slab main face:", modal(300, 280, 345, 300))
print("slab left face:", modal(229, 300, 240, 330))
print("slab top face:", modal(300, 205, 340, 214))
print("slab outline (top edge dark):", modal(280, 216, 320, 222))
print("filter main face:", modal(435, 285, 465, 305))
print("filter left face:", modal(417, 285, 424, 310))
print("filter top face:", modal(435, 252, 460, 260))
print("dash color:", modal(365, 330, 410, 338))
print("X color:", modal(388, 246, 412, 264))
print("= color:", modal(505, 285, 538, 305))
print("+ color:", modal(550, 305, 568, 325))
print("neuron ring:", modal(575, 285, 610, 315))
print("neuron center:", modal(585, 292, 605, 306))
print("title red:", modal(200, 65, 750, 85))
print("question ink:", modal(160, 418, 790, 448))
print("equation red:", modal(330, 455, 595, 482))

print("\n== SLAB QUADS per face ==")
main = np.abs(a - np.array([175, 103, 18])).sum(axis=2) < 75
top = np.abs(a - np.array([122, 70, 14])).sum(axis=2) < 75
left = np.abs(a - np.array([200, 120, 25])).sum(axis=2) < 60
for name, m in [("main", main), ("top", top), ("left?", left)]:
    sub = m[190:400, 210:380]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"{name}: x {210+xs.min()}..{210+xs.max()} y {190+ys.min()}..{190+ys.max()} n={len(xs)}")
print("-- main face per-column top/bottom (clean cols) --")
for x in list(range(244, 360, 8)):
    col = np.where(main[190:400, x])[0]
    if len(col):
        print(f"  x={x}: {190+col.min()}..{190+col.max()}")
print("-- top face per-column --")
for x in list(range(244, 360, 8)):
    col = np.where(top[190:400, x])[0]
    if len(col):
        print(f"  x={x}: {190+col.min()}..{190+col.max()} n={len(col)}")

print("\n== CYAN COLUMN OUTLINE (tight cyan 41,171,226 tol 90) ==")
oc = np.abs(a - np.array([41, 171, 226])).sum(axis=2) < 90
sub = oc[230:345, 220:295]
ys, xs = np.where(sub)
print("outline bbox:", (220 + xs.min(), 230 + ys.min(), 220 + xs.max(), 230 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
for x in range(222, 292, 2):
    col = np.where(oc[230:345, x])[0]
    if len(col):
        print(f"  x={x}: {230+col.min()}..{230+col.max()} n={len(col)}")

print("\n== DASHED LINES (x 362..414, tighter cyan tol 130) ==")
dm = np.abs(a - np.array([86, 196, 240])).sum(axis=2) < 200
sub = dm[240:345, 362:414]
rows = sub.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 2 and not inb:
        s = i; inb = True
    elif v <= 2 and inb:
        bands.append((240 + s, 240 + i - 1)); inb = False
if inb: bands.append((240 + s, 240 + 344 - 240 + 240 - 1))
print("dash row bands:", bands)
for (b0, b1) in bands:
    yc = (b0 + b1) // 2
    row = dm[yc, 220:420]
    xs2 = np.where(row)[0]
    if len(xs2):
        pat = "".join("#" if v else "." for v in row[140:200])
        print(f"  band y~{b0}..{b1} center {yc}: x {220+xs2.min()}..{220+xs2.max()} pattern[360..420]={pat}")

print("\n== FILTER per-column (cyan tol 130 + dark blue tol 120) ==")
fc = np.abs(a - np.array([41, 171, 226])).sum(axis=2) < 130
fb = np.abs(a - np.array([27, 117, 187])).sum(axis=2) < 120
for x in range(412, 480, 3):
    c = np.where(fc[240:345, x])[0]
    b = np.where(fb[240:345, x])[0]
    s = f"x={x}: cyan {240+c.min()}..{240+c.max()}" if len(c) else f"x={x}: cyan -"
    s += f" | blue {240+b.min()}..{240+b.max()} n={len(b)}" if len(b) else " | blue -"
    print(" ", s)

print("\n== X sign (blue tol 120, region 370..420 x 230..270) ==")
sub = fb[230:270, 370:420]
ys, xs = np.where(sub)
print("X bbox:", (370 + xs.min(), 230 + ys.min(), 370 + xs.max(), 230 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
for y in range(230, 270, 2):
    r = np.where(fb[y, 370:420])[0]
    if len(r):
        print(f"  y={y}: x {370+r.min()}..{370+r.max()}")

print("\n== '=' sign (region 495..545 x 275..315, dark-ish) ==")
sub = lum[275:315, 495:545] < 200
ys, xs = np.where(sub)
print("= bbox:", (495 + xs.min(), 275 + ys.min(), 495 + xs.max(), 275 + ys.max()) if len(xs) else "EMPTY")
for y in range(275, 315):
    r = np.where(lum[y, 495:545] < 200)[0]
    if len(r):
        print(f"  y={y}: x {495+r.min()}..{495+r.max()} n={len(r)}")

print("\n== '+' sign (region 545..575 x 300..330, gray lum<210) ==")
sub = lum[300:330, 545:575] < 210
ys, xs = np.where(sub)
print("+ bbox:", (545 + xs.min(), 300 + ys.min(), 545 + xs.max(), 300 + ys.max()) if len(xs) else "EMPTY")
for y in range(300, 330):
    r = np.where(lum[y, 545:575] < 210)[0]
    if len(r):
        print(f"  y={y}: x {545+r.min()}..{545+r.max()} n={len(r)}")

print("\n== NEURON ==")
oring = np.abs(a - np.array([225, 130, 30])).sum(axis=2) < 130
sub = oring[270:325, 565:630]
ys, xs = np.where(sub)
print("ring bbox:", (565 + xs.min(), 270 + ys.min(), 565 + xs.max(), 270 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
cym = np.abs(a - np.array([41, 171, 226])).sum(axis=2) < 130
sub = cym[270:325, 565:630]
ys, xs = np.where(sub)
print("center bbox:", (565 + xs.min(), 270 + ys.min(), 565 + xs.max(), 270 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))

print("\n== LABELS ==")
ink_bbox(198, 298, 232, 325, 150, "7-left")
ink_bbox(243, 315, 278, 348, 150, "7-bottom")
ink_bbox(470, 272, 505, 300, 170, "7-right-of-filter")
ink_bbox(450, 310, 480, 340, 170, "7-below-filter")
ink_bbox(410, 332, 445, 360, 170, "3-below-filter")
ink_bbox(155, 240, 250, 265, 150, "3dims-text")
ink_bbox(265, 150, 400, 212, 150, "RGB-text")
ink_bbox(150, 410, 810, 452, 150, "question")
ink_bbox(300, 450, 640, 492, 200, "equation")

print("\n== TITLE LINES ==")
ink_bbox(140, 55, 850, 96, 150, "title-L1")
ink_bbox(140, 96, 850, 140, 150, "title-L2")

print("\n== ARROWS (dark ink) ==")
# long arrow to '3' label: region between question and filter
ink_bbox(425, 340, 560, 412, 120, "arrow-to-3")
# long arrow to neuron
ink_bbox(580, 310, 690, 432, 120, "arrow-to-neuron")
# 3dims arrow (horizontal line y~265..275, x 185..275)
ink_bbox(185, 262, 280, 278, 120, "3dims-arrow")
# tiny arrows near 7 labels
ink_bbox(222, 300, 245, 322, 150, "7left-tiny-arrow")
ink_bbox(243, 322, 275, 342, 150, "7bottom-tiny-arrow")
