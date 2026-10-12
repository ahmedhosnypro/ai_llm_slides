#!/usr/bin/env python3
"""PIL ink forensics on the ground-truth frame slide_032.jpg (960x540, 1px = 1pt).

Measures: top red rule, title red ink, left white box + blue border + blue text
lines, right red label '2-D Image', right white box + red border, diagram
internals (Grayscale ink, pen icon, brown parallelogram, blue filter rect, red
Filters word + red arrow), bottom black strip, panel gray. Frame px (1px = 1pt).
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_032.jpg"
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

# ---------- global structure: red / blue / black / brown / white masks ----------
red = (r > 120) & (g < 110) & (b < 110)
blue = (b > 120) & (b > r + 50) & (b > g + 40)
black = (r < 70) & (g < 70) & (b < 70)
white = (r > 235) & (g > 235) & (b > 235)
brown = (r > 120) & (r < 220) & (g > 60) & (g < 170) & (b < 110) & (r > g + 25) & (g > b)

# ---------- top rule: red rows near the top ----------
print("\n--- top edge red rows (y 0..60) ---")
for y in range(0, 60):
    n = red[y].sum()
    if n > 100:
        xs = np.where(red[y])[0]
        print(f"y={y}: red n={n} x {xs.min()}..{xs.max()}")

# ---------- bottom black strip ----------
print("\n--- bottom edge black rows (y 480..539) ---")
for y in range(480, 540):
    n = black[y].sum()
    if n > 200:
        xs = np.where(black[y])[0]
        print(f"y={y}: black n={n} x {xs.min()}..{xs.max()}")

# ---------- title red ink (below the top rule, inside panel) ----------
tmask = np.zeros_like(red)
tmask[60:150, 60:900] = red[60:150, 60:900]
bb = bbox(tmask, "title red ink")
if bb:
    ys, xs = np.where(tmask)
    cols = np.unique(xs)
    gaps = []
    prev = cols[0]
    for c in cols[1:]:
        if c - prev > 12:
            gaps.append((prev, c))
        prev = c
    print("title word gaps (>12px):", gaps[:20])
    # row profile for cap height
    rows = np.where(tmask.sum(axis=1) > 0)[0]
    print("title ink rows:", rows.min(), "..", rows.max())

# ---------- left box: blue border + white fill + blue text ----------
print("\n--- long horizontal blue runs in y 120..450 (left box border) ---")
for y in range(120, 460):
    row = blue[y, :660]
    xs2 = np.where(row)[0]
    if len(xs2) > 100:
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
        if longest[2] >= 100:
            print(f"y={y}: blue run x {longest[0]}..{longest[1]} (len {longest[2]})")

print("\n--- long vertical blue runs in x 40..680 (left box border) ---")
for x in range(40, 680):
    col = blue[120:470, x]
    ys2 = np.where(col)[0] + 120
    if len(ys2) > 60:
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
        if longest[2] >= 60:
            print(f"x={x}: blue run y {longest[0]}..{longest[1]} (len {longest[2]})")

# blue text line bands inside the left box
if bb:
    pass
# left-box interior: find white fill bbox in left region
wmask = np.zeros_like(white)
wmask[110:470, 40:680] = white[110:470, 40:680]
bw = bbox(wmask, "left box white fill")

# blue text lines: blue ink inside the left box interior
if bw:
    nmask = np.zeros_like(blue)
    nmask[bw[2]+6:bw[3]-5, bw[0]+6:bw[1]-5] = blue[bw[2]+6:bw[3]-5, bw[0]+6:bw[1]-5]
    rows = np.where(nmask.sum(axis=1) > 2)[0]
    if len(rows):
        bands = []
        s = p = rows[0]
        for c in rows[1:]:
            if c - p <= 4:
                p = c
            else:
                bands.append((s, p))
                s = p = c
        bands.append((s, p))
        print("left box blue text line bands (y ranges):")
        for (y0, y1) in bands:
            xs3 = np.where(nmask[y0:y1+1].sum(axis=0) > 0)[0]
            print(f"  band y {y0}..{y1} (h {y1-y0+1}): x {xs3.min()}..{xs3.max()}")

# ---------- right label '2-D Image' (red text, right half, upper of lower half) ----------
rmask = np.zeros_like(red)
rmask[150:280, 620:960] = red[150:280, 620:960]
bbox(rmask, "right-label red ink band y150..280 x620..960")

# ---------- right box: red border rectangle bottom-right ----------
print("\n--- long horizontal red runs y 230..540 x>=560 (right box border) ---")
for y in range(230, 540):
    row = red[y, 560:]
    xs4 = np.where(row)[0] + 560
    if len(xs4) > 100:
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
        if longest[2] >= 100:
            print(f"y={y}: red run x {longest[0]}..{longest[1]} (len {longest[2]})")

print("\n--- long vertical red runs x 560..960 y 230..540 (right box border) ---")
for x in range(560, 960):
    col = red[230:540, x]
    ys5 = np.where(col)[0] + 230
    if len(ys5) > 60:
        runs = []
        s = p = ys5[0]
        for c in ys5[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p, p - s + 1))
                s = p = c
        runs.append((s, p, p - s + 1))
        longest = max(runs, key=lambda t: t[2])
        if longest[2] >= 60:
            print(f"x={x}: red run y {longest[0]}..{longest[1]} (len {longest[2]})")

# ---------- right box interior content ----------
# white fill of right box
w2 = np.zeros_like(white)
w2[230:540, 560:960] = white[230:540, 560:960]
bbox(w2, "right box white fill")

# black ink inside right box (Grayscale word + pen icon)
kb = None
if bw:
    pass
kmask = np.zeros_like(black)
kmask[230:540, 560:960] = black[230:540, 560:960]
kb = bbox(kmask, "right box black ink (Grayscale + pen icon)")
if kb:
    rows = np.where(kmask.sum(axis=1) > 0)[0]
    bands = []
    s = p = rows[0]
    for c in rows[1:]:
        if c - p <= 5:
            p = c
        else:
            bands.append((s, p))
            s = p = c
    bands.append((s, p))
    print("black ink bands in right box:")
    for (y0, y1) in bands:
        xs5 = np.where(kmask[y0:y1+1].sum(axis=0) > 0)[0]
        print(f"  band y {y0}..{y1} (h {y1-y0+1}): x {xs5.min()}..{xs5.max()}")

# brown parallelogram
brmask = np.zeros_like(brown)
brmask[230:540, 560:960] = brown[230:540, 560:960]
bbrown = bbox(brmask, "brown parallelogram")
if bbrown:
    # per-row extents to trace the parallelogram shape
    print("brown per-row extents (every 12 rows):")
    for y in range(bbrown[2], bbrown[3] + 1, 12):
        xs6 = np.where(brmask[y])[0]
        if len(xs6):
            print(f"  y={y}: x {xs6.min()}..{xs6.max()}")

# blue filter rectangle
bl2 = np.zeros_like(blue)
bl2[230:540, 560:960] = blue[230:540, 560:960]
bblue = bbox(bl2, "blue ink in right box (filter rect)")
if bblue:
    print("blue per-row extents (every 4 rows):")
    for y in range(bblue[2], bblue[3] + 1, 4):
        xs7 = np.where(bl2[y])[0]
        if len(xs7):
            print(f"  y={y}: x {xs7.min()}..{xs7.max()}")

# red ink inside right box (Filters word + arrow)
rd2 = np.zeros_like(red)
rd2[230:540, 560:960] = red[230:540, 560:960]
bred = bbox(rd2, "red ink in right box (Filters + arrow)")
if bred:
    print("red per-row extents (every 6 rows):")
    for y in range(bred[2], bred[3] + 1, 6):
        xs8 = np.where(rd2[y])[0]
        if len(xs8):
            print(f"  y={y}: x {xs8.min()}..{xs8.max()}")

# ---------- colors ----------
def modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:4]]
    cnts = np.sort(counts)[::-1][:4]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

print()
modal(460, 520, 200, 220, "panel gray sample (between boxes)")
modal(200, 400, 300, 320, "left box fill sample")
modal(700, 850, 300, 320, "right box fill sample")
modal(300, 500, 30, 40, "above-panel canvas sample (y30..40)")
modal(100, 300, 480, 500, "lower panel sample")
