#!/usr/bin/env python3
"""Forensics round 2 for slide_006: borders, 12th bullet, underlines, font solving."""
from PIL import Image
import numpy as np, collections

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# ---- 1. red-ish mask, looser ----
red = (R > 110) & (G < 110) & (B < 110) & (R - G > 60) & (R - B > 60)
rr = red.sum(axis=1)
print("-- red rows (count>50) --")
for y in range(H):
    if rr[y] > 50:
        xs = np.nonzero(red[y])[0]
        print(f"row {y}: n={rr[y]} x {xs.min()}..{xs.max()}")
rc = red.sum(axis=0)
print("-- red cols (count>50) --")
for x in range(W):
    if rc[x] > 50:
        ys = np.nonzero(red[:, x])[0]
        print(f"col {x}: n={rc[x]} y {ys.min()}..{ys.max()}")

# ---- 2. strip scan y=270 from x=40..120 and x=830..925 ----
print("\n-- strip y=270 --")
row = a[270]
for x in list(range(40, 100, 4)) + list(range(832, 925, 4)):
    print(f"  x={x}: {tuple(row[x])}")

# ---- 3. 12th bullet region: all ink y 480..516, x 45..915 ----
print("\n-- 12th bullet region --")
zone = a[478:516, 45:915]
dark = (zone[..., 0] < 150) & (zone[..., 1] < 150) & (zone[..., 2] < 150)
ys, xs = np.nonzero(dark)
if len(ys):
    print(f"dark ink: n={len(ys)} y {ys.min()+478}..{ys.max()+478} x {xs.min()+45}..{xs.max()+45}")
    for yy in range(478, 516):
        cnt = dark[yy - 478].sum()
        if cnt > 2:
            xr = np.nonzero(dark[yy - 478])[0]
            print(f"  row {yy}: n={cnt} x {xr.min()+45}..{xr.max()+45}")
# blue check in same region
blue = (zone[..., 2] > 110) & (zone[..., 0] < 110) & (zone[..., 1] < 110)
print("blue px in region:", int(blue.sum()))

# ---- 4. header per-line extents + underline rows ----
dark_full = (R < 120) & (G < 120) & (B < 120)
print("\n-- header lines --")
for (y0, y1) in [(138, 163), (164, 190)]:
    m = dark_full[y0:y1, 45:915]
    rr_ = m.sum(axis=1)
    for i, y in enumerate(range(y0, y1)):
        if rr_[i] > 3:
            xr = np.nonzero(m[i])[0]
            print(f"  row {y}: n={rr_[i]} x {xr.min()+45}..{xr.max()+45}")

# ---- 5. dot geometry precise ----
print("\n-- dots precise --")
dk = (R < 130) & (G < 130) & (B < 130)
for cy in range(195, 500):
    seg = dk[cy, 170:195]
    if seg.sum() >= 2:
        xr = np.nonzero(seg)[0]
        print(f"  row {cy}: x {xr.min()+170}..{xr.max()+170} n={seg.sum()}")

# ---- 6. title stroke profile (serif check): horizontal run-length stats ----
print("\n-- title row-run stats (baseline zone) --")
red_t = (R > 140) & (G < 90) & (B < 90)
for y in [85, 90, 95, 100, 105, 110, 112, 113, 114, 115, 116, 118, 120, 123]:
    m = red_t[y, 140:840]
    n = m.sum()
    # longest run
    best = cur = 0
    for v in m:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    print(f"  y={y}: n={n} longest_run={best}")

# ---- 7. ink row profile title: find baseline (bulk dropoff) ----
tt = red_t[46:130, 45:915].sum(axis=1)
print("title rows:", [(y+46, int(tt[y])) for y in range(len(tt)) if tt[y] > 5])
