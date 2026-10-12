#!/usr/bin/env python3
"""Pass 2: fine measurements — yellow box edges/border, arrow full extent,
title/navy/border colors, photo rectangles, font metric data."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_040.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def modal(x0, x1, y0, y1, label, mask=None):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    if mask is not None:
        reg = mask[y0:y1+1, x0:x1+1].reshape(-1, 3)
        reg = reg[(reg[:, 0] + reg[:, 1] + reg[:, 2]) >= 0]
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:4]
    print(f"{label}: " + ", ".join('#%02X%02X%02X(%d)' % (*vals[i], counts[i]) for i in order))

# ---- yellow box: fill profile. Fill = pale cream (FAFCE7-ish: r,g ~250, b ~231) ----
fill = (r > 240) & (g > 240) & (b > 215) & (b < 245)
win = fill[330:540, 30:720]
rows = np.where(win.sum(axis=1) > 30)[0] + 330
cols = np.where(win.sum(axis=0) > 30)[0] + 30
print("yellow FILL rows:", rows.min(), "..", rows.max(), " cols:", cols.min(), "..", cols.max())
# percentile-based edges (robust)
rowsum = win.sum(axis=1); colsum = win.sum(axis=0)
rr = np.where(rowsum > 100)[0] + 330
cc = np.where(colsum > 100)[0] + 30
print("yellow FILL strong rows:", rr.min(), "..", rr.max(), " strong cols:", cc.min(), "..", cc.max())

# ---- blue border rectangle: long blue runs ----
blue = (b > 150) & (r < 90) & (g < 90)
print("\n--- blue horiz runs >=50 in y 340..530 ---")
for y in range(340, 531):
    xs = np.where(blue[y, :720])[0]
    if len(xs) > 50:
        runs = []; s = p = xs[0]
        for c in xs[1:]:
            if c == p + 1: p = c
            else: runs.append((s, p)); s = p = c
        runs.append((s, p))
        for (a, bb) in runs:
            if bb - a + 1 >= 50: print(f"y={y}: x {a}..{bb} (len {bb-a+1})")
print("--- blue vert runs >=30 in x 30..720 ---")
for x in range(30, 721):
    ys = np.where(blue[340:530, x])[0] + 340
    if len(ys) > 30:
        runs = []; s = p = ys[0]
        for c in ys[1:]:
            if c == p + 1: p = c
            else: runs.append((s, p)); s = p = c
        runs.append((s, p))
        for (a, bb) in runs:
            if bb - a + 1 >= 30: print(f"x={x}: y {a}..{bb} (len {bb-a+1})")

# ---- arrow: white + red, wide window ----
white = (r > 225) & (g > 225) & (b > 225)
red = (r > 120) & (g < 110) & (b < 110)
wm = np.zeros_like(white); wm[380:510, 600:800] = white[380:510, 600:800]
ys, xs = np.where(wm)
print("\narrow WHITE extent: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
rm = np.zeros_like(red); rm[380:510, 600:800] = red[380:510, 600:800]
ys2, xs2 = np.where(rm)
print("arrow RED outline extent: x", xs2.min(), "..", xs2.max(), " y", ys2.min(), "..", ys2.max())
# arrow row profile to see the block shape
for y in range(ys.min(), ys.max() + 1, 4):
    xr = np.where(wm[y])[0]
    if len(xr): print(f"  white y={y}: x {xr.min()}..{xr.max()} n={len(xr)}")

# ---- title ink color + metrics ----
redt = (r > 120) & (g < 110) & (b < 110)
tmask = np.zeros_like(redt); tmask[50:135, 60:900] = redt[50:135, 60:900]
modal(0, W, 0, H, "title ink modal", mask=tmask)
# cap height: column of 'H' (x 204..) vertical extent; baseline find
seg = tmask[:, 204:280]
ys3 = np.where(seg.sum(axis=1) > 0)[0]
print("title 'How' region y extent:", ys3.min(), "..", ys3.max())
# full title descender: 'y' in 'many'... take full ink
ys4 = np.where(tmask.sum(axis=1) > 0)[0]
print("title full ink y extent:", ys4.min(), "..", ys4.max())
# H cap only: first 12 cols of ink
xs5 = np.where(tmask.sum(axis=0) > 0)[0]
segH = tmask[:, xs5[0]:xs5[0]+18]
ysH = np.where(segH.sum(axis=1) > 0)[0]
print(f"title 'H' cap: y {ysH.min()}..{ysH.max()} (cap height {ysH.max()-ysH.min()+1})")

# ---- navy text color ----
navy = (b > 90) & (r < 100) & (g < 100) & (b > r + 40) & (b > g + 40)
modal(0, W, 0, H, "navy text modal", mask=navy)

# ---- blue border color (long runs only) ----
bord = np.zeros_like(blue)
bord[352:358, 70:650] = blue[352:358, 70:650]
modal(0, W, 0, H, "blue border modal (top stroke)", mask=bord)

# ---- photo boxes: precise. left photo x 97..403, y 155..319; right x 432..731, y 158..319 ----
# verify edges via red-run midlines and check interior non-gray content extent
nonbg = (np.abs(r - 233) > 22) | (np.abs(g - 233) > 22) | (np.abs(b - 231) > 22)
for label, (x0, x1, y0, y1) in {
    "LEFT photo": (90, 410, 148, 326),
    "RIGHT photo": (425, 738, 150, 326),
    "FILTER grid": (718, 895, 344, 504),
}.items():
    sub = nonbg[y0:y1+1, x0:x1+1]
    ys6, xs6 = np.where(sub)
    print(f"{label} content: x {xs6.min()+x0}..{xs6.max()+x0}  y {ys6.min()+y0}..{ys6.max()+y0}")

# ---- meme caption text inside left photo (white all-caps) ----
lw = (r > 200) & (g > 200) & (b > 200)
lm = np.zeros_like(lw); lm[150:330, 90:410] = lw[150:330, 90:410]
ys7 = np.where(lm.sum(axis=1) > 8)[0]
print("left photo white-caption rows:", ys7.min() if len(ys7) else None, "..", ys7.max() if len(ys7) else None)
bands = []
if len(ys7):
    s = p = ys7[0]
    for c in ys7[1:]:
        if c - p <= 4: p = c
        else: bands.append((s, p)); s = p = c
    bands.append((s, p))
    print("caption bands:", bands)

# ---- filter grid interior colors sanity ----
modal(730, 880, 360, 490, "filter grid interior")

# ---- panel gray + canvas ----
modal(500, 700, 200, 300, "panel gray (mid area)")
modal(5, 35, 100, 300, "canvas outside panel")
