#!/usr/bin/env python3
"""Ink forensics for 001_introduction slide_006 (960x540, 1px = 1pt = 1/72in).
Measures: chrome panel, red content box, title ink, header ink, bullet bands,
bullet dots, colors (modal), black footer bar. Banked under qa/slide006/."""
from PIL import Image
import numpy as np, json, collections

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

R, G, B = a[..., 0], a[..., 1], a[..., 2]

# ---- modal colors in candidate regions ----
def modal(region_mask, name):
    ys, xs = np.nonzero(region_mask)
    if len(ys) == 0:
        print(name, "EMPTY"); return None
    px_ = a[ys, xs]
    # quantize to /8 buckets to defeat JPEG noise
    q = (px_ // 8) * 8
    cnt = collections.Counter(map(tuple, q))
    top = cnt.most_common(6)
    # core = fully saturated pixels only (min channel distance from 0 or 255)
    print(f"{name}: n={len(ys)} modal(top6, /8-quantized): {top[:6]}")
    # exact mode among the most-saturated pixels
    return top

# ---- 1. chrome panel red border (top horizontal runs) ----
red = (R > 140) & (G < 90) & (B < 90)
print("\n-- red pixel rows (count>200) --")
rows = red.sum(axis=1)
for y in range(H):
    if rows[y] > 200:
        xs = np.nonzero(red[y])[0]
        print(f"row {y}: n={rows[y]} x {xs.min()}..{xs.max()}")
print("-- red pixel cols (count>100) --")
cols = red.sum(axis=0)
for x in range(W):
    if cols[x] > 100:
        ys2 = np.nonzero(red[:, x])[0]
        print(f"col {x}: n={cols[x]} y {ys2.min()}..{ys2.max()}")

# ---- 2. white content box (near-white, inside panel) ----
white = (R > 235) & (G > 235) & (B > 235)
inner = np.zeros_like(white); inner[50:515, 50:910] = True
wbox = white & inner
wr = wbox.sum(axis=1); wc = wbox.sum(axis=0)
wy = [y for y in range(H) if wr[y] > 400]
wx = [x for x in range(W) if wc[x] > 200]
print(f"\nwhite-box rows y {min(wy)}..{max(wy)}  cols x {min(wx)}..{max(wx)}")

# ---- 3. black footer bar ----
blk = (R < 60) & (G < 60) & (B < 60)
br = blk.sum(axis=1)
bar_rows = [y for y in range(H) if br[y] > 700]
if bar_rows:
    y0, y1 = min(bar_rows), max(bar_rows)
    xs = np.nonzero(blk[(y0+y1)//2])[0]
    print(f"\nblack bar rows y {y0}..{y1}, mid-row x {xs.min()}..{xs.max()}")

# ---- 4. gray canvas / panel check ----
print("\n-- gray samples (canvas & panel) --")
for (x, y, name) in [(10, 10, "canvas corner"), (30, 270, "left of panel"), (480, 55, "panel top inside"),
                     (60, 270, "panel left margin"), (480, 300, "inside white box"), (900, 300, "panel right margin")]:
    patch = a[max(0,y-2):y+3, max(0,x-2):x+3].reshape(-1, 3)
    print(f"{name} @({x},{y}): mean {patch.mean(axis=0).round(1)}")

# ---- 5. title ink (red text between panel top and box top) ----
title_zone = np.zeros_like(red); title_zone[46:129, 45:915] = True
tink = red & title_zone
tys, txs = np.nonzero(tink)
if len(tys):
    print(f"\ntitle red ink: x {txs.min()}..{txs.max()}  y {tys.min()}..{tys.max()}  n={len(tys)}")
    modal(tink, "title red modal")
    # row profile for cap-height/baseline
    tr = tink.sum(axis=1)
    rows_t = [(y, int(tr[y])) for y in range(H) if tr[y] > 3]
    print("title red row profile:", rows_t[:3], "...", rows_t[-3:] if len(rows_t) > 3 else "")
    # column extent per word-cluster
    tc = tink.sum(axis=0)
    nz = np.nonzero(tc)[0]
    print(f"title red col extent {nz.min()}..{nz.max()}, center {(nz.min()+nz.max())/2}")

# ---- 6. dark ink (header black text) ----
dark = (R < 110) & (G < 110) & (B < 110)
hdr_zone = np.zeros_like(dark); hdr_zone[130:200, 60:900] = True
hink = dark & hdr_zone
hys, hxs = np.nonzero(hink)
if len(hys):
    print(f"\nheader dark ink: x {hxs.min()}..{hxs.max()}  y {hys.min()}..{hys.max()}  n={len(hys)}")
    hr = hink.sum(axis=1)
    bands = []
    inb = False
    for y in range(H):
        if hr[y] > 2 and not inb: y0 = y; inb = True
        elif hr[y] <= 2 and inb: bands.append((y0, y - 1)); inb = False
    print("header row bands:", bands)

# ---- 7. blue bullet text ----
blue = (B > 110) & (R < 110) & (G < 110)
bl_zone = np.zeros_like(blue); bl_zone[130:520, 45:915] = True
blink_ = blue & bl_zone
bys, bxs = np.nonzero(blink_)
print(f"\nblue ink: n={len(bys)}")
if len(bys):
    modal(blink_, "blue modal")
    br_ = blink_.sum(axis=1)
    bands = []
    inb = False
    for y in range(H):
        if br_[y] > 2 and not inb: y0 = y; inb = True
        elif br_[y] <= 2 and inb:
            if y - y0 >= 4: bands.append((y0, y - 1))
            inb = False
    if inb: bands.append((y0, H - 1))
    print(f"blue row bands ({len(bands)}):")
    for (y0, y1) in bands:
        sel = blink_[y0:y1 + 1]
        xs_ = np.nonzero(sel.any(axis=0))[0]
        print(f"  y {y0}..{y1} (h {y1-y0+1})  x {xs_.min()}..{xs_.max()}")

# ---- 8. bullet dots (small dark round marks in white box) ----
# look at dark ink within bullet zone but left of text
dot_zone = np.zeros_like(dark); dot_zone[130:520, 45:200] = True
dink = dark & dot_zone
dys, dxs = np.nonzero(dink)
print(f"\ndark ink in dot zone (x<200): n={len(dys)}")
if len(dys):
    dr_ = dink.sum(axis=1)
    bands = []
    inb = False
    for y in range(H):
        if dr_[y] > 1 and not inb: y0 = y; inb = True
        elif dr_[y] <= 1 and inb: bands.append((y0, y - 1)); inb = False
    for (y0, y1) in bands:
        sel = dink[y0:y1 + 1]
        xs_ = np.nonzero(sel.any(axis=0))[0]
        print(f"  dot band y {y0}..{y1}  x {xs_.min()}..{xs_.max()}")

json.dump({"done": True}, open("/tmp/forensics_done.json", "w"))
