#!/usr/bin/env python3
"""measure2: scanline histograms + raw color samples for slide_022.jpg"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def near(hexcol, tol):
    r, g, b = int(hexcol[0:2], 16), int(hexcol[2:4], 16), int(hexcol[4:6], 16)
    d = np.abs(a[:, :, 0] - r) + np.abs(a[:, :, 1] - g) + np.abs(a[:, :, 2] - b)
    return d <= tol

blue = near("0000CC", 150)
print("=== BLUE col runs (cols with >=20 blue px) ===")
colcnt = blue.sum(axis=0)
runs = []
inr = False
for x in range(W):
    if colcnt[x] >= 20 and not inr:
        s = x; inr = True
    elif colcnt[x] < 20 and inr:
        runs.append((s, x - 1, int(colcnt[s:x].max()))); inr = False
if inr: runs.append((s, W - 1, int(colcnt[s:].max())))
print(runs)
print("=== BLUE row runs (rows with >=20 blue px) ===")
rowcnt = blue.sum(axis=1)
runs = []
inr = False
for y in range(H):
    if rowcnt[y] >= 20 and not inr:
        s = y; inr = True
    elif rowcnt[y] < 20 and inr:
        runs.append((s, y - 1, int(rowcnt[s:y].max()))); inr = False
if inr: runs.append((s, H - 1, int(rowcnt[s:].max())))
print(runs)

# what are the actual stroke colors? sample left panel OUTPUT container border area
# left panel: blue spans up to ~x470? sample a horizontal line mid-panel
print("\n=== raw pixel samples (row y=300) x=100..480 every 4px, non-background ===")
prev = None
for x in range(100, 485, 1):
    px = tuple(a[300, x])
    if abs(px[0]-233)+abs(px[1]-233)+abs(px[2]-231) > 90:  # not panel gray E9E9E7
        if prev is None or x - prev > 3:
            print(f"  x={x}: {px}")
        prev = x
