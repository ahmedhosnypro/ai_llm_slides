#!/usr/bin/env python3
"""Fine measurement pass 2 for slide_042.jpg: box border exact position/color,
per-line ink detail, red/green math runs, title/subtitle."""
import numpy as np
from PIL import Image

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_042.jpg"
im = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W = im.shape[:2]

# --- box border hunt: strong red = r-g>60 and r-b>60 and r>110
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
strong_red = (r - g > 60) & (r - b > 60) & (r > 110)

print("== rows with >500 strong-red px (borders) ==")
for y in range(H):
    n = strong_red[y].sum()
    if n > 500:
        xs = np.where(strong_red[y])[0]
        print(f"  row {y}: x {xs.min()}..{xs.max()} n={n} color@400={tuple(im[y,400])} color@800={tuple(im[y,800])}")
print("== cols with >200 strong-red px ==")
for x in range(W):
    n = strong_red[:, x].sum()
    if n > 200:
        ys = np.where(strong_red[:, x])[0]
        print(f"  col {x}: y {ys.min()}..{ys.max()} n={n} color@300={tuple(im[300,x])}")

# --- border core color: median of row 197 strong-red pixels
row = im[197][strong_red[197]]
if len(row):
    print("row197 border median color:", np.median(row, axis=0))
col = im[:, 920][strong_red[:, 920]]
if len(col):
    print("col920 border median color:", np.median(col, axis=0))

# --- title bbox precise
title = strong_red[60:120]
ys, xs = np.where(title)
print(f"title: x {xs.min()}..{xs.max()} y {ys.min()+60}..{ys.max()+60}")
print("  title core color:", np.median(im[60:120][strong_red[60:120]], axis=0))

# --- subtitle lines
for y0, y1, lbl in [(140, 172, "sub line1"), (172, 195, "sub line2")]:
    m = strong_red[y0:y1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"{lbl}: x {xs.min()}..{xs.max()} y {ys.min()+y0}..{ys.max()+y0} core:",
              np.median(im[y0:y1][m], axis=0))

# --- blue text: b-r>60, b-g>40
blue = (b - r > 60) & (b - g > 40)
print("== blue line bands ==")
rows = np.where(blue[200:500].sum(axis=1) > 3)[0] + 200
bands = []
s = p = rows[0]
for i in rows[1:]:
    if i == p + 1: p = i
    else: bands.append((s, p)); s = p = i
bands.append((s, p))
for s0, e0 in bands:
    m = blue[s0:e0+1]
    xs = np.where(m.sum(axis=0) > 0)[0]
    print(f"  y {s0}..{e0}: x {xs.min()}..{xs.max()} core:", np.median(im[s0:e0+1][m], axis=0))

# --- red & green runs inside box lines (excluding borders x 70..74, 876..880)
inside = np.zeros((H, W), bool); inside[200:480, 78:872] = True
red_in = strong_red & inside
green = (g - r > 40) & (g - b > 40) & (g > 90) & inside
print("== red runs per line band ==")
for y0, y1 in [(230, 255), (280, 310), (340, 370), (395, 450)]:
    m = red_in[y0:y1]
    ys, xs = np.where(m)
    if len(ys):
        # cluster x
        xsu = np.unique(xs)
        cl = []; s = p = xsu[0]
        for i in xsu[1:]:
            if i <= p + 6: p = i
            else: cl.append((s, p)); s = p = i
        cl.append((s, p))
        print(f"  y{y0}-{y1}: red x-clusters {cl} core:", np.median(im[y0:y1][m], axis=0))
print("== green clusters per line band ==")
for y0, y1 in [(280, 310), (340, 370), (395, 450)]:
    m = green[y0:y1]
    ys, xs = np.where(m)
    if len(ys):
        xsu = np.unique(xs)
        cl = []; s = p = xsu[0]
        for i in xsu[1:]:
            if i <= p + 6: p = i
            else: cl.append((s, p)); s = p = i
        cl.append((s, p))
        print(f"  y{y0}-{y1}: green x-clusters {cl} core:", np.median(im[y0:y1][m], axis=0))
    else:
        print(f"  y{y0}-{y1}: no green")

# --- line 1 red quote-r detail
m = red_in[230:255]
ys, xs = np.where(m)
if len(ys):
    print("line1 red (quoted r): x", xs.min(), "..", xs.max(), "y", ys.min()+230, "..", ys.max()+230)
