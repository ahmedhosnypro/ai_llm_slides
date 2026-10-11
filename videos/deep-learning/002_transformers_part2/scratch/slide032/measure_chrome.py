#!/usr/bin/env python3
"""Measure chrome landmarks + content ink in slide_032.jpg (960x540, 1px=1pt).

Step 1: find the four chrome border landmarks (gray panel E9E9E7 bounded by red
C00000 border) and fit the frame->slide mapping like slide_002 did.
"""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def mask_color(rlo, rhi, glo, ghi, blo, bhi):
    return (R >= rlo) & (R <= rhi) & (G >= glo) & (G <= ghi) & (B >= blo) & (B <= bhi)

red = mask_color(140, 230, 0, 70, 0, 90)          # C00000-ish border/title red
gray = mask_color(225, 240, 225, 240, 220, 235)   # E9E9E7 panel
white = mask_color(240, 256, 240, 256, 240, 256)

# panel-left: the leftmost column with a long vertical red run; panel-right similar.
col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
print("columns with >100 red px:", [int(c) for c in np.where(col_red > 100)[0]])
print("rows with >100 red px:", [int(r) for r in np.where(row_red > 100)[0]])

# vertical profile of red at candidate border columns
for c in [x for x in np.where(col_red > 100)[0]]:
    ys = np.where(red[:, c])[0]
    if len(ys):
        print(f"col {c}: red rows {ys.min()}..{ys.max()} n={len(ys)}")
for r in [x for x in np.where(row_red > 100)[0]]:
    xs = np.where(red[r, :])[0]
    if len(xs):
        print(f"row {r}: red cols {xs.min()}..{xs.max()} n={len(xs)}")

# gray panel extent: find columns/rows where gray dominates
col_gray = gray.sum(axis=0)
row_gray = gray.sum(axis=1)
gcols = np.where(col_gray > 200)[0]
grows = np.where(row_gray > 200)[0]
print("gray-dominant cols:", (int(gcols.min()), int(gcols.max())) if len(gcols) else None)
print("gray-dominant rows:", (int(grows.min()), int(grows.max())) if len(grows) else None)
