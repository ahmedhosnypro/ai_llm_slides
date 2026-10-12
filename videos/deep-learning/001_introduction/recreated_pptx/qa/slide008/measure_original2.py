#!/usr/bin/env python3
"""Second forensic pass: top-of-frame check, red bands below title (headers), box geometry,
bullet dots, per-line x extents, modal colors."""
from PIL import Image
import numpy as np
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_008.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def modal(x0, y0, x1, y1, label, n=5):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    cnt = Counter(map(tuple, reg))
    print(f"{label}: {cnt.most_common(n)}")

# --- top of frame: what's in rows 0..63? ---
print("-- rows 0..63: any red (R>110,G<90,B<90) count per row --")
red = (R > 110) & (G < 90) & (B < 90)
for y in range(0, 64):
    c = red[y].sum()
    if c > 5:
        xs = np.nonzero(red[y])[0]
        print(f"  y={y}: n={c} x {xs.min()}..{xs.max()}")
print("-- modal colors rows 0..30, 30..45, 45..60 --")
modal(0, 0, 960, 30, "rows 0..30")
modal(0, 30, 960, 45, "rows 30..45")
modal(0, 45, 960, 60, "rows 45..60")
modal(0, 0, 30, 540, "left edge cols 0..30")
modal(930, 0, 960, 540, "right edge cols 930..960")

# --- title lines: full red-band segmentation y60..152 ---
red_title = red.copy()
red_title[:60] = False
red_title[152:] = False
rows_t = red_title.sum(axis=1)
segs = []
start = None
for y in range(60, 152):
    if rows_t[y] > 5 and start is None:
        start = y
    elif rows_t[y] <= 5 and start is not None:
        segs.append((start, y - 1)); start = None
if start is not None:
    segs.append((start, 151))
print("\n-- title red bands --")
for s, e in segs:
    band = red_title[s:e + 1]
    ys2, xs2 = np.nonzero(band)
    print(f"  y {s}..{e} (h {e-s+1}): x {xs2.min()}..{xs2.max()} (advance {xs2.max()-xs2.min()+1}, center {(xs2.min()+xs2.max())/2})")

# --- red bands y152..540 EXCLUDING box borders (x58 col, x460 col, y153 row, y513 row) ---
red2 = red.copy()
red2[:152] = False
red2[152:155, :] = False   # top border
red2[511:516, :] = False   # bottom border
red2[:, 56:61] = False     # left border
red2[:, 458:463] = False   # right border
rows_r = red2.sum(axis=1)
segs2 = []
start = None
for y in range(152, H):
    if rows_r[y] > 5 and start is None:
        start = y
    elif rows_r[y] <= 5 and start is not None:
        segs2.append((start, y - 1)); start = None
print("\n-- red bands below title (headers) --")
for s, e in segs2:
    band = red2[s:e + 1]
    ys2, xs2 = np.nonzero(band)
    print(f"  y {s}..{e} (h {e-s+1}): x {xs2.min()}..{xs2.max()} (advance {xs2.max()-xs2.min()+1})")

# --- box border geometry: red cols/rows ---
box = red.copy()
box[:150] = False
cols_b = box.sum(axis=0)
print("\n-- box vertical border columns (red count > 200) --")
for x in range(W):
    if cols_b[x] > 200:
        print(f"  x={x}: {cols_b[x]}")
rows_b = box.sum(axis=1)
print("-- box horizontal border rows (red count > 200) --")
for y in range(H):
    if rows_b[y] > 200:
        print(f"  y={y}: {rows_b[y]}")

# --- white box interior extent (white modal) ---
white = (R > 245) & (G > 245) & (B > 245)
# interior sample
modal(200, 250, 300, 280, "box interior")
modal(700, 250, 760, 280, "outside-box right region")
modal(100, 60, 860, 150, "title region background")

# --- bullet dots: dark px columns in a bullet line band ---
dark = (R < 100) & (G < 100) & (B < 100)
print("\n-- bullet line 1 'Python' (y188..199): dark col profile --")
band = dark[188:200]
cols_d = band.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if cols_d[x] > 0 and not inrun:
        s = x; inrun = True
    elif cols_d[x] == 0 and inrun:
        runs.append((s, x - 1)); inrun = False
print("  col runs:", runs[:12])

print("\n-- bullet line 3 'Matlab' (y239..250): dark col runs --")
band = dark[239:251]
cols_d = band.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if cols_d[x] > 0 and not inrun:
        s = x; inrun = True
    elif cols_d[x] == 0 and inrun:
        runs.append((s, x - 1)); inrun = False
print("  col runs:", runs[:12])

# --- header 1 red col profile (y165..181) ---
print("\n-- header1 red col runs (y163..182) --")
band = red[163:182]
cols_r = band.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if cols_r[x] > 0 and not inrun:
        s = x; inrun = True
    elif cols_r[x] == 0 and inrun:
        runs.append((s, x - 1)); inrun = False
print("  col runs:", runs[:16])

# --- ink colors: title red modal (saturated px only) ---
print("\n-- ink color modals --")
tt = red.copy(); tt[:60] = False; tt[152:] = False
ys, xs = np.nonzero(tt)
px = a[ys, xs]
cnt = Counter(map(tuple, px))
print("title red:", cnt.most_common(6))
ys, xs = np.nonzero(red[163:182])
px = a[163:182][ys, xs]
cnt = Counter(map(tuple, px))
print("header1 red:", cnt.most_common(6))
ys, xs = np.nonzero(dark[239:251])
px = a[239:251][ys, xs]
cnt = Counter(map(tuple, px))
print("bullet Matlab dark:", cnt.most_common(6))
# bottom black bar extent
bb = (R < 60) & (G < 60) & (B < 60)
ys, xs = np.nonzero(bb[519:540])
print(f"bottom bar: x {xs.min()}..{xs.max()}, y 519..539")
