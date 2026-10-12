#!/usr/bin/env python3
"""measure_original.py — slide 035 ink forensics, pass 1.
Frame: videos/deep-learning/001_introduction/unique_slides/slide_035.jpg (960x540, 1px=1pt=1/72in).
Measures every region's ink bbox + color samples; grids cell-by-cell.
"""
import numpy as np
from PIL import Image

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{label}: EMPTY")
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(f"{label}: x{x0}..{x1} y{y0}..{y1}  (w={x1-x0+1} h={y1-y0+1}) n={len(xs)}")
    return (x0, x1, y0, y1)

def sample(x0, x1, y0, y1, label):
    reg = a[y0:y1+1, x0:x1+1].reshape(-1, 3)
    med = np.median(reg, axis=0).astype(int)
    print(f"  sample {label} x{x0}..{x1} y{y0}..{y1}: median rgb={tuple(med)} #{med[0]:02X}{med[1]:02X}{med[2]:02X}")

print("=== 1. RED TOP RULE (thin red horizontal line, top area) ===")
red = (R > 140) & (G < 90) & (B < 90)
for y in range(0, 60):
    cnt = red[y, :].sum()
    if cnt > 300:
        xs = np.where(red[y, :])[0]
        print(f"row y={y}: red count {cnt}, x{xs.min()}..{xs.max()}")

print("=== 2. TITLE (red bold text) ===")
title_zone = np.zeros_like(red); title_zone[36:100, :] = True
tmask = red & title_zone
tb = bbox(tmask, "title red ink")
# row profile of title ink
if tb:
    rows = tmask[tb[2]:tb[3]+1, :].sum(axis=1)
    nz = [(tb[2]+i, int(c)) for i, c in enumerate(rows) if c > 0]
    print("  title row profile (y,count):", nz[:3], "...", nz[-3:])
    # column extremes per major band to find text rows
    ys, xs = np.where(tmask)
    print("  title x-histogram summary: leftmost cols", np.percentile(xs, [0, 5, 50, 95, 100]).astype(int))
sample(tb[0], tb[1], tb[2], tb[3], "title ink (modal)")

print("=== 3. IMAGE LABEL (black bold 'Image', left area) ===")
dark = (R < 90) & (G < 90) & (B < 90)
lz = np.zeros_like(dark); lz[100:170, 40:300] = True
bbox(dark & lz, "Image label ink")

print("=== 4. LEFT 5x5 GRID (red border, green numerals, faint photo) ===")
# red border on left side
lrz = np.zeros_like(red); lrz[100:420, 40:320] = True
lred = red & lrz
lb = bbox(lred, "left grid red ink (border)")
if lb:
    # border stroke rows/cols: count red pixels per row/col within bbox
    for y in range(lb[2], lb[3]+1):
        c = lred[y, lb[0]:lb[1]+1].sum()
        if c > (lb[1]-lb[0])*0.5:
            print(f"  horizontal red stroke row y={y}: {c}")
    for x in range(lb[0], lb[1]+1):
        c = lred[lb[2]:lb[3]+1, x].sum()
        if c > (lb[3]-lb[2])*0.5:
            print(f"  vertical red stroke col x={x}: {c}")
# green numerals
green = (G > 100) & (G - R > 40) & (G - B > 40)
lgz = np.zeros_like(green); lgz[150:400, 60:300] = True
lg = green & lgz
lgb = bbox(lg, "left grid green numerals")
if lb:
    sample(lb[0]+30, lb[0]+60, lb[2]+30, lb[2]+60, "inside left grid (photo tint)")

print("=== 5. FILTER LABEL + 3x3 YELLOW GRID ===")
fz = np.zeros_like(dark); fz[100:170, 230:420] = True
bbox(dark & fz, "Filter label ink")
yellow = (R > 180) & (G > 170) & (B < 120)
yz = np.zeros_like(yellow); yz[150:350, 230:420] = True
ymask = yellow & yz
yb = bbox(ymask, "filter yellow cells")
if yb:
    rows = ymask[yb[2]:yb[3]+1, :].sum(axis=1)
    prev = False
    for i, c in enumerate(rows):
        cur = c > 30
        if cur != prev:
            print(f"  yellow rows transition at y={yb[2]+i} (count {c})")
            prev = cur
    cols = ymask[:, yb[0]:yb[1]+1].sum(axis=0)
    prev = False
    for i, c in enumerate(cols):
        cur = c > 30
        if cur != prev:
            print(f"  yellow cols transition at x={yb[0]+i} (count {c})")
            prev = cur

