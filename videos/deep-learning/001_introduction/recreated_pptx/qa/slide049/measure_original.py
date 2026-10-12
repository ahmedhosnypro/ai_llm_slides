#!/usr/bin/env python3
"""PIL measure of ground-truth frame slide_049.jpg (960x540, 1px = 1pt).
Banked as qa/slide049/measure_original_out.txt (pass 1)."""
import sys, json
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_049.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"size {W}x{H}")

def modal(region, thresh=None):
    """modal color of a region (array), optionally excluding near-threshold colors"""
    px = region.reshape(-1, 3)
    if thresh is not None:
        keep = np.abs(px - np.array(thresh)).sum(1) > 60
        px = px[keep] if keep.any() else px
    if len(px) == 0:
        return None
    q = (px // 8) * 8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    m = vals[counts.argmax()]
    return "#%02X%02X%02X" % tuple(m), int(counts.max()), len(q)

# ---- 1. chrome verification ----
print("\n== chrome ==")
print("corner TL (5,5):", a[5,5], " corner TR (5,954):", a[5,W-5])
# white strip: find rows where x=480 is white
col = a[:, 480]
for y in range(0, 70):
    r,g,b = col[y]
    if not (r>235 and g>235 and b>235):
        print(f"first non-white row at y={y}: {tuple(col[y])}")
        break
# panel gray extent: scan row 300 for gray E9E9E7-ish bounds
row = a[300]
gray = (np.abs(row[:,0]-0xE9)<14) & (np.abs(row[:,1]-0xE9)<14) & (np.abs(row[:,2]-0xE7)<14)
xs = np.where(gray)[0]
print("gray-ish row300 x-range:", (int(xs[0]), int(xs[-1])) if len(xs) else None, "count", len(xs))
# red border columns/rows: scan for red C00000-ish
red = (row[:,0]>140) & (row[:,1]<90) & (row[:,2]<90)
xs = np.where(red)[0]
print("red row300 cols:", xs[:20], "...", xs[-20:] if len(xs)>20 else "")
colred = (a[:,480,0]>140) & (a[:,480,1]<90) & (a[:,480,2]<90)
ys = np.where(colred)[0]
print("red col480 rows:", ys[:10], "...", ys[-10:] if len(ys)>10 else "")
# badge region check (893,71) r18
badge = a[71-22:71+22, 893-22:893+22]
print("badge region modal:", modal(badge))
# black bottom bar
rowb = a[530]
black = (rowb.sum(axis=1) < 90)
xs = np.where(black)[0]
print("black row530 cols:", (int(xs[0]), int(xs[-1])) if len(xs) else None, "count", len(xs))
for y in [500, 505, 510, 512, 515, 517, 519, 521]:
    row = a[y]; blk = (row.sum(axis=1) < 90); xs = np.where(blk)[0]
    print(f"  black row{y}: n={len(xs)}", (int(xs[0]), int(xs[-1])) if len(xs) else "")

# ---- 2. title ----
print("\n== title ==")
# search band y 60..140 for red ink
band = a[55:150]
redm = (band[:,:,0]>120) & (band[:,:,1]<80) & (band[:,:,2]<80)
ys, xs = np.where(redm)
if len(ys):
    print("title red ink bbox: x", int(xs.min()), "..", int(xs.max()), " y", int(ys.min())+55, "..", int(ys.max())+55)
    print("title modal:", modal(band[redm]))
# column profile of title red ink to find word gaps
y0, y1 = int(ys.min())+55, int(ys.max())+55
sub = a[y0:y1+1]
redm2 = (sub[:,:,0]>120) & (sub[:,:,1]<80) & (sub[:,:,2]<80)
colhas = redm2.any(axis=0)
runs = []
inr = False
for x in range(W):
    if colhas[x] and not inr: start=x; inr=True
    elif not colhas[x] and inr: runs.append((start, x-1)); inr=False
if inr: runs.append((start, W-1))
print("title ink col-runs (words):", runs)

# ---- 3. blue box ----
print("\n== blue box ==")
# blue border: search whole frame for strong blue
bluem = (a[:,:,2]>120) & (a[:,:,0]<100) & (a[:,:,1]<100)
ys, xs = np.where(bluem)
print("strong-blue ink bbox: x", int(xs.min()), "..", int(xs.max()), " y", int(ys.min()), "..", int(ys.max()))
# box border rows: for each row count strong-blue pixels
rowcounts = bluem.sum(axis=1)
big = np.where(rowcounts > 300)[0]
print("rows with >300 blue px (horizontal borders):", big)
colcounts = bluem.sum(axis=0)
bigc = np.where(colcounts > 150)[0]
print("cols with >150 blue px (vertical borders):", bigc)
# box fill modal (center area away from text)
print("box fill modal @ (480, 300±20, x 700..760):", modal(a[300-20:300+20, 700:760]))

# ---- 4. text lines inside box ----
print("\n== text lines inside box ==")
# dark ink (navy/black/red) inside box region; first find box interior from borders
bx0, bx1, by0, by1 = int(bigc[0]), int(bigc[-1]), int(big[0]), int(big[-1])
print(f"box stroke-center approx: x {bx0}..{bx1}, y {by0}..{by1}")
inner = a[by0+4:by1-3, bx0+4:bx1-3]
dark = inner.sum(axis=2) < 330   # dark ink incl. navy (0,0,139 sum=139), red 192, black
rowhas = dark.any(axis=1)
# find line bands
bands = []
inb = False
for i, v in enumerate(rowhas):
    if v and not inb: s = i; inb = True
    elif not v and inb:
        if i - s >= 2: bands.append((s, i-1))
        inb = False
if inb: bands.append((s, len(rowhas)-1))
print("dark-ink bands (relative to inner):", bands)
for k, (s, e) in enumerate(bands):
    seg = inner[s:e+1]
    dm = seg.sum(axis=2) < 330
    ys2, xs2 = np.where(dm)
    x0i, x1i = int(xs2.min())+bx0+4, int(xs2.max())+bx0+4
    y0i, y1i = s+by0+4, e+by0+4
    # modal ink color of the darkest pixels
    px = seg[dm]
    q = (px//8)*8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    print(f"band{k}: y {y0i}..{y1i} (h {y1i-y0i+1})  x {x0i}..{x1i} (w {x1i-x0i+1})  top colors: {' '.join('#%02X%02X%02X'%tuple(t) for t in top)} n={counts.max()}/{dm.sum()}")

# ---- 5. per-line color segments (red accents) ----
print("\n== per-line color segments ==")
for k, (s, e) in enumerate(bands):
    seg = inner[s:e+1]
    dm = seg.sum(axis=2) < 400
    ys2, xs2 = np.where(dm)
    x0i = int(xs2.min()); x1i = int(xs2.max())
    # classify columns: red-ish vs blue-ish vs black
    segabs = a[s+by0+4:e+by0+5, x0i+bx0+4:x1i+bx0+5]
    colcls = []
    for x in range(segabs.shape[1]):
        col = segabs[:, x]
        d = col.sum(axis=1) < 400
        if not d.any(): colcls.append(None); continue
        ink = col[d]
        r, g, b = ink.mean(axis=0)
        if r > 100 and g < 90 and b < 90: colcls.append("R")
        elif b > r + 40: colcls.append("B")
        else: colcls.append("K")
    # collapse into runs
    runs = []
    cur = None; start = 0
    for i, c in enumerate(colcls):
        cc = c if c else cur
        if cc != cur:
            if cur is not None: runs.append((cur, start, i-1))
            cur = cc; start = i
    if cur is not None: runs.append((cur, start, len(colcls)-1))
    runs = [(c, x0i+st, x0i+en) for c, st, en in runs if c and en-st >= 1]
    print(f"band{k} y{s+by0+4}..{e+by0+4}:", [(c, st, en) for c, st, en in runs])

# ---- 6. underline detection: horizontal ink rows near/below baseline ----
print("\n== underline check ==")
for k, (s, e) in enumerate(bands):
    # look at rows e+1..e+8 below the band within box
    below = inner[e+1:min(e+9, inner.shape[0])]
    if below.size == 0: continue
    dm = below.sum(axis=2) < 400
    if dm.any():
        ys2, xs2 = np.where(dm)
        print(f"band{k}: ink below band at rel-rows +1..+8, x {int(xs2.min())+bx0+4}..{int(xs2.max())+bx0+4}, count {dm.sum()}")
        for r in range(below.shape[0]):
            rowink = below[r].sum(axis=1) < 400
            xsr = np.where(rowink)[0]
            if len(xsr) > 5:
                print(f"   +{r+1}: x {int(xsr.min())+bx0+4}..{int(xsr.max())+bx0+4} n={len(xsr)}")
    else:
        print(f"band{k}: no ink below")

# ---- 7. bullet dots ----
print("\n== bullet dots (left of text) ==")
# scan x range near box left border for round dots
for k, (s, e) in enumerate(bands):
    seg = inner[s:e+1]
    dm = seg.sum(axis=2) < 400
    ys2, xs2 = np.where(dm)
    print(f"band{k}: ink starts at x={int(xs2.min())+bx0+4}")

# ---- 8. mouse cursor artifact ----
print("\n== cursor region (93%, 79%) = (893, 427) ==")
reg = a[410:450, 870:920]
dm = reg.sum(axis=2) < 300
ys2, xs2 = np.where(dm)
print("dark ink in cursor region:", "none" if not dm.any() else f"x {int(xs2.min())+870}..{int(xs2.max())+870} y {int(ys2.min())+410}..{int(ys2.max())+410} n={dm.sum()}")
