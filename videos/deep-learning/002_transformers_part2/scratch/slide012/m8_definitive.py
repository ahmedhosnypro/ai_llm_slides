#!/usr/bin/env python3
# m8_definitive.py — slide 012 definitive measurement (this worker; prior measure1-7 banked)
# Measures chrome landmarks (mapping fit), every content region, ink colors per region.
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

print("=== 1. CHROME LANDMARKS ===")
darkred = (r > 120) & (g < 90) & (b < 90)
# vertical borders: columns with long dark-red runs in fy 50..510
colruns = darkred[50:510, :].sum(axis=0)
vcols = [x for x in range(0, W) if colruns[x] > 380]
print("vertical border cols (run>380):", vcols)
rowruns = darkred[:, 100:800].sum(axis=1)
hrows = [y for y in range(0, H) if rowruns[y] > 500]
print("horizontal border rows (run>500):", hrows)
# bottom stroke: darker red rows near 510..525 full width
for y in range(505, 530):
    xs = np.where(darkred[y, :])[0]
    if len(xs) > 700:
        print(f"bottom-stroke row fy {y}: n={len(xs)} fx {xs.min()}..{xs.max()}")
# panel gray extent: E9E9E7 (233,233,231) vs white 255
gray = (np.abs(r - 233) < 6) & (np.abs(g - 233) < 6) & (np.abs(b - 231) < 6)
grows = [y for y in range(30, 540) if gray[y, 400:500].mean() > 0.8]
print("gray-panel rows sample (x400-500):", grows[0] if grows else None, "..", grows[-1] if grows else None)
# badge: yellow FDFD96 (253,253,150)-ish in fx 840..920 fy 40..100
yel = (r > 235) & (g > 235) & (b < 200) & (b > 110)
ys, xs = np.where(yel[35:110, 830:925])
if len(ys):
    print("badge yellow bbox: fx", xs.min() + 830, "..", xs.max() + 830, " fy", ys.min() + 35, "..", ys.max() + 35,
          " center", (xs.min() + xs.max()) / 2 + 830, (ys.min() + ys.max()) / 2 + 35)
    print("badge fill sample:", med(875, 68, 880, 72))
# purple ring sample
print("badge ring sample (top of badge):", med(876, 55, 886, 58))

print("\n=== 2. TITLE / SUBTITLE ===")
ink = (lum < 200) | ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) > 45)
for (y0, y1, nm) in [(50, 80, "title"), (78, 100, "subtitle")]:
    m = ink[y0:y1, 62:898]
    xs = np.where(m.any(axis=0))[0]
    ys_ = np.where(m.any(axis=1))[0]
    if len(xs):
        print(f"{nm}: fx {xs.min()+62}..{xs.max()+62}  fy {y0+ys_.min()}..{y0+ys_.max()}")
        # row profile for cap/x-height + underline
        for yy in range(y0, y1):
            n = m[yy - y0, :].sum()
            if n > 8:
                seg = np.where(m[yy - y0, :])[0]
                print(f"   fy {yy}: n={n} fx {seg.min()+62}..{seg.max()+62}")
# title color core
tys, txs = np.where(ink[52:76, 62:898])
tpix = a[52:76, 62:898][tys, txs]
tcore = tpix[(tpix[:, 0] > 150) & (tpix[:, 1] < 80)]
print("title red core:", tuple(int(v) for v in np.median(tcore, axis=0)) if len(tcore) else None, "n=", len(tcore))
sys_, sxs = np.where(ink[80:100, 62:898])
spix = a[80:100, 62:898][sys_, sxs]
score = spix[(spix[:, 2] > 120) & (spix[:, 0] < 110)]
print("subtitle blue core:", tuple(int(v) for v in np.median(score, axis=0)) if len(score) else None, "n=", len(score))

print("\n=== 3. EMBEDDING BLOCK (fx 60..245, fy 118..265) ===")
for y in range(118, 266):
    xs = np.where(ink[y, 60:246])[0]
    if len(xs) > 3:
        print(f"   fy {y}: fx {xs.min()+60}..{xs.max()+60} n={len(xs)}")
print("embed label red core:", med(*[int(v) for v in [0, 0, 0, 0]][0:0]) if False else None)
# red text core in label zone
zone = a[125:158, 90:240]
zt = zone.reshape(-1, 3)
zred = zt[(zt[:, 0] > 140) & (zt[:, 1] < 90) & (zt[:, 2] < 90)]
print("embed label red core:", tuple(int(v) for v in np.median(zred, axis=0)) if len(zred) else None, "n=", len(zred))
# pink box
pink = (r - g > 20) & (b - g > 8) & (r > 230)
sub = pink[150:280, 60:250]
ys, xs = np.where(sub)
if len(ys) > 50:
    print("pink box: fx", xs.min() + 60, "..", xs.max() + 60, " fy", ys.min() + 150, "..", ys.max() + 150,
          "fill sample", med(150, 195, 158, 200))
