#!/usr/bin/env python3
"""PIL measure pass 2 of slide_049.jpg — fixed inner-box slice, title isolation,
panel colors, per-line segments, underlines, bullets."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_049.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)

def modal(px):
    if len(px) == 0: return None
    q = (px // 8) * 8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)
    return [("#%02X%02X%02X" % tuple(vals[i]), int(counts[i])) for i in order[:4]]

# ---- panel colors (outside blue box) ----
print("== panel ==")
for (y, x0, x1, tag) in [(300, 46, 96, "left-of-box y300"), (300, 866, 914, "right-of-box y300"),
                          (500, 46, 96, "left-of-box y500"), (60, 700, 910, "top-right y60"),
                          (140, 46, 96, "left y140"), (240, 46, 96, "left y240")]:
    print(f"  {tag} x{x0}..{x1}:", modal(a[y, x0:x1].reshape(-1,3)))
# red border columns: row 500 (below box, above black bar)
row = a[500]
redm = (row[:,0]>120) & (row[:,1]<90) & (row[:,2]<90)
xs = np.where(redm)[0]
print("  red cols @row500:", xs.tolist())
print("  modal @row500 x52..60:", modal(a[500,52:60].reshape(-1,3)), " x916..922:", modal(a[500,916:922].reshape(-1,3)))
# top border rows: col 700 (right of title text region? title ends x707; use col 800)
col = a[:,800]
redm = (col[:,0]>120) & (col[:,1]<90) & (col[:,2]<90)
ys = np.where(redm)[0]
print("  red rows @col800:", ys.tolist())
# gray panel horizontal extent at row 130 (between title and box)
row = a[130]
gray = (np.abs(row[:,0]-0xE9)<20) & (np.abs(row[:,1]-0xE9)<20) & (np.abs(row[:,2]-0xE7)<20)
xs = np.where(gray)[0]
print("  gray-ish extent @row130:", (int(xs[0]), int(xs[-1])) if len(xs) else None, "count", len(xs))

# ---- title (restricted to x 250..710) ----
print("\n== title ==")
sub = a[40:160, 250:712]
redm = (sub[:,:,0]>120) & (sub[:,:,1]<80) & (sub[:,:,2]<80)
ys, xs = np.where(redm)
y0, y1 = int(ys.min())+40, int(ys.max())+40
x0, x1 = int(xs.min())+250, int(xs.max())+250
print(f"title ink bbox: x {x0}..{x1} (w {x1-x0+1})  y {y0}..{y1} (h {y1-y0+1})")
print("  ink modal:", modal(sub[redm].reshape(-1,3)))
# column profile: word runs
colhas = redm.any(axis=0)
runs = []; inr=False
for x in range(sub.shape[1]):
    if colhas[x] and not inr: s=x; inr=True
    elif not colhas[x] and inr: runs.append((s+250, x-1+250)); inr=False
if inr: runs.append((s+250, sub.shape[1]-1+250))
print("  word col-runs:", runs)
# row profile: cap band (rows where many red px) vs descender
rowc = redm.sum(axis=1)
for y in range(sub.shape[0]):
    if rowc[y] > 0: print(f"   y={y+40}: {rowc[y]}", end=";")
print()

# ---- blue box borders ----
print("\n== blue box ==")
bluem = (a[:,:,2]>110) & (a[:,:,0]<110) & (a[:,:,1]<110)
sub = bluem[140:510, 80:880]
rowc = sub.sum(axis=1)
print("  blue rows (count>100):", [(y+140, int(rowc[y])) for y in range(len(rowc)) if rowc[y]>100])
colc = sub.sum(axis=0)
print("  blue cols (count>100):", [(x+80, int(colc[x])) for x in range(len(colc)) if colc[x]>100])
print("  border modal @row153 x300..500:", modal(a[153,300:500].reshape(-1,3)), "@row154:", modal(a[154,300:500].reshape(-1,3)))
print("  border modal @col100 y300..400:", modal(a[300:400,100].reshape(-1,3)), "@col101:", modal(a[300:400,101].reshape(-1,3)))
print("  border modal @col860 y300..400:", modal(a[300:400,860].reshape(-1,3)))

# ---- text lines: dark ink inside box interior x 104..857, y 157..488 ----
print("\n== text lines ==")
ix0, ix1, iy0, iy1 = 104, 858, 157, 489
inner = a[iy0:iy1, ix0:ix1]
dark = inner.sum(axis=2) < 420
rowhas = dark.any(axis=1)
bands = []; inb=False
for i, v in enumerate(rowhas):
    if v and not inb: s=i; inb=True
    elif not v and inb:
        if i-s >= 1: bands.append((s, i-1)); 
        inb=False
if inb: bands.append((s, len(rowhas)-1))
print("bands (abs y):", [(s+iy0, e+iy0) for s,e in bands])
for k,(s,e) in enumerate(bands):
    seg = inner[s:e+1]
    dm = seg.sum(axis=2) < 420
    ys2, xs2 = np.where(dm)
    print(f"band{k}: y {s+iy0}..{e+iy0} (h {e-s+1}) x {int(xs2.min())+ix0}..{int(xs2.max())+ix0} (w {int(xs2.max())-int(xs2.min())+1}) n={int(dm.sum())}")
    print("   ink modal:", modal(seg[dm].reshape(-1,3)))

# ---- per-line color segments ----
print("\n== per-line color segments (R/B/K runs >=2px) ==")
for k,(s,e) in enumerate(bands):
    segabs = a[s+iy0:e+iy0+1, ix0:ix1]
    d = segabs.sum(axis=2) < 420
    colcls = []
    for x in range(segabs.shape[1]):
        col = segabs[:, x]; dd = d[:, x]
        if not dd.any(): colcls.append(None); continue
        ink = col[dd]
        r, g, b = ink.mean(axis=0)
        if r > 100 and r > b + 50 and g < 100: colcls.append("R")
        elif b > r + 40: colcls.append("B")
        else: colcls.append("K")
    runs = []; cur=None; st=0
    for i,c in enumerate(colcls):
        if c != cur:
            if cur is not None and i-st >= 2: runs.append((cur, st+ix0, i-1+ix0))
            elif cur is not None: runs.append((cur+"?", st+ix0, i-1+ix0))
            cur=c; st=i
    if cur is not None: runs.append((cur, st+ix0, len(colcls)-1+ix0))
    print(f" band{k} y{s+iy0}..{e+iy0}:", runs)

# ---- underline check (rows below each band, x where band had ink) ----
print("\n== underline check ==")
for k,(s,e) in enumerate(bands):
    found = []
    for r in range(e+1, min(e+10, iy1-iy0)):
        rowink = inner[r].sum(axis=1) < 420
        xsr = np.where(rowink)[0]
        if len(xsr) > 8:
            # contiguous?
            print(f"  band{k}: +{r-e} row y={r+iy0}: x {int(xsr.min())+ix0}..{int(xsr.max())+ix0} n={len(xsr)}")
            found.append(r)
    if not found: print(f"  band{k}: no underline rows")

# ---- bullet dots: round dots left of text ----
print("\n== bullet dots ==")
for k,(s,e) in enumerate(bands):
    seg = inner[s:e+1]
    dm = seg.sum(axis=2) < 420
    ys2, xs2 = np.where(dm)
    xmin = int(xs2.min())
    # ink columns histogram near left
    colc = dm.sum(axis=0)
    lead = [(x+ix0, int(colc[x])) for x in range(0, 120) if colc[x] > 0]
    print(f"  band{k} leading cols (first 15): {lead[:15]}")

# ---- bottom black bar / cursor ----
print("\n== artifacts ==")
row = a[525]
blk = (row.sum(axis=1) < 90)
xs = np.where(blk)[0]
print("black bar @row525:", (int(xs[0]), int(xs[-1])) if len(xs) else None)
# first/last black rows
colm = (a[:,:,0]<60)&(a[:,:,1]<60)&(a[:,:,2]<60)
rowsum = colm[:, 100:900].sum(axis=1)
print("black rows (n>500):", np.where(rowsum>500)[0].tolist())
reg = a[415:445, 875:915]
dm = reg.sum(axis=2) < 380
if dm.any():
    ys2, xs2 = np.where(dm)
    print("cursor ink: x", int(xs2.min())+875, "..", int(xs2.max())+875, " y", int(ys2.min())+415, "..", int(ys2.max())+415, " n=", int(dm.sum()))
