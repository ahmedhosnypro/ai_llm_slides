#!/usr/bin/env python3
"""Pass 3: isolate the pure-red stroke (arrow + 'Filters' word) from the plane
fill (#AF6712 has g~103; a C00000-class stroke has g<70), deep-scan the pen
icon, check the plane edges for an outline stroke, and measure the blue filter
rectangle geometry."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_032.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  "
          f"(w {xs.max()-xs.min()+1}, h {ys.max()-ys.min()+1}, n={len(ys)})")
    return (xs.min(), xs.max(), ys.min(), ys.max())

def modal(pixels, label, k=5):
    if not len(pixels):
        print(f"{label}: no pixels")
        return
    vals, counts = np.unique(pixels.reshape(-1, 3), axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:k]]
    cnts = np.sort(counts)[::-1][:k]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

# ---------- pure-red stroke (g<70): arrow + Filters word ----------
pure_red = (r > 130) & (g < 70) & (b < 80)
pm = np.zeros_like(pure_red)
pm[275:500, 616:886] = pure_red[275:500, 616:886]
bb = bbox(pm, "pure-red stroke in right box interior")
if bb:
    print("per-column top/bottom (every 5 cols):")
    for x in range(bb[0], bb[1] + 1, 5):
        ys = np.where(pm[:, x])[0]
        if len(ys):
            print(f"  x={x}: y {ys.min()}..{ys.max()} n={len(ys)}")
    print("per-row extents (every 5 rows):")
    for y in range(bb[2], bb[3] + 1, 5):
        xs = np.where(pm[y])[0]
        if len(xs):
            print(f"  y={y}: x {xs.min()}..{xs.max()} n={len(xs)}")
modal(IM[pm], "pure-red stroke color")

# ---------- medium red (70<=g<95): transition pixels ----------
med = (r > 130) & (g >= 70) & (g < 95) & (b < 80)
mm = np.zeros_like(med)
mm[275:500, 616:886] = med[275:500, 616:886]
bb2 = bbox(mm, "medium-red (g70..95) in interior")

# ---------- pen icon deep scan: any pixel <210 in x 614..644, y 300..510 ----------
dark = (r < 210) & (g < 210) & (b < 210)
dm = np.zeros_like(dark)
dm[300:512, 614:644] = dark[300:512, 614:644]
bbox(dm, "pen icon region ink (<210, x614..644 y300..512)")
if dm.sum():
    ys, xs = np.where(dm)
    print("ink density rows:", np.unique(ys)[:50])

# also scan a wider left strip inside the box
dm2 = np.zeros_like(dark)
dm2[275:500, 616:645] = dark[275:500, 616:645]
bbox(dm2, "left strip of box ink (<210, x616..644)")

# ---------- plane edge outline check ----------
# plane top edge: from (645,408) to (774,312): y = 408 - 0.75*(x-645)
print("\nplane edge color samples (along top edge, perpendicular):")
for x in range(660, 770, 20):
    ye = 408 - 0.75 * (x - 645)
    col = IM[int(ye) - 4:int(ye) + 5, x]
    print(f"  x={x} y~{ye:.0f}: {['#%02X%02X%02X' % tuple(p) for p in col]}")
print("plane left edge (x=645) samples:")
for y in range(420, 500, 15):
    row = IM[y, 641:652]
    print(f"  y={y}: {['#%02X%02X%02X' % tuple(p) for p in row]}")

# ---------- blue filter rectangle geometry (loose cyan mask) ----------
cyan = (b > 120) & (g > 90) & (r < 120)
cm = np.zeros_like(cyan)
cm[330:390, 720:775] = cyan[330:390, 720:775]
bbc = bbox(cm, "blue filter rect (cyan, x720..775 y330..390)")
if bbc:
    print("filter per-row extents:")
    for y in range(bbc[2], bbc[3] + 1):
        xs = np.where(cm[y])[0]
        if len(xs):
            print(f"  y={y}: x {xs.min()}..{xs.max()} n={len(xs)}")
modal(IM[cm], "filter stroke color")

# ---------- Grayscale word fine bands ----------
black = (r < 130) & (g < 130) & (b < 130)
km = np.zeros_like(black)
km[270:315, 660:880] = black[270:315, 660:880]
bbk = bbox(km, "Grayscale word ink")
if bbk:
    rows = np.where(km.sum(axis=1) > 0)[0]
    print("Grayscale ink rows:", rows.min(), "..", rows.max())

# ---------- label solve prep: word bboxes ----------
red = (r > 120) & (g < 110) & (b < 110)
lm = np.zeros_like(red)
lm[220:262, 620:960] = red[220:262, 620:960]
cols = np.unique(np.where(lm)[1])
words = []
s = p = cols[0]
for c in cols[1:]:
    if c - p <= 8:
        p = c
    else:
        words.append((int(s), int(p)))
        s = p = c
words.append((int(s), int(p)))
print("\nlabel word bboxes:", words)

# ---------- title per-word row bands (baseline detection) ----------
tm = np.zeros_like(red)
tm[60:150, 60:900] = red[60:150, 60:900]
tw = [(176, 280), (293, 323), (336, 392), (405, 505), (518, 563), (576, 773)]
print("title per-word row bands:")
for (x0, x1) in tw:
    sub = tm[:, x0:x1 + 1]
    ys = np.where(sub.sum(axis=1) > 0)[0]
    print(f"  x {x0}..{x1}: y {ys.min()}..{ys.max()}")