# circles: red rims inside pink box
circ = darkred[150:280, 60:250]
ys, xs = np.where(circ)
print("red ink in pink zone: fx", xs.min() + 60, "..", xs.max() + 60, "fy", ys.min() + 150, "..", ys.max() + 150)

print("\n=== 4. PANELS (strict pastel) ===")
green = (np.abs(r - 201) < 26) & (np.abs(g - 239) < 16) & (np.abs(b - 201) < 26)
orange = (np.abs(r - 245) < 16) & (np.abs(g - 223) < 18) & (np.abs(b - 192) < 24)
lav = (np.abs(r - 201) < 24) & (np.abs(g - 201) < 24) & (np.abs(b - 242) < 16)
for name, m in [("green", green), ("orange", orange), ("lavender", lav)]:
    ys, xs = np.where(m[100:400, :])
    if len(ys) > 500:
        print(f"{name}: n={len(ys)} fx {np.percentile(xs,0.2):.0f}..{np.percentile(xs,99.8):.0f} fy {np.percentile(ys,0.2)+100:.0f}..{np.percentile(ys,99.8)+100:.0f}")
print("panel fill samples: H1", med(300, 160, 306, 164), "H2", med(470, 160, 476, 164), "H3", med(640, 160, 646, 164))
print("panel edge samples: H1 top", med(300, 166, 320, 169), "H1 bot", med(300, 330, 320, 333))
# panel rounded-rect border colors
print("H1 border sample (left edge):", med(246, 240, 249, 244), " H2:", med(412, 240, 415, 244), " H3:", med(572, 240, 575, 244))

print("\n=== 5. HEADERS 'W_Q of Head N' ===")
maroon = (r > 100) & (r < 200) & (g < 70) & (b < 70)
for (x0, x1, nm) in [(240, 400, "H1"), (405, 565, "H2"), (565, 730, "H3")]:
    m = maroon[115:160, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 10:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+115}..{ys.max()+115} n={len(ys)}")
zone = a[120:160, 240:730].reshape(-1, 3)
zc = zone[(zone[:, 0] > 100) & (zone[:, 0] < 200) & (zone[:, 1] < 70) & (zone[:, 2] < 70)]
print("header maroon core:", tuple(int(v) for v in np.median(zc, axis=0)) if len(zc) else None, "n=", len(zc))

print("\n=== 6. CELL GRIDS per panel ===")
cellish = (r > 235) & (g > 228) & (b < 235) & (b > 150)  # cream/yellow cell fill
for (x0, x1, nm) in [(240, 400, "H1"), (405, 565, "H2"), (565, 730, "H3")]:
    m = cellish[140:350, x0:x1]
    colc = m.sum(axis=0); rowc = m.sum(axis=1)
    cbands = [c for c in spans(colc > (rowc.max() if len(rowc) else 1) * 0 + 18, x0, 5)]
    rbands = spans(rowc > 18, 140, 5)
    print(f"{nm} cell col bands: {cbands}")
    print(f"{nm} cell row bands: {rbands}")
print("cell fill sample:", med(250, 176, 258, 182), med(420, 176, 428, 182))
# cell rim color
rim = a[170:340, 240:730].reshape(-1, 3)
rimc = rim[(rim[:, 0] > 100) & (rim[:, 0] < 190) & (rim[:, 1] > 80) & (rim[:, 1] < 160) & (rim[:, 2] < 110)]
print("cell rim core (olive):", tuple(int(v) for v in np.median(rimc, axis=0)) if len(rimc) else None, "n=", len(rimc))
# per-row text colors: sample glyph cores per row band inside H1 (fx 245..395)
# row bands measured above; sample per band
print("H1 row glyph cores (dark pixels per row band):")
for (ry0, ry1) in [(172, 196), (208, 235), (248, 278), (286, 318)]:
    zone = a[ry0:ry1, 245:395].reshape(-1, 3)
    zd = zone[zone.sum(axis=1) < 420]
    if len(zd) > 5:
        print(f"  fy {ry0}..{ry1}:", tuple(int(v) for v in np.median(zd, axis=0)), "n=", len(zd))

