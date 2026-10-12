#!/usr/bin/env python3
"""Slide 038 — m20: caption gaps/underscores, dot colors, block-arrow geometry,
plus-ring, container dash, annotation cores, label ink metrics."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

print("== caption: red-ish ink column profile y494..508, x265..565 (word blobs + gaps) ==")
redish = (R > 110) & (G < 160) & (B < 120) & (R - B > 60)
seg = redish[494:509, 265:565]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 0 and not inr: s = i; inr = True
    elif v == 0 and inr:
        runs.append((s + 265, i + 265)); inr = False
if inr: runs.append((s + 265, 565))
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] <= 3: merged[-1] = (merged[-1][0], b)
    else: merged.append((a, b))
print("  blobs:", [(a, b, b - a) for a, b in merged])
print("  slide:", [(round(invx(a), 1), round(invx(b), 1)) for a, b in merged])
print("  baseline-row check (underscore?): red px per row x265..565:")
for y in range(494, 509):
    print(f"    y={y}: {int(redish[y, 265:565].sum())}")

print("== dot colors: census 3x3 at each top dot center (frame x 629,648,666,684,699 y~268) ==")
for cx in (629, 648, 666, 684, 699):
    px_ = img[266:272, cx-3:cx+4].reshape(-1, 3)
    dark = px_[(px_[:, 2] > 120) & (px_[:, 0] < 100)]
    if len(dark): print(f"  top dot x{cx}: mean ({dark[:,0].mean():.0f},{dark[:,1].mean():.0f},{dark[:,2].mean():.0f}) n={len(dark)}")
for cx in (629, 648, 666, 684, 699):
    px_ = img[474:480, cx-3:cx+4].reshape(-1, 3)
    dark = px_[(px_[:, 1] > 120) & (px_[:, 0] < 150) & (px_[:, 2] < 120)]
    if len(dark): print(f"  x-row dot x{cx}: mean ({dark[:,0].mean():.0f},{dark[:,1].mean():.0f},{dark[:,2].mean():.0f}) n={len(dark)}")

print("== block arrow col2: blue outline per-row min/max x, rows 382..401 (mid->navy) ==")
blue = (B > 120) & (B - R > 40) & (G < 130)
for y in range(382, 402):
    cols = np.where(blue[y, 265:295])[0]
    if len(cols): print(f"  y={y}: x {cols.min()+265}..{cols.max()+265} n={len(cols)}")
print("== block arrow col2: rows 450..470 (navy->X) ==")
for y in range(450, 471):
    cols = np.where(blue[y, 265:295])[0]
    if len(cols): print(f"  y={y}: x {cols.min()+265}..{cols.max()+265} n={len(cols)}")
print("== block arrow interior fill sample (mid->navy col2, y390 x276..279) ==")
print("  ", [tuple(img[390, x]) for x in range(274, 283)])
print("== block arrow outline color sample ==")
px_ = img[384:400, 270:290]
m = blue[384:400, 270:290]
if m.sum(): print("  outline mean:", px_[m].mean(axis=0).round(0), "n=", int(m.sum()))

print("== plus ring: census col1 circle (x199..213, y334..348) ==")
seg = img[334:349, 198:215]
m = (seg[:, :, 0] > 110) & (seg[:, :, 1] < 90) & (seg[:, :, 2] < 90)
if m.sum(): print("  ring mean:", seg[m].mean(axis=0).round(0), "n=", int(m.sum()))
print("  raw row y=341 x196..216:", [tuple(img[341, x]) for x in range(196, 217, 2)])

print("== container dash color census (top border y284..288, x100..800) ==")
green = (G > 100) & (G - R > 25) & (G - B > 25)
seg = img[283:290, 100:800]
m = green[283:290, 100:800]
if m.sum(): print("  dash mean:", seg[m].mean(axis=0).round(0), "n=", int(m.sum()))
print("== container fill census (inside, avoiding bar/dots: y290..293 x120..160, y350..356 x400..500) ==")
for (y0,y1,x0,x1) in ((290,294,120,160),(350,357,400,500),(324,332,610,700)):
    seg2 = img[y0:y1, x0:x1].reshape(-1,3)
    print(f"  ({x0}..{x1},{y0}..{y1}): mean ({seg2[:,0].mean():.0f},{seg2[:,1].mean():.0f},{seg2[:,2].mean():.0f})")

print("== annotation cores (bold-italic text) ==")
for name, y0, y1, x0, x1 in (("blue1", 369, 378, 72, 158), ("orange1", 417, 423, 72, 158), ("red1", 455, 464, 72, 154)):
    seg3 = img[y0:y1, x0:x1].reshape(-1, 3)
    lum = 0.299*seg3[:,0]+0.587*seg3[:,1]+0.114*seg3[:,2]
    dk = seg3[lum < 130]
    if len(dk): print(f"  {name}: mean ({dk[:,0].mean():.0f},{dk[:,1].mean():.0f},{dk[:,2].mean():.0f}) n={len(dk)}")

print("== top-row label metrics col1: Y ink bbox + sub bbox (dark-red mask) ==")
drm = (R > 100) & (G < 110) & (B < 110) & (R - G > 40)
for (x0,x1,y0,y1,lab) in ((196,215,258,278,'col1'),(269,290,258,278,'col2'),(560,585,258,278,'col6'),(746,775,258,278,'col7'),(818,848,258,278,'col8')):
    seg4 = drm[y0:y1, x0:x1]
    rows = np.where(seg4.sum(axis=1) > 0)[0]
    cols = np.where(seg4.sum(axis=0) > 0)[0]
    if len(rows):
        print(f"  {lab}: ink x {cols.min()+x0}..{cols.max()+x0} (w={cols.max()-cols.min()+1}) y {rows.min()+y0}..{rows.max()+y0} (h={rows.max()-rows.min()+1})")

print("== X-row label ink (should match top) ==")
for (x0,x1,y0,y1,lab) in ((196,215,466,486,'col1'),(818,848,466,486,'col8')):
    seg4 = drm[y0:y1, x0:x1]
    rows = np.where(seg4.sum(axis=0) > 0)[0]
    cols = np.where(seg4.sum(axis=1) > 0)[0]
    rows2 = np.where(seg4.sum(axis=1) > 0)[0]
    cols2 = np.where(seg4.sum(axis=0) > 0)[0]
    if len(rows2):
        print(f"  {lab}: ink x {cols2.min()+x0}..{cols2.max()+x0} (w={cols2.max()-cols2.min()+1}) y {rows2.min()+y0}..{rows2.max()+y0} (h={rows2.max()-rows2.min()+1})")

print("== mid-row label ink col2 (prime check: ink above-right of Y) ==")
drm2 = (R > 100) & (G < 120) & (B < 120) & (R - G > 30)
seg5 = drm2[364:384, 268:292]
rows = np.where(seg5.sum(axis=1) > 0)[0]
cols = np.where(seg5.sum(axis=0) > 0)[0]
print(f"  mid col2: ink x {cols.min()+268}..{cols.max()+268} y {rows.min()+364}..{rows.max()+364}")
# per-row extents
for r in rows:
    cc = np.where(seg5[r])[0]
    print(f"    y={r+364}: x {cc.min()+268}..{cc.max()+268}")
print("== top col2 per-row extents (for comparison) ==")
seg6 = drm[258:280, 268:292]
for r in np.where(seg6.sum(axis=1) > 0)[0]:
    cc = np.where(seg6[r])[0]
    print(f"    y={r+258}: x {cc.min()+268}..{cc.max()+268}")
