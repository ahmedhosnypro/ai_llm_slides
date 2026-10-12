#!/usr/bin/env python3
"""Pass 2: fine measurements for slide_032.jpg — label bbox, left box border
(loose ink scan), right-box interior red bands, modal colors, pen icon, blue
text lines with fine gaps, baselines, background samples."""
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

# ---------- 1. clean '2-D Image' label bbox ----------
red = (r > 120) & (g < 110) & (b < 110)
lm = np.zeros_like(red)
lm[215:268, 620:960] = red[215:268, 620:960]
bb = bbox(lm, "label '2-D Image' red ink (y215..268)")
if bb:
    rows = np.where(lm.sum(axis=1) > 0)[0]
    print("label ink rows:", rows.min(), "..", rows.max())
    cols = np.unique(np.where(lm)[1])
    gaps = []
    prev = cols[0]
    for c in cols[1:]:
        if c - prev > 8:
            gaps.append((int(prev), int(c)))
        prev = c
    print("label word gaps (>8px):", gaps)

# ---------- 2. left box border: loose non-white scan ----------
nonwhite = (r < 225) | (g < 225) | (b < 225)
nm = np.zeros_like(nonwhite)
nm[100:480, 30:700] = nonwhite[100:480, 30:700]
print("\n--- left region non-white rows with long runs (border candidates) ---")
for y in range(100, 480):
    xs = np.where(nm[y])[0]
    if len(xs) > 150:
        runs = []
        s = p = xs[0]
        for c in xs[1:]:
            if c <= p + 3:
                p = c
            else:
                runs.append((s, p, p - s + 1))
                s = p = c
        runs.append((s, p, p - s + 1))
        longest = max(runs, key=lambda t: t[2])
        if longest[2] >= 150:
            print(f"y={y}: nonwhite run x {longest[0]}..{longest[1]} (len {longest[2]})")
print("--- left region non-white cols with long runs ---")
for x in range(30, 700):
    ys = np.where(nm[100:480, x])[0] + 100
    if len(ys) > 100:
        runs = []
        s = p = ys[0]
        for c in ys[1:]:
            if c <= p + 3:
                p = c
            else:
                runs.append((s, p, p - s + 1))
                s = p = c
        runs.append((s, p, p - s + 1))
        longest = max(runs, key=lambda t: t[2])
        if longest[2] >= 100:
            print(f"x={x}: nonwhite run y {longest[0]}..{longest[1]} (len {longest[2]})")

# ---------- 3. right box interior red bands (exclude border) ----------
im2 = np.zeros_like(red)
im2[275:499, 617:887] = red[275:499, 617:887]
bb2 = bbox(im2, "right box INTERIOR red ink")
if bb2:
    rows = np.where(im2.sum(axis=1) > 0)[0]
    bands = []
    s = p = rows[0]
    for c in rows[1:]:
        if c - p <= 6:
            p = c
        else:
            bands.append((s, p))
            s = p = c
    bands.append((s, p))
    print("interior red bands:")
    for (y0, y1) in bands:
        xs3 = np.where(im2[y0:y1+1].sum(axis=0) > 0)[0]
        print(f"  band y {y0}..{y1} (h {y1-y0+1}): x {xs3.min()}..{xs3.max()}")

# ---------- 4b. interior red per-column profile (arrow vs Filters word) ----------
print("\ninterior red per-column top/bottom (every 8 cols):")
for x in range(645, 843, 8):
    ys6 = np.where(im2[:, x])[0]
    if len(ys6):
        print(f"  x={x}: y {ys6.min()}..{ys6.max()} n={len(ys6)}")
print("interior red per-row extents (every 8 rows):")
for y in range(312, 496, 8):
    xs6 = np.where(im2[y])[0]
    if len(xs6):
        print(f"  y={y}: x {xs6.min()}..{xs6.max()} n={len(xs6)}")

