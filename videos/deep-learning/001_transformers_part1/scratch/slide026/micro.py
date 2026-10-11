#!/usr/bin/env python3
"""Focused micro-structure analysis."""
import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def region_scan(name, x0, y0, x1, y1, k=10):
    reg = A[y0:y1, x0:x1].reshape(-1, 3)
    b = (reg // 8) * 8 + 4
    pal, cnt = np.unique(b, axis=0, return_counts=True)
    o = np.argsort(-cnt)[:k]
    tot = len(reg)
    s = ", ".join(f"#{pal[i][0]:02X}{pal[i][1]:02X}{pal[i][2]:02X}({100*cnt[i]//tot}%)" for i in o)
    print(f"[{name}] {s}")

def mask_blobs(name, target, tol, x0, y0, x1, y1, minpx=25, limit=16):
    sub = A[y0:y1, x0:x1]
    t = np.array(target)
    m = (np.abs(sub - t).sum(axis=2) <= tol)
    L, n = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(L)):
        mm = L[sl] == i + 1
        real = int(mm.sum())
        if real < minpx: continue
        out.append((real, x0 + sl[1].start, x0 + sl[1].stop - 1, y0 + sl[0].start, y0 + sl[0].stop - 1))
    out.sort(reverse=True)
    print(f"[{name}] {len(out)} blobs:", "; ".join(f"n{r} x{a}..{b} y{c}..{d}" for r, a, b, c, d in out[:limit]))

print("== A: Y box + green arrow (x540..660 y105..200) ==")
region_scan("A", 540, 105, 660, 200, 12)
mask_blobs("A_green", (0, 176, 80), 130, 540, 105, 660, 200, minpx=20)
mask_blobs("A_ybox_border", (0, 150, 60), 200, 540, 105, 660, 200, minpx=15)

print("\n== B: nodes/lines region (x490..775 y225..395) ==")
mask_blobs("B_white_circles", (252, 252, 250), 18, 490, 225, 775, 395, minpx=30)
mask_blobs("B_red", (220, 30, 30), 160, 490, 225, 775, 395, minpx=25, limit=20)
region_scan("B_node1_guess", 540, 236, 575, 258, 8)

print("\n== C: strip glyph structure (y485..505, x180..500) ==")
for x in range(180, 500, 4):
    c = A[494, x]
    pass
# classify columns in the strip band
band = A[487:503, 175:500]
cls = []
for x in range(band.shape[1]):
    col = band[:, x]
    med = np.median(col, axis=0)
    r, g, b = med
    if r > 240 and g > 240 and b < 215: k = "Y"       # yellow
    elif r > 230 and g < 215 and b > 190: k = "P"     # pink
    elif r > 200 and g > 170 and b > 230: k = "L"     # lavender
    elif g > r and g > b and g > 230: k = "m"         # mint fill
    elif r > 240 and g > 240 and b > 240: k = "w"     # white
    elif r < 150: k = "R"                              # red/dark
    else: k = "."
    cls.append(k)
s = "".join(cls)
print("strip cols x175..500 (Y=yellow P=pink L=lav m=mint w=white R=red):")
for i in range(0, len(s), 65):
    print(f"  x{175+i:3d}: {s[i:i+65]}")

print("\n== D: left-stack glyph row 1 (y239..254, x55..145) ==")
band = A[240:253, 55:145]
cls = []
for x in range(band.shape[1]):
    col = band[:, x]
    med = np.median(col, axis=0)
    r, g, b = med
    if r > 240 and g > 240 and b < 220: k = "Y"
    elif r > 230 and g < 220 and b > 190: k = "P"
    elif r > 200 and g > 170 and b > 230: k = "L"
    elif g > r and g > b and g > 230: k = "m"
    elif r > 240 and g > 240 and b > 240: k = "w"
    elif r < 160 and g < 160: k = "R"
    else: k = "."
    cls.append(k)
print("  " + "".join(cls) + f"   (x55+idx)")

print("\n== E: pills (y156..188) — non-peach columns ==")
band = A[156:188, 240:720]
pct = []
for x in range(band.shape[1]):
    col = band[:, x]
    nonpeach = (np.abs(col - np.array([247, 227, 206])).sum(axis=1) > 60).mean()
    pct.append(nonpeach)
runs, s = [], None
for i, v in enumerate(pct):
    if v > 0.35 and s is None: s = i
    if v <= 0.35 and s is not None: runs.append((240 + s, 240 + i - 1)); s = None
if s is not None: runs.append((240 + s, 240 + len(pct) - 1))
print("  pill-ish column runs:", runs)
# pill fill color: sample inside first run
if runs:
    a, b2 = runs[0]
    reg = A[160:184, a+3:b2-3].reshape(-1, 3)
    print("  pill1 fill median:", np.median(reg, axis=0))

print("\n== F: dashed border colors ==")
for nm, (x, y) in {"Lstack_top_border": (98, 227), "Lstack_left_border": (58, 300),
                   "Rstack_top_border": (803, 227), "strip_top_border": (300, 474),
                   "strip_left_border": (177, 494)}.items():
    c = A[y, x]; print(f"  {nm:20s} ({x},{y}) #{c[0]:02X}{c[1]:02X}{c[2]:02X}")

print("\n== G: red line cores (min-lum pixel along lines) ==")
for nm, (x0, x1, y) in {"stackrow1_line": (150, 250, 246), "wline1": (600, 750, 247),
                        "wline4": (600, 750, 372), "query": (294, 302, 440)}.items():
    seg = A[y, x0:x1]
    i = np.argmin(seg.sum(axis=1))
    c = seg[i]
    print(f"  {nm:16s} y={y} darkest@x{x0+i}: #{c[0]:02X}{c[1]:02X}{c[2]:02X} {tuple(c)}")

print("\n== H: X2 highlight ==")
mask_blobs("H_border", (200, 0, 150), 220, 255, 468, 345, 512, minpx=12, limit=8)
region_scan("H_x2_glyph", 262, 474, 336, 508, 10)

print("\n== I: dashed feed curves ==")
mask_blobs("I_left", (150, 200, 90), 190, 30, 390, 200, 480, minpx=15, limit=12)
mask_blobs("I_right", (150, 200, 90), 190, 840, 380, 920, 490, minpx=15, limit=12)
region_scan("I_leftzone", 40, 395, 180, 475, 10)
region_scan("I_rightzone", 845, 380, 920, 490, 10)

print("\n== J: subtitle red tokens ==")
sub = A[78:102, 180:800]
m = (sub[:, :, 0] > 130) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
L, n = ndimage.label(m)
for i, sl in enumerate(ndimage.find_objects(L)):
    mm = L[sl] == i + 1
    if mm.sum() < 8: continue
    print(f"  red token x{180+sl[1].start}..{180+sl[1].stop-1} y{78+sl[0].start}..{78+sl[0].stop-1} n={int(mm.sum())}")
sat = sub[(sub[:, :, 0] > 130) & (sub[:, :, 1] < 90)]
if len(sat): print("  red core median:", np.median(sat, axis=0))

print("\n== K: title/subtitle ink bboxes (dark px) ==")
for nm, (yy0, yy1) in {"line1": (50, 79), "line2": (79, 104)}.items():
    band = A[yy0:yy1, 60:900]
    m = band.sum(axis=2) < 330
    ys, xs = np.where(m)
    print(f"  {nm}: x{60+xs.min()}..{60+xs.max()} y{yy0+ys.min()}..{yy0+ys.max()} n={len(xs)}")
