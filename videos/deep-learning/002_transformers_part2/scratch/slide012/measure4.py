#!/usr/bin/env python3
# measure4.py — structural bands: panels, matrices, cells, braces, outputs, results
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def med(x0, y0, x1, y1):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    m = np.median(sub, axis=0).astype(int)
    return tuple(m.tolist())

def spans_in_row(y, x0=30, x1=930, pred=None, minlen=2):
    m = pred(a[y, x0:x1]) if pred else None
    xs = np.where(m)[0]
    if len(xs) == 0: return []
    out = []
    s = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x - prev > 3:
            if prev - s >= minlen: out.append((s + x0, prev + x0))
            s = x
        prev = x
    if prev - s >= minlen: out.append((s + x0, prev + x0))
    return out

# 1) Locate the three pastel panels by scanning fy 150..340 for pastel fills
print("=== pastel fill col-profile fy 170..330 ===")
def pastel(px):
    r_, g_, b_ = px[..., 0], px[..., 1], px[..., 2]
    mx_ = np.maximum(np.maximum(r_, g_), b_)
    return (mx_ > 180) & (px.max(axis=-1) - px.min(axis=-1) > 15) & (mx_ < 252)
p = pastel(a[170:330, :])
colcnt = p.sum(axis=0)
xs = [x for x in range(30, 930) if colcnt[x] > 30]
print("pastel-heavy fx:", xs[0] if xs else None, "..", xs[-1] if xs else None)
# find gaps (panel boundaries)
gaps = []
prev = xs[0]
for x in xs[1:]:
    if x - prev > 6: gaps.append((prev, x))
    prev = x
print("gaps:", gaps)

print("=== pastel fill row-profile fx 250..800 ===")
rowcnt = p[:, 250:800].sum(axis=1)
ys = [y + 170 for y in range(160) if rowcnt[y] > 60]
print("pastel-heavy fy:", ys[0] if ys else None, "..", ys[-1] if ys else None)

# 2) sample panel fills
print("\n=== panel fill samples ===")
for x in [280, 460, 640, 700]:
    print(f"x={x} y=180:", med(x, 175, x + 4, 185))

# 3) matrix cells: white squares inside panels — scan for white boxes in fy 165..330
print("\n=== white cells inside panels (row fy 175..330, x 250..790) ===")
white = (r > 235) & (g > 235) & (b > 235)
wc = white[170:330, 250:790]
rr = wc.sum(axis=1)
bands = []
for i, n in enumerate(rr):
    y = i + 170
    if n > 40:
        if bands and y - bands[-1][1] <= 2: bands[-1] = (bands[-1][0], y)
        else: bands.append((y, y))
print("white-cell row bands fy:", bands)

# 4) red braces: tall vertical red strokes right of each matrix
print("\n=== deep-red vertical strokes fy 120..350 ===")
br = (r > 140) & (g < 90) & (b < 90)
for y in range(120, 350, 4):
    xs = np.where(br[y, 30:930])[0]
    if len(xs) > 0:
        groups = []
        s = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x - prev > 4:
                groups.append((s + 30, prev + 30)); s = x
            prev = x
        groups.append((s + 30, prev + 30))
        if y % 20 == 0 or len(groups) > 0:
            pass
        if y % 20 == 0:
            print(f"fy {y}: red groups {groups}")

# 5) bottom region fy 340..520 detailed
print("\n=== bottom region bands (any ink) fy 340..520 ===")
mx = np.maximum(np.maximum(r, g), b)
mn_ = np.minimum(np.minimum(r, g), b)
ink = (mx - mn_ > 50) | (mx < 160)
for y in range(340, 515):
    xs = np.where(ink[y, 30:930])[0]
    if len(xs) > 6:
        groups = []
        s = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x - prev > 6:
                groups.append((s + 30, prev + 30)); s = x
            prev = x
        groups.append((s + 30, prev + 30))
        print(f"fy {y}: n={len(xs):3d} groups {groups[:8]}")

# 6) blue text rows fy 340..500 (Y_2 results, y labels)
print("\n=== blue ink fy 340..500 ===")
bl = (b - r > 40) & (b - g > 30) & (b > 110)
for y in range(340, 500):
    xs = np.where(bl[y, 30:930])[0]
    if len(xs) > 4:
        groups = []
        s = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x - prev > 8:
                groups.append((s + 30, prev + 30)); s = x
            prev = x
        groups.append((s + 30, prev + 30))
        print(f"fy {y}: groups {groups[:8]}")
