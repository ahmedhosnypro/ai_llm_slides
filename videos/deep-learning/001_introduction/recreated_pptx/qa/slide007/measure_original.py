#!/usr/bin/env python3
"""Re-PIL-measure the ORIGINAL slide_007.jpg (ground truth, 960x540, 1px=1pt).
Verifies the predecessor's measurements (its numbers were never checked).
Regions: outer 'L' frame lines, inner red frame, black strip, title box +
title line inks, 4 domain boxes (bounds + modal colors), 4 arrow curves
(stroke centers traced in the arrow band), arrowhead tips, badge area.
"""
from PIL import Image
import numpy as np

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_007.jpg"
img = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = img.shape[:2]
print(f"size {W}x{H}")

def lum(a):
    return 0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]

L = lum(img)

def col_profile_red(x0, x1, y0, y1, thr=120):
    """rows where red-ish (R high, G,B low) pixels exist in band."""
    band = img[y0:y1, x0:x1]
    red = (band[...,0] > thr) & (band[...,1] < 110) & (band[...,2] < 110)
    rows = np.where(red.any(axis=1))[0] + y0
    return rows

def dark_rows(x0, x1, y0, y1, thr=80):
    band = L[y0:y1, x0:x1]
    dark = band < thr
    return np.where(dark.any(axis=1))[0] + y0

def dark_cols(x0, x1, y0, y1, thr=80):
    band = L[y0:y1, x0:x1]
    dark = band < thr
    return np.where(dark.any(axis=0))[0] + x0

print("\n== per-slide outer frame (red L) ==")
# top line: scan columns 200..700 rows 35..55 for red
for y in range(30, 60):
    row = img[y, 200:700]
    n = int(((row[:,0] > 120) & (row[:,1] < 110) & (row[:,2] < 110)).sum())
    if n > 50:
        print(f"top line row y={y} redcount={n}")
# left line: scan rows 60..200 cols 40..80
for x in range(40, 90):
    col = img[60:200, x]
    n = int(((col[:,0] > 120) & (col[:,1] < 110) & (col[:,2] < 110)).sum())
    if n > 50:
        print(f"left line col x={x} redcount={n}")
# extents
red_top = col_profile_red(60, 900, 30, 60)
print("top line x-extent: ", end="")
r = img[42, :, ]
mask = (r[:,0] > 120) & (r[:,1] < 110) & (r[:,2] < 110)
xs = np.where(mask)[0]
print(f"y42 red cols {xs.min() if len(xs) else '-'}..{xs.max() if len(xs) else '-'} n={len(xs)}")
# left line vertical extent at x=58
c = img[:, 58]
maskc = (c[:,0] > 120) & (c[:,1] < 110) & (c[:,2] < 110)
ys = np.where(maskc)[0]
print(f"x58 red rows {ys.min() if len(ys) else '-'}..{ys.max() if len(ys) else '-'} n={len(ys)}")
# any right-side outer red? scan cols 890..940 rows 40..520
right = img[40:520, 890:945]
rm = (right[...,0] > 120) & (right[...,1] < 110) & (right[...,2] < 110)
print(f"right zone red px: {int(rm.sum())}")
# any bottom outer red? rows 495..520 cols 100..900 (outside inner frame bottom)
bot = img[490:519, 100:900]
bm = (bot[...,0] > 120) & (bot[...,1] < 110) & (bot[...,2] < 110)
print(f"below-inner-frame red px (y490..518): {int(bm.sum())}")

print("\n== inner red frame ==")
# left stroke: cols 60..80, rows 200..400
for x in range(60, 85):
    col = img[200:400, x]
    n = int(((col[:,0] > 120) & (col[:,1] < 110) & (col[:,2] < 110)).sum())
    if n > 100:
        print(f"inner left col x={x} n={n}")
# right stroke: cols 885..905
for x in range(885, 906):
    col = img[200:400, x]
    n = int(((col[:,0] > 120) & (col[:,1] < 110) & (col[:,2] < 110)).sum())
    if n > 100:
        print(f"inner right col x={x} n={n}")
# top stroke rows 110..130 cols 200..800
for y in range(110, 130):
    row = img[y, 200:800]
    n = int(((row[:,0] > 120) & (row[:,1] < 110) & (row[:,2] < 110)).sum())
    if n > 300:
        print(f"inner top row y={y} n={n}")
# bottom stroke rows 475..495
for y in range(475, 496):
    row = img[y, 200:800]
    n = int(((row[:,0] > 120) & (row[:,1] < 110) & (row[:,2] < 110)).sum())
    if n > 300:
        print(f"inner bottom row y={y} n={n}")

print("\n== black bottom strip ==")
rows = dark_rows(100, 900, 500, 540, thr=60)
print(f"dark rows y{rows.min()}..{rows.max()}")
cols = dark_cols(0, 960, 530, 539, thr=60)
print(f"strip cols x{cols.min()}..{cols.max()}")

print("\n== title box ==")
rows = dark_rows(250, 720, 100, 270, thr=60)
cols = dark_cols(250, 720, 140, 250, thr=60)
print(f"box rows y{rows.min()}..{rows.max()}, cols x{cols.min()}..{cols.max()}")
# yellow text inks inside box
box = img[rows.min():rows.max()+1, cols.min():cols.max()+1]
ylw = (box[...,0] > 200) & (box[...,1] > 200) & (box[...,2] < 120)
ys = np.where(ylw.any(axis=1))[0] + rows.min()
print("yellow text rows:", ys.min(), "..", ys.max())
# find line gaps: consecutive runs
runs = []
start = ys[0]; prev = ys[0]
for y in ys[1:]:
    if y > prev + 3:
        runs.append((start, prev)); start = y
    prev = y
