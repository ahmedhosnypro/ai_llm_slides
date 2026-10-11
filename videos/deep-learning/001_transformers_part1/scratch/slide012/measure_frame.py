#!/usr/bin/env python3
"""Measure slide_012.jpg (960x540, 1px=1pt) — the arXiv page-1 screenshot slide.

Prints: red border rect + stroke width, tan/pink highlight clusters, black rule,
ink bboxes (title/authors/abstract/watermark), and sampled core colors.
"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_012.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"frame {W}x{H}")

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# ---- red border (C00000 = 192,0,0) ----
red = (r > 130) & (g < 80) & (b < 80)
col_counts = red.sum(axis=0)
row_counts = red.sum(axis=1)
vcols = [x for x in range(W) if col_counts[x] > 200]
hrows = [y for y in range(H) if row_counts[y] > 200]
def runs(idx):
    out, start = [], None
    for i, v in enumerate(idx):
        if start is None:
            start = v
        elif v != idx[i-1] + 1:
            out.append((start, idx[i-1])); start = v
    if start is not None:
        out.append((start, idx[-1]))
    return out
print("red vertical col runs:", runs(vcols))
print("red horizontal row runs:", runs(hrows))

# ---- tan (F7D5A8 = 247,213,168) ----
tan = (np.abs(r - 247) < 25) & (np.abs(g - 213) < 30) & (np.abs(b - 168) < 35)
from scipy import ndimage
lab, n = ndimage.label(tan)
print("tan clusters:")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 50:
        continue
    print(f"  bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(ys)}")

# ---- pink (FF9BE8 = 255,155,232) ----
pink = (r > 235) & (g > 110) & (g < 200) & (b > 200)
lab, n = ndimage.label(pink)
print("pink clusters:")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 30:
        continue
    print(f"  bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(ys)}")

# ---- dark ink ----
lum = (r * 299 + g * 587 + b * 114) // 1000
dark = lum < 110
print("dark ink row profile (rows with >60 dark px):")
prof = [(y, int(dark[y].sum())) for y in range(H) if dark[y].sum() > 60]
# summarize into bands
bands = []
prev = None
for y, c in prof:
    if prev is None or y > prev[1] + 3:
        bands.append([y, y, c])
    else:
        bands[-1][1] = y
    prev = bands[-1]
for y0, y1, c in bands:
    xs = np.where(dark[y0:y1+1].any(axis=0))[0]
    print(f"  band y[{y0},{y1}] n={c} x[{xs.min()},{xs.max()}]")

# ---- gray watermark strip ----
grayish = (np.abs(r - g) < 18) & (np.abs(g - b) < 18) & (lum > 110) & (lum < 190)
wm_region = grayish[:, 90:150]
ys, xs = np.where(wm_region)
if len(ys):
    print(f"gray watermark strip x[{90+xs.min()},{90+xs.max()}] y[{ys.min()},{ys.max()}] n={len(ys)}")
