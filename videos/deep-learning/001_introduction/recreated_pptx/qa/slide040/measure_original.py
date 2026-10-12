#!/usr/bin/env python3
"""PIL ink forensics on the ground-truth frame slide_040.jpg (960x540, 1px = 1pt).

Measures: title ink, left photo (grumpy cat) border box, right photo (dog) border
box, yellow text box + blue border + text line bands, block arrow, filter-grid
image border box, bottom black strip. All in frame px (1px = 1pt = 1/72 in).
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_040.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
print(f"frame {W}x{H}")

r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  "
          f"(w {xs.max()-xs.min()+1}, h {ys.max()-ys.min()+1}, n={len(ys)})")
    return (xs.min(), xs.max(), ys.min(), ys.max())

# ---------- title (red ink, top band, inside panel, away from border) ----------
red = (r > 120) & (g < 110) & (b < 110)
tmask = np.zeros_like(red)
tmask[50:135, 60:900] = red[50:135, 60:900]
bbox(tmask, "title red ink")
# per-column red counts -> word gaps
ys, xs = np.where(tmask)
if len(xs):
    cols = np.unique(xs)
    gaps = []
    prev = cols[0]
    for c in cols[1:]:
        if c - prev > 12:
            gaps.append((prev, c))
        prev = c
    print("title word gaps (>12px):", gaps[:20])

# ---------- photos: red border rectangles in upper band ----------
# long horizontal red runs in y 130..380
print("\n--- horizontal red runs (>=60 px) in band y 120..400 ---")
for y in range(120, 400):
    row = red[y]
    xs2 = np.where(row)[0]
    if len(xs2) > 60:
        # longest contiguous run
        runs = []
        s = p = xs2[0]
        for c in xs2[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p, p - s + 1))
                s = p = c
        runs.append((s, p, p - s + 1))
        longest = max(runs, key=lambda t: t[2])
        if longest[2] >= 60:
            print(f"y={y}: run x {longest[0]}..{longest[1]} (len {longest[2]})")

print("\n--- vertical red runs (>=40 px) in band x 60..910 ---")
for x in range(60, 910):
    col = red[:, x]
    ys2 = np.where(col[120:520])[0] + 120
    if len(ys2) > 40:
        runs = []
        s = p = ys2[0]
        for c in ys2[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p, p - s + 1))
                s = p = c
        runs.append((s, p, p - s + 1))
        longest = max(runs, key=lambda t: t[2])
        if longest[2] >= 40:
            print(f"x={x}: run y {longest[0]}..{longest[1]} (len {longest[2]})")

# ---------- yellow text box (fill ~FFFFE1) ----------
yelbox = (r > 235) & (g > 235) & (b > 200) & (b < 240) & (np.abs(r - g) < 12)
ymask = np.zeros_like(yelbox)
ymask[330:520, 40:700] = yelbox[330:520, 40:700]
bb = bbox(ymask, "yellow text box fill")

# ---------- blue border (0000CC-ish) ----------
blue = (b > 130) & (r < 90) & (g < 90)
bmask = np.zeros_like(blue)
bmask[330:520, 40:700] = blue[330:520, 40:700]
bbox(bmask, "blue border/text (bottom-left region)")

# ---------- dark-blue text lines inside the yellow box ----------
navy = (b > 90) & (r < 100) & (g < 100) & (b > r + 40) & (b > g + 40)
nmask = np.zeros_like(navy)
if bb:
    nmask[bb[2]+4:bb[3]-3, bb[0]+6:bb[1]-5] = navy[bb[2]+4:bb[3]-3, bb[0]+6:bb[1]-5]
    rows = np.where(nmask.sum(axis=1) > 2)[0]
    if len(rows):
        bands = []
        s = p = rows[0]
        for c in rows[1:]:
            if c - p <= 3:
                p = c
            else:
                bands.append((s, p))
                s = p = c
        bands.append((s, p))
        print("navy text line bands (y ranges):", bands)
        for (y0, y1) in bands:
            xs3 = np.where(nmask[y0:y1+1].sum(axis=0) > 0)[0]
            print(f"  band y {y0}..{y1}: x {xs3.min()}..{xs3.max()}")

# ---------- block arrow (white fill + red outline, between box and grid) ----------
print("\n--- white pixels in arrow region x 660..760, y 400..470 ---")
white = (r > 225) & (g > 225) & (b > 225)
amask = np.zeros_like(white)
amask[400:470, 660:760] = white[400:470, 660:760]
bbox(amask, "arrow white fill")
amask2 = np.zeros_like(red)
amask2[400:470, 660:760] = red[400:470, 660:760]
bbox(amask2, "arrow red outline (region scan)")

# ---------- filter grid image (bottom right) ----------
print("\n--- red border box bottom-right: horizontal runs y 320..520, x>=700 ---")
for y in range(320, 525):
    row = red[y, 700:]
    xs4 = np.where(row)[0] + 700
    if len(xs4) > 80:
        runs = []
        s = p = xs4[0]
        for c in xs4[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p, p - s + 1))
                s = p = c
        runs.append((s, p, p - s + 1))
        longest = max(runs, key=lambda t: t[2])
        if longest[2] >= 80:
            print(f"y={y}: run x {longest[0]}..{longest[1]} (len {longest[2]})")

# non-background content bbox in bottom-right quadrant (excluding yellow box)
nonbg = (np.abs(r - 233) > 25) | (np.abs(g - 233) > 25) | (np.abs(b - 231) > 25)
gmask = np.zeros_like(nonbg)
gmask[330:520, 700:920] = nonbg[330:520, 700:920]
bbox(gmask, "bottom-right content (non-panel-gray)")

# ---------- black strip ----------
black = (r < 60) & (g < 60) & (b < 60)
b2 = np.zeros_like(black)
b2[480:540, :] = black[480:540, :]
bb2 = bbox(b2, "black strip (y 480..540)")
if bb2:
    rows_b = np.where(black[:, 100:800].sum(axis=1) > 400)[0]
    print("full-width black rows:", rows_b.min() if len(rows_b) else None,
          "..", rows_b.max() if len(rows_b) else None)

# ---------- sample colors ----------
def modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    cnts = np.sort(counts)[::-1][:3]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

modal(500, 560, 470, 490, "panel gray sample (right of text box)")
modal(200, 400, 360, 380, "yellow box fill sample")
modal(60, 95, 90, 110, "title red sample")
