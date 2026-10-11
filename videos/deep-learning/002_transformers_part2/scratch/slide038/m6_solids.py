#!/usr/bin/env python3
"""Slide 038 — solid shapes via row-count profiles: navy block, gray bar, yellow caption, vector rows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

navy = (B > 100) & (R < 70) & (G < 70) & (B - R > 60)
gray = (abs(R - G) < 12) & (abs(G - B) < 12) & (R > 190) & (R < 230)
yellow = (R > 200) & (G > 180) & (B < 120)

def solid_bands(mask, y0, y1, x0, x1, thresh, label):
    prof = mask[y0:y1, x0:x1].sum(axis=1)
    runs, inr = [], False
    for i, v in enumerate(prof):
        if v > thresh and not inr:
            s = i; inr = True
        elif v <= thresh and inr:
            runs.append((s + y0, i + y0)); inr = False
    if inr: runs.append((s + y0, y1))
    for a, b in runs:
        band = mask[a:b, x0:x1]
        colprof = band.sum(axis=0)
        cols = np.where(colprof > (b - a) * 0.5)[0]
        if len(cols):
            print(f"  {label} SOLID y {a}..{b-1} x {cols.min()+x0}..{cols.max()+x0}"
                  f" -> slide x {invx(cols.min()+x0)}..{invx(cols.max()+x0)} y {invy(a)}..{invy(b-1)}  (h={b-a})")

print("== navy SOLID (>400 rows) ==")
solid_bands(navy, 250, 511, 66, 892, 400, "navy")
print("== gray SOLID (>300 rows) ==")
solid_bands(gray, 250, 511, 66, 892, 300, "gray")
print("== yellow SOLID (>100 rows) ==")
solid_bands(yellow, 250, 511, 66, 892, 100, "yellow")

# vector bars: rows with several yellow/gray/pink cell clusters. Print row counts of
# "cell-ish" colors (saturated non-white non-red non-blue) to locate the three rows.
cellish = ((R > 200) & (G > 180) & (B < 140)) | ((G > 150) & (G - R > 30) & (G - B > 30)) | \
          ((R > 220) & (G > 150) & (G < 215) & (B > 150) & (B < 215))
prof = cellish[250:511, 66:892].sum(axis=1)
print("== cellish row profile (count>40 bands) ==")
runs, inr = [], False
for i, v in enumerate(prof):
    if v > 40 and not inr:
        s = i; inr = True
    elif v <= 40 and inr:
        runs.append((s + 250, i + 250)); inr = False
if inr: runs.append((s + 250, 511))
for a, b in runs:
    print(f"  cells band y {a}..{b-1} -> slide y {invy(a)}..{invy(b-1)} (h={b-a})")

# blue dots rows (0000CC dots) and green dots
bluedot = (B > 140) & (R < 80) & (G < 80)
greendot = (G > 150) & (G - R > 60) & (G - B > 60)
for name, m in (("blue dots", bluedot), ("green dots", greendot)):
    prof = m[250:511, 66:892].sum(axis=1)
    runs, inr = [], False
    for i, v in enumerate(prof):
        if v > 3 and not inr:
            s = i; inr = True
        elif v <= 3 and inr:
            if i - s >= 2:
                runs.append((s + 250, i + 250))
            inr = False
    print(f"== {name} bands ==")
    for a, b in runs:
        band = m[a:b, 66:892]
        cols = np.where(band.sum(axis=0) > 0)[0]
        # cluster columns
        cl, cur = [], [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] <= 3: cur.append(c)
            else: cl.append(cur); cur = [c]
        cl.append(cur)
        centers = [round((c[0] + c[-1]) / 2 + 66, 1) for c in cl]
        print(f"  y {a}..{b-1} n_clusters={len(cl)} centers={centers} -> slide y {invy(a)}..{invy(b-1)}")
