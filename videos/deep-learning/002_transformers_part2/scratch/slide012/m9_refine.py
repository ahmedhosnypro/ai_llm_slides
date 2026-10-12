#!/usr/bin/env python3
# m9_refine.py — slide 012 refinement: panels, cells, strips, braces, results, magenta, title parts
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r + g + b) / 3

def med(x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0))

def spans(mask1d, base=0, minlen=2):
    out, s = [], None
    for i, v in enumerate(mask1d):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((base + s, base + i - 1))
            s = None
    if s is not None: out.append((base + s, base + len(mask1d) - 1))
    return out

print("=== A. PANEL EDGES (per-panel col/row scans) ===")
# fill predicates tuned to measured samples: H1 (214,255,230) H2 (247,231,208) H3 (212,212,250)
def pastel(c, tol=22):
    return (np.abs(r - c[0]) < tol) & (np.abs(g - c[1]) < tol) & (np.abs(b - c[2]) < tol)
P1, P2, P3 = pastel((214, 255, 230)), pastel((247, 231, 208)), pastel((212, 212, 250))
for nm, m, xm in [("H1", P1, 320), ("H2", P2, 485), ("H3", P3, 645)]:
    col = np.where(m[150:360, xm])[0] + 150
    row = np.where(m[195, x0:x1] if False else m[195, :])[0]  # placeholder
    # column extent at mid-row fy 250
    row2 = np.where(m[250, :])[0]
    # restrict to panel zone
    z = {'H1': (235, 400), 'H2': (400, 570), 'H3': (560, 740)}[nm]
    row2 = row2[(row2 >= z[0]) & (row2 <= z[1])]
    col = col[(col >= 140) & (col <= 360)]
    print(f"{nm}: fy {col.min()}..{col.max()} (mid-col fx {xm})   fx {row2.min()}..{row2.max()} (mid-row fy 250)")
print("panel borders: H1 left edge col fx 244..247 sample", med(245, 250, 247, 254))
# header rows precise: any dark ink in header bands
ink = (lum < 205)
for (x0, x1, nm) in [(235, 400, "H1hdr"), (400, 570, "H2hdr"), (560, 740, "H3hdr")]:
    m = ink[130:165, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 10:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+130}..{ys.max()+130} n={len(ys)}")

print("\n=== B. CELL BOXES per panel (rim-anchored) ===")
# rims: olive/dark border of each cell; scan for cell rectangles via cream fill > and rim darkness
cream = (r > 235) & (g > 225) & (b < 240) & (b > 150)
for nm, (x0, x1) in [("H1", (240, 400)), ("H2", (402, 568)), ("H3", (562, 730))]:
    m = cream[150:345, x0:x1]
    colc = m.sum(axis=0); rowc = m.sum(axis=1)
    cb = spans(colc > 8, x0, 6)
    rb = spans(rowc > 8, 150, 4)
    print(f"{nm} cream col bands: {cb}")
    print(f"{nm} cream row bands: {rb}")
# cell fill + rim color from a clean cell interior and its border
print("cell interior H1c1:", med(270, 182, 276, 188), " H2c1:", med(424, 182, 430, 188))
print("cell rim: H1 top edge of r1c2:", med(304, 176, 310, 179))

print("\n=== C. ROW GLYPH COLORS per panel (W_ij labels) ===")
# sample dark glyph cores per row band per panel (threshold: saturation-ish dark)
for nm, (x0, x1) in [("H1", (245, 395)), ("H2", (410, 560)), ("H3", (572, 722))]:
    for (ry0, ry1, rn) in [(172, 198, "r1"), (209, 236, "r2"), (250, 278, "r3"), (289, 316, "r4")]:
        zone = a[ry0:ry1, x0:x1].reshape(-1, 3)
        # glyph pixels: strongly colored or dark
        zd = zone[(zone.sum(axis=1) < 430)]
        if len(zd) > 4:
            print(f"{nm} {rn}: modal-dark", tuple(int(v) for v in np.median(zd, axis=0)), "n=", len(zd))
        else:
            print(f"{nm} {rn}: (none) n={len(zd)}")