print("\n=== 7. BRACES (tall x3 + short) + '=' ===")
reddish = (r > 130) & (g < 100) & (b < 100)
for (x0, x1, nm, y0, y1) in [(390, 415, "brace1", 120, 350), (556, 578, "brace2", 120, 350),
                              (714, 740, "brace3", 120, 350), (714, 745, "shortbrace", 340, 400)]:
    m = reddish[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 5:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
zone = a[130:340, 392:412].reshape(-1, 3)
zc = zone[(zone[:, 0] > 140) & (zone[:, 1] < 90) & (zone[:, 2] < 90)]
print("brace red core:", tuple(int(v) for v in np.median(zc, axis=0)) if len(zc) else None, "n=", len(zc))
# '='
m = reddish[350:395, 190:235]
ys, xs = np.where(m)
if len(ys):
    print("'=': fx", xs.min() + 190, "..", xs.max() + 190, " fy", ys.min() + 350, "..", ys.max() + 350)

print("\n=== 8. OUTPUT STRIPS + y CELLS ===")
for (x0, x1, nm) in [(240, 400, "strip1"), (405, 565, "strip2"), (565, 730, "strip3")]:
    m = green[340:400, x0:x1] if nm == "strip1" else (orange[340:400, x0:x1] if nm == "strip2" else lav[340:400, x0:x1])
    ys, xs = np.where(m)
    if len(ys) > 50:
        print(f"{nm} pastel: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+340}..{ys.max()+340} n={len(ys)}")
print("strip fills: s1", med(300, 362, 306, 366), " s2", med(470, 362, 476, 366), " s3", med(640, 362, 646, 366))
# y cells: reddish rims (cells have red-brown rims per 009/010 family) — scan rows 355..385
rimcells = (r > 120) & (r < 210) & (g < 110) & (b < 110)
m = rimcells[350:392, 240:740]
colc = m.sum(axis=0)
print("y-cell rim col bands:", spans(colc > 6, 240, 4))
rowc = m.sum(axis=1)
print("y-cell rim row bands:", spans(rowc > 20, 350, 3))
# first-cell saturated fills
print("s1 y1 fill sample:", med(252, 362, 258, 368), " s2 y1:", med(415, 362, 421, 368), " s3 y1:", med(577, 362, 583, 368))
# y text color: dark glyph pixels in strip zone
zone = a[355:385, 245:735].reshape(-1, 3)
zd = zone[zone.sum(axis=1) < 420]
print("strip glyph core (all):", tuple(int(v) for v in np.median(zd, axis=0)) if len(zd) else None, "n=", len(zd))
zblue = zd[(zd[:, 2] > zd[:, 0] + 40)]
zred = zd[(zd[:, 0] > zd[:, 2] + 40)]
print("  blue-ish:", tuple(int(v) for v in np.median(zblue, axis=0)) if len(zblue) else None, "n=", len(zblue))
print("  red-ish:", tuple(int(v) for v in np.median(zred, axis=0)) if len(zred) else None, "n=", len(zred))

print("\n=== 9. CAPTIONS (red 2-line) ===")
for (x0, x1, nm) in [(240, 400, "cap1"), (405, 565, "cap2"), (565, 730, "cap3")]:
    m = reddish[388:420, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 20:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+388}..{ys.max()+388} n={len(ys)}")
        for yy in range(388, 420):
            seg = np.where(m[yy - 388, :])[0]
            if len(seg) > 3:
                print(f"   fy {yy}: fx {seg.min()+x0}..{seg.max()+x0} n={len(seg)}")

print("\n=== 10. RESULT SYMBOLS (blue Y2^(h)) ===")
bluish = (b > 120) & (b - r > 40) & (g < b)
for (x0, x1, nm) in [(240, 400, "res1"), (405, 565, "res2"), (565, 730, "res3")]:
    m = bluish[415:455, x0:x1]
    ys, xs = np.where(m)
    if len(ys) > 5:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+415}..{ys.max()+415} n={len(ys)}")
zone = a[415:455, 240:730].reshape(-1, 3)
zb = zone[(zone[:, 2] > zone[:, 0] + 40) & (zone[:, 2] > 120)]
print("result blue core:", tuple(int(v) for v in np.median(zb, axis=0)) if len(zb) else None, "n=", len(zb))

print("\n=== 11. MAGENTA X_2 + ARROW (Head 2 bottom) ===")
mag = (r > 130) & (b > 130) & (g < 110) & (np.abs(r - b) < 60)
m = mag[240:345, 405:565]
ys, xs = np.where(m)
if len(ys) > 5:
    print("magenta: fx", xs.min() + 405, "..", xs.max() + 405, " fy", ys.min() + 240, "..", ys.max() + 240, " n=", len(ys))
    zone = a[240:345, 405:565]
    zm = zone[mag[240:345, 405:565]]
    print("magenta core:", tuple(int(v) for v in np.median(zm.reshape(-1, 3), axis=0)))

print("\n=== 12. CURSOR (dark gray/black in H1 grid, omit) ===")
dark = (lum < 110)
m = dark[200:260, 240:400]
ys, xs = np.where(m)
if len(ys) > 3:
    print("cursor-ish dark: fx", xs.min() + 240, "..", xs.max() + 240, " fy", ys.min() + 200, "..", ys.max() + 200, " n=", len(ys))

print("\n=== 13. MAPPING ===")
# fit: use chrome left 58/59 <-> 42, right ~901 <-> 919, top 43 <-> 45, bottom stroke 516 <-> 540
print("certified-002 mapping check: fx2sx(58.5)=%.1f fx2sx(901.5)=%.1f fy2sy(43.5)=%.1f fy2sy(516)=%.1f" %
      ((58.5 - 17.628) / 0.961232, (901.5 - 17.628) / 0.961232, 43.5 / 0.955556, 516 / 0.955556))
