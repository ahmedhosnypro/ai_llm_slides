#!/usr/bin/env python3
"""PIL forensics pass 2 — slide_047.jpg fine measurements."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_047.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

def bbox(x0, y0, x1, y1, pred, label):
    sub = a[y0:y1, x0:x1]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"{label:36s} EMPTY")
        return None
    r = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    print(f"{label:36s} x {r[0]}..{r[2]}  y {r[1]}..{r[3]}  (w {r[2]-r[0]+1} h {r[3]-r[1]+1})")
    return r

dark  = lambda s: (s.sum(axis=2) < 330)
notred = lambda s: ~((s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60))
dk_notred = lambda s: (s.sum(axis=2) < 330) & notred(s)
red   = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
blue  = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)
darkblue = lambda s: (s[:,:,2] > 60) & (s[:,:,2] - s[:,:,0] > 30) & (s.sum(axis=2) < 420)

# --- what is at y 43..70 (above title)? ---
print("-- top area y 40..70 --")
for y in (43, 50, 60, 65):
    dk = np.nonzero(dk_notred(a[y:y+1])[0])[0]
    print(f"  y={y}: dark-notred n={len(dk)}", (int(dk.min()), int(dk.max())) if len(dk) else "")

# --- title detail ---
print("\n-- title --")
r = bbox(60, 55, 900, 110, red, "title red runs")
b = bbox(60, 55, 900, 110, blue, "title blue runs")
# red segments along x (gaps = words)
sub = a[60:105, 60:900]
rm = red(sub)
colhas = rm.sum(axis=0) > 0
segs = []
s = None
for i, v in enumerate(colhas):
    if v and s is None: s = i
    elif not v and s is not None:
        if i - s > 3: segs.append((60+s, 60+i-1))
        s = None
if s is not None: segs.append((60+s, 60+len(colhas)-1))
print("title red x-segments (w>3):", segs)
bm = blue(sub)
colhasb = bm.sum(axis=0) > 0
segsb = []
s = None
for i, v in enumerate(colhasb):
    if v and s is None: s = i
    elif not v and s is not None:
        if i - s > 3: segsb.append((60+s, 60+i-1))
        s = None
if s is not None: segsb.append((60+s, 60+len(colhasb)-1))
print("title blue x-segments (w>3):", segsb)
print("title red px sample:", a[85, 200].tolist(), a[85, 700].tolist())
print("title blue px sample:", a[85, 480].tolist())
# title y-extent per color
ry, rx = np.nonzero(red(a[55:110, 60:900]))
by, bx = np.nonzero(blue(a[55:110, 60:900]))
print("red y-extent:", 55+ry.min(), 55+ry.max(), " blue y-extent:", 55+by.min(), 55+by.max())

# --- intro lines: exact y-bands + left/right edges + colors ---
print("\n-- intro lines y 120..215 x 60..900 --")
sub = a[120:215, 60:900]
m = (sub.sum(axis=2) < 520)
rows = m.sum(axis=1)
run = None
for i, v in enumerate(rows):
    y = 120 + i
    if v > 2 and run is None: run = y
    elif v <= 2 and run is not None:
        seg2 = a[run:y, 60:900]
        mm = (seg2.sum(axis=2) < 520)
        ys2, xs2 = np.nonzero(mm)
        rm2 = red(seg2); bm2 = darkblue(seg2)
        ry2, rx2 = np.nonzero(rm2); by2, bx2 = np.nonzero(bm2)
        print(f"line y {run}..{y-1} h={y-run} x {60+xs2.min()}..{60+xs2.max()}"
              + (f" RED x {60+rx2.min()}..{60+rx2.max()} (n={len(rx2)})" if len(rx2) else " (no red)")
              + (f" DBLUE x {60+bx2.min()}..{60+bx2.max()} (n={len(bx2)})" if len(bx2) else " (no dblue)"))
        run = None
if run is not None:
    seg2 = a[run:215, 60:900]
    mm = (seg2.sum(axis=2) < 520)
    ys2, xs2 = np.nonzero(mm)
    rm2 = red(seg2); bm2 = darkblue(seg2)
    ry2, rx2 = np.nonzero(rm2); by2, bx2 = np.nonzero(bm2)
    print(f"line y {run}..214 (open) x {60+xs2.min()}..{60+xs2.max()}"
          + (f" RED n={len(rx2)}" if len(rx2) else " (no red)")
          + (f" DBLUE n={len(bx2)}" if len(bx2) else " (no dblue)"))
print("line1 sample (y=140,x=100):", a[140, 100].tolist())
print("line2 sample (y=166,x=100):", a[166, 100].tolist())
print("line3 sample (y=192,x=100):", a[192, 100].tolist())

# --- content box borders: exact strokes ---
print("\n-- content box border strokes --")
# horizontal strokes: rows where red count in x 60..900 is high
sub = a[200:520, 60:900]
rm = red(sub)
rowcount = rm.sum(axis=1)
for i, c in enumerate(rowcount):
    if c > 200:
        print(f"  red row y={200+i}: count {c}")
# vertical strokes: cols where red count in y 210..500 is high
sub = a[210:500, 40:920]
rm = red(sub)
colcount = rm.sum(axis=0)
for j, c in enumerate(colcount):
    if c > 100:
        print(f"  red col x={40+j}: count {c}")
print("box border color sample:", a[220, 400].tolist(), a[487, 400].tolist())

# --- bullet markers (dark rings?) scan x 88..118 ---
print("\n-- bullet markers x 88..118, y 220..360 --")
seg = a[220:360, 88:118]
mm = (seg.sum(axis=2) < 600)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    yy = np.sort(np.unique(ys2))
    splits = np.nonzero(np.diff(yy) > 3)[0]
    start = 0
    for idx in list(splits) + [len(yy)-1]:
        band = yy[start:idx+1]
        bm2 = mm[band.min():band.max()+1]
        bys, bxs = np.nonzero(bm2)
        print(f"  marker y {220+band.min()}..{220+band.max()} x {88+bxs.min()}..{88+bxs.max()} n={len(bxs)}")
        start = idx + 1
    print("  marker px sample:", a[230, 105].tolist())
else:
    print("  none")

# --- bullet line 1/2 text: exact extent + color ---
print("\n-- bullet lines 1-2 --")
b1 = bbox(95, 222, 560, 250, dk_notred, "line1 dark-notred ink")
b2 = bbox(95, 252, 560, 278, dk_notred, "line2 dark-notred ink")
print("line1 text sample:", a[234, 200].tolist())
print("line2 text sample:", a[264, 200].tolist())
# 'average' bold underline? check underline row in line2
sub = a[268:276, 130:300]
mm = (sub.sum(axis=2) < 500)
for i in range(mm.shape[0]):
    cnt = mm[i].sum()
    if cnt > 30:
        print(f"  line2 underline row y={268+i}: dark count {cnt}")

# --- bullet 3/4: blue label boxes + equations ---
print("\n-- bullet 3 label box (blue border) --")
seg = a[280:320, 95:330]
bm = blue(seg)
ys2, xs2 = np.nonzero(bm)
if len(xs2):
    print(f"  blue ink x {95+xs2.min()}..{95+xs2.max()} y {280+ys2.min()}..{280+ys2.max()}")
print("  blue border px:", a[285, 110].tolist(), a[300, 109].tolist())
# label box border columns: blue count per column
colcount = bm.sum(axis=0)
cols = np.nonzero(colcount > 10)[0]
print("  blue border cols:", (95+cols.min(), 95+cols.max()) if len(cols) else "none", [int(95+c) for c in cols[:8]])
rowcount = bm.sum(axis=1)
rowsb = np.nonzero(rowcount > 10)[0]
print("  blue border rows:", (280+rowsb.min(), 280+rowsb.max()) if len(rowsb) else "none", [int(280+r) for r in rowsb[:8]])
# eq 3 region: x right of box
b3 = bbox(315, 280, 560, 318, dk_notred, "eq3 ink (x>315)")
b3r = bbox(315, 280, 560, 318, red, "eq3 red ink")
print("  eq3 px sample:", a[298, 350].tolist())
seg = a[280:318, 315:560]
mm = (seg.sum(axis=2) < 500)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    yy = np.sort(np.unique(ys2))
    print("  eq3 y-bands:", end=" ")
    splits = np.nonzero(np.diff(yy) > 2)[0]
    start = 0
    bands = []
    for idx in list(splits) + [len(yy)-1]:
        bands.append((280+yy[start], 280+yy[idx])); start = idx+1
    print(bands)

print("\n-- bullet 4 label box --")
seg = a[318:360, 95:330]
bm = blue(seg)
ys2, xs2 = np.nonzero(bm)
if len(xs2):
    print(f"  blue ink x {95+xs2.min()}..{95+xs2.max()} y {318+ys2.min()}..{318+ys2.max()}")
b4 = bbox(315, 318, 560, 358, dk_notred, "eq4 ink (x>315)")
b4r = bbox(315, 318, 560, 358, red, "eq4 red ink")
print("  eq4 px sample:", a[338, 350].tolist())
seg = a[318:358, 315:560]
mm = (seg.sum(axis=2) < 500)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    yy = np.sort(np.unique(ys2))
    splits = np.nonzero(np.diff(yy) > 2)[0]
    start = 0
    bands = []
    for idx in list(splits) + [len(yy)-1]:
        bands.append((318+yy[start], 318+yy[idx])); start = idx+1
    print("  eq4 y-bands:", bands)

# --- legend box fine ---
print("\n-- legend box --")
# exact border: red rows/cols in x 440..610, y 340..500
seg = a[340:500, 440:610]
rm = red(seg)
rowcount = rm.sum(axis=1)
rowsr = np.nonzero(rowcount > 60)[0]
print("  legend red border rows:", [int(340+r) for r in rowsr])
colcount = rm.sum(axis=0)
colsr = np.nonzero(colcount > 60)[0]
print("  legend red border cols:", [int(440+c) for c in colsr])
# text bands inside (x 455..600, y 350..490)
sub = a[350:490, 450:600]
mm = (sub.sum(axis=2) < 480)
rows = mm.sum(axis=1)
run = None
bands = []
for i, v in enumerate(rows):
    y = 350 + i
    if v > 1 and run is None: run = y
    elif v <= 1 and run is not None:
        bands.append((run, y-1)); run = None
if run is not None: bands.append((run, 489))
print("  legend text bands:", bands)
# header color + letter/word colors
print("  header sample (Where:):", a[365, 470].tolist())
print("  row1 letter sample:", a[385, 465].tolist(), " word sample:", a[385, 490].tolist())
print("  fill sample:", a[430, 470].tolist())
# letters red? words blue?
seg = a[380:480, 455:600]
rmm = red(seg); bmm = darkblue(seg)
ry2, rx2 = np.nonzero(rmm); by2, bx2 = np.nonzero(bmm)
print("  red ink in legend body: n=", len(rx2), " blue ink: n=", len(bx2))
if len(rx2): print("   red x-range:", 455+rx2.min(), "..", 455+rx2.max())
if len(bx2): print("   blue x-range:", 455+bx2.min(), "..", 455+bx2.max())

# --- 4x4 grid: cell boundaries via white gaps ---
print("\n-- 4x4 grid cells --")
green = lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
yellow= lambda s: (s[:,:,0] > 180) & (s[:,:,1] > 170) & (s[:,:,2] < 130)
redf  = lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90)
cyan  = lambda s: (s[:,:,2] > 150) & (s[:,:,1] > 120) & (s[:,:,0] < 140) & (s[:,:,2] - s[:,:,0] > 60)
sub = a[355:495, 560:740]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
colcount = colored.sum(axis=0)
cols = np.nonzero(colcount > 10)[0]
rowcount = colored.sum(axis=1)
rws = np.nonzero(rowcount > 10)[0]
print(f"  grid overall x {560+cols.min()}..{560+cols.max()} y {355+rws.min()}..{355+rws.max()}")
# column profile: gaps where colcount < 5
prof = colcount.copy()
gaps = [i for i in range(len(prof)) if prof[i] < 5]
# cluster gaps
runs = []
if gaps:
    s = gaps[0]; p = gaps[0]
    for g in gaps[1:]:
        if g != p+1:
            runs.append((s, p)); s = g
        p = g
    runs.append((s, p))
print("  x-gap runs (grid coords):", runs)
gapsr = [i for i in range(len(rws)) if rws.min() <= i <= rws.max() and rowcount[i] < 5]
runsr = []
if gapsr:
    s = gapsr[0]; p = gapsr[0]
    for g in gapsr[1:]:
        if g != p+1:
            runsr.append((s, p)); s = g
        p = g
    runsr.append((s, p))
print("  y-gap runs (grid coords):", [(355+s, 355+e) for s, e in runsr])
# numerals: dark ink in grid area
sub = a[355:495, 560:740]
mm = (sub.sum(axis=2) < 250) & notred(sub)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    print(f"  numeral ink x {560+xs2.min()}..{560+xs2.max()} y {355+ys2.min()}..{355+ys2.max()} n={len(xs2)}")

# --- arrow (dark, not red) fine ---
print("\n-- arrow --")
bbox(730, 390, 795, 465, dk_notred, "arrow dark-notred ink")
print("  arrow px sample:", a[425, 760].tolist())
# fraction: red
bbox(795, 390, 835, 465, red, "fraction red ink")
# separate numerator/denominator bands
seg = a[390:465, 795:835]
rm = red(seg)
rows = rm.sum(axis=1)
bands = []
run = None
for i, v in enumerate(rows):
    y = 390 + i
    if v > 1 and run is None: run = y
    elif v <= 1 and run is not None:
        bands.append((run, y-1)); run = None
if run is not None: bands.append((run, 464))
print("  fraction y-bands:", bands)

# --- output grid cells ---
print("\n-- 2x2 output grid --")
sub = a[385:470, 795:890]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
colcount = colored.sum(axis=0)
cols = np.nonzero(colcount > 5)[0]
rowcount = colored.sum(axis=1)
rws = np.nonzero(rowcount > 5)[0]
print(f"  out grid overall x {795+cols.min()}..{795+cols.max()} y {385+rws.min()}..{385+rws.max()}")
gaps = [i for i in range(cols.min(), cols.max()+1) if colcount[i] < 4]
print("  x-gaps:", [(795+g) for g in gaps])
gapsr = [i for i in range(rws.min(), rws.max()+1) if rowcount[i] < 4]
print("  y-gaps:", [(385+g) for g in gapsr])
mm = (sub.sum(axis=2) < 250) & notred(sub)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    print(f"  numerals ink n={len(xs2)}")

# --- bottom strip exact top ---
print("\n-- bottom strip --")
for y in range(505, 525):
    dk = np.nonzero(a[y:y+1].sum(axis=2)[0] < 150)[0]
    if len(dk) > 100:
        print(f"  strip starts y={y} (n={len(dk)})")
        break
