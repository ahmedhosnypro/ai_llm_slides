#!/usr/bin/env python3
"""Slide 045 — strip colors, dot rows, row y-bands, FFN box internals, annotation box lines."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
SX, OX = 0.962329, 17.582
SY, OY = 0.957576, -0.0909
def sx_(fx): return (fx - OX) / SX
def sy_(fy): return (fy - OY) / SY

# 1) strip colors across X-row col1 bar (fx 174..235, y 483..495): mode color per x
print("== X row col1 strip colors (y 484..494 mode) ==")
prev = None
for x in range(170, 240):
    col = img[484:495, x]
    med = tuple(np.median(col, axis=0).astype(int))
    if prev is None or max(abs(med[i]-prev[i]) for i in range(3)) > 25:
        print(x, med, f"slide_x={sx_(x):.1f}")
        prev = med

# 2) dot rows with looser masks
blue = (B - R > 40) & (B - G > 40) & (B > 110)
for nm, (ya, yb) in [("C", (380, 394)), ("A", (168, 182)), ("B", (274, 288))]:
    seg = blue[ya:yb, 590:700]
    cols = np.where(seg.sum(axis=0) > 2)[0]
    cl = []
    if len(cols):
        s = p = cols[0]
        for c in cols[1:]:
            if c > p + 4: cl.append((s, p)); s = c
            p = c
        cl.append((s, p))
    ys = np.where(seg.any(axis=1))[0]
    print(f"row {nm} blue dots fx centers:", [round((a+b)/2+590,1) for a,b in cl],
          "dia:", [b-a+1 for a,b in cl], "y", (ys.min()+ya, ys.max()+ya) if len(ys) else None)
green = (G - R > 40) & (G - B > 40) & (G > 110)
seg = green[482:498, 590:700]
cols = np.where(seg.sum(axis=0) > 2)[0]
cl = []
if len(cols):
    s = p = cols[0]
    for c in cols[1:]:
        if c > p + 4: cl.append((s, p)); s = c
        p = c
    cl.append((s, p))
ys = np.where(seg.any(axis=1))[0]
print("row D green dots fx centers:", [round((a+b)/2+590,1) for a,b in cl],
      "dia:", [b-a+1 for a,b in cl], "y", (ys.min()+482, ys.max()+482) if len(ys) else None)

# 3) full row bands: vertical profile of non-white density across bar columns (fx 174..864)
nonwhite = ~((R > 235) & (G > 235) & (B > 235))
print("== vertical density profile (fx 174..864) ==")
dens = nonwhite[:, 174:864].sum(axis=1)
inband = False
for y in range(155, 520):
    d = dens[y]
    if not inband and d > 40:
        start = y; inband = True
    elif inband and d <= 12:
        print(f"band {start}..{y-1} (h={y-start}) -> slide y {sy_(start):.1f}..{sy_(y-1):.1f}")
        inband = False

# 4) FFN box: blue border rows/cols (long runs)
bluestrong = (B > 120) & (R < 110) & (G < 110)
rows = [y for y in range(195, 265) if bluestrong[y, 70:890].mean() > 0.75]
print("FFN border rows:", rows)
cols_ = [x for x in range(60, 900) if bluestrong[202:256, x].mean() > 0.75]
print("FFN border cols:", cols_[:6], cols_[-6:] if len(cols_) > 6 else "")
# FFN title ink (navy bold italic + red RELU): dark pixels inside 203..256 above icons
dark = (R < 120) & (G < 120) & (B < 160)
seg = dark[204:222, 200:760]
rr = np.where(seg.any(axis=1))[0]; cc = np.where(seg.any(axis=0))[0]
print("FFN title ink fx", cc.min()+200, cc.max()+200, "fy", rr.min()+204, rr.max()+204,
      "-> slide", round(sx_(cc.min()+200),1), round(sx_(cc.max()+200),1), round(sy_(rr.min()+204),1), round(sy_(rr.max()+204),1))
# red RELU inside title
redink = (R > 150) & (G < 70) & (B < 70)
seg = redink[204:224, 200:780]
cc = np.where(seg.any(axis=0))[0]
if len(cc): print("RELU red ink fx", cc.min()+200, cc.max()+200)

# 5) FFN icon tiles: lemon tiles FFFFCC-ish with orange border, band y 228..256
lemon = (R > 240) & (G > 240) & (B > 160) & (B < 225)
seg = lemon[226:258, 60:900]
colsum = seg.sum(axis=0)
cols = np.where(colsum > 8)[0]
cl = []
if len(cols):
    s = p = cols[0]
    for c in cols[1:]:
        if c > p + 6: cl.append((s, p)); s = c
        p = c
    cl.append((s, p))
print("FFN tiles:", len(cl))
for a, b in cl:
    seg2 = seg[:, a:b+1]
    ys = np.where(seg2.any(axis=1))[0]
    cx = (a+b)/2+60
    print(f"   tile fx {a+60}..{b+60} w={b-a+1} cx={cx:.1f} y {ys.min()+226}..{ys.max()+226} -> slide cx {sx_(cx):.1f} w {(b-a+1)/SX:.1f} y {sy_(ys.min()+226):.1f}..{sy_(ys.max()+226):.1f}")

# 6) annotation box lines: dark ink rows inside box (fy 88..152)
dark2 = (R < 150) & (G < 150) & (B < 200)
seg = dark2[86:154, 80:880]
rowsum = seg.sum(axis=1)
bands = []
inb = False
for i, d in enumerate(rowsum):
    if not inb and d > 6: st = i; inb = True
    elif inb and d <= 3:
        bands.append((st+86, i-1+86)); inb = False
if inb: bands.append((st+86, len(rowsum)-1+86))
print("annot text line bands:", bands)
for (a, b) in bands:
    seg2 = seg[a-86:b-86+1]
    cc = np.where(seg2.any(axis=0))[0]
    print(f"   line y {a}..{b} -> slide {sy_(a):.1f}..{sy_(b):.1f}  x {cc.min()+80}..{cc.max()+80} -> slide {sx_(cc.min()+80):.1f}..{sx_(cc.max()+80):.1f}")
