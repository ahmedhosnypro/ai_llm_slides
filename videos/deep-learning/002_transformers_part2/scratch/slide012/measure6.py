#!/usr/bin/env python3
# measure6.py — final: panel tops/bottoms, cell grids, embedding box, headers, X_2 ann
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def med(x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0))

print("=== panel vertical extent: pastel fill rows per panel ===")
green = (np.abs(r - 201) < 22) & (np.abs(g - 239) < 18) & (np.abs(b - 201) < 22)
orange = (np.abs(r - 245) < 18) & (np.abs(g - 223) < 18) & (np.abs(b - 192) < 22)
lav = (np.abs(r - 201) < 22) & (np.abs(g - 201) < 22) & (np.abs(b - 242) < 18)
for name, m, x0, x1 in [("green", green, 245, 393), ("orange", orange, 411, 559), ("lavender", lav, 571, 719)]:
    sub = m[:, x0:x1]
    rowc = sub.sum(axis=1)
    ys = [y for y in range(100, 400) if rowc[y] > 20]
    if ys: print(f"{name}: fy {ys[0]}..{ys[-1]} (fill rows)")
    print(f"  fill sample (mid):", med(x0 + 60, (ys[0]+ys[-1])//2 if ys else 250, x0 + 64, (ys[0]+ys[-1])//2 + 4 if ys else 254))

print("\n=== panel header text: dark ink rows fy 140..175 per panel ===")
ink = (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b) > 50) | (np.maximum(np.maximum(r, g), b) < 160)
for name, x0, x1 in [("H1", 245, 393), ("H2", 411, 559), ("H3", 571, 719)]:
    for y in range(140, 178):
        xs = np.where(ink[y, x0:x1])[0]
        if len(xs) > 3:
            print(f"{name} fy {y}: fx {xs.min()+x0}..{xs.max()+x0} n={len(xs)}")
    print()

print("=== cell grid: white squares inside H1 (fx 245..393) fy 175..340 ===")
white = (r > 240) & (g > 240) & (b > 240)
sub = white[175:340, 245:393]
rowc = sub.sum(axis=1)
bands = []
for i, n in enumerate(rowc):
    y = i + 175
    if n > 30:
        if bands and y - bands[-1][1] <= 3: bands[-1] = (bands[-1][0], y)
        else: bands.append((y, y))
print("H1 white-cell row bands:", bands)
# cols within first band
if bands:
    y0, y1 = bands[0]
    colc = white[y0:y1 + 1, 245:393].sum(axis=0)
    xs = [x + 245 for x in range(148) if colc[x] > 3]
    print("H1 row1 white cols:", (xs[0], xs[-1]) if xs else None, "n", len(xs))
    # find col groups
    groups = []
    if xs:
        s = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x - prev > 3: groups.append((s, prev)); s = x
            prev = x
        groups.append((s, prev))
    print("H1 row1 cell col groups:", groups)

print("\n=== embedding box: pink rect + 4 circles ===")
pink = (r - g > 18) & (b - g > 4) & (r > 225) & (r < 255) & (b > 200) & (b < 252)
sub = pink[155:245, 90:260]
ys, xs = np.where(sub)
if len(ys) > 50:
    print("pink box: fx", xs.min() + 90, "..", xs.max() + 90, "fy", ys.min() + 155, "..", ys.max() + 155, "n", len(ys))
    print("pink fill sample:", med(120, 200, 130, 210))
# circles: white runs inside pink box at its vertical middle
white = (r > 240) & (g > 240) & (b > 240)
yc = 195
xs = np.where(white[yc, 90:280])[0]
groups = []
if len(xs):
    s = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x - prev > 3: groups.append((s + 90, prev + 90)); s = x
        prev = x
    groups.append((s + 90, prev + 90))
print(f"white runs at fy {yc} (embed circles):", groups)
# circle vertical extent at first run
if groups:
    cx0 = (groups[0][0] + groups[0][1]) // 2
    ys2 = np.where(white[150:260, cx0])[0]
    if len(ys2): print(f"circle at fx {cx0}: fy {ys2.min()+150}..{ys2.max()+150}")

print("\n=== X_2 magenta annotation + arrow (H2 panel, fx 480..560, fy 250..335) ===")
mag = (r > 130) & (b > 130) & (g < 110) & (r - g > 60) & (b - g > 50)
sub = mag[245:340, 460:560]
ys, xs = np.where(sub)
if len(ys) > 3:
    print("magenta: fx", xs.min() + 460, "..", xs.max() + 460, "fy", ys.min() + 245, "..", ys.max() + 245, "n", len(ys))
else:
    print("magenta none:", len(ys))
    # looser
    mag2 = (r - g > 40) & (b - g > 30) & (r > 120) & (b > 120)
    sub = mag2[230:345, 440:570]
    ys, xs = np.where(sub)
    if len(ys) > 3:
        print("magenta(loose): fx", xs.min() + 440, "..", xs.max() + 440, "fy", ys.min() + 230, "..", ys.max() + 230, "n", len(ys))

print("\n=== H2/H3 red rims of saturated y1 squares (strip fills?) fy 355..390 ===")
print("strip1 y1 fill:", med(262, 365, 280, 375))
print("strip2 y1 fill:", med(425, 365, 443, 375))
print("strip3 y1 fill:", med(587, 365, 603, 375))
print("strip1 y2 fill:", med(298, 365, 312, 375))
print("strip fills between boxes:", med(390, 370, 400, 375), med(560, 370, 568, 375), med(713, 370, 719, 375))

print("\n=== badges/chrome cross-check ===")
print("badge yellow sample:", med(875, 70, 880, 74))
print("chrome red border left:", med(58, 300, 60, 304))
