#!/usr/bin/env python3
"""Left panel: inner chart bounds, corner marks, box fills (modes), circle blobs."""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
H, W = im.shape[:2]

def mode_of(x0, x1, y0, y1, exclude_dark=True):
    reg = im[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    if exclude_dark:
        keep = reg.sum(axis=1) > 240
        if keep.sum() > 10:
            reg = reg[keep]
    q = (reg // 8) * 8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    m = vals[counts.argmax()]
    return m

def show(name, x0, x1, y0, y1):
    m = mode_of(x0, x1, y0, y1)
    print(f"{name:28s} x{x0}-{x1} y{y0}-{y1} fill #{m[0]:02X}{m[1]:02X}{m[2]:02X}")

print("== LEFT inner chart corners (raw px) ==")
for (x, y) in [(58,268),(59,269),(60,270),(61,271),(62,272),(58,275),(61,280),(190,268),(189,270),(187,275),(188,290),(59,290),(60,300),(58,470),(59,480),(190,470),(189,480),(187,488),(63,490),(120,489),(120,492),(120,494)]:
    p = im[y, x]
    print(f"  ({x:3d},{y:3d}) #{p[0]:02X}{p[1]:02X}{p[2]:02X} {tuple(p)}")

print("== LEFT inner chart vertical extent (col x=120, classify tan-family vs box) ==")
col = im[:, 120]
for y in range(440, 525):
    p = col[y]
    pass
# print col x=75 (left of boxes) and x=180 (right of boxes) raw transitions
for X in (66, 75, 180, 185):
    print(f" col x={X}:")
    prev = None
    for y in range(262, 525):
        p = im[y, X]
        s = f"{p[0]:02X}{p[1]:02X}{p[2]:02X}"
        if prev is None or (abs(int(p[0])-int(prev[0]))+abs(int(p[1])-int(prev[1]))+abs(int(p[2])-int(prev[2])) > 60):
            print(f"   y={y}: #{s} {tuple(p)}")
        prev = p

print("== LEFT box fill modes ==")
show("MatMul top", 110, 168, 298, 309)
show("SoftMax", 84, 138, 332, 343)
show("Mask (opt.)", 81, 141, 365, 376)
show("Scale", 94, 128, 398, 409)
show("MatMul bottom", 85, 137, 432, 443)
show("inner chart bg", 70, 100, 276, 292)
show("panel tan", 50, 56, 300, 500)

print("== LEFT circles: blobs y448-492 ==")
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
redm = (r > 140) & (g < 100) & (b < 100)
sub = redm[448:495, 44:210]
ys, xs = np.where(sub)
if len(ys):
    # column histogram to split circles
    colsum = sub.sum(axis=0)
    print("  red col-sum (x offset +44):")
    runs = []
    inr = False
    for i, v in enumerate(colsum):
        if v > 0 and not inr:
            inr, s0 = True, i
        elif v == 0 and inr:
            inr = False
            runs.append((s0 + 44, i - 1 + 44))
    if inr:
        runs.append((s0 + 44, len(colsum) - 1 + 44))
    print("   red runs:", runs)
for x0, x1 in runs:
    sub2 = redm[448:495, x0:x1+1]
    yy, xx = np.where(sub2)
    print(f"   red blob x{x0}-{x1}: y{yy.min()+448}-{yy.max()+448}")
# dark circles (K, V)
darkm = (r < 150) & (g < 100) & (b < 130) & (r + g + b < 330) & (r > g)
sub = darkm[448:495, 44:210]
colsum = sub.sum(axis=0)
runs = []
inr = False
for i, v in enumerate(colsum):
    if v > 1 and not inr:
        inr, s0 = True, i
    elif v <= 1 and inr:
        inr = False
        runs.append((s0 + 44, i - 1 + 44))
if inr:
    runs.append((s0 + 44, len(colsum) - 1 + 44))
print("  dark-plum runs:", runs)
for x0, x1 in runs:
    sub2 = darkm[448:495, x0:x1+1]
    yy, xx = np.where(sub2)
    if len(yy) < 30:
        continue
    print(f"   plum blob x{x0}-{x1}: y{yy.min()+448}-{yy.max()+448} n={len(yy)}")

print("== LEFT circle fill modes (interior, excluding white letters) ==")
for nm, x0, x1, y0, y1 in [("Q", 82, 98, 458, 486), ("K", 120, 136, 458, 486), ("V", 158, 174, 458, 486)]:
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    keep = reg.sum(axis=1) < 500
    reg2 = reg[keep] if keep.sum() > 10 else reg
    q = (reg2 // 8) * 8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    m = vals[counts.argmax()]
    print(f"  {nm}: mode #{m[0]:02X}{m[1]:02X}{m[2]:02X}  (n_dark={keep.sum()}/{len(keep)})")