print("\n=== D. STRIPS: exact bounds, fills between cells, y-cell boxes ===")
# scan fy 370 for pastel runs
for nm, m, z in [("s1", P1, (235, 400)), ("s2", P2, (400, 570)), ("s3", P3, (560, 740))]:
    row = np.where(m[368, :])[0]
    row = row[(row >= z[0]) & (row <= z[1])]
    col = np.where(m[340:395, (z[0]+z[1])//2])[0] + 340
    if len(row) and len(col):
        print(f"{nm}: fx {row.min()}..{row.max()} (fy368)  fy {col.min()}..{col.max()} (mid)")
print("strip fills between cells: s1", med(289, 362, 292, 368), " s2", med(452, 362, 455, 368), " s3", med(612, 362, 615, 368))
# y-cell rects: rims are darker; use 'any ink' groups at fy 360..382 (from measure4)
inkm = (lum < 215)
m = inkm[356:386, 240:740]
colc = m.sum(axis=0)
print("y-cell ink col bands:", spans(colc > 8, 240, 5))
rowb = spans(m.sum(axis=1) > 30, 356, 3)
print("y-cell ink row bands:", rowb)
# first-cell saturated fills: sample inside first y-cell of each strip
print("y1 fills: s1", med(262, 364, 272, 374), " s2", med(425, 364, 435, 374), " s3", med(587, 364, 597, 374))
# y-label color per strip (glyph cores inside cells, excluding rims)
for nm, (x0, x1) in [("s1", (250, 395)), ("s2", (412, 560)), ("s3", (574, 720))]:
    zone = a[360:382, x0:x1].reshape(-1, 3)
    zd = zone[(zone.sum(axis=1) < 400)]
    if len(zd):
        print(f"{nm} y-glyph cores:", tuple(int(v) for v in np.median(zd, axis=0)), "n=", len(zd))

print("\n=== E. BRACES (loose) ===")
loose_red = (r - g > 30) & (r - b > 25) & (r > 140)
for (x0, x1, nm, y0, y1) in [(388, 416, "brace1", 120, 360), (554, 580, "brace2", 120, 360),
                              (712, 742, "brace3", 120, 360), (712, 745, "shortb", 340, 400)]:
    m = loose_red[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 3:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
# brace stroke x-position per row (brace1)
m = loose_red[140:340, 388:416]
for yy in [140, 160, 180, 200, 220, 240, 245, 250, 260, 280, 300, 320, 335]:
    seg = np.where(loose_red[yy, 388:416])[0]
    if len(seg):
        print(f"brace1 fy {yy}: fx {seg.min()+388}..{seg.max()+388}")
# short brace rows
for yy in [348, 352, 356, 360, 364, 368, 372, 376, 380, 384, 388]:
    seg = np.where(loose_red[yy, 712:745])[0]
    if len(seg):
        print(f"shortb fy {yy}: fx {seg.min()+712}..{seg.max()+712}")

print("\n=== F. RESULT SYMBOLS (loose blue) ===")
loose_blue = (b - r > 25) & (b > 110)
for (x0, x1, nm) in [(240, 400, "res1"), (405, 565, "res2"), (565, 730, "res3")]:
    m = loose_blue[408:460, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 5:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+408}..{ys.max()+408} n={len(ys)}")
        for yy in range(408, 460):
            seg = np.where(m[yy - 408, :])[0]
            if len(seg) > 2:
                print(f"   fy {yy}: fx {seg.min()+x0}..{seg.max()+x0} n={len(seg)}")
zone = a[410:455, 240:730].reshape(-1, 3)
zb = zone[(zone[:, 2] - zone[:, 0] > 45) & (zone[:, 2] > 130)]
print("result blue core:", tuple(int(v) for v in np.median(zb, axis=0)) if len(zb) else None, "n=", len(zb))

print("\n=== G. MAGENTA ZONE (Head 2 bottom, ASCII) ===")
mag = (r - g > 40) & (b - g > 40)
m = mag[255:340, 405:570]
ys, xs = np.where(m)
if len(ys) > 3:
    print("magenta bbox: fx", xs.min() + 405, "..", xs.max() + 405, " fy", ys.min() + 255, "..", ys.max() + 255, " n=", len(ys))
for yy in range(262, 340, 2):
    row = "".join("#" if mag[yy, x] else "." for x in range(490, 570, 1))
    print(f"fy {yy:3d} {row}")
zone = a[262:340, 480:570]
zm = zone[mag[262:340, 480:570]]
if len(zm):
    print("magenta core:", tuple(int(v) for v in np.median(zm.reshape(-1, 3), axis=0)), "n=", len(zm))

print("\n=== H. TITLE UNDERLINE + SUBTITLE RED W_q + SUBTITLE UNDERLINE ===")
# title underline segments at fy 75..79
for yy in [75, 76, 77, 78]:
    m2 = (lum[yy, 62:900] < 210)
    segs = spans(m2, 62, 4)
    print(f"fy {yy} title-band segs: {segs}")
# subtitle red pixels (W_q token?)
subred = (r - b > 45) & (r > 130)
m3 = subred[78:100, 62:900]
ys, xs = np.where(m3)
if len(ys) > 3:
    print("subtitle red-ish: fx", xs.min() + 62, "..", xs.max() + 62, " fy", ys.min() + 78, "..", ys.max() + 78, " n=", len(ys))
    zc = a[78:100, 62:900][m3]
    print("subtitle red core:", tuple(int(v) for v in np.median(zc, axis=0)))
# subtitle underline segments fy 93..98
for yy in [94, 95, 96, 97]:
    m4 = (lum[yy, 62:900] < 215)
    segs = spans(m4, 62, 4)
    print(f"fy {yy} sub-band segs: {segs}")

print("\n=== I. EMBEDDING CIRCLES ===")
# circles: white fill + red rim, inside pink box (fx ~100..248, fy ~150..195)
pinkish = (r - g > 14) & (b - g > 2) & (r > 235) & (g < 245)
m5 = pinkish[145:200, 90:260]
ys, xs = np.where(m5)
if len(ys) > 30:
    print("pink box: fx", xs.min() + 90, "..", xs.max() + 90, " fy", ys.min() + 145, "..", ys.max() + 145, "n=", len(ys))
print("pink fill:", med(110, 170, 114, 174), med(240, 170, 244, 174))
# red rims of circles
rr = (r - g > 35) & (r > 130)
m6 = rr[150:200, 95:260]
ys, xs = np.where(m6)
if len(ys):
    print("circle rims bbox: fx", xs.min() + 95, "..", xs.max() + 95, " fy", ys.min() + 150, "..", ys.max() + 150, "n=", len(ys))
# per-circle: scan rim columns at cy
mrow = rr[172, 95:260]
print("fy172 rim segs:", spans(mrow, 95, 1))
# X label color inside circles
zone = a[160:185, 100:250].reshape(-1, 3)
zb2 = zone[(zone[:, 2] - zone[:, 0] > 40) & (zone[:, 2] > 110)]
print("X-label blue core:", tuple(int(v) for v in np.median(zb2, axis=0)) if len(zb2) else None, "n=", len(zb2))

print("\n=== J. '=' color ===")
zone = a[364:380, 200:220].reshape(-1, 3)
zr = zone[(zone[:, 0] - zone[:, 1] > 40)]
print("'=' red core:", tuple(int(v) for v in np.median(zr, axis=0)) if len(zr) else None, "n=", len(zr))

print("\n=== K. mapped slide coords (certified mapping) ===")
f2s = lambda fx: (fx - 17.628) / 0.961232
f2sy = lambda fy: fy / 0.955556
for nm, fx, fy in [("title-l", 159, 58), ("title-r", 800, 74), ("sub-l", 90, 81), ("sub-r", 866, 96),
                   ("H1-tl", 245, 162), ("H3-br", 719, 335), ("strip1-l", 255, 358), ("strip3-r", 724, 383),
                   ("cap1-l", 263, 393), ("res1-l", 313, 420), ("eq-l", 204, 368), ("eq-r", 216, 376)]:
    print(f"{nm}: frame ({fx},{fy}) -> slide ({f2s(fx):.1f},{f2sy(fy):.1f})")
