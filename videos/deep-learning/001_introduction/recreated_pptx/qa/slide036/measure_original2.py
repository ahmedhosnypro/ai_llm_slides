#!/usr/bin/env python3
"""Measure pass 2: surgical element geometry on slide_036.jpg."""
from PIL import Image
import numpy as np
from collections import Counter

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg"
im = Image.open(IM).convert("RGB")
a = np.asarray(im).astype(int)

def orange_mask(sub):
    return (np.abs(sub - np.array([175, 103, 18])).sum(axis=2) < 120)

def dark_brown_mask(sub):
    return (np.abs(sub - np.array([120, 68, 12])).sum(axis=2) < 110)

print("== slab quad: orange top/bottom per column (tol 120) ==")
for x in range(218, 366, 6):
    col = orange_mask(a[190:400, x:x+1, :])
    idx = np.where(col)[0]
    if len(idx):
        print(f"x={x}: y {190+idx.min()}..{190+idx.max()}  (h={idx.max()-idx.min()+1})")

print("\n== slab left/right per row ==")
for y in range(200, 400, 8):
    row = orange_mask(a[y:y+1, 200:380, :])
    idx = np.where(row)[0]
    if len(idx):
        print(f"y={y}: x {200+idx.min()}..{200+idx.max()}")

print("\n== dark brown (top/side face) per column x 210..380 ==")
for x in range(218, 380, 6):
    col = dark_brown_mask(a[150:400, x:x+1, :])
    idx = np.where(col)[0]
    if len(idx):
        print(f"x={x}: y {150+idx.min()}..{150+idx.max()} n={len(idx)}")

print("\n== dark brown modal in top strip (300..370, 195..215) ==")
sub = a[195:215, 300:370].reshape(-1, 3)
print(Counter(map(tuple, sub)).most_common(6))

print("\n== cyan column on slab face: cyan pixels x 215..355 ==")
cyan = (np.abs(a - np.array([41, 171, 226])).sum(axis=2) < 240)
sub = cyan[220:350, 215:358]
ys, xs = np.where(sub)
print("cyan col bbox:", 215 + xs.min(), 220 + ys.min(), 215 + xs.max(), 220 + ys.max(), "n=", len(xs))
# column edges: cyan presence per column
for x in range(215, 358, 4):
    col = cyan[220:350, x:x+1].reshape(-1)
    idx = np.where(col)[0]
    if len(idx):
        print(f"  x={x}: cyan y {220+idx.min()}..{220+idx.max()} n={len(idx)}")

print("\n== column interior modal (x 240..275, y 270..310) ==")
sub = a[270:310, 240:275].reshape(-1, 3)
print(Counter(map(tuple, sub)).most_common(6))

print("\n== dashed lines: cyan pixels right of slab x 362..425 ==")
sub = cyan[240:340, 362:425]
rowcount = sub.sum(axis=1)
runs = []
inrun = False
for i, v in enumerate(rowcount):
    if v > 0 and not inrun:
        start = i; inrun = True
    elif v == 0 and inrun:
        runs.append((240 + start, 240 + i - 1)); inrun = False
if inrun: runs.append((240 + start, 240 + len(rowcount) - 1))
print("cyan line row-bands:", runs)
print("modal cyan of dashes:", Counter(map(tuple, a[250:330, 365:420].reshape(-1, 3)[(np.abs(a[250:330, 365:420].reshape(-1,3) - np.array([86,196,240])).sum(axis=1) < 150)])).most_common(4))
# dash pattern along the middle band
if runs:
    mid = (runs[0][0] + runs[0][1]) // 2
    row = cyan[mid:mid+1, 360:430].reshape(-1)
    print(f"dash pattern row y={mid}:", "".join("#" if v else "." for v in row))

print("\n== filter slab: cyan + dark blue x 405..495 ==")
sub = a[240:350, 405:495]
mc = np.abs(sub - np.array([41, 171, 226])).sum(axis=2) < 200
md = np.abs(sub - np.array([27, 117, 187])).sum(axis=2) < 160
ys, xs = np.where(mc)
print("filter cyan bbox:", (405 + xs.min(), 240 + ys.min(), 405 + xs.max(), 240 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
ys, xs = np.where(md)
print("filter darkblue bbox:", (405 + xs.min(), 240 + ys.min(), 405 + xs.max(), 240 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
for x in range(405, 495, 3):
    c1 = mc[:, x - 405]; c2 = md[:, x - 405]
    i1 = np.where(c1)[0]; i2 = np.where(c2)[0]
    if len(i1) or len(i2):
        s = f"x={x}: cyan {240+i1.min()}..{240+i1.max()}" if len(i1) else f"x={x}: cyan -"
        s += f" | dark {240+i2.min()}..{240+i2.max()} n={len(i2)}" if len(i2) else " | dark -"
        print(" ", s)

print("\n== blue X sign ==")
bx = (np.abs(a - np.array([27, 117, 187])).sum(axis=2) < 200)
sub = bx[225:270, 370:430]
ys, xs = np.where(sub)
print("X bbox:", (370 + xs.min(), 225 + ys.min(), 370 + xs.max(), 225 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
print("X modal:", Counter(map(tuple, a[225:270, 370:430][sub])).most_common(3))

print("\n== '=' sign (dark, x 495..545) ==")
lum = a.sum(axis=2) / 3
sub = lum[265:310, 495:545] < 120
ys, xs = np.where(sub)
print("= bbox:", (495 + xs.min(), 265 + ys.min(), 495 + xs.max(), 265 + ys.max()) if len(xs) else "EMPTY")
print("= modal:", Counter(map(tuple, a[265:310, 495:545][sub])).most_common(3))

print("\n== '+' sign (gray, x 545..570) ==")
sub = lum[295:330, 545:572] < 190
ys, xs = np.where(sub)
print("+ bbox:", (545 + xs.min(), 295 + ys.min(), 545 + xs.max(), 295 + ys.max()) if len(xs) else "EMPTY")
print("+ modal:", Counter(map(tuple, a[295:330, 545:572][sub])).most_common(5))

print("\n== neuron icon (x 570..630) ==")
orange_ring = np.abs(a - np.array([232, 134, 46])).sum(axis=2) < 170
sub = orange_ring[265:330, 565:635]
ys, xs = np.where(sub)
print("neuron orange bbox:", (565 + xs.min(), 265 + ys.min(), 565 + xs.max(), 265 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
cy = (np.abs(a - np.array([41, 171, 226])).sum(axis=2) < 200)
sub = cy[265:330, 565:635]
ys, xs = np.where(sub)
print("neuron cyan bbox:", (565 + xs.min(), 265 + ys.min(), 565 + xs.max(), 265 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
print("neuron ring modal:", Counter(map(tuple, a[265:330, 565:635][orange_ring[265:330, 565:635]])).most_common(3))
