#!/usr/bin/env python3
"""Measure landmarks on the 300dpi page-1 raster (2550x3300)."""
from PIL import Image
import numpy as np

PG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide012/page300-01.png"
im = Image.open(PG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"page {W}x{H}")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = (r * 299 + g * 587 + b * 114) // 1000
dark = lum < 128

# ink bands (rows with >30 dark px), page-wide
prof = [(y, int(dark[y].sum())) for y in range(H) if dark[y].sum() > 30]
bands = []
for y, c in prof:
    if bands and y <= bands[-1][1] + 6:
        bands[-1][1] = y; bands[-1][2] = max(bands[-1][2], c)
    else:
        bands.append([y, y, c])
print("== ink bands ==")
for y0, y1, c in bands:
    seg = dark[y0:y1+1]
    xs = np.where(seg.any(axis=0))[0]
    print(f"  y[{y0},{y1}] h={y1-y0+1} maxn={c} x[{xs.min()},{xs.max()}]")

# watermark: gray-ish (low sat) text on left margin
sat = np.max(a, axis=2) - np.min(a, axis=2)
wm = (sat < 60) & (lum > 90) & (lum < 200)
wm[:, 200:] = False
ys, xs = np.where(wm)
if len(ys):
    print(f"== watermark bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(ys)}")
    wrow = wm.sum(axis=1)
    rows = [y for y in range(H) if wrow[y] > 3]
    print(f"   wm text rows span y[{rows[0]},{rows[-1]}]")

# title bbox precise: region y 200..600
treg = dark[200:700, :]
ys, xs = np.where(treg)
print(f"title region ink bbox x[{xs.min()},{xs.max()}] y[{200+ys.min()},{200+ys.max()}]")
