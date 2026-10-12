#!/usr/bin/env python3
# measure_original.py — PIL forensics on the ground-truth frame slide_006.jpg (960x540, 1px=1pt).
# Measures: title ink, content box border, header 2-line serif block (bold+underline phrase),
# 12 bullet bands (blue) + bullet dots (black), black bottom bar, modal colors, cursor zone.
from PIL import Image
import numpy as np

ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
H, W = a.shape[:2]
print(f"frame {W}x{H}")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (r > 110) & (r - g > 45) & (r - b > 35)
blue = (b > 105) & (b - r > 55) & (b - g > 55)
dark = a.max(axis=2) < 150
blackbar = a.max(axis=2) < 80
ink = dark | red | blue

def bbox(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (int(xs.min()) + x0, int(xs.max()) + x0, int(ys.min()) + y0, int(ys.max()) + y0)

def modal(mask, x0, x1, y0, y1):
    px = a[y0:y1, x0:x1][mask[y0:y1, x0:x1]]
    if not len(px):
        return None
    vals, counts = np.unique(px, axis=0, return_counts=True)
    # top-3 modes
    order = np.argsort(-counts)[:3]
    return [(tuple(int(v) for v in vals[i]), int(counts[i])) for i in order]

print("== title (red ink, y 55..130) ==")
tb = bbox(red, 100, 900, 55, 130)
print("title ink bbox (L,R,T,B):", tb, "-> advance", tb[1] - tb[0] + 1, "cap-h", tb[3] - tb[2] + 1)
print("title red modal:", modal(red, tb[0], tb[1], tb[2], tb[3]))
# column profile at the title mid-row to look at stroke shape (serif check)
midy = (tb[2] + tb[3]) // 2
row = red[midy, tb[0]:tb[1] + 1]
runs = []
inrun = False
for i, v in enumerate(row):
    if v and not inrun:
        s = i; inrun = True
    elif not v and inrun:
        runs.append((s + tb[0], i - 1 + tb[0], i - s)); inrun = False
if inrun:
    runs.append((s + tb[0], len(row) - 1 + tb[0], len(row) - s))
print("title mid-row stroke runs (first 12):", runs[:12])

print("== content box (red border) ==")
print("box top edge:", bbox(red, 300, 700, 120, 145))
print("box bottom edge:", bbox(red, 300, 700, 480, 516))
print("box left edge:", bbox(red, 60, 100, 250, 450))
print("box right edge:", bbox(red, 860, 910, 250, 450))
# border modal color
bb = bbox(red, 300, 700, 485, 510)
if bb:
    print("border red modal:", modal(red, bb[0], bb[1], bb[2], bb[3]))

print("== header block (dark ink inside box top, x 90..880, y box_top+2 .. box_top+75) ==")
boxT = bbox(red, 300, 700, 120, 145)[2]
hb = bbox(dark, 90, 880, boxT + 3, boxT + 80)
print("header ink bbox:", hb)
# split header lines by row profile
if hb:
    rows = dark[hb[2]:hb[3] + 1, hb[0]:hb[1] + 1].sum(axis=1)
    bands = []
    inb = False
    for i, v in enumerate(rows):
        if v > 0 and not inb:
            s = i; inb = True
        elif v == 0 and inb:
            bands.append((s + hb[2], i - 1 + hb[2])); inb = False
    if inb:
        bands.append((s + hb[2], len(rows) - 1 + hb[2]))
    print("header line bands (top..bottom):", bands)
    for k, (y0, y1) in enumerate(bands):
        lb = bbox(dark, 90, 880, y0, y1 + 1)
        print(f"  header L{k}: bbox {lb} advance {lb[1]-lb[0]+1}")
    # underline: check for a long horizontal dark run in the lower part of line 1
    y0, y1 = bands[0]
    for yy in range(y0, y1 + 1):
        seg = dark[yy, 90:500]
        if seg.sum() > 150:
            xs2 = np.where(seg)[0]
            print(f"  underline candidate row y={yy}: run x {xs2.min()+90}..{xs2.max()+90} len {seg.sum()}")
    print("header black modal:", modal(dark, hb[0], hb[1], bands[0][0], bands[-1][1]))

print("== bullet bands (blue, x 100..880, y below header .. box_bottom) ==")
boxB = bbox(red, 300, 700, 480, 516)[2]
by0 = (bands[-1][1] if hb else boxT + 80) + 3
blb = bbox(blue, 100, 880, by0, boxB)
print("blue overall bbox:", blb)
rows = blue[by0:boxB, 100:880].sum(axis=1)
bands2 = []
inb = False
for i, v in enumerate(rows):
    if v > 0 and not inb:
        s = i; inb = True
    elif v == 0 and inb:
        bands2.append((s + by0, i - 1 + by0)); inb = False
if inb:
    bands2.append((s + by0, len(rows) - 1 + by0))
print(f"n blue bands: {len(bands2)}")
for k, (y0, y1) in enumerate(bands2):
    lb = bbox(blue, 100, 880, y0, y1 + 1)
    print(f"  bullet {k+1}: y {y0}..{y1} (h {y1-y0+1}) x {lb[0]}..{lb[1]} adv {lb[1]-lb[0]+1}")
centers = [ (y0 + y1) / 2 for y0, y1 in bands2 ]
if len(centers) > 1:
    print("pitch between band centers:", [round(centers[i+1] - centers[i], 1) for i in range(len(centers) - 1)])
print("bullet blue modal:", modal(blue, 100, 880, by0, boxB))

print("== bullet dots (dark, x left of blue text) ==")
# blue text left edge across all bands
lefts = [bbox(blue, 100, 880, y0, y1 + 1)[0] for y0, y1 in bands2]
print("blue text left edges:", lefts)
txl = min(lefts)
db = bbox(dark, 95, txl - 2, by0, boxB)
print("dots overall bbox (x<%d):" % txl, db)
# per-band dot detection
for k, (y0, y1) in enumerate(bands2):
    d = bbox(dark, 95, txl - 2, y0 - 2, y1 + 3)
    if d:
        print(f"  dot {k+1}: bbox {d} cx {(d[0]+d[1])/2:.1f} cy {(d[2]+d[3])/2:.1f} d {d[1]-d[0]+1}x{d[3]-d[2]+1}")

print("== black bottom bar ==")
print("bar bbox:", bbox(blackbar, 0, 960, 505, 540))

print("== last bullet vs box bottom border ==")
if bands2:
    ly0, ly1 = bands2[-1]
    print(f"last blue band y {ly0}..{ly1}; box bottom border top row {boxB}")
    print(f"  gap border_top - band_bottom = {boxB - ly1}")
    # check for blue ink BELOW the border row inside x range
    below = blue[boxB:boxB + 12, 100:880]
    print("  blue px below border row:", int(below.sum()))

print("== cursor zone (spec: ~27% x, 73% y => (259, 394)) ==")
print("dark ink bbox near cursor zone:", bbox(dark, 230, 300, 360, 430))
