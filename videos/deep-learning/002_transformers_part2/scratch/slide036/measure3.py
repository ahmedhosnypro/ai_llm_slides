#!/usr/bin/env python3
"""Stage 3: diagram elements — banner cols, token cells, arrows, dots, gutter labels,
title, caption, panel text lines; color cores; dump zoom crops for vision checks."""
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide036"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# --- banner cols (rows 396..442 interior) ---
navy = (r < 80) & (g < 80) & (b > 70) & (b < 180)
band = navy[396:443]
ncols = band.sum(axis=0)
nbc = [x for x in range(W) if ncols[x] > 40]
print("banner cols:", nbc[0], "..", nbc[-1])
inner = im[400:438, nbc[0]+6:nbc[0]+60].reshape(-1, 3)
print("banner fill median:", np.median(inner, axis=0), " p10:", np.percentile(inner, 10, axis=0))
# white text rows inside banner
white = (r > 200) & (g > 200) & (b > 200)
wrows = white[396:443, nbc[0]:nbc[-1]].sum(axis=1)
tw = [y+396 for y in range(47) if wrows[y] > 10]
print("banner white-text rows:", tw[0] if tw else None, "..", tw[-1] if tw else None)

# --- token rows: sample pixels across the Y band (y 340..385) and X band (y 460..505) ---
print("\n=== Y band row 360 samples (every 12px, x 200..900):")
print(" ".join(f"{x}:{tuple(im[360,x])}" for x in range(200, 900, 12)))
print("=== X band row 480 samples:")
print(" ".join(f"{x}:{tuple(im[480,x])}" for x in range(200, 900, 12)))

# find token-box colored cells: any saturated non-white non-red pixel in bands
def cellblobs(y0, y1, tag):
    sub = im[y0:y1]
    sr, sg, sb = sub[:,:,0], sub[:,:,1], sub[:,:,2]
    m = (np.max(sub, axis=2) - np.min(sub, axis=2)) > 25  # any tint
    cols = m.sum(axis=0)
    # group contiguous col runs with >3 tinted px
    runs, s, p = [], None, None
    for x in range(len(cols)):
        if cols[x] > 3:
            if s is None: s = p = x
            elif x == p+1: p = x
            else: runs.append((s,p)); s = p = x
    if s is not None: runs.append((s,p))
    print(f"{tag} tinted col runs (x0,x1,w):", [(a, b_, b_-a+1) for a,b_ in runs if b_-a+1 > 8])
    return runs

print()
yr = cellblobs(348, 388, "Y band")
xr = cellblobs(455, 500, "X band")

# vertical extent of one token box: col through the middle of first box
if yr:
    x0 = (yr[0][0]+yr[0][1])//2
    print(f"\ncol {x0} y 340..400:", " ".join(f"{y}:{tuple(im[y,x0])}" for y in range(340, 400, 2)))
    x1 = (yr[-1][0]+yr[-1][1])//2
    print(f"col {x1} y 340..400:", " ".join(f"{y}:{tuple(im[y,x1])}" for y in range(340, 400, 2)))
if xr:
    x0 = (xr[0][0]+xr[0][1])//2
    print(f"\ncol {x0} y 455..510:", " ".join(f"{y}:{tuple(im[y,x0])}" for y in range(455, 510, 2)))

# --- arrows: strong blue 0000FF between X row and banner / banner and Y row ---
blueF = (b > 170) & (r < 90) & (g < 90)
mid1 = blueF[388:394]  # between banner top? actually arrows are above/below banner
ar_up = blueF[348:392]; ar_dn = blueF[446:500]
for tag, arr, y0 in (("arrows above banner (348..392)", ar_up, 348), ("arrows below banner (446..500)", ar_dn, 446)):
    cols = arr.sum(axis=0)
    runs, s, p = [], None, None
    for x in range(len(cols)):
        if cols[x] > 3:
            if s is None: s = p = x
            elif x == p+1: p = x
            else: runs.append((s,p)); s = p = x
    if s is not None: runs.append((s,p))
    print(f"\n{tag} col runs:", [(a, b_, b_-a+1) for a,b_ in runs])
    rows = arr.sum(axis=1)
    rr = [y+y0 for y in range(len(rows)) if rows[y] > 5]
    if rr: print(f"   rows {rr[0]}..{rr[-1]}")
    if runs:
        a, b_ = runs[len(runs)//2]
        print(f"   mid arrow col {a}..{b_} shape sample row-mid:", " ".join(f"{x}:{tuple(im[(rr[0]+rr[-1])//2, x])}" for x in range(a-2, b_+3, 2)))

# --- dots: blue/green dots between 6th and 7th boxes ---
print("\n=== gap scan Y row (row ~365, x 570..640):", " ".join(f"{x}:{tuple(im[365,x])}" for x in range(560, 650, 2)))
print("=== gap scan X row (row ~480, x 570..640):", " ".join(f"{x}:{tuple(im[480,x])}" for x in range(560, 650, 2)))

# --- gutter labels: red text left of boxes ---
red = (r > 110) & (g < 110) & (b < 110)
gut = red[340:510, 60:200]
rows = gut.sum(axis=1)
print("\n=== gutter red rows (y 340..510, x 60..200):", [(y+340, int(rows[y])) for y in range(len(rows)) if rows[y] > 2])

# --- title bbox ---
tred = red[40:110, :]
ys, xs = np.where(tred)
print("title red bbox: x", xs.min(), "..", xs.max(), " y", ys.min()+40, "..", ys.max()+40)

# --- caption: yellow band + text ---
yelhl = (r > 230) & (g > 230) & (b < 140)
ys, xs = np.where(yelhl[480:520, :])
if len(ys):
    print("caption yellow bbox: x", xs.min(), "..", xs.max(), " y", ys.min()+480, "..", ys.max()+480)
# caption text color: dark pixels inside yellow band
band = im[484:505, xs.min():xs.max()]
dark = (band.max(axis=2) < 150)
ys2, xs2 = np.where(dark)
if len(ys2):
    px = band[ys2, xs2]
    print("caption text px median:", np.median(px, axis=0), "n=", len(ys2))

# --- info panel text lines: blue ink rows in panel (x 105..855, y 112..332) ---
blue = (b > 120) & (r < 120) & (g < 120)
ptxt = blue[112:333, 105:856]
rows = ptxt.sum(axis=1)
print("\n=== panel blue-ink rows:")
inline = False
for y in range(len(rows)):
    if rows[y] > 2 and not inline:
        start = y+112; inline = True
    elif rows[y] <= 2 and inline:
        print(f"   line band {start}..{y+111} (h={y+111-start})")
        inline = False

# --- color cores ---
def core(mask, tag):
    ys, xs = np.where(mask)
    if len(ys) < 10: print(tag, "n/a"); return
    px = im[ys, xs]
    print(f"{tag}: n={len(ys)} median {np.median(px,axis=0)} p25 {np.percentile(px,25,axis=0)}")

print()
core((b > 150) & (r < 60) & (g < 60), "body blue (b>150,r<60,g<60)")
core((r > 150) & (g < 60) & (b < 60), "red core (title/labels)")
green = (g > 120) & (r < 120) & (b < 120)
core(green, "green dots")
core((r > 235) & (g > 235) & (b > 110) & (b < 200), "pale yellow cells")
