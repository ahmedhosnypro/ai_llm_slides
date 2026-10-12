#!/usr/bin/env python3
"""measure_original4.py — slide 035 pass 4: output-grid structure strips,
left-grid digits, caption box/border/words/underline, fills, arrow 1px trace."""
import numpy as np
from PIL import Image

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== N1. OUTPUT GRID: vertical strips (median color per y at fixed x) ===")
for x in [694, 700, 725, 750, 780, 807, 840, 865, 872, 880]:
    col = a[185:385, x]
    # detect transitions: print y where color changes class significantly
    prev = None
    out = []
    for i, (r, g, b) in enumerate(col):
        y = 185 + i
        key = (r // 40, g // 40, b // 40)
        if key != prev:
            out.append(f"y{y}:#{r:02X}{g:02X}{b:02X}")
            prev = key
    print(f"x={x}: " + " ".join(out[:40]))

print("=== N2. OUTPUT GRID: horizontal strips (median color per x at fixed y) ===")
for y in [188, 195, 210, 228, 232, 240, 255, 274, 278, 290, 315, 319, 335, 370, 375]:
    row = a[y, 688:890]
    prev = None
    out = []
    for i, (r, g, b) in enumerate(row):
        x = 688 + i
        key = (r // 40, g // 40, b // 40)
        if key != prev:
            out.append(f"x{x}:#{r:02X}{g:02X}{b:02X}")
            prev = key
    print(f"y={y}: " + " ".join(out[:36]))

print("=== N3. '4' CELL: dense 4px grid samples ===")
for y in range(192, 232, 4):
    row = []
    for x in range(694, 756, 6):
        r, g, b = a[y, x]
        row.append(f"{r:02X}{g:02X}{b:02X}")
    print(f"y{y}: " + " ".join(row))

print("=== N4. LEFT GRID digits: per-cell with green-digit mask ===")
# digit green: sample darkest green pixels; use G-R>60
digm = (G - R > 60) & (G - B > 30) & (G > 60)
bx0, by0, cw, ch = 78, 208, 32.8, 25.8
grid_vals = []
for r in range(5):
    line = []
    for c in range(5):
        x0 = int(bx0 + c * cw) + 4; x1 = int(bx0 + (c + 1) * cw) - 4
        y0 = int(by0 + r * ch) + 3; y1 = int(by0 + (r + 1) * ch) - 3
        sub = digm[y0:y1, x0:x1]
        n = int(sub.sum())
        w = 0; hgt = 0
        if n:
            ys, xs = np.where(sub)
            w = int(xs.max() - xs.min() + 1); hgt = int(ys.max() - ys.min() + 1)
        line.append(f"n={n:3d} w={w:2d} h={hgt:2d}")
    print(f"  row{r+1}: " + " | ".join(line))
# digit color: median of digm pixels in whole grid
zz = np.zeros((540, 960), bool); zz[210:336, 80:240] = True
dm = digm & zz
ys, xs = np.where(dm)
print("left digit median color:", tuple(np.median(a[ys, xs], axis=0).astype(int)), "n=", len(xs))

print("=== N5. FILTER + PANEL fills (mask medians) ===")
# filter yellow fill
yz = np.zeros((540, 960), bool); yz[222:288, 273:362] = True
ym = (R > 200) & (G > 190) & (B < 160) & yz
ys, xs = np.where(ym)
print("filter fill median:", tuple(np.median(a[ys, xs], axis=0).astype(int)), "n=", len(xs))
# filter border (olive) sample: rows between cells
print("filter border samples:", [f"#{a[y,285,0]:02X}{a[y,285,1]:02X}{a[y,285,2]:02X}" for y in (242, 243, 265, 266)])
# panel yellow fill
yz2 = np.zeros((540, 960), bool); yz2[203:326, 407:574] = True
ym2 = (R > 200) & (G > 190) & (B < 160) & yz2
ys, xs = np.where(ym2)
print("panel yellow fill median:", tuple(np.median(a[ys, xs], axis=0).astype(int)), "n=", len(xs))
# panel green fill
gz2 = np.zeros((540, 960), bool); gz2[330:414, 580:689] = True
gm2 = (G - R > 60) & (G - B > 40) & gz2
ys, xs = np.where(gm2)
print("panel green fill median:", tuple(np.median(a[ys, xs], axis=0).astype(int)), "n=", len(xs))
# panel digit color: dark pixels inside cells
dzm = np.zeros((540, 960), bool); dzm[205:412, 408:688] = True
dk = (R < 120) & (G < 120) & (B < 120) & dzm
ys, xs = np.where(dk)
print("panel digit median:", tuple(np.median(a[ys, xs], axis=0).astype(int)), "n=", len(xs))
# multiplier red median
mz2 = np.zeros((540, 960), bool); mz2[225:328, 430:580] = True
rm = (R - G > 70) & (R - B > 70) & (R > 130) & mz2
ys, xs = np.where(rm)
print("multiplier red median:", tuple(np.median(a[ys, xs], axis=0).astype(int)), "n=", len(xs))

print("=== N6. CAPTION BOX: border + rect exact ===")
# loose blue mask
blu = (B - R > 25) & (B > 80)
print("vertical border cols x60..95 / x860..900 (blue count in y440..510):")
for x in list(range(60, 96)) + list(range(858, 902)):
    c = blu[440:510, x].sum()
    if c > 10:
        print(f"  x={x}: {c}")
print("horizontal border rows y432..516 (blue count in x70..890):")
for y in range(432, 516):
    c = blu[y, 70:890].sum()
    if c > 200:
        print(f"  y={y}: {c}")
# vertical strip x=500 y425..540
print("vertical strip x=500 y425..540:")
prev = None
for y in range(425, 540):
    r, g, b = a[y, 500]
    key = (r // 25, g // 25, b // 25)
    if key != prev:
        print(f"  y{y}: #{r:02X}{g:02X}{b:02X} ({r},{g},{b})")
        prev = key

print("=== N7. CAPTION LINE 2: word runs (gap>3) + blue clusters + underline ===")
reg_y0, reg_y1, reg_x0, reg_x1 = 476, 510, 80, 500
reg = a[reg_y0:reg_y1, reg_x0:reg_x1]
rr, gg, bb = reg[:,:,0], reg[:,:,1], reg[:,:,2]
redm = (rr - gg > 50) & (rr - bb > 50) & (rr > 110)
blum = (bb - rr > 20) & (bb > 80)
colprof = redm.sum(axis=0)
runs = []
inrun = False
gap = 0
for x in range(reg.shape[1]):
    if colprof[x] > 0:
        if not inrun: s_ = x; inrun = True
        gap = 0
    else:
        if inrun:
            gap += 1
            if gap > 3:
                runs.append((s_ + reg_x0, x - gap + reg_x0)); inrun = False
if inrun: runs.append((s_ + reg_x0, reg.shape[1] - 1 + reg_x0))
print("line2 red word runs:", runs)
ys, xs = np.where(redm)
print(f"line2 red row extent y{ys.min()+reg_y0}..{ys.max()+reg_y0}")
# underline: red rows near bottom
rowprof = redm.sum(axis=1)
for i, c in enumerate(rowprof):
    if c > 50:
        print(f"  red row y={i+reg_y0}: count {c}")
ys, xs = np.where(blum)
if len(xs):
    print(f"line2 blue n={len(xs)} bbox x{xs.min()+reg_x0}..{xs.max()+reg_x0} y{ys.min()+reg_y0}..{ys.max()+reg_y0}")
    # cluster columns
    colb = blum.sum(axis=0)
    clusters = [(x + reg_x0, int(colb[x])) for x in range(reg.shape[1]) if colb[x] > 2]
    print("  blue col clusters (>2):", clusters[:30])

print("=== N8. CAPTION LINE 1: word runs (gap>4) for font fit ===")
reg = a[448:478, 60:900]
rr, gg, bb = reg[:,:,0], reg[:,:,1], reg[:,:,2]
blum = (bb - rr > 20) & (bb > 80)
colprof = blum.sum(axis=0)
runs = []
inrun = False
gap = 0
for x in range(reg.shape[1]):
    if colprof[x] > 0:
        if not inrun: s_ = x; inrun = True
        gap = 0
    else:
        if inrun:
            gap += 1
            if gap > 4:
                runs.append((s_ + 60, x - gap + 60)); inrun = False
if inrun: runs.append((s_ + 60, reg.shape[1] - 1 + 60))
print("line1 word runs:", runs)
ys, xs = np.where(blum)
print(f"line1 rows y{ys.min()+448}..{ys.max()+448}")

print("=== N9. ARROW 1px trace (x495..745 y183..225, dark<130) ===")
dk2 = (R < 130) & (G < 130) & (B < 130)
for y in range(183, 226):
    row = np.where(dk2[y, 495:745])[0]
    if len(row):
        segs = []
        s_ = row[0]; p = row[0]
        for x in row[1:]:
            if x - p > 2:
                segs.append((s_ + 495, p + 495)); s_ = x
            p = x
        segs.append((s_ + 495, p + 495))
        print(f"y={y}: {[(int(u), int(v)) for u, v in segs]}")

print("=== N10. ORIGINAL PANEL right border scan x870..915 ===")
reddish = (R - G > 35) & (R - B > 35)
for x in range(870, 916):
    c = reddish[100:400, x].sum()
    if c > 30:
        print(f"  col x={x}: {c}")
print("original panel gray extent at y=250: x42..? / x?..918")
row = a[250, :]
grayish = (abs(row[:, 0] - 233) < 14) & (abs(row[:, 1] - 233) < 14) & (abs(row[:, 2] - 231) < 14)
xs = np.where(grayish)[0]
print(f"  gray cols y250: x{xs.min()}..{xs.max()}")
