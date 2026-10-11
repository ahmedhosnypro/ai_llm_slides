#!/usr/bin/env python3
"""Find gray panel E9E9E7 edges + red border lines in slide_042.jpg (relaxed thresholds)."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)

# gray panel E9E9E7 ~ (233,233,231): near-neutral, mid-high
gray = (abs(a[:, :, 0] - 233) < 14) & (abs(a[:, :, 1] - 233) < 14) & (abs(a[:, :, 2] - 231) < 14)
white = (a[:, :, 0] > 248) & (a[:, :, 1] > 248) & (a[:, :, 2] > 246)

# panel row at y=300: scan x for white->gray transition
row = 300
xs_gray = np.nonzero(gray[row])[0]
print(f"row {row}: gray x {xs_gray.min()}..{xs_gray.max()}")
# columns where gray starts/ends
col_has_gray_mid = gray[100:500, :].sum(axis=0)
gcols = np.nonzero(col_has_gray_mid > 200)[0]
print(f"columns mostly gray: {gcols.min()}..{gcols.max()}, count {len(gcols)}")
# gaps in gcols (white label boxes inside panel)
d = np.diff(gcols)
gaps = [(gcols[i], gcols[i + 1]) for i in range(len(d)) if d[i] > 3]
print("gray-column gaps (white box columns):", gaps)

# rows where gray present across x 60..880
row_has_gray_mid = gray[:, 60:880].sum(axis=1)
grows = np.nonzero(row_has_gray_mid > 400)[0]
print(f"rows mostly gray: {grows.min()}..{grows.max()}")
d = np.diff(grows)
rgaps = [(grows[i], grows[i + 1]) for i in range(len(d)) if d[i] > 3]
print("gray-row gaps (white box rows):", rgaps)

# red-ish border: relaxed r>100 g<110 b<110 and dominant r
redish = (a[:, :, 0] > 100) & (a[:, :, 0] - a[:, :, 1] > 40) & (a[:, :, 0] - a[:, :, 2] > 40)
# vertical lines: for each candidate column in left band, count in y 60..510
for band_name, lo, hi in [("left", 30, 100), ("right", 860, 940)]:
    best = []
    for x in range(lo, hi):
        c = redish[60:510, x].sum()
        if c > 200: best.append((x, int(c)))
    print(f"{band_name} red columns:", best)
for band_name, lo, hi in [("top", 20, 70), ("bottom", 480, 540)]:
    best = []
    for y in range(lo, hi):
        c = redish[y, 100:860].sum()
        if c > 300: best.append((y, int(c)))
    print(f"{band_name} red rows:", best)

# blue content frame #0000CC-ish: b dominant, r low
blueish = (a[:, :, 2] > 100) & (a[:, :, 2] - a[:, :, 0] > 40) & (a[:, :, 2] - a[:, :, 1] > 40)
for band_name, lo, hi in [("left", 20, 120), ("right", 850, 950)]:
    best = []
    for x in range(lo, hi):
        c = blueish[60:520, x].sum()
        if c > 150: best.append((x, int(c)))
    print(f"{band_name} blue columns:", best)
for band_name, lo, hi in [("top", 80, 180), ("bottom", 430, 540)]:
    best = []
    for y in range(lo, hi):
        c = blueish[y, 100:860].sum()
        if c > 300: best.append((y, int(c)))
    print(f"{band_name} blue rows:", best)

# black letterbox strip at bottom: dark pixels
dark = (a[:, :, 0] < 60) & (a[:, :, 1] < 60) & (a[:, :, 2] < 60)
rows_dark = dark.sum(axis=1)
for y in range(H - 40, H):
    if rows_dark[y] > 100:
        print(f"dark row {y}: {rows_dark[y]}")
