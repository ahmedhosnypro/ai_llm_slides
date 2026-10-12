#!/usr/bin/env python3
"""Pass 1b — fix modal(mask); chrome-region colors; panel vertical borders; title cap."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_042.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def modal(x0, x1, y0, y1, label, mask=None):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    if mask is not None:
        m = mask[y0:y1+1, x0:x1+1]
        reg = IM[y0:y1+1, x0:x1+1][m]
        if len(reg) == 0:
            print(f"{label}: mask empty"); return
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:4]
    print(f"{label}: " + ", ".join('#%02X%02X%02X(%d)' % (*vals[i], counts[i]) for i in order))

def bbox(mask, x0, x1, y0, y1, label, minpix=1):
    sub = np.zeros_like(mask)
    sub[y0:y1+1, x0:x1+1] = mask[y0:y1+1, x0:x1+1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"{label}: EMPTY"); return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  (n={len(xs)})")
    return (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))

# ---- chrome regions ----
modal(44, 74, 200, 400, "chrome zone between x42 border and inner panel (x44-74)")
modal(44, 900, 48, 132, "chrome zone above inner panel top (y48-132, x44-900)")
modal(5, 40, 100, 300, "canvas left of chrome panel")
modal(925, 958, 100, 300, "canvas right of chrome panel")
# chrome border strokes
redv = (r > 120) & (g < 110) & (b < 110)
for x in range(40, 50):
    col = np.where(redv[50:520, x])[0]
    if len(col) > 200: print(f"chrome left red stroke candidate x={x}: n={len(col)} y {col.min()+50}..{col.max()+50}")
for x in range(912, 922):
    col = np.where(redv[50:520, x])[0]
    if len(col) > 200: print(f"chrome right red stroke candidate x={x}: n={len(col)} y {col.min()+50}..{col.max()+50}")

# ---- inner panel borders ----
print("\n--- INNER PANEL red border ---")
modal(78, 890, 133, 140, "inner panel top stroke modal", mask=redv)
# vertical strokes near x78 and x890, y140..505
for x in range(74, 84):
    col = np.where(redv[140:506, x])[0]
    if len(col) > 250: print(f"inner LEFT stroke x={x}: n={len(col)} y {col.min()+140}..{col.max()+140}")
for x in range(884, 896):
    col = np.where(redv[140:506, x])[0]
    if len(col) > 250: print(f"inner RIGHT stroke x={x}: n={len(col)} y {col.min()+140}..{col.max()+140}")
# horizontal bottom
for y in range(503, 512):
    row = np.where(redv[y, 80:888])[0]
    if len(row) > 500: print(f"inner BOTTOM stroke y={y}: n={len(row)} x {row.min()+80}..{row.max()+80}")

# ---- title ----
redt = (r > 120) & (g < 110) & (b < 110)
tmask = np.zeros_like(redt); tmask[40:130, 40:920] = redt[40:130, 40:920]
modal(0, W, 0, H, "title ink modal", mask=tmask)
ys = np.where(tmask.sum(axis=1) > 0)[0]
xs = np.where(tmask.sum(axis=0) > 0)[0]
print(f"title ink: x {xs.min()}..{xs.max()} (center {(xs.min()+xs.max())/2})  y {ys.min()}..{ys.max()}")
# cap 'O': first glyph
segO = tmask[:, xs.min():xs.min()+24]
ysO = np.where(segO.sum(axis=1) > 0)[0]
print(f"first-glyph cap: y {ysO.min()}..{ysO.max()} cap-height {ysO.max()-ysO.min()+1}")
# 'p' descender zone: look at rows below baseline across full title
print("rowsum by row (y78..116):", [(int(y), int(tmask[y].sum())) for y in range(78, 117)])

# ---- equations box: black border + white ----
print("\n--- EQUATION BOX detail ---")
black = (r < 90) & (g < 90) & (b < 90)
eb = bbox(black, 320, 545, 300, 480, "eqbox black ink")
if eb:
    x0, x1, y0, y1 = eb
    modal(x0, x1, y0, y1, "eqbox region modal")
    # border strokes
    print("eqbox horiz black runs >=80px:")
    for y in range(y0, y1+1):
        rrow = np.where(black[y, x0:x1+1])[0]
        if len(rrow) >= 80:
            runs = []; s = p = rrow[0]
            for c in rrow[1:]:
                if c <= p+2: p = c
                else: runs.append((s,p)); s = p = c
            runs.append((s,p))
            for (a, bb) in runs:
                if bb-a+1 >= 80: print(f"  y={y}: x {a+x0}..{bb+x0} len {bb-a+1}")
    print("eqbox vert black runs >=60px:")
    for x in range(x0, x1+1):
        rcol = np.where(black[y0:y1+1, x])[0]
        if len(rcol) >= 60:
            runs = []; s = p = rcol[0]
            for c in rcol[1:]:
                if c <= p+2: p = c
                else: runs.append((s,p)); s = p = c
            runs.append((s,p))
            for (a, bb) in runs:
                if bb-a+1 >= 60: print(f"  x={x}: y {a+y0}..{bb+y0} len {bb-a+1}")

# ---- legend ----
print("\n--- LEGEND detail ---")
blueleg = (b > 120) & (r < 110) & (g < 110) & (b > r + 50)
bl = bbox(blueleg, 60, 300, 350, 520, "legend blue symbols")
if bl:
    modal(60, 300, 350, 520, "legend blue modal", mask=blueleg)
    # per-line bands
    sub = np.zeros_like(blueleg); sub[350:520, 60:300] = blueleg[350:520, 60:300]
    rows = np.where(sub.sum(axis=1) > 0)[0] + 350
    bands = []; s = p = rows[0]
    for c in rows[1:]:
        if c - p <= 3: p = c
        else: bands.append((s, p)); s = p = c
    bands.append((s, p))
    print("legend blue line bands (y):", bands)
blk2 = np.zeros_like(black); blk2[350:520, 60:300] = black[350:520, 60:300]
rows = np.where(blk2.sum(axis=1) > 0)[0] + 350
if len(rows):
    bands = []; s = p = rows[0]
    for c in rows[1:]:
        if c - p <= 3: p = c
        else: bands.append((s, p)); s = p = c
    bands.append((s, p))
    print("legend black line bands (y):", bands)
    xs2 = np.where(blk2.sum(axis=0) > 0)[0]
    print("legend black ink x extent:", xs2.min(), "..", xs2.max())
