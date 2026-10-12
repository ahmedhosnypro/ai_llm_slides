#!/usr/bin/env python3
"""Slide 038 — m9: precise vertical bands (bars, bar outlines), column centers,
title word profile, navy block extent, caption, annotation rows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)
IN = lambda pt: round(pt / 72, 3)

def band_profile(mask, y0, y1, x0, x1, thresh, label, min_h=1):
    prof = mask[y0:y1, x0:x1].sum(axis=1)
    runs, inr = [], False
    for i, v in enumerate(prof):
        if v > thresh and not inr:
            s = i; inr = True
        elif v <= thresh and inr:
            if i - s >= min_h: runs.append((s + y0, i + y0))
            inr = False
    if inr and (y1 - s) >= min_h: runs.append((s + y0, y1))
    for a, b in runs:
        band = mask[a:b, x0:x1]
        colprof = band.sum(axis=0)
        cols = np.where(colprof > 0)[0]
        print(f"  {label}: y {a}..{b-1} (h={b-a}) x {cols.min()+x0}..{cols.max()+x0}"
              f" -> slide y {invy(a)}..{invy(b-1)} x {invx(cols.min()+x0)}..{invx(cols.max()+x0)}"
              f"  in: y {IN(invy(a))}..{IN(invy(b-1))} x {IN(invx(cols.min()+x0))}..{IN(invx(cols.max()+x0))}")

# non-white ink mask (anything clearly darker than the white panel)
ink = (R < 200) | (G < 200) | (B < 200)
print("== ink row profile inside diagram panel x 150..880 (bands h>=2, thresh 8) ==")
band_profile(ink, 251, 511, 150, 880, 8, "ink")

print("== per-column-1 profile: x 190..225 (column 1: labels/bars/circles) ==")
band_profile(ink, 251, 511, 190, 228, 1, "col1")

print("== title red word profile (columns with red ink, rows 66..95) ==")
red = (R > 120) & (G < 110) & (B < 110)
seg = red[66:95, 150:850]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 0 and not inr:
        s = i; inr = True
    elif v == 0 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 850))
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] <= 6: merged[-1] = (merged[-1][0], b)
    else: merged.append((a, b))
print("  word blobs:", [(a, b) for a, b in merged])

print("== navy block precise: rows 395..460, threshold >300 ==")
navy = (B > 100) & (R < 70) & (G < 70) & (B - R > 60)
band_profile(navy, 395, 460, 66, 892, 300, "navy")
seg = navy[405:445, 66:892]
colprof = seg.sum(axis=0)
cols = np.where(colprof > 30)[0]
print(f"  navy cols(>30/40rows): {cols.min()+66}..{cols.max()+66} -> slide x {invx(cols.min()+66)}..{invx(cols.max()+66)} in {IN(invx(cols.min()+66))}..{IN(invx(cols.max()+66))}")

print("== gray LayerNorm bar: rows 290..325, gray mask ==")
gray = (abs(R - G) < 14) & (abs(G - B) < 14) & (R > 185) & (R < 235)
band_profile(gray, 288, 328, 66, 892, 500, "graybar")
seg = gray[299:318, 66:892]
colprof = seg.sum(axis=0)
cols = np.where(colprof > 12)[0]
print(f"  gray cols(>12/19rows): {cols.min()+66}..{cols.max()+66} -> slide x {invx(cols.min()+66)}..{invx(cols.max()+66)} in {IN(invx(cols.min()+66))}..{IN(invx(cols.max()+66))}")

print("== top vector bars: dark outline rows x 190..320 ==")
dark = (R < 120) & (G < 120) & (B < 120)
band_profile(dark, 251, 300, 190, 320, 3, "dark-top")

print("== mid vector bars: dark outline rows x 190..320, y 340..410 ==")
band_profile(dark, 340, 412, 190, 320, 3, "dark-mid")

print("== X vector bars: dark outline rows x 190..320, y 450..500 ==")
band_profile(dark, 450, 500, 190, 320, 3, "dark-x")

print("== yellow cells (top/mid/x rows) x 190..870 ==")
yellow = (R > 200) & (G > 180) & (B < 140)
band_profile(yellow, 251, 511, 150, 880, 20, "yellow")

print("== caption band (yellow highlight) rows 490..512 ==")
band_profile(yellow, 488, 512, 150, 880, 30, "caption")

print("== 8 column centers from X-row blue labels (y 456..468) ==")
blue = (B > 130) & (R < 90) & (G < 90)
seg = blue[456:468, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 0 and not inr:
        s = i; inr = True
    elif v == 0 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] <= 4: merged[-1] = (merged[-1][0], b)
    else: merged.append((a, b))
print("  label blobs (frame x):", [(a, b) for a, b in merged])
print("  centers (slide pt):", [round(invx((a + b) / 2), 1) for a, b in merged])

print("== vector bar x extents (top row yellow cells, y 285..300) ==")
seg = yellow[283:300, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 2 and not inr:
        s = i; inr = True
    elif v <= 2 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  yellow cell blobs:", [(a, b) for a, b in runs])

print("== green up-arrows (between bar bottom and circles), x per column, y 320..336 ==")
green = (G > 120) & (G - R > 40) & (G - B > 40)
seg = green[320:336, 150:880]
colprof = seg.sum(axis=0)
cols = np.where(colprof > 0)[0]
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 0 and not inr:
        s = i; inr = True
    elif v == 0 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  green arrow blobs:", [(a, b) for a, b in runs])

print("== red arrows bar->toprow? darkred vertical strokes y 272..296 per column ==")
darkred = (R > 100) & (R < 220) & (G < 80) & (B < 80)
seg = darkred[272:296, 150:880]
colprof = seg.sum(axis=0)
runs, inr = [], False
for i, v in enumerate(colprof):
    if v > 2 and not inr:
        s = i; inr = True
    elif v <= 2 and inr:
        runs.append((s + 150, i + 150)); inr = False
if inr: runs.append((s + 150, 880))
print("  red stroke blobs y272-296:", [(a, b) for a, b in runs])

print("== blue arrows X->block (y 480..497) and block->Y' (y 375..398) per column ==")
for lo, hi, lab in ((478, 498, "X->blk"), (374, 400, "blk->Y")):
    seg = blue[lo:hi, 150:880]
    colprof = seg.sum(axis=0)
    runs, inr = [], False
    for i, v in enumerate(colprof):
        if v > 2 and not inr:
            s = i; inr = True
        elif v <= 2 and inr:
            runs.append((s + 150, i + 150)); inr = False
    if inr: runs.append((s + 150, 880))
    print(f"  {lab} blobs:", [(a, b) for a, b in runs])

print("== orange residual arrows: full profile x 150..880 y 284..500 ==")
orange = (R > 150) & (G > 60) & (G < 150) & (B < 80) & (R - B > 90)
band_profile(orange, 284, 500, 150, 880, 2, "orange")
