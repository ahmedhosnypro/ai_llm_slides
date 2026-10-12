#!/usr/bin/env python3
"""measure2_structure.py — slide 034 band structure: find content rows between chrome.
Scans for non-panel ink (panel E9E9E7 = 233,233,231), reports row bands and
column extents per band."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(float)
H, W, _ = img.shape
r, g, b = img[..., 0], img[..., 1], img[..., 2]

# panel background
panel = (np.abs(r - 233) < 14) & (np.abs(g - 233) < 14) & (np.abs(b - 231) < 16)
ink = ~panel
# exclude chrome strokes + letterbox
ink[:60, :930] = ink[:60, :930]  # keep (badge/title zone)
ink[:, :60] = False
ink[:, 898:] = False  # right stroke + badge zone x>=898
ink[514:, :] = False   # bottom stroke + letterbox
# white canvas above panel (y<45) is not ink either
white = (r > 248) & (g > 248) & (b > 248)
ink = ink & ~white

rowink = ink.sum(axis=1)
print("=== ROW BANDS (row: inkcount, threshold>8) ===")
bands = []
inb = False
for y in range(45, 514):
    if rowink[y] > 8 and not inb:
        start = y; inb = True
    elif rowink[y] <= 8 and inb:
        bands.append((start, y - 1)); inb = False
if inb: bands.append((start, 513))
# merge close bands (gap<=2)
merged = []
for b0 in bands:
    if merged and b0[0] - merged[-1][1] <= 2:
        merged[-1] = (merged[-1][0], b0[1])
    else:
        merged.append(list(b0))
for y0, y1 in merged:
    band = ink[y0:y1 + 1]
    xs = np.where(band.any(axis=0))[0]
    print(f"band y {y0}..{y1} (h={y1-y0+1})  x {xs.min()}..{xs.max()}  maxrow={rowink[y0:y1+1].max():.0f}")
