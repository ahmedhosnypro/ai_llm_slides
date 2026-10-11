#!/usr/bin/env python3
"""Forensics 11: last details."""
import numpy as np
from PIL import Image
from collections import Counter

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# callout fill: text-free strips
print("callout right strip x636-650 y117-136:", tuple(round(v,1) for v in im[117:136, 636:650].reshape(-1,3).mean(axis=0)))
print("callout left strip x465-478 y117-136:", tuple(round(v,1) for v in im[117:136, 465:478].reshape(-1,3).mean(axis=0)))
patch = im[118:135, 636:650].reshape(-1,3)
print("callout right strip modal:", Counter(tuple(int(v)//8*8 for v in p) for p in patch).most_common(2))

# hatch arrow raw rows
print("\n=== hatch raw row y483 x180-260 (every 2) ===")
print([f"{x}:{tuple(int(v) for v in im[483,x])}" for x in range(180, 261, 4)])
print("=== hatch raw row y483 x300-380 (every 4) ===")
print([f"{x}:{tuple(int(v) for v in im[483,x])}" for x in range(300, 381, 4)])

# hatch right end / arrowhead devmap
def devmap(xa, xb, ya, yb, label, thr=18):
    print(f"--- {label} ---")
    for y in range(ya, yb):
        row = []
        for x in range(xa, xb):
            px = im[y, x]
            d_panel = abs(int(px[0])-233)+abs(int(px[1])-233)+abs(int(px[2])-231)
            d_line = abs(int(px[0])-167)+abs(int(px[1])-175)+abs(int(px[2])-184)
            row.append("X" if min(d_panel, d_line) > thr else ".")
        print(f"{y:3d} " + "".join(row))
devmap(745, 815, 470, 500, "hatch right end + arrowhead")

# kernel label rows
red = (r > 140) & (g < 110) & (b < 110)
m = red[148:185, 50:150]
rowsum = m.sum(axis=1)
print("\nkernel label red rowsum y148-184:", {y+148: int(v) for y, v in enumerate(rowsum) if v > 0})
xs = np.where(m.sum(axis=0) > 0)[0] + 50
print(f"kernel label x-extent: {xs.min()}..{xs.max()}")

# banner: blue text looser mask bbox + band perpendicular width at two x
bl = (b - r > 30) & (b - g > 20) & (b > 90)
ys, xs = np.where(bl[330:510, 550:930])
print(f"\nbanner blue text bbox: x {xs.min()+550}..{xs.max()+550} y {ys.min()+330}..{ys.max()+330} n={len(xs)}")
# perpendicular width: sample along the band center line
import math
ang = math.atan2(366.5-489, 900-580)
print(f"band angle: {math.degrees(ang):.1f} deg")
for xx in (640, 760, 880):
    col = np.where(bl[330:510, xx])[0] + 330
    if len(col):
        print(f"  blue text at x={xx}: y {col.min()}..{col.max()} (n={len(col)})")

# FM2 cyan x-extent at row 325
row = im[325, 456:538]
cy = [x+456 for x, px in enumerate(row) if px[1]-px[0] > 25]
print(f"\nFM2 cyan x-extent at y325: {min(cy)}..{max(cy)}" if cy else "none")

# WV yellow x-extent at y190
row = im[190, 150:260]
ye = [x+150 for x, px in enumerate(row) if px[0] > 240 and px[1] > 240 and px[2] < 225]
print(f"WV yellow x-extent at y190: {min(ye)}..{max(ye)}" if ye else "none")

# FM1 peach x-extent at y390 (cells 13-15 region)
row = im[390, 300:400]
pe = [x+300 for x, px in enumerate(row) if px[0] > 235 and 195 < px[1] < 240 and 160 < px[2] < 215]
print(f"FM1 peach x-extent at y390: {min(pe)}..{max(pe)}" if pe else "none")

# seq label y-profile (gap check) x137-147
m2 = red[165:470, 137:148]
rowsum2 = m2.sum(axis=1)
ys2 = [y+165 for y, v in enumerate(rowsum2) if v > 0]
gaps = [(a, b2) for a, b2 in zip(ys2, ys2[1:]) if b2 - a > 4]
print(f"\nseq label ink rows {ys2[0]}..{ys2[-1]}, gaps>4: {gaps}")

# badge ring color sample (just outside yellow disc)
print("badge ring samples:", [tuple(int(v) for v in im[y, x]) for y, x in [(71, 874), (71, 912), (53, 893), (89, 893)]])

# title: leftmost/rightmost red + per-letter columns to sanity check center
m3 = red[55:80, 150:850]
cols = np.where(m3.sum(axis=0) > 0)[0] + 150
print(f"title cols {cols.min()}..{cols.max()} center {(cols.min()+cols.max())/2}")
