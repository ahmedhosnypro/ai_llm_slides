#!/usr/bin/env python3
"""Verify right border col, top border row, and core ink colors for slide_035.jpg."""
from PIL import Image
import numpy as np

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_035.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
red = (R > 120) & (R - G > 60) & (R - B > 60)

# right border: scan cols 890..915 over rows 60..500
for x in range(890, 916):
    n = red[60:500, x].sum()
    if n > 50:
        ys = np.where(red[:, x])[0]
        print(f"col {x}: n={n} rows {ys.min()}..{ys.max()}")
# top border: scan rows 35..55 over cols 100..860
for y in range(35, 56):
    n = red[y, 100:860].sum()
    if n > 50:
        xs = np.where(red[y, :])[0]
        print(f"row {y}: n={n} cols {xs.min()}..{xs.max()}")

# core colors: title red core (densest red pixels), body blue core
ys, xs = np.where(red)
sel = (ys >= 156) & (ys <= 200) & (xs >= 172) & (xs <= 780)
print("title red core mean RGB:", a[ys[sel], xs[sel]].mean(axis=0).round(1),
      "median:", np.median(a[ys[sel], xs[sel]], axis=0))

blue = (B > 120) & (B - R > 60) & (B - G > 60)
ys, xs = np.where(blue)
sel2 = (ys >= 340) & (ys <= 442) & (xs >= 213) & (xs <= 576)
print("body blue core mean RGB:", a[ys[sel2], xs[sel2]].mean(axis=0).round(1),
      "median:", np.median(a[ys[sel2], xs[sel2]], axis=0))

# 'Adding' blue separately
sel3 = (ys >= 292) & (ys <= 324) & (xs >= 120) & (xs <= 233)
print("Adding blue core mean RGB:", a[ys[sel3], xs[sel3]].mean(axis=0).round(1),
      "median:", np.median(a[ys[sel3], xs[sel3]], axis=0))

# gray panel core + white margin sample
print("panel gray sample (300,300):", a[300, 300], " (600,200):", a[200, 600])
print("outer white sample (20,20):", a[20, 20], " (940,300):", a[300, 940])
