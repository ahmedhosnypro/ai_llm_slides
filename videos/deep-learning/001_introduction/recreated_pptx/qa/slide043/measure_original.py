#!/usr/bin/env python3
"""PIL ink forensics on the ground-truth frame slide_043.jpg (960x540, 1px = 1pt).

Measures: chrome, title red ink + word gaps, inner red panel borders, bullet line
bands + markers, 5x5 Image grid (cell borders, fills, per-cell number bboxes,
red x0/x1 annotations), labels (Image / After conv 1 / After conv 2), block arrows,
3x3 grid + cells, 1x1 output cell, blue explanation box + navy text line bands,
bottom black strip, modal colors. All in frame px (1px = 1pt = 1/72 in).
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_043.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
print(f"frame {W}x{H}")

r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  "
          f"(w {xs.max()-xs.min()+1}, h {ys.max()-ys.min()+1}, n={len(ys)})")
    return (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))

def bands(mask, axis=1, gap=3, minpix=2, label=""):
    """contiguous row/col bands of ink"""
    proj = mask.sum(axis=axis)
    idx = np.where(proj > minpix)[0]
    if not len(idx):
        print(f"{label}: EMPTY bands")
        return []
    out = []
    s = p = idx[0]
    for c in idx[1:]:
        if c - p <= gap:
            p = c
        else:
            out.append((int(s), int(p)))
            s = p = c
    out.append((int(s), int(p)))
    print(f"{label} bands: {out}")
    return out

# ---------- chrome ----------
red = (r > 120) & (g < 110) & (b < 110)
print("\n--- chrome ---")
print("panel red border rows (long horiz runs y<540):")
for y in range(40, 60):
    xs2 = np.where(red[y])[0]
    if len(xs2) > 400:
        print(f"  y={y}: n={len(xs2)} x {xs2.min()}..{xs2.max()}")
for x in (40, 41, 42, 43, 44, 916, 917, 918, 919, 920):
    ys2 = np.where(red[:, x])[0]
    if len(ys2):
        print(f"  x={x}: red n={len(ys2)} y {ys2.min()}..{ys2.max()}")

# ---------- title ----------
print("\n--- title red ink ---")
tmask = np.zeros_like(red)
tmask[50:135, 50:900] = red[50:135, 50:900]
tb = bbox(tmask, "title red ink")
ys, xs = np.where(tmask)
cols = np.unique(xs)
gaps = []
prev = cols[0]
for c in cols[1:]:
    if c - prev > 8:
        gaps.append((int(prev), int(c)))
    prev = c
print("title word gaps (>8px):", gaps)
# word segment widths
segs = []
s = cols[0]
p = cols[0]
for c in cols[1:]:
    if c - p > 8:
        segs.append((int(s), int(p), int(p - s + 1)))
        s = c
    p = c
segs.append((int(s), int(p), int(p - s + 1)))
print("title word segments (x0,x1,w):", segs)

# ---------- red panel borders (inner frames) ----------
print("\n--- long horizontal red runs (>=100 px) y 90..420 ---")
for y in range(90, 420):
    row = red[y]
    xs2 = np.where(row)[0]
    if len(xs2) > 100:
        runs = []
        s = p = xs2[0]
        for c in xs2[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((int(s), int(p), int(p - s + 1)))
                s = p = c
        runs.append((int(s), int(p), int(p - s + 1)))
        for run in runs:
            if run[2] >= 100:
                print(f"y={y}: run x {run[0]}..{run[1]} (len {run[2]})")

print("\n--- vertical red runs (>=40 px) x 40..920 ---")
for x in range(40, 920):
    col = red[:, x]
    ys2 = np.where(col[100:540])[0] + 100
    if len(ys2) > 40:
        runs = []
        s = p = ys2[0]
        for c in ys2[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((int(s), int(p), int(p - s + 1)))
                s = p = c
        runs.append((int(s), int(p), int(p - s + 1)))
        for run in runs:
            if run[2] >= 40:
                print(f"x={x}: run y {run[0]}..{run[1]} (len {run[2]})")

# ---------- bullets (dark gray text) ----------
print("\n--- bullets ---")
dark = (r < 130) & (g < 130) & (b < 130)
bmask = np.zeros_like(dark)
bmask[110:215, 120:560] = dark[110:215, 120:560]
bb = bands(bmask, axis=1, gap=4, minpix=3, label="bullet text rows")
for (y0, y1) in bb:
    seg = bmask[y0:y1+1]
    xs3 = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  band y {y0}..{y1}: x {xs3.min()}..{xs3.max()} (h {y1-y0+1})")

# bullet markers (hollow circles, tan/gold outline)
tan = (r > 150) & (r < 240) & (g > 110) & (g < 210) & (b < 140) & (r > b + 60)
mk = np.zeros_like(tan)
mk[110:215, 120:190] = tan[110:215, 120:190]
bbox(mk, "bullet markers (tan outline, left strip)")

# ---------- grids ----------
print("\n--- 5x5 grid: yellow + green cells ---")
yellow = (r > 200) & (g > 180) & (b < 160) & (g < 240)
green = (g > 140) & (r < 140) & (b < 140) & (g > r + 40) & (g > b + 40)
gm = np.zeros_like(green)
gm[200:420, 200:520] = green[200:420, 200:520]
gbb = bbox(gm, "green cells bbox")
ym = np.zeros_like(yellow)
ym[200:420, 200:520] = yellow[200:420, 200:520]
ybb = bbox(ym, "yellow cells bbox")

print("\n--- grid border scan: dark pixels in grid region ---")
grid_dark = (r < 100) & (g < 100) & (b < 100)
dm = np.zeros_like(grid_dark)
dm[200:420, 200:520] = grid_dark[200:420, 200:520]
# column profile of dark pixels -> cell border x positions
colprof = dm.sum(axis=0)
cols_border = [int(c) for c in np.where(colprof > 60)[0]]
print("strong dark columns (borders):", cols_border)
rowprof = dm.sum(axis=1)
rows_border = [int(c) for c in np.where(rowprof > 60)[0]]
print("strong dark rows (borders):", rows_border)

# ---------- labels (black handwriting above grids) ----------
print("\n--- diagram labels ---")
lbl_dark = (r < 110) & (g < 110) & (b < 110)
lm = np.zeros_like(lbl_dark)
lm[185:240, 200:520] = lbl_dark[185:240, 200:520]
bbox(lm, "label 'Image' region ink")
lm2 = np.zeros_like(lbl_dark)
lm2[185:240, 520:700] = lbl_dark[185:240, 520:700]
bbox(lm2, "label 'After conv 1' region ink")
lm3 = np.zeros_like(lbl_dark)
lm3[185:240, 690:910] = lbl_dark[185:240, 690:910]
bbox(lm3, "label 'After conv 2' region ink")

# ---------- arrows ----------
print("\n--- arrows (white fill + dark outline) ---")
white = (r > 215) & (g > 215) & (b > 215)
am = np.zeros_like(white)
am[280:340, 430:530] = white[280:340, 430:530]
bbox(am, "arrow1 white fill (x 430..530)")
am2 = np.zeros_like(white)
am2[280:340, 640:740] = white[280:340, 640:740]
bbox(am2, "arrow2 white fill (x 640..740)")

# ---------- 3x3 grid + 1x1 cell (gray-olive) ----------
print("\n--- 3x3 grid / 1x1 cell: gray-olive fill ---")
grayol = (np.abs(r - 154) < 40) & (np.abs(g - 154) < 40) & (np.abs(b - 138) < 40)
zm = np.zeros_like(grayol)
zm[230:390, 500:720] = grayol[230:390, 500:720]
zb = bbox(zm, "gray-olive 3x3 bbox (x 500..720)")
zm2 = np.zeros_like(grayol)
zm2[270:340, 720:820] = grayol[270:340, 720:820]
bbox(zm2, "gray-olive 1x1 cell (x 720..820)")

# 3x3 cell borders (dark)
dm2 = np.zeros_like(grid_dark)
dm2[230:390, 500:720] = grid_dark[230:390, 500:720]
colprof2 = dm2.sum(axis=0)
print("3x3 strong dark cols:", [int(c) for c in np.where(colprof2 > 30)[0] + 500])
rowprof2 = dm2.sum(axis=1)
print("3x3 strong dark rows:", [int(c) for c in np.where(rowprof2 > 30)[0] + 230])

# per-cell number bboxes in 5x5: black ink inside each cell
print("\n--- 5x5 per-cell number ink (black) ---")
num_dark = (r < 90) & (g < 90) & (b < 90)
if gbb and ybb:
    gx0, gx1, gy0, gy1 = gbb[0], gbb[1], gbb[2], gbb[3]
    cw = (gx1 - gx0 + 1) / 5.0
    ch = (gy1 - gy0 + 1) / 5.0
    print(f"grid bbox x {gx0}..{gx1} y {gy0}..{gy1}; cell w {cw:.1f} h {ch:.1f}")
    for ri in range(5):
        cells = []
        for ci in range(5):
            cx0 = int(gx0 + ci * cw) + 2
            cx1 = int(gx0 + (ci + 1) * cw) - 2
            cy0 = int(gy0 + ri * ch) + 2
            cy1 = int(gy0 + (ri + 1) * ch) - 2
            reg = num_dark[cy0:cy1, cx0:cx1]
            if reg.sum() > 3:
                ys4, xs4 = np.where(reg)
                cells.append((cx0 + xs4.min(), cx0 + xs4.max(),
                              cy0 + ys4.min(), cy0 + ys4.max()))
            else:
                cells.append(None)
        print(f" row {ri}: {cells}")

# ---------- red x0/x1 annotations ----------
print("\n--- red x0/x1 annotations (small red ink inside yellow cells) ---")
red2 = (r > 150) & (g < 90) & (b < 90)
xm = np.zeros_like(red2)
if ybb:
    xm[ybb[2]:ybb[3]+1, ybb[0]:ybb[1]+1] = red2[ybb[2]:ybb[3]+1, ybb[0]:ybb[1]+1]
    bands(xm, axis=1, gap=2, minpix=1, label="x0/x1 rows")
    bands(xm, axis=0, gap=2, minpix=1, label="x0/x1 cols")
    bbox(xm, "x0/x1 total bbox")

# ---------- 3x3 numbers ----------
print("\n--- 3x3 per-cell number ink ---")
if zb:
    zx0, zx1, zy0, zy1 = zb[0], zb[1], zb[2], zb[3]
    cw2 = (zx1 - zx0 + 1) / 3.0
    ch2 = (zy1 - zy0 + 1) / 3.0
    print(f"3x3 bbox x {zx0}..{zx1} y {zy0}..{zy1}; cell w {cw2:.1f} h {ch2:.1f}")
    for ri in range(3):
        cells = []
        for ci in range(3):
            cx0 = int(zx0 + ci * cw2) + 3
            cx1 = int(zx0 + (ci + 1) * cw2) - 3
            cy0 = int(zy0 + ri * ch2) + 3
            cy1 = int(zy0 + (ri + 1) * ch2) - 3
            reg = num_dark[cy0:cy1, cx0:cx1]
            if reg.sum() > 3:
                ys4, xs4 = np.where(reg)
                cells.append((cx0 + xs4.min(), cx0 + xs4.max(),
                              cy0 + ys4.min(), cy0 + ys4.max()))
            else:
                cells.append(None)
        print(f" row {ri}: {cells}")

# 1x1 cell number
print("\n--- 1x1 '18' number ink ---")
bbox(num_dark[280:340, 730:810], "18 ink (region x 730..810, y 280..340)")

# ---------- blue explanation box ----------
print("\n--- blue explanation box ---")
blue = (b > 130) & (b > r + 40) & (b > g + 40)
blm = np.zeros_like(blue)
blm[380:520, 40:920] = blue[380:520, 40:920]
bbox(blm, "blue border/text (bottom region)")
navy = (b > 90) & (r < 100) & (g < 100) & (b > r + 40)
nm = np.zeros_like(navy)
nm[385:515, 60:900] = navy[385:515, 60:900]
nb = bands(nm, axis=1, gap=4, minpix=3, label="navy text rows")
for (y0, y1) in nb:
    seg = nm[y0:y1+1]
    xs3 = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  band y {y0}..{y1}: x {xs3.min()}..{xs3.max()} (h {y1-y0+1})")
# box fill (white) bbox — the box interior is white vs panel gray
whitem = np.zeros_like(white)
whitem[385:515, 50:910] = white[385:515, 50:910]
bbox(whitem, "white box fill (bottom region)")

# ---------- bottom black strip (artifact) ----------
black = (r < 60) & (g < 60) & (b < 60)
b2 = np.zeros_like(black)
b2[490:540, :] = black[490:540, :]
bbox(b2, "bottom black strip (artifact)")

# ---------- modal colors ----------
def modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:4]]
    cnts = np.sort(counts)[::-1][:4]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

print("\n--- color samples ---")
modal(300, 380, 250, 300, "5x5 yellow cell fill")
modal(420, 500, 350, 400, "5x5 green cell fill")
modal(540, 600, 260, 300, "3x3 gray-olive fill")
modal(750, 790, 300, 330, "1x1 cell fill")
modal(100, 200, 470, 500, "panel gray (bottom left)")
modal(200, 800, 430, 460, "blue box fill (top area)")
modal(95, 500, 55, 90, "title red ink area (bg+ink)")
