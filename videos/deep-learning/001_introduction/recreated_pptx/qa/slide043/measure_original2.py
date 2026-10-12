#!/usr/bin/env python3
"""Second, refined PIL forensics pass on slide_043.jpg (960x540, 1px = 1pt).

Fixes pass-1 mask contamination: panel gray E9E9E7 passed the >215 white test;
title band included the inner panel border; 3x3 bbox included arrow2; per-cell
fill modal sampling instead of bbox guessing; connected-component red blobs for
x0/x1; border-line profiling for both grids.
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_043.jpg"
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
    return (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))

def rowbands(mask, y0, y1, x0, x1, gap=4, minpix=2, label=""):
    m = np.zeros_like(mask)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    proj = m.sum(axis=1)
    idx = np.where(proj > minpix)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for c in idx[1:]:
            if c - p <= gap:
                p = c
            else:
                out.append((int(s), int(p)))
                s = p = c
        out.append((int(s), int(p)))
    print(f"{label} row bands: {out}")
    return out

def modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    cnts = np.sort(counts)[::-1][:3]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

# ---------- chrome border scan (looser red) ----------
print("--- chrome ---")
redish = (r > 140) & (g < 140) & (b < 140)
for y in list(range(40, 60)):
    xs2 = np.where(redish[y, :])[0]
    if len(xs2) > 300:
        print(f"  chrome top border row y={y}: n={len(xs2)} x {xs2.min()}..{xs2.max()}")
for x in [40, 42, 44, 56, 57, 58, 59, 60, 916, 918, 920, 922]:
    ys2 = np.where(redish[:, x])[0]
    if len(ys2) > 20:
        print(f"  chrome side x={x}: n={len(ys2)} y {ys2.min()}..{ys2.max()}")

# ---------- title (exclude panel border x<75) ----------
print("\n--- title ---")
red = (r > 120) & (g < 110) & (b < 110)
t = np.zeros_like(red)
t[40:108, 75:890] = red[40:108, 75:890]
tb = bbox(t, "title ink")
rowbands(t, 40, 108, 75, 890, gap=2, minpix=2, label="title rows")
if tb:
    cols = np.unique(np.where(t[tb[2]:tb[3]+1])[1])
    segs = []
    s = p = cols[0]
    for c in cols[1:]:
        if c - p > 7:
            segs.append((int(s), int(p), int(p - s + 1)))
            s = c
        p = c
    segs.append((int(s), int(p), int(p - s + 1)))
    print("title word segments:", segs)
modal(120, 400, 60, 90, "title ink+bg sample")

# ---------- inner red panel ----------
print("\n--- inner panel border ---")
for y in range(105, 118):
    xs2 = np.where(red[y, 60:900])[0] + 60
    if len(xs2) > 300:
        print(f"  top border y={y}: x {xs2.min()}..{xs2.max()}")
for y in range(372, 388):
    xs2 = np.where(red[y, 60:900])[0] + 60
    if len(xs2) > 300:
        print(f"  bottom border y={y}: x {xs2.min()}..{xs2.max()}")
for x in range(74, 90):
    ys2 = np.where(red[100:400, x])[0] + 100
    if len(ys2) > 100:
        print(f"  left border x={x}: y {ys2.min()}..{ys2.max()}")
for x in range(838, 852):
    ys2 = np.where(red[100:400, x])[0] + 100
    if len(ys2) > 100:
        print(f"  right border x={x}: y {ys2.min()}..{ys2.max()}")

# ---------- bullets ----------
print("\n--- bullets (dark <160) ---")
dark = (r < 160) & (g < 160) & (b < 160)
bl = np.zeros_like(dark)
bl[115:210, 140:570] = dark[115:210, 140:570]
bands = rowbands(bl, 115, 210, 140, 570, gap=5, minpix=2, label="bullet lines")
for (y0, y1) in bands:
    m = bl[y0:y1+1]
    xs3 = np.where(m.sum(axis=0) > 0)[0]
    print(f"  line y {y0}..{y1}: x {xs3.min()}..{xs3.max()} (h {y1-y0+1})")
# markers: non-background in x 120..145
panel = (np.abs(r-233) < 14) & (np.abs(g-233) < 14) & (np.abs(b-231) < 14)
nonpanel = ~panel & ~dark
mk = np.zeros_like(nonpanel)
mk[115:210, 118:148] = nonpanel[115:210, 118:148]
rowbands(mk, 115, 210, 118, 148, gap=3, minpix=2, label="bullet markers")
ys4, xs4 = np.where(mk)
if len(ys4):
    print(f"  marker ink bbox: x {xs4.min()}..{xs4.max()} y {ys4.min()}..{ys4.max()}")
modal(126, 134, 128, 134, "bullet marker color sample")

# ---------- diagram labels (full width, above grids) ----------
print("\n--- labels row y 195..245 ---")
lbl = np.zeros_like(dark)
lbl[195:245, 200:910] = dark[195:245, 200:910]
rowbands(lbl, 195, 245, 200, 910, gap=4, minpix=2, label="label rows")
cols = np.where(lbl.sum(axis=0) > 0)[0]
if len(cols):
    segs = []
    s = p = cols[0]
    for c in cols[1:]:
        if c - p > 14:
            segs.append((int(s), int(p), int(p - s + 1)))
            s = c
        p = c
    segs.append((int(s), int(p), int(p - s + 1)))
    print("label segments (x0,x1,w):", segs)

# ---------- 5x5 grid: border profiling + per-cell fills ----------
print("\n--- 5x5 grid borders (dark <150 any) ---")
darkish = (r < 150) & (g < 150) & (b < 150)
dm = np.zeros_like(darkish)
dm[220:385, 235:445] = darkish[220:385, 235:445]
colprof = dm.sum(axis=0)
strong_cols = [int(c) for c in np.where(colprof > 100)[0]]
print("5x5 strong border cols (n>100):", strong_cols)
rowprof = dm.sum(axis=1)
strong_rows = [int(c) for c in np.where(rowprof > 100)[0]]
print("5x5 strong border rows (n>100):", strong_rows)
# what color are the border lines? sample a border column region
if strong_cols:
    c0 = strong_cols[0]
    modal(c0, c0+1, 240, 370, f"5x5 border col {c0} color")

# green cell bbox with proper green mask
green = (g > 150) & (g > r + 50) & (g > b + 50)
ym = np.zeros_like(green)
ym[220:385, 235:445] = green[220:385, 235:445]
bbox(ym, "green fill bbox")
yellow = (r > 220) & (g > 200) & (b < 140)
ym2 = np.zeros_like(yellow)
ym2[220:385, 235:445] = yellow[220:385, 235:445]
bbox(ym2, "yellow fill bbox")

print("\n--- 5x5 per-cell modal fill (interior 8px inset) ---")
# use border cols/rows if found; else assume from fill bboxes
# cells: use yellow+green union bbox
fill = green | yellow
fm = np.zeros_like(fill)
fm[220:385, 235:445] = fill[220:385, 235:445]
ys5, xs5 = np.where(fm)
gx0, gx1, gy0, gy1 = xs5.min(), xs5.max(), ys5.min(), ys5.max()
print(f"grid fill bbox x {gx0}..{gx1} y {gy0}..{gy1} (w {gx1-gx0+1} h {gy1-gy0+1})")
cw = (gx1 - gx0 + 1) / 5.0
ch = (gy1 - gy0 + 1) / 5.0
print(f"cell {cw:.1f} x {ch:.1f}")
for ri in range(5):
    rowcols = []
    for ci in range(5):
        ix0 = int(gx0 + ci * cw + cw * 0.3)
        ix1 = int(gx0 + (ci + 1) * cw - cw * 0.3)
        iy0 = int(gy0 + ri * ch + ch * 0.3)
        iy1 = int(gy0 + (ri + 1) * ch - ch * 0.3)
        reg = IM[iy0:iy1, ix0:ix1].reshape(-1, 3)
        vals, counts = np.unique(reg, axis=0, return_counts=True)
        top = vals[np.argmax(counts)]
        rowcols.append('#%02X%02X%02X' % tuple(top))
    print(f" row {ri}: {rowcols}")

# ---------- red x0/x1 connected blobs ----------
print("\n--- x0/x1 red blobs (connected components) ---")
red3 = (r > 140) & (g < 110) & (b < 110)
xm = np.zeros_like(red3)
xm[220:330, 240:400] = red3[220:330, 240:400]
visited = np.zeros_like(xm)
blobs = []
ys6, xs6 = np.where(xm)
from collections import deque
for sy, sx in zip(ys6, xs6):
    if visited[sy, sx]:
        continue
    q = deque([(sy, sx)])
    visited[sy, sx] = 1
    pts = []
    while q:
        y, x = q.popleft()
        pts.append((y, x))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and xm[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = 1
                    q.append((ny, nx))
    ys7 = [p[0] for p in pts]; xs7 = [p[1] for p in pts]
    blobs.append((min(xs7), max(xs7), min(ys7), max(ys7), len(pts)))
blobs.sort(key=lambda t: (t[2], t[0]))
print(f"{len(blobs)} blobs:")
for bl_ in blobs:
    print(f"  x {bl_[0]}..{bl_[1]} y {bl_[2]}..{bl_[3]} (w {bl_[1]-bl_[0]+1} h {bl_[3]-bl_[2]+1} n {bl_[4]})")

# ---------- 3x3 grid precise ----------
print("\n--- 3x3 grid ---")
grayol = (np.abs(r - 149) < 35) & (np.abs(g - 163) < 35) & (np.abs(b - 138) < 35)
zm = np.zeros_like(grayol)
zm[240:375, 495:680] = grayol[240:375, 495:680]
zb = bbox(zm, "3x3 gray fill bbox")
dm3 = np.zeros_like(darkish)
dm3[240:375, 495:680] = darkish[240:375, 495:680]
colprof3 = dm3.sum(axis=0)
print("3x3 strong border cols (n>60):", [int(c) for c in np.where(colprof3 > 60)[0]])
rowprof3 = dm3.sum(axis=1)
print("3x3 strong border rows (n>60):", [int(c) for c in np.where(rowprof3 > 60)[0]])
modal(520, 560, 255, 290, "3x3 fill sample")
if zb:
    cw3 = (zb[1] - zb[0] + 1) / 3.0
    ch3 = (zb[3] - zb[2] + 1) / 3.0
    print(f"3x3 cell {cw3:.1f} x {ch3:.1f}")
    nd = (r < 100) & (g < 100) & (b < 100)
    for ri in range(3):
        cells = []
        for ci in range(3):
            cx0 = int(zb[0] + ci * cw3) + 4
            cx1 = int(zb[0] + (ci + 1) * cw3) - 4
            cy0 = int(zb[2] + ri * ch3) + 4
            cy1 = int(zb[2] + (ri + 1) * ch3) - 4
            reg = nd[cy0:cy1, cx0:cx1]
            if reg.sum() > 3:
                yy, xx = np.where(reg)
                cells.append((cx0 + xx.min(), cx0 + xx.max(), cy0 + yy.min(), cy0 + yy.max()))
            else:
                cells.append(None)
        print(f" row {ri}: {cells}")

# ---------- 1x1 cell ----------
print("\n--- 1x1 cell ---")
zm2 = np.zeros_like(grayol)
zm2[275:335, 695:830] = grayol[275:335, 695:830]
bbox(zm2, "1x1 gray fill bbox")
nd2 = (r < 100) & (g < 100) & (b < 100)
nm2 = np.zeros_like(nd2)
nm2[280:330, 730:800] = nd2[280:330, 730:800]
bbox(nm2, "'18' ink bbox")

# ---------- arrows (white >245 fill + outline) ----------
print("\n--- arrows ---")
white2 = (r > 245) & (g > 245) & (b > 245)
a1 = np.zeros_like(white2)
a1[270:350, 425:540] = white2[270:350, 425:540]
bbox(a1, "arrow1 white fill")
a2 = np.zeros_like(white2)
a2[270:350, 640:750] = white2[270:350, 640:750]
bbox(a2, "arrow2 white fill")
# arrow outline: dark pixels adjacent to white fill
dk1 = np.zeros_like(darkish)
dk1[270:350, 425:540] = darkish[270:350, 425:540]
bbox(dk1, "arrow1 dark outline+ink")
dk2 = np.zeros_like(darkish)
dk2[270:350, 640:750] = darkish[270:350, 640:750]
bbox(dk2, "arrow2 dark outline+ink")
modal(455, 465, 295, 305, "arrow1 fill sample")

# ---------- blue box ----------
print("\n--- blue explanation box ---")
blue = (b > 120) & (b > r + 30) & (b > g + 20)
bm = np.zeros_like(blue)
bm[380:525, 40:930] = blue[380:525, 40:930]
bb2 = bbox(bm, "blue border+text bbox")
# box border rows: full-width-ish blue runs
for y in range(380, 525):
    xs2 = np.where(bm[y])[0]
    if len(xs2) > 300:
        print(f"  blue border row y={y}: n={len(xs2)} x {xs2.min()}..{xs2.max()}")
for x in range(60, 100):
    ys2 = np.where(bm[:, x])[0]
    if len(ys2) > 60:
        print(f"  blue left border x={x}: n={len(ys2)} y {ys2.min()}..{ys2.max()}")
for x in range(860, 920):
    ys2 = np.where(bm[:, x])[0]
    if len(ys2) > 60:
        print(f"  blue right border x={x}: n={len(ys2)} y {ys2.min()}..{ys2.max()}")
modal(200, 700, 395, 400, "blue top border sample")
navy = (b > 90) & (r < 110) & (g < 110) & (b > r + 30)
nm3 = np.zeros_like(navy)
nm3[400:515, 75:900] = navy[400:515, 75:900]
bands3 = rowbands(nm3, 400, 515, 75, 900, gap=5, minpix=3, label="navy lines")
for (y0, y1) in bands3:
    m = nm3[y0:y1+1]
    xs3 = np.where(m.sum(axis=0) > 0)[0]
    print(f"  line y {y0}..{y1}: x {xs3.min()}..{xs3.max()} (h {y1-y0+1})")
# white box fill (>250)
white3 = (r > 249) & (g > 249) & (b > 249)
wf = np.zeros_like(white3)
wf[385:520, 45:925] = white3[385:520, 45:925]
bbox(wf, "box white fill bbox")

# ---------- misc samples ----------
print("\n--- more color samples ---")
modal(46, 60, 455, 495, "panel gray left strip")
modal(60, 75, 200, 260, "panel gray above box left")
modal(440, 470, 390, 400, "between inner panel bottom & box")
modal(925, 950, 200, 300, "canvas outside panel right")
modal(200, 300, 500, 512, "below blue box (panel?)")
