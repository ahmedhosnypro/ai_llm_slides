#!/usr/bin/env python3
"""measure_original2.py — slide 035 pass 2: precise masks, per-cell forensics,
arrow trace, caption box, red rule rescan, color samples."""
import numpy as np
from PIL import Image

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def px(x, y, label=""):
    r, g, b = a[y, x]
    print(f"  ({x},{y}) rgb=({r},{g},{b}) #{r:02X}{g:02X}{b:02X} {label}")

print("=== A. RED TOP RULE rescan (loose reddish) y0..70 ===")
reddish = (R - G > 60) & (R - B > 60)
for y in range(0, 70):
    c = reddish[y, :].sum()
    if c > 100:
        xs = np.where(reddish[y, :])[0]
        print(f"row y={y}: reddish {c} x{xs.min()}..{xs.max()}")

print("=== B. CHROME ZONES in original frame ===")
print("panel left border col candidates (reddish cols x30..60, y100..400):")
for x in range(30, 62):
    c = reddish[100:400, x].sum()
    if c > 50:
        print(f"  col x={x}: {c}")
print("panel top border row candidates (reddish rows y38..52, x100..800):")
for y in range(38, 53):
    c = reddish[y, 100:800].sum()
    if c > 100:
        print(f"  row y={y}: {c}")
px(20, 20, "top-left canvas")
px(480, 20, "top-center canvas")
px(20, 250, "left margin")
px(500, 460, "between caption?")

