#!/usr/bin/env python3
"""Slide 038 — diagram interior: navy block, gray bar, vector bars, plus row, green container, dots."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)
P0, P1, P2, P3 = 65, 893, 249, 511  # diagram panel frame bounds (exclusive right/bottom: 893? check)

# masks
navy = (B > 100) & (R < 70) & (G < 70) & (B - R > 60)
gray = (abs(R - G) < 12) & (abs(G - B) < 12) & (R > 190) & (R < 230)
green = (G > 120) & (G - R > 40) & (G - B > 40)
orange = (R > 150) & (G > 60) & (G < 150) & (B < 80) & (R - B > 90)
darkred = (R > 100) & (R < 220) & (G < 80) & (B < 80)
yellow = (R > 200) & (G > 180) & (B < 120)
pink = (R > 220) & (G > 140) & (G < 210) & (B > 140) & (B < 210)

def bbox(mask, y0, y1, x0, x1, label):
    seg = mask[y0:y1, x0:x1]
    if seg.sum() < 10:
        print(f"  {label}: none ({seg.sum()} px)")
        return
    rows = np.where(seg.sum(axis=1) > 0)[0]
    cols = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  {label}: x {cols.min()+x0}..{cols.max()+x0} y {rows.min()+y0}..{rows.max()+y0}"
          f" (n={seg.sum()}) -> slide x {invx(cols.min()+x0)}..{invx(cols.max()+x0)}"
          f" y {invy(rows.min()+y0)}..{invy(rows.max()+y0)}")

print("== navy block ==")
bbox(navy, 250, 511, 66, 892, "navy")
print("== gray LayerNorm bar ==")
bbox(gray, 250, 511, 66, 892, "gray bar")
print("== green (container + arrows) row profile ==")
g = green[250:511, 66:892]
prof = g.sum(axis=1)
runs = []
inr = False
for i, v in enumerate(prof):
    if v > 3 and not inr:
        s = i; inr = True
    elif v <= 3 and inr:
        runs.append((s + 250, i + 250)); inr = False
if inr: runs.append((s + 250, 511))
for a, b in runs:
    band = green[a:b, 66:892]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"  green band y {a}..{b-1} x {cols.min()+66}..{cols.max()+66} -> slide y {invy(a)}..{invy(b-1)} x {invx(cols.min()+66)}..{invx(cols.max()+66)}")
print("== orange (residual arrows + label) row profile ==")
o = orange[250:511, 66:892]
prof = o.sum(axis=1)
runs = []
inr = False
for i, v in enumerate(prof):
    if v > 2 and not inr:
        s = i; inr = True
    elif v <= 2 and inr:
        runs.append((s + 250, i + 250)); inr = False
if inr: runs.append((s + 250, 511))
for a, b in runs:
    band = orange[a:b, 66:892]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"  orange band y {a}..{b-1} x {cols.min()+66}..{cols.max()+66} -> slide y {invy(a)}..{invy(b-1)} x {invx(cols.min()+66)}..{invx(cols.max()+66)}")
print("== darkred (plus circles, red arrows, labels) row profile ==")
d = darkred[250:511, 66:892]
prof = d.sum(axis=1)
runs = []
inr = False
for i, v in enumerate(prof):
    if v > 2 and not inr:
        s = i; inr = True
    elif v <= 2 and inr:
        runs.append((s + 250, i + 250)); inr = False
if inr: runs.append((s + 250, 511))
for a, b in runs:
    band = darkred[a:b, 66:892]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"  darkred band y {a}..{b-1} x {cols.min()+66}..{cols.max()+66} -> slide y {invy(a)}..{invy(b-1)} x {invx(cols.min()+66)}..{invx(cols.max()+66)}")
print("== yellow in panel (vector cells + caption highlight) ==")
bbox(yellow, 250, 511, 66, 892, "yellow")
print("== pink cells ==")
bbox(pink, 250, 511, 66, 892, "pink")
