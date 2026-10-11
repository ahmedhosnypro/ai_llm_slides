#!/usr/bin/env python3
"""Measure the bottleneck callout box: fill, border, corner radius, text lines, underlines, connector."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

# --- find the light-blue box: fill core color ---
win = b[150:300, 30:500]
# light-blue-ish: B > R and B > G significantly, high brightness
r, g, bl = win[:, :, 0], win[:, :, 1], win[:, :, 2]
lb = (bl > r + 25) & (bl > g + 15) & (bl > 180)
ys, xs = np.nonzero(lb)
print("light-blue px:", len(ys))
if len(ys):
    print("box bbox (frame coords): x", 30 + xs.min(), "..", 30 + xs.max(), " y", 150 + ys.min(), "..", 150 + ys.max())
    # fill color mode
    cols = win[lb]
    print("fill mean color:", cols.mean(axis=0).round(1), " median:", np.median(cols, axis=0))

# --- border: dark blue stroke around the box ---
# scan row through box center for dark-blue pixels
cy = 220
row = b[cy, 30:500]
db = np.nonzero((row[:, 2] > row[:, 0] + 30) & (row[:, 2] < 200))[0]
print(f"\nrow y={cy} dark-blue x:", (30 + db).tolist()[:30])
cx_ = 240
col = b[150:300, cx_]
dbv = np.nonzero((col[:, 2] > col[:, 0] + 30) & (col[:, 2] < 200))[0]
print(f"col x={cx_} dark-blue y:", (150 + dbv).tolist()[:30])

# --- text lines inside the box: dark ink rows ---
x0, x1, y0, y1 = 50, 470, 160, 280
sub = b[y0:y1, x0:x1]
ink = sub.sum(axis=2) < 330  # dark blue text/border ink
rows = ink.sum(axis=1)
bands = []
cur = None
for i, v in enumerate(rows):
    if v > 0:
        if cur and (y0 + i) - cur[1] <= 2:
            cur[1] = y0 + i; cur[2] += int(v)
        else:
            if cur: bands.append(tuple(cur))
            cur = [y0 + i, y0 + i, int(v)]
if cur: bands.append(tuple(cur))
print("\nink row-bands in box (y0,y1,px):")
for bd in bands:
    m = ink[bd[0] - y0:bd[1] - y0 + 1]
    xs_ = np.nonzero(m.sum(axis=0) > 0)[0]
    print(f"  y {bd[0]}..{bd[1]} h={bd[1]-bd[0]+1} px={bd[2]} x {x0+xs_.min()}..{x0+xs_.max()}")

# --- text color core (darkest) ---
lum = sub.sum(axis=2)
iy, ix = np.unravel_index(np.argmin(lum), lum.shape)
print("\ntext darkest color:", sub[iy, ix])

# --- connector from box right edge toward ctx arrow: dark ink right of box, y 180..270 ---
# first find box right edge precisely
print("\nconnector scan: dark-blue/dark ink in x 440..500, y 170..280")
for yy in range(170, 281, 4):
    row = b[yy, 440:505]
    dk = np.nonzero(row.sum(axis=1) < 400)[0]
    if len(dk):
        print(f"  y={yy}: x {(440+dk).tolist()}")
