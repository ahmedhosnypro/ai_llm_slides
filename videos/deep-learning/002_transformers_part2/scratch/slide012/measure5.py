#!/usr/bin/env python3
# measure5.py — targeted: canvas, pink box, panels/headers, cell grids, mystery strokes
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def med(x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0))

print("=== chrome bg samples ===")
for pt in [(100, 300), (480, 355), (870, 300), (120, 200), (750, 460)]:
    print(pt, med(pt[0], pt[1], pt[0] + 4, pt[1] + 4))

print("\n=== white canvas detection (strict >246) ===")
white = (r > 246) & (g > 246) & (b > 246)
# column profile in fy 200..460
colc = white[200:460, :].sum(axis=0)
xs = [x for x in range(60, 900) if colc[x] > 120]
print("white cols:", (xs[0], xs[-1]) if xs else None, "n:", len(xs))
gaps = []
if xs:
    prev = xs[0]
    for x in xs[1:]:
        if x - prev > 8: gaps.append((prev, x))
        prev = x
    print("gaps:", gaps)
rowc = white[:, 100:800].sum(axis=1)
ys = [y for y in range(100, 520) if rowc[y] > 150]
print("white rows:", (ys[0], ys[-1]) if ys else None)

print("\n=== pink embedding box (r-g>18, b-g>6, r>230) ===")
pink = (r - g > 18) & (b - g > 4) & (r > 225) & (b < 250)
ys, xs = np.where(pink)
if len(ys) > 200:
    print("n=", len(ys), "fx", xs.min(), "..", xs.max(), "fy", ys.min(), "..", ys.max())
    # largest blob region: histogram over fy
    import collections
    cnt = collections.Counter(ys // 10 * 10)
    print("fy hist:", sorted(cnt.items())[:20])
    cnt2 = collections.Counter(xs // 10 * 10)
    print("fx hist:", sorted(cnt2.items())[:20])

print("\n=== panel bounds (strict pastel fills) ===")
green = (np.abs(r - 201) < 22) & (np.abs(g - 239) < 18) & (np.abs(b - 201) < 22)
orange = (np.abs(r - 245) < 18) & (np.abs(g - 223) < 18) & (np.abs(b - 192) < 22)
lav = (np.abs(r - 201) < 22) & (np.abs(g - 201) < 22) & (np.abs(b - 242) < 18)
for name, m in [("green", green), ("orange", orange), ("lavender", lav)]:
    ys, xs = np.where(m)
    if len(ys) > 300:
        print(f"{name}: n={len(ys)} fx {np.percentile(xs,0.5):.0f}..{np.percentile(xs,99.5):.0f} fy {np.percentile(ys,0.5):.0f}..{np.percentile(ys,99.5):.0f}")

print("\n=== dark-red panel headers (maroon ~ (136,0,21)? sample) ===")
for y in [155, 158, 160, 163, 166]:
    xs = np.where((r[y, 240:760] > 90) & (r[y, 240:760] < 190) & (g[y, 240:760] < 80) & (b[y, 240:760] < 80))[0]
    if len(xs):
        print(f"fy {y}: maroon fx {xs.min()+240}..{xs.max()+240} n={len(xs)}")

print("\n=== cell grid per panel: white-cell col bands fy 200..320 ===")
white2 = (r > 240) & (g > 240) & (b > 240)
wc = white2[200:320, :]
colc2 = wc.sum(axis=0)
bands = []
s = None
for x in range(60, 900):
    v = colc2[x] > 25
    if v and s is None: s = x
    if not v and s is not None:
        if x - s > 6: bands.append((s, x - 1))
        s = None
print("white col bands:", bands)

print("\n=== ASCII map: fx 190..320, fy 340..400 (mystery stroke + =) ===")
br = (r > 140) & (g < 95) & (b < 95)
for y in range(340, 400, 2):
    row = "".join("#" if br[y, x] else "." for x in range(190, 320, 2))
    print(f"fy {y:3d} {row}")

print("\n=== ASCII map: fx 690..745, fy 340..395 (short brace) ===")
for y in range(340, 395, 2):
    row = "".join("#" if br[y, x] else "." for x in range(690, 745, 1))
    print(f"fy {y:3d} {row}")

print("\n=== title underline check fy 74..82, fx 200..900 ===")
ink = (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b) > 50) | (np.maximum(np.maximum(r, g), b) < 160)
for y in range(74, 84):
    xs = np.where(ink[y, 100:905])[0]
    if len(xs) > 5:
        print(f"fy {y}: fx {xs.min()+100}..{xs.max()+100} n={len(xs)}")

print("\n=== title/subtitle ink extents (excl chrome fx<62, fx>898) ===")
for (y0, y1, nm) in [(56, 78, "title"), (80, 97, "subtitle")]:
    m = ink[y0:y1, 62:898]
    xs = np.where(m.any(axis=0))[0]
    ys_ = np.where(m.any(axis=1))[0]
    if len(xs): print(f"{nm}: fx {xs.min()+62}..{xs.max()+62} fy {y0+ys_.min()}..{y0+ys_.max()}")

print("\n=== embedding label lines fy 125..155 (x 60..300) ===")
for y in range(125, 156):
    xs = np.where(ink[y, 60:320])[0]
    if len(xs) > 3:
        print(f"fy {y}: fx {xs.min()+60}..{xs.max()+60} n={len(xs)}")

print("\n=== embedding circles (white circles with red rims in pink box) ===")
# red rims in the embedding area
emb = br[160:260, 60:320]
ys, xs = np.where(emb)
if len(ys): print("red ink in embed area: fx", xs.min()+60, "..", xs.max()+60, "fy", ys.min()+160, "..", ys.max()+160)

print("\n=== magenta annotation (strict: r>140,b>140,g<100) in fy 260..330 ===")
mag = (r > 140) & (b > 140) & (g < 100)
sub = mag[255:335, 240:560]
ys, xs = np.where(sub)
if len(ys) > 5:
    print("magenta: fx", xs.min()+240, "..", xs.max()+240, "fy", ys.min()+255, "..", ys.max()+255, "n", len(ys))
else:
    print("magenta: none", len(ys))