print("=== 6. COMPUTATION PANEL (white rect, gray border, right side) ===")
# gray border BFBFBF-ish
grayline = (abs(R - 191) < 40) & (abs(G - 191) < 40) & (abs(B - 191) < 40) & (abs(R - G) < 15) & (abs(G - B) < 15)
pz = np.zeros_like(grayline); pz[140:460, 360:940] = True
gm = grayline & pz
gb = bbox(gm, "panel gray border ink")
if gb:
    for y in range(gb[2], gb[3]+1):
        c = gm[y, gb[0]:gb[1]+1].sum()
        if c > (gb[1]-gb[0])*0.6:
            print(f"  panel horiz stroke y={y}: {c}")
    for x in range(gb[0], gb[1]+1):
        c = gm[gb[2]:gb[3]+1, x].sum()
        if c > (gb[3]-gb[2])*0.6:
            print(f"  panel vert stroke x={x}: {c}")

print("=== 7. PANEL YELLOW 3x3 (with red multipliers) ===")
pz2 = np.zeros_like(yellow); pz2[150:400, 380:700] = True
pym = yellow & pz2
pyb = bbox(pym, "panel yellow 3x3")
# red multipliers inside panel (tiny red text)
mz = np.zeros_like(red); mz[150:400, 380:700] = True
mm = red & mz
mmb = bbox(mm, "panel red multiplier ink")
if pyb:
    rows = pym[pyb[2]:pyb[3]+1, :].sum(axis=1)
    prev = False
    for i, c in enumerate(rows):
        cur = c > 20
        if cur != prev:
            print(f"  panel yellow row transition y={pyb[2]+i} (count {c})")
            prev = cur
    cols = pym[:, pyb[0]:pyb[1]+1].sum(axis=0)
    prev = False
    for i, c in enumerate(cols):
        cur = c > 20
        if cur != prev:
            print(f"  panel yellow col transition x={pyb[0]+i} (count {c})")
            prev = cur

print("=== 8. PANEL GREEN CELLS (16 non-highlight) ===")
pz3 = np.zeros_like(green); pz3[150:400, 380:700] = True
pg = green & pz3
pgb = bbox(pg, "panel green cells")

print("=== 9. OUTPUT 3x3 GRID (tan borders) + '4' cell ===")
tan = (abs(R - 201) < 45) & (abs(G - 168) < 45) & (abs(B - 118) < 50) & (R - B > 40)
tz = np.zeros_like(tan); tz[150:420, 650:920] = True
tm = tan & tz
tmb = bbox(tm, "output grid tan ink")
if tmb:
    for y in range(tmb[2], tmb[3]+1):
        c = tm[y, tmb[0]:tmb[1]+1].sum()
        if c > (tmb[1]-tmb[0])*0.5:
            print(f"  tan horiz stroke y={y}: {c}")
    for x in range(tmb[0], tmb[1]+1):
        c = tm[tmb[2]:tmb[3]+1, x].sum()
        if c > (tmb[3]-tmb[2])*0.5:
            print(f"  tan vert stroke x={x}: {c}")
olive = (R > 80) & (R < 140) & (G > 80) & (G < 140) & (B < 100) & (abs(R - G) < 25)
oz = np.zeros_like(olive); oz[150:420, 650:920] = True
om = olive & oz
ob = bbox(om, "output '4' olive cell")

print("=== 10. CURVED BLACK ARROW (inside panel) ===")
az = np.zeros_like(dark); az[150:430, 430:900] = True
am = dark & az
ab = bbox(am, "arrow+numerals black ink in panel zone")

print("=== 11. CAPTION BOX (light yellow, blue border) ===")
ly = (R > 230) & (G > 225) & (B > 190) & (B < 240) & (R - B > 10)
cz = np.zeros_like(ly); cz[400:520, 20:940] = True
cm = ly & cz
cb = bbox(cm, "caption light-yellow box")
blue = (B > 140) & (B - R > 60) & (B - G > 40)
bz2 = np.zeros_like(blue); bz2[400:530, 20:940] = True
bm = blue & bz2
bb = bbox(bm, "caption blue ink (border+text)")

print("=== 12. BLACK BOTTOM BAR ===")
bz3 = np.zeros_like(dark); bz3[500:540, :] = True
bbar = dark & bz3
bbb = bbox(bbar, "bottom black bar")
if bbb:
    rows = bbar[:, :].sum(axis=1)
    for y in range(500, 540):
        if rows[y] > 200:
            print(f"  bar row y={y}: count {int(rows[y])}")

print("=== 13. HOUSE CHROME ZONES (expect no badge in original) ===")
sample(860, 925, 45, 100, "badge zone (top-right)")
sample(0, 41, 200, 300, "left margin outside panel")
sample(43, 917, 470, 500, "panel lower area")

print("=== 14. PANEL GRID NUMERALS (black bold in panel 5x5) ===")
# within yellow 3x3 and green cells
if pyb and pgb:
    gz = np.zeros_like(dark)
    gz[pyb[2]-8:pgb[3]+8, pyb[0]-8:pgb[1]+8] = True
    gz[pgb[2]-8:pgb[3]+8, pgb[0]-8:pgb[1]+8] = True
    nm = dark & gz
    nb = bbox(nm, "panel grid numeral ink")
