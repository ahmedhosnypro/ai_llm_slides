#!/usr/bin/env python3
"""Slide 043 refined chrome: strict border mask, tight badge window, red-text title mask
(g<b+35 excludes orange cube faces), callout/bottom-box borders."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# strict border red (042-comparable)
red = (r > 130) & (r - g > 60) & (r - b > 60)
band = red[140:380, :]
colfrac = band.mean(axis=0)
print("STRICT cols>0.9:", [(x, round(colfrac[x], 3)) for x in range(W) if colfrac[x] > 0.9])
mid = red[:, 250:750]
rowfrac = mid.mean(axis=1)
print("STRICT rows>0.9:", [(y, round(rowfrac[y], 3)) for y in range(H) if rowfrac[y] > 0.9])

# badge: scan tight window x 840..930, y 40..100 for yellow; print per-row extents
yel = (r > 200) & (g > 200) & (b < 180)
print("badge yellow rows (y40..100, x840..930):")
for y in range(40, 101):
    xs = [x for x in range(840, 931) if yel[y, x]]
    if xs:
        print(" y", y, "x", xs[0], "..", xs[-1], "n", len(xs))

# title: red-text mask (excludes orange: g<b+35)
tred = (r > 150) & (r - g > 60) & (r - b > 60) & (g < b + 35)
t = tred[45:135, 150:820]
tf = t.mean(axis=1)
rows = [(45 + i, round(v, 3)) for i, v in enumerate(tf) if v > 0.02]
print("TITLE rows>0.02:", rows)
cols = t.mean(axis=0)
nz = [150 + i for i, v in enumerate(cols) if v > 0.02]
print("TITLE ink x-extent:", (nz[0], nz[-1]) if nz else None)

# callout box border (red rect around cream box, center of slide): scan x 300..660, y 150..300
# cream fill: r>240,g>240,b<220
cream = (r > 235) & (g > 235) & (b > 190) & (b < 235)
ys, xs = np.where(cream[140:300, 300:680])
print("CREAM bbox x", xs.min() + 300, "..", xs.max() + 300, " y", ys.min() + 140, "..", ys.max() + 140)

# bottom green-bordered box: green border
grn = (g > 120) & (g - r > 60) & (g - b > 60)
ys, xs = np.where(grn[350:540, :])
print("GREEN border bbox x", xs.min(), "..", xs.max(), " y", ys.min() + 350, "..", ys.max() + 350)
