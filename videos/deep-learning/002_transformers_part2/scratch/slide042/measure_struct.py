#!/usr/bin/env python3
"""Decisive structure scans for slide_042:
(a) middle grid column count via bright-green runs on scanlines
(b) right block fine hue-class map (2px)
(c) blue content frame bbox
(d) label box red borders (loose threshold)
(e) whitish sliver in right block
(f) left stack cube boundaries
(g) median core colors of each colored region
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def med(x0, y0, x1, y1, cond):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    m = cond(reg)
    if m.sum() == 0: return None, 0
    return tuple(int(np.median(reg[m, i])) for i in range(3)), int(m.sum())

print("=== (a) MIDDLE GRID column scan: bright green runs, y=280..410 step 10, x370..520 ===")
green = (g > 150) & (g - r > 60) & (g - b > 100)
for y in range(280, 411, 10):
    xs = np.nonzero(green[y, 370:520])[0]
    if len(xs) == 0: continue
    runs = []
    st = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x > prev + 2:
            runs.append((370 + st, 370 + prev)); st = x
        prev = x
    runs.append((370 + st, 370 + prev))
    print(f"  y{y}: {len(runs)} runs: {runs}")

print()
print("=== (f) LEFT STACK cube rows: green runs x165..215, y255..435 step 5 ===")
for y in range(255, 436, 5):
    xs = np.nonzero(green[y, 165:216])[0]
    if len(xs) == 0:
        print(f"  y{y}: none")
    else:
        print(f"  y{y}: x {165+xs.min()}..{165+xs.max()} n={len(xs)}")

print()
print("=== (c) BLUE content frame: blue border pixels (b>r+40, b>110, b-g>20) ===")
blue = (b > 110) & (b - r > 40) & (b - g > 20)
ys, xs = np.nonzero(blue)
print(f"  all blue bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
# vertical lines: cols with many blue pixels
cc = blue.sum(axis=0)
print("  blue cols count>200:", [(x, int(cc[x])) for x in range(W) if cc[x] > 200])
rc = blue.sum(axis=1)
print("  blue rows count>200:", [(y, int(rc[y])) for y in range(H) if rc[y] > 200])

print()
print("=== (d) label box red borders: loose red (r>90, r-g>40, r-b>40) long horiz runs y150..280 ===")
loose = (r > 90) & (r - g > 40) & (r - b > 40)
for y in range(150, 281):
    xs = np.nonzero(loose[y, 60:900])[0]
    if len(xs) < 100: continue
    # find long runs
    runs = []
    st = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x > prev + 3:
            if prev - st > 30: runs.append((60 + st, 60 + prev))
            st = x
        prev = x
    if prev - st > 30: runs.append((60 + st, 60 + prev))
    if runs: print(f"  y{y}: {runs}")

print()
print("=== (d2) label box vertical borders: loose red long vert runs x60..900, y150..280 ===")
for x in range(60, 900):
    ys2 = np.nonzero(loose[150:280, x])[0]
    if len(ys2) < 40: continue
    runs = []
    st = ys2[0]; prev = ys2[0]
    for y in ys2[1:]:
        if y > prev + 3:
            if prev - st > 20: runs.append((150 + st, 150 + prev))
            st = y
        prev = y
    if prev - st > 20: runs.append((150 + st, 150 + prev))
    if runs: print(f"  x{x}: {runs}")

print()
print("=== (e) whitish sliver in right block x640..880 y230..480: near-white not background ===")
# background inside blue frame is white; the sliver is a light-gray/white shape on colored slabs
# find pixels with r,g,b all 200..255 and low saturation, SURROUNDED by colored region — just count per row
wt = (r > 200) & (g > 200) & (b > 200) & (abs(r - g) < 25) & (abs(g - b) < 25)
print("  white-ish rows y230..330 (x640..880):")
for y in range(230, 331, 2):
    xs2 = np.nonzero(wt[y, 640:880])[0]
    if len(xs2) > 6:
        print(f"    y{y}: n={len(xs2)} x {640+xs2.min()}..{640+xs2.max()}")

print()
print("=== (g) median core colors ===")
def mmed(name, x0, y0, x1, y1, cond):
    c, n = med(x0, y0, x1, y1, cond)
    print(f"  {name}: median {c} n={n}  hex={'%02X%02X%02X' % c if c else '-'}")

mmed("magenta front face", 660, 340, 740, 460, lambda p: (p[:, 0] > 120) & (p[:, 2] > 120) & (p[:, 1] < 90))
mmed("magenta side strip", 762, 390, 784, 460, lambda p: (p[:, 0] > 120) & (p[:, 2] > 120) & (p[:, 1] < 90))
mmed("green side strip (right blk)", 788, 350, 800, 450, lambda p: (p[:, 1] > 150) & (p[:, 1] - p[:, 0] > 40))
mmed("orange side strip", 808, 350, 818, 425, lambda p: (p[:, 0] > 180) & (p[:, 1] > 60) & (p[:, 1] < 180) & (p[:, 2] < 90))
mmed("yellow side strip", 826, 300, 834, 405, lambda p: (p[:, 0] > 200) & (p[:, 1] > 180) & (p[:, 2] < 120))
mmed("blue side strip", 839, 300, 842, 395, lambda p: (p[:, 2] > 130) & (p[:, 2] - p[:, 0] > 20))
mmed("mid grid front green", 390, 290, 500, 400, lambda p: (p[:, 1] > 150) & (p[:, 1] - p[:, 0] > 60) & (p[:, 1] - p[:, 2] > 100))
mmed("mid grid top dark", 390, 258, 500, 266, lambda p: (p[:, 1] < 120) & (p[:, 1] - p[:, 0] > 10))
mmed("left stack front", 175, 280, 205, 420, lambda p: (p[:, 1] > 150) & (p[:, 1] - p[:, 0] > 60) & (p[:, 1] - p[:, 2] > 100))
mmed("left stack top dark", 175, 266, 205, 274, lambda p: (p[:, 1] < 120) & (p[:, 1] - p[:, 0] > 10))
mmed("title red", 300, 80, 700, 100, lambda p: (p[:, 0] > 140) & (p[:, 0] - p[:, 1] > 70) & (p[:, 0] - p[:, 2] > 70))
mmed("blue frame", 888, 250, 892, 450, lambda p: (p[:, 2] > 90) & (p[:, 2] - p[:, 0] > 30))
