#!/usr/bin/env python3
"""v6: body-text core colors, callout geometry detail, vector zone full profiles."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def core_colors(y0, y1, x0, x1, label, sumthr=430):
    band = a[y0:y1, x0:x1]
    dark = band.sum(axis=2) < sumthr
    ys, xs = np.where(dark)
    if not len(ys):
        print(f"{label}: no dark px"); return
    cc = Counter(map(tuple, band[ys, xs]))
    print(f"{label}: n={len(ys)} top: {cc.most_common(5)}")

# body text cores
core_colors(292, 310, 103, 200, "L2 'Values are' (blue?)")
core_colors(227, 245, 87, 300, "L1 lead-in (blue italic?)")
core_colors(324, 342, 185, 550, "L3 plain blue part")
core_colors(452, 471, 102, 358, "L6 blue 'Position Vector Length = 2'")
core_colors(452, 471, 365, 850, "L6 red warning")
core_colors(292, 310, 362, 520, "L2 green (bounded values)")
core_colors(135, 165, 220, 860, "callout text")
core_colors(128, 170, 110, 170, "vector inner text")

# callout fill column profile (rows 115..178)
fill = (a[:, :, 0] > 200) & (a[:, :, 1] > 200) & (a[:, :, 2] > 150) & (a[:, :, 2] < 235) & (a[:, :, 0] - a[:, :, 2] > 20)
fz = fill[115:179]
fc = fz.sum(axis=0)
runs = []
inr = False
for c in range(960):
    if fc[c] > 20 and not inr: inr, r0 = True, c
    elif fc[c] <= 20 and inr:
        inr = False
        if c - r0 > 4: runs.append((r0, c - 1))
if inr: runs.append((r0, 959))
print("\ncallout fill col runs (rows 115..178):", runs)

# callout fill row profile within its col range
if runs:
    c0, c1 = runs[0][0], runs[-1][1]
    fr = fill[:, c0:c1 + 1].sum(axis=1)
    rrows = np.where(fr > 100)[0]
    print("callout fill rows>100:", (int(rrows.min()), int(rrows.max())) if len(rrows) else None)
    print("fill row profile 105..195:", [(r, int(fr[r])) for r in range(105, 196, 3)])

# vector zone: loose red row/col profiles
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
redl = (R - G > 30) & (R - B > 30) & (R > 130)
vz = redl[95:206, 60:216]
rr = vz.sum(axis=1); cc = vz.sum(axis=0)
print("\nvector loose-red rows (count>3):", [(95 + i, int(rr[i])) for i in np.where(rr > 3)[0]])
print("vector loose-red cols (count>3):", [(60 + i, int(cc[i])) for i in np.where(cc > 3)[0]])

# white box extent recheck: white-ish rows/cols in zone
wm = (R > 235) & (G > 235) & (B > 235)
wz = wm[95:206, 60:216]
wr = wz.sum(axis=1); wc = wz.sum(axis=0)
print("white rows>10:", [(95 + i, int(wr[i])) for i in np.where(wr > 10)[0]][:4], "...",
      [(95 + i, int(wr[i])) for i in np.where(wr > 10)[0]][-4:])
print("white cols>10:", [(60 + i, int(wc[i])) for i in np.where(wc > 10)[0]][:4], "...",
      [(60 + i, int(wc[i])) for i in np.where(wc > 10)[0]][-4:])

# navy border of main panel: strict scan rows 200..215 and 500..515
navy = (R < 100) & (G < 100) & (B > 85) & (B < 175)
print("\nnavy rows 200..215:", [(r, int(navy[r, 70:890].sum())) for r in range(200, 216)])
print("navy rows 500..515:", [(r, int(navy[r, 70:890].sum())) for r in range(500, 516)])
print("navy cols 70..90:", [(c, int(navy[210:510, c].sum())) for c in range(70, 91, 2)])
print("navy cols 870..890:", [(c, int(navy[210:510, c].sum())) for c in range(870, 891, 2)])
cc2 = Counter(map(tuple, a[209:212, 300:600][navy[209:212, 300:600]]))
print("navy border top core colors:", cc2.most_common(4))