# ---------- 4. blue text lines with fine gaps + baselines ----------
blue = (b > 120) & (b > r + 50) & (b > g + 40)
bm = np.zeros_like(blue)
bm[110:470, 45:675] = blue[110:470, 45:675]
rows = np.where(bm.sum(axis=1) > 2)[0]
print("\nleft box blue text fine bands (gap>2):")
if len(rows):
    bands = []
    s = p = rows[0]
    for c in rows[1:]:
        if c - p <= 2:
            p = c
        else:
            bands.append((s, p))
            s = p = c
    bands.append((s, p))
    for (y0, y1) in bands:
        xs4 = np.where(bm[y0:y1+1].sum(axis=0) > 0)[0]
        print(f"  band y {y0}..{y1} (h {y1-y0+1}): x {xs4.min()}..{xs4.max()}")
        # row profile of the band (find baseline: last row with many px)
        rowsum = bm[y0:y1+1].sum(axis=1)
        heavy = np.where(rowsum > max(2, rowsum.max() * 0.25))[0] + y0
        print(f"    heavy rows {heavy.min()}..{heavy.max()}")

# ---------- 5. modal colors ----------
print()
modal(IM[(red[:, :] & (np.arange(H)[:, None] >= 75) & (np.arange(H)[:, None] <= 115))], "title red ink")
tm = np.zeros_like(red); tm[75:115, 170:780] = red[75:115, 170:170+610]
modal(IM[tm], "title red ink (masked)")
modal(IM[bm], "left box blue text ink")
modal(IM[lm], "label '2-D Image' ink")
# left box border color sample
modal(IM[139:141, 100:500], "left box top border (y139..140)")
modal(IM[420:423, 100:500], "left box bottom border (y420..422)")
modal(IM[150:400, 78:79], "left box left border (x78)")
modal(IM[150:400, 589:591], "left box right border (x589..590)")
modal(IM[270:500, 612:614], "right box left border (x612..613)")
# plane interior
modal(IM[415:470, 660:740], "plane interior sample (x660..740 y415..470)")
modal(IM[430:465, 650:700], "plane lower-left sample")
modal(IM[330:360, 750:775], "plane upper-right sample")
# filter rect region
modal(IM[340:375, 728:762], "filter rect region")
# pen icon region
modal(IM[305:370, 616:680], "pen icon region")
# grayscale word ink
gm = np.zeros_like(red)
gm[276:309, 684:864] = True
# modal of dark pixels there
dk = IM[276:309, 684:864]
dkmask = (dk[:,:,0] < 120) & (dk[:,:,1] < 120) & (dk[:,:,2] < 120)
modal(dk[dkmask], "Grayscale word ink (dark px)")

# ---------- 6. pen icon bbox (dark ink, left edge inside right box) ----------
black = (r < 100) & (g < 100) & (b < 100)
km = np.zeros_like(black)
km[309:400, 616:684] = black[309:400, 616:684]
bbox(km, "pen icon dark ink (x616..684 y309..400)")

# ---------- 7. background samples ----------
for (x, y, lbl) in [(550, 250, "between boxes (x550 y250)"),
                    (930, 350, "right margin (x930 y350)"),
                    (480, 490, "bottom center (x480 y490)"),
                    (480, 130, "below title (x480 y130)"),
                    (50, 200, "left edge inside (x50 y200)"),
                    (900, 500, "bottom right (x900 y500)"),
                    (200, 515, "just above black strip (x200 y515)")]:
    reg = IM[y-3:y+4, x-3:x+4].reshape(-1, 3)
    modal(reg, lbl, k=2)

# ---------- 8. title fine rows: baseline + cap ----------
tm2 = np.zeros_like(red); tm2[60:150, 60:900] = red[60:150, 60:900]
rowsum = tm2.sum(axis=1)
print("\ntitle row profile (y: count) nonzero bands:")
ys = np.where(rowsum > 0)[0]
bands = []
s = p = ys[0]
for c in ys[1:]:
    if c - p <= 2:
        p = c
    else:
        bands.append((s, p))
        s = p = c
bands.append((s, p))
print("title bands:", bands)
# column profile for word bboxes
colsum = tm2.sum(axis=0)
xs = np.where(colsum > 0)[0]
words = []
s = p = xs[0]
for c in xs[1:]:
    if c - p <= 12:
        p = c
    else:
        words.append((int(s), int(p)))
        s = p = c
words.append((int(s), int(p)))
print("title word bboxes:", words)