print("=== C. TITLE fine metrics ===")
reddish_t = reddish.copy()
tz = np.zeros_like(reddish_t); tz[55:110, :] = True
tm = reddish_t & tz
ys, xs = np.where(tm)
print(f"title ink bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
# per-column top/bottom to find cap top / baseline / descender
colstop = {}
for x in range(xs.min(), xs.max() + 1):
    col = np.where(tm[:, x])[0]
    if len(col):
        colstop[x] = (col.min(), col.max())
tops = np.array([v[0] for v in colstop.values()])
bots = np.array([v[1] for v in colstop.values()])
print(f"column-top percentiles: p5={np.percentile(tops,5):.0f} p25={np.percentile(tops,25):.0f} p50={np.percentile(tops,50):.0f}")
print(f"column-bottom percentiles: p75={np.percentile(bots,75):.0f} p95={np.percentile(bots,95):.0f} max={bots.max()}")
# gaps => word boundaries
cols_with_ink = sorted(colstop.keys())
gaps = []
prev = cols_with_ink[0]
for x in cols_with_ink[1:]:
    if x - prev > 6:
        gaps.append((prev, x, x - prev))
    prev = x
print("word gaps (end,start,width):", gaps)
# word extents
words = []
start = cols_with_ink[0]
prev = start
for x in cols_with_ink[1:] + [9999]:
    if x - prev > 6:
        words.append((start, prev))
        start = x
    prev = x
print("word extents:", words, "total ink width", xs.max() - xs.min() + 1)
# stroke thickness sample: vertical stroke of 'H' at left
hx = xs.min()
col = np.where(tm[:, hx:hx+14])[0]
print("first-14-col ink rows:", col.min(), col.max())

print("=== D. LEFT GRID: red border exact rect ===")
# sample along suspected border rows/cols
print("vertical scan x60..320 at y=270 (looking for red border cols):")
row = a[270, 60:320]
for i, (r, g, b) in enumerate(row):
    if r - g > 50 and r - b > 50:
        print(f"  x={60+i}: ({r},{g},{b})")
print("horizontal scan y190..350 at x=150 (red border rows):")
colv = a[190:350, 150]
for i, (r, g, b) in enumerate(colv):
    if r - g > 50 and r - b > 50:
        print(f"  y={190+i}: ({r},{g},{b})")
print("scan y190..350 at x=280:")
colv = a[190:350, 280]
for i, (r, g, b) in enumerate(colv):
    if r - g > 50 and r - b > 50:
        print(f"  y={190+i}: ({r},{g},{b})")

print("=== E. LEFT GRID: green numerals per cell (need grid lines) ===")
green = (G > 90) & (G - R > 30) & (G - B > 30)
lz = np.zeros_like(green); lz[190:350, 60:320] = True
lg = green & lz
ys, xs = np.where(lg)
print(f"green ink bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")
# column profile of green to find 5 columns
colprof = lg.sum(axis=0)
runs = []
inrun = False
for x in range(60, 320):
    if colprof[x] > 2 and not inrun:
        s = x; inrun = True
    elif colprof[x] <= 2 and inrun:
        runs.append((s, x - 1)); inrun = False
print("green col runs:", runs)
rowprof = lg.sum(axis=1)
runs = []
inrun = False
for y in range(190, 350):
    if rowprof[y] > 2 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 2 and inrun:
        runs.append((s, y - 1)); inrun = False
print("green row runs:", runs)
# grid cell separators: darkish lines inside the grid? sample rows/cols of darker pixels
print("sample colors inside left grid:")
px(100, 225, "r1c1 area")
px(200, 270, "mid cell")
px(160, 320, "bottom cell")
px(85, 270, "left border area")
px(245, 270, "right-of-green area")

print("=== F. FILTER GRID exact ===")
yellow = (R > 170) & (G > 160) & (B < 140) & (R - B > 60)
fz = np.zeros_like(yellow); fz[190:340, 240:400] = True
fm = yellow & fz
colprof = fm.sum(axis=0)
print("filter yellow col profile nonzero runs:")
inrun = False
for x in range(240, 400):
    if colprof[x] > 5 and not inrun:
        s = x; inrun = True
    elif colprof[x] <= 5 and inrun:
        print(f"  x{s}..{x-1}"); inrun = False
if inrun: print(f"  x{s}..399")
rowprof = fm.sum(axis=1)
print("filter yellow row profile nonzero runs:")
inrun = False
for y in range(190, 340):
    if rowprof[y] > 5 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 5 and inrun:
        print(f"  y{s}..{y-1}"); inrun = False
if inrun: print(f"  y{s}..339")
# filter numerals (black in yellow zone)
darkf = (R < 100) & (G < 100) & (B < 100)
nz = np.zeros_like(darkf); nz[200:330, 250:400] = True
nm = darkf & nz
ys, xs = np.where(nm)
print(f"filter numeral ink bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")

print("=== G. PANEL GRID exact (yellow 3x3 + green cells + numerals + multipliers) ===")
pz = np.zeros_like(yellow); pz[190:340, 390:700] = True
pm = yellow & pz
colprof = pm.sum(axis=0)
print("panel yellow col runs:")
inrun = False
for x in range(390, 700):
    if colprof[x] > 5 and not inrun:
        s = x; inrun = True
    elif colprof[x] <= 5 and inrun:
        print(f"  x{s}..{x-1}"); inrun = False
if inrun: print(f"  x{s}..699")
rowprof = pm.sum(axis=1)
print("panel yellow row runs:")
inrun = False
for y in range(190, 340):
    if rowprof[y] > 5 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 5 and inrun:
        print(f"  y{s}..{y-1}"); inrun = False
if inrun: print(f"  y{s}..339")
# green cells col/row runs
green2 = (G > 90) & (G - R > 25) & (G - B > 25)
gz = np.zeros_like(green2); gz[190:430, 390:720] = True
gm = green2 & gz
colprof = gm.sum(axis=0)
print("panel green col runs:")
inrun = False
for x in range(390, 720):
    if colprof[x] > 5 and not inrun:
        s = x; inrun = True
    elif colprof[x] <= 5 and inrun:
        print(f"  x{s}..{x-1}"); inrun = False
if inrun: print(f"  x{s}..719")
rowprof = gm.sum(axis=1)
print("panel green row runs:")
inrun = False
for y in range(190, 430):
    if rowprof[y] > 5 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 5 and inrun:
        print(f"  y{s}..{y-1}"); inrun = False
if inrun: print(f"  y{s}..429")

print("=== H. RED MULTIPLIERS per yellow cell ===")
redm = (R > 130) & (R - G > 70) & (R - B > 70)
mz = np.zeros_like(redm); mz[195:335, 395:600] = True
mm = redm & mz
ys, xs = np.where(mm)
print(f"multiplier red ink total n={len(xs)} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")

print("=== I. OUTPUT GRID exact (tan borders) ===")
tanish = (R > 150) & (R - B > 25) & (G > 110) & (G - B > 15) & (R - G > 5)
tzz = np.zeros_like(tanish); tzz[180:390, 660:920] = True
tmm = tanish & tzz
colprof = tmm.sum(axis=0)
print("output tan col runs (count>8):")
inrun = False
for x in range(660, 920):
    if colprof[x] > 8 and not inrun:
        s = x; inrun = True
    elif colprof[x] <= 8 and inrun:
        print(f"  x{s}..{x-1}"); inrun = False
if inrun: print(f"  x{s}..919")
rowprof = tmm.sum(axis=1)
print("output tan row runs (count>8):")
inrun = False
for y in range(180, 390):
    if rowprof[y] > 8 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 8 and inrun:
        print(f"  y{s}..{y-1}"); inrun = False
if inrun: print(f"  y{s}..389")
# '4' cell fill: sample inside first cell
print("output cell fill samples:")
px(720, 210, "out r1c1 upper")
px(720, 225, "out r1c1 lower")
px(790, 210, "out r1c2")
px(850, 210, "out r1c3")
px(720, 260, "out r2c1")
px(850, 350, "out r3c3")
# numeral '4' ink inside r1c1
dark4 = (R < 120) & (G < 120) & (B < 120)
o4 = np.zeros_like(dark4); o4[192:232, 692:752] = True
m4 = dark4 & o4
ys, xs = np.where(m4)
if len(xs):
    print(f"'4' dark ink bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")
    reg = a[ys, xs]
    print("  '4' ink median color:", tuple(np.median(reg, axis=0).astype(int)))

print("=== J. ARROW trace (black ink between/over grids) ===")
darkj = (R < 100) & (G < 100) & (B < 100)
# band between panel grid and output grid
ajz = np.zeros_like(darkj); ajz[150:420, 688:760] = True
am = darkj & ajz
ys, xs = np.where(am)
print(f"black ink in x688..760: n={len(xs)}")
if len(xs):
    print(f"  bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
    # topmost ink = arrow start?
    for yy in range(ys.min(), ys.max() + 1):
        row = np.where(am[yy, :])[0]
        if len(row):
            print(f"  y={yy}: x{row.min()}..{row.max()} n={len(row)}")
# black ink ABOVE the yellow block (arrow start region y150..200, x400..600)
az2 = np.zeros_like(darkj); az2[150:205, 395:640] = True
am2 = darkj & az2
ys, xs = np.where(am2)
print(f"black ink above yellow block y150..204 x395..640: n={len(xs)}")
if len(xs):
    print(f"  bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
    for yy in range(ys.min(), ys.max() + 1):
        row = np.where(am2[yy, :])[0]
        if len(row):
            print(f"  y={yy}: x{row.min()}..{row.max()} n={len(row)}")

print("=== K. CAPTION BOX exact ===")
# find the box fill: light yellow FFFFE1
lymask = (R > 235) & (G > 230) & (B > 195) & (B < 245) & (R - B > 8) & (G - B > 8)
cz = np.zeros_like(lymask); cz[420:530, 20:940] = True
cmm = lymask & cz
rowprof = cmm.sum(axis=1)
print("caption fill row runs (count>200):")
inrun = False
for y in range(420, 530):
    if rowprof[y] > 200 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 200 and inrun:
        print(f"  y{s}..{y-1}"); inrun = False
if inrun: print(f"  y{s}..529")
colprof = cmm.sum(axis=0)
print("caption fill col runs (count>30):")
inrun = False
for x in range(20, 940):
    if colprof[x] > 30 and not inrun:
        s = x; inrun = True
    elif colprof[x] <= 30 and inrun:
        print(f"  x{s}..{x-1}"); inrun = False
if inrun: print(f"  x{s}..939")
# blue border of caption box: scan for saturated blue rows/cols around the box
blueish = (B - R > 40) & (B > 120)
print("caption border scan rows y425..525 (blue count>300):")
for y in range(425, 525):
    c = blueish[y, 30:930].sum()
    if c > 300:
        print(f"  row y={y}: {c}")
print("caption border scan cols x50..900 (blue count>25):")
for x in range(50, 900):
    c = blueish[430:520, x].sum()
    if c > 25:
        print(f"  col x={x}: {c}")
# caption text lines: dark blue + red inks inside box
btext = (B - R > 60) & (B - G > 40)
rtext = (R > 140) & (R - G > 90) & (R - B > 90)
linez = np.zeros_like(btext); linez[440:515, 60:900] = True
bt = btext & linez
rt = rtext & linez
ys, xs = np.where(bt)
print(f"caption blue text ink x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")
rowprof = bt.sum(axis=1)
print("blue text row runs (count>3):")
inrun = False
for y in range(440, 515):
    if rowprof[y] > 3 and not inrun:
        s = y; inrun = True
    elif rowprof[y] <= 3 and inrun:
        print(f"  y{s}..{y-1}"); inrun = False
ys, xs = np.where(rt)
print(f"caption red text ink: n={len(xs)}", f"x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}" if len(xs) else "")

print("=== L. LABELS 'Image'/'Filter' search y150..205 ===")
darkl = (R < 110) & (G < 110) & (B < 110)
for (x0, x1, lab) in [(50, 320, "Image-zone"), (230, 420, "Filter-zone")]:
    lz2 = np.zeros_like(darkl); lz2[150:205, x0:x1] = True
    lm = darkl & lz2
    ys, xs = np.where(lm)
    if len(xs):
        print(f"{lab}: ink x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")
        # column gaps for word structure
        colprof = lm.sum(axis=0)
        runs = []
        inrun = False
        for x in range(x0, x1):
            if colprof[x] > 0 and not inrun:
                s = x; inrun = True
            elif colprof[x] == 0 and inrun:
                runs.append((s, x - 1)); inrun = False
        print(f"  col runs: {runs}")
    else:
        print(f"{lab}: EMPTY")