runs.append((start, prev))
print("title line ink runs (y):", runs)
for (a, b) in runs:
    band = img[a:b+1, cols.min():cols.max()+1]
    ym = (band[...,0] > 200) & (band[...,1] > 200) & (band[...,2] < 120)
    xs = np.where(ym.any(axis=0))[0] + cols.min()
    print(f"  line y{a}..{b} x{xs.min()}..{xs.max()} cap_h={b-a+1}")

print("\n== domain boxes (bounds + modal colors) ==")
def modal(a):
    vals, counts = np.unique(a.reshape(-1, 3), axis=0, return_counts=True)
    return tuple(vals[counts.argmax()])
# scan row 380 (mid-box) for saturated color runs
row = img[380]
segs = []
cur = None
for x in range(60, 920):
    r, g, b = row[x]
    sat = (max(r,g,b) - min(r,g,b)) > 60
    if sat and cur is None:
        cur = x
    elif not sat and cur is not None:
        segs.append((cur, x-1)); cur = None
if cur is not None: segs.append((cur, 919))
print("saturated segments on row 380:", segs)
for (a, b) in segs:
    reg = img[340:430, a:b+1]
    m = modal(reg)
    # vertical extent of the box color at its center col
    xc = (a+b)//2
    col = img[280:470, xc]
    same = (np.abs(col - np.array(m)).sum(axis=1) < 60)
    ys = np.where(same)[0] + 280
    # text inks (white) inside box
    white = (reg[...,0] > 200) & (reg[...,1] > 200) & (reg[...,2] > 200)
    wys = np.where(white.any(axis=1))[0] + 340
    wruns = []
    if len(wys):
        st = wys[0]; pv = wys[0]
        for y in wys[1:]:
            if y > pv + 3:
                wruns.append((st, pv)); st = y
            pv = y
        wruns.append((st, pv))
    print(f"box x{a}..{b} modal{m} vext y{ys.min()}..{ys.max()} white-text runs y={wruns}")

print("\n== arrows: trace red stroke centers in band y245..330 ==")
# red mask in the fan band (exclude title box area y<=250 and box tops y>=328)
band = img[252:330, 60:920]
red = (band[...,0] > 120) & (band[...,1] < 110) & (band[...,2] < 110)
# label connected runs per row -> collect stroke centers
import collections
centers = collections.defaultdict(list)  # x_bucket -> list of (y, x)
for yy in range(red.shape[0]):
    xs = np.where(red[yy])[0]
    if len(xs) == 0: continue
    # split into runs with gap > 4
    groups = []
    st = xs[0]; pv = xs[0]
    for x in xs[1:]:
        if x > pv + 4:
            groups.append((st, pv)); st = x
        pv = x
    groups.append((st, pv))
    for (a, b) in groups:
        if a < 2 or b > red.shape[1]-3:  # clipped at band edge
            pass
        cx = (a + b) / 2 + 60
        centers[round(cx)].append((yy + 252, cx))
# print a downsampled trace: for each y row, list stroke-center xs
print("row -> stroke centers (x):")
for yy in range(0, red.shape[0], 4):
    xs = np.where(red[yy])[0]
    if len(xs) == 0: continue
    groups = []
    st = xs[0]; pv = xs[0]
    for x in xs[1:]:
        if x > pv + 4:
            groups.append((st, pv)); st = x
        pv = x
    groups.append((st, pv))
    print(f"  y={yy+252}: " + ", ".join(f"{(a+b)/2+60:.1f}(w{b-a+1})" for a, b in groups))

print("\n== arrowheads (solid red triangles) below y=310 ==")
band2 = img[305:330, 60:920]
red2 = (band2[...,0] > 120) & (band2[...,1] < 110) & (band2[...,2] < 110)
for yy in range(red2.shape[0]):
    xs = np.where(red2[yy])[0]
    if len(xs) == 0: continue
    groups = []
    st = xs[0]; pv = xs[0]
    for x in xs[1:]:
        if x > pv + 4:
            groups.append((st, pv)); st = x
        pv = x
    groups.append((st, pv))
    print(f"  y={yy+305}: " + ", ".join(f"{(a+b)/2+60:.1f}(w{b-a+1})" for a, b in groups))

print("\n== shared origin area (title box bottom, y245..258) ==")
band3 = img[245:262, 400:600]
red3 = (band3[...,0] > 120) & (band3[...,1] < 110) & (band3[...,2] < 110)
ys3, xs3 = np.where(red3)
if len(xs3):
    print(f"red ink y{ys3.min()+245}..{ys3.max()+245} x{xs3.min()+400}..{xs3.max()+400} n={len(xs3)}")

print("\n== top gray band + panel colors ==")
print("modal top band (y50..110, x100..800):", modal(img[50:110, 100:800]))
print("modal left margin (y100..400, x10..35):", modal(img[100:400, 10:35]))
print("modal right margin (y100..400, x925..955):", modal(img[100:400, 925:955]))
print("modal inside inner frame (y150..300, x80..280, excl title):", modal(img[260:320, 80:280]))
print("canvas corner (y0..10):", modal(img[0:10, 0:10]))
