#!/usr/bin/env python3
"""Fine profile of border strokes, badge, dark strip extent, title ink."""
from PIL import Image
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_058.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[..., 0], im[..., 1], im[..., 2]

red = (R > 110) & (R - G > 50) & (R - B > 40)
print("red px total:", red.sum())

colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
# columns/rows with elevated red counts
print("cols>40:", [(x, int(colcount[x])) for x in range(W) if colcount[x] > 40])
print("rows>40:", [(y, int(rowcount[y])) for y in range(H) if rowcount[y] > 40])

# dark strip x-extent
dark = (R < 60) & (G < 60) & (B < 60)
drow = dark[525]
xs = np.nonzero(drow)[0]
print("dark row 525 x-extent:", xs.min(), xs.max(), "n", len(xs))
# check rows just above 518
for y in [514, 515, 516, 517, 518]:
    print("row", y, "dark frac", round(dark[y].mean(), 3), "red frac", round(red[y].mean(), 3),
          "mean RGB", im[y][dark[y]].mean(axis=0).round(1) if dark[y].sum() else "-")

# gray panel extent: E9E9E7-ish (sampled loosely)
gray = (abs(R - 0xE9) < 14) & (abs(G - 0xE9) < 14) & (abs(B - 0xE7) < 16)
grow = gray[300]
xs = np.nonzero(grow)[0]
print("gray row 300 x-extent:", xs.min(), xs.max())
gcol = gray[:, 480]
ys = np.nonzero(gcol)[0]
print("gray col 480 y-extent:", ys.min(), ys.max())

# title ink: dark red text — sample central band
title = (R > 120) & (R - G > 40) & (R - B > 30)
band = title[180:340, :]
ys, xs = np.nonzero(band)
if len(xs):
    print("title ink bbox y", ys.min() + 180, ys.max() + 180, "x", xs.min(), xs.max(), "n", len(xs))
    # row profile to split the two lines
    rr = band.sum(axis=1)
    runs = []
    inrun = False
    for i, v in enumerate(rr):
        if v > 2 and not inrun:
            start = i; inrun = True
        elif v <= 2 and inrun:
            runs.append((start + 180, i - 1 + 180)); inrun = False
    if inrun:
        runs.append((start + 180, len(rr) - 1 + 180))
    print("title line runs (y):", runs)
    for (a, b) in runs:
        sub = band[a - 180:b - 180 + 1]
        yy, xx = np.nonzero(sub)
        print(f"  line y {a}..{b} x {xx.min()}..{xx.max()} cx {(xx.min()+xx.max())/2}")
