#!/usr/bin/env python3
"""Derivation rows 1..7 bands in x66..740; left/right edges; trailing glyphs; per-row colors."""
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)

def runs(m, minlen=1):
    out, i, n = [], 0, len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]: j += 1
            if j - i >= minlen: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# interior of derivation panel excluding ribbon/callout: x68..735, y258..510
pan = a[258:512, 68:736]
mx = pan.max(axis=2); mn = pan.min(axis=2)
ink = (mn < 195) | ((mx - mn) > 40)
rowsum = ink.sum(axis=1)
bands = runs(rowsum > 2, 3)
print("derivation rows (x68..736):")
for y0, y1 in bands:
    seg = pan[y0:y1 + 1]
    m2 = (seg.min(axis=2) < 195) | ((seg.max(axis=2) - seg.min(axis=2)) > 40)
    cols = np.where(m2.any(axis=0))[0]
    occ = m2.any(axis=0)
    rr = runs(occ, 2)
    red = (seg[:, :, 0] - seg[:, :, 1] > 40) & (seg[:, :, 0] > 110)
    blue = (seg[:, :, 2] - seg[:, :, 0] > 40) & (seg[:, :, 2] > 95)
    # text core rows (exclude antialiasing)
    print(f"  y{258+y0}..{258+y1} (h{y1-y0+1}) x{68+cols.min()}..{68+cols.max()}  "
          f"red={int(red.sum())} blue={int(blue.sum())}  ink-runs(n={len(rr)}) first={68+rr[0][0]}..{68+rr[0][1]} last={68+rr[-1][0]}..{68+rr[-1][1]}")
    # last few runs (trailing glyphs)
    tail = [(68 + r0, 68 + r1) for r0, r1 in rr[-3:]]
    print(f"     tail runs: {tail}")

# yellow highlights anywhere in panel (looser)
yel = (pan[:, :, 0] > 215) & (pan[:, :, 1] > 215) & (pan[:, :, 2] < 185) & ((pan[:, :, 0] - pan[:, :, 2]) > 45)
lab, _ = label(yel)
print("\nyellow/cream highlight comps >60px in derivation panel:")
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 60:
        print(f"  y{258+sl[0].start}..{258+sl[0].stop-1} x{68+sl[1].start}..{68+sl[1].stop-1} ({w}x{h})")

# cyan highlights looser
cyn = (pan[:, :, 2] > 185) & (pan[:, :, 1] > 170) & (pan[:, :, 0] < 185) & ((pan[:, :, 2] - pan[:, :, 0]) > 40)
lab, _ = label(cyn)
print("cyan highlight comps >60px:")
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 60:
        print(f"  y{258+sl[0].start}..{258+sl[0].stop-1} x{68+sl[1].start}..{68+sl[1].stop-1} ({w}x{h})")

# CALLOUT box: bounds + fill + border color
print("\n== CALLOUT ==")
reg = a[460:512, 560:750]
g = (reg[:, :, 1] - reg[:, :, 0] > 30) & (reg[:, :, 1] > 120) & (reg[:, :, 1] - reg[:, :, 2] > 10)
lab, _ = label(g)
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 100:
        print(f"  green comp: y{460+sl[0].start}..{460+sl[0].stop-1} x{560+sl[1].start}..{560+sl[1].stop-1} ({w}x{h})")
# border ring detection: for each row, green cols
for y in (470, 472, 485, 498, 500):
    row = reg[y - 460]
    gcols = np.where((row[:, 1] - row[:, 0] > 30) & (row[:, 1] > 120))[0]
    print(f"  y{y} green cols:", (560 + gcols.min(), 560 + gcols.max()) if len(gcols) else None)
for x in (576, 578, 650, 731, 733):
    col = reg[:, x - 560]
    grows = np.where((col[:, 1] - col[:, 0] > 30) & (col[:, 1] > 120))[0]
    print(f"  x{x} green rows:", (460 + grows.min(), 460 + grows.max()) if len(grows) else None)
red = (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] > 130)
ys, xs = np.where(red)
if len(ys):
    print(f"  red text bbox: x{560+xs.min()}..{560+xs.max()} y{460+ys.min()}..{460+ys.max()}")

# RIBBON: rotated strip — measure angle via pale-yellow mask PCA
print("\n== RIBBON ==")
reg2 = a[395:516, 725:870]
py = (reg2[:, :, 0] > 230) & (reg2[:, :, 1] > 225) & (reg2[:, :, 2] > 150) & (reg2[:, :, 2] < 230) & ((reg2[:, :, 0] - reg2[:, :, 2]) > 15)
ys, xs = np.where(py)
if len(ys):
    pts = np.stack([xs, ys]).astype(float)
    ctr = pts.mean(axis=1)
    cov = np.cov(pts)
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, -1]  # major axis
    ang = np.degrees(np.arctan2(v[1], v[0]))
    print(f"  pale-yellow npx={len(ys)} bbox x{725+xs.min()}..{725+xs.max()} y{395+ys.min()}..{395+ys.max()}")
    print(f"  major axis angle (deg, y-down screen): {ang:.1f}  -> CCW-from-horizontal ≈ {-ang:.1f}")
    # ribbon width along minor axis
    minor = evecs[:, 0]
    proj_minor = (pts.T - ctr) @ minor
    print(f"  minor extent ≈ {proj_minor.max()-proj_minor.min():.0f}px; major extent ≈ {(pts.T-ctr)@evecs[:,-1] and (lambda p: p.max()-p.min())((pts.T-ctr)@evecs[:,-1]):.0f}px")
# red text inside ribbon
red2 = (reg2[:, :, 0] - reg2[:, :, 1] > 60) & (reg2[:, :, 0] > 130)
ys2, xs2 = np.where(red2)
if len(ys2):
    pts2 = np.stack([xs2, ys2]).astype(float)
    c2 = pts2.mean(axis=1); cov2 = np.cov(pts2)
    ev2, evec2 = np.linalg.eigh(cov2)
    ang2 = np.degrees(np.arctan2(evec2[1, -1], evec2[0, -1]))
    print(f"  red text bbox x{725+xs2.min()}..{725+xs2.max()} y{395+ys2.min()}..{395+ys2.max()} npx={len(ys2)} axis angle {ang2:.1f} (CCW ≈ {-ang2:.1f})")
