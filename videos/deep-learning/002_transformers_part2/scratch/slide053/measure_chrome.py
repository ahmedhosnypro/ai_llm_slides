#!/usr/bin/env python3
"""Measure chrome landmarks of slide_053.jpg (960x540) to derive frame->slide mapping.

Chrome landmarks (playlist law): gray panel E9E9E7 spanning x 42..918 px, y 45 px ->
slide bottom (in TRUE slide coords, 1px=1pt), thin red C00000 border on panel
left/right/top, badge circle d36px centered (893,71).
Finds: red vertical borders (left/right), red horizontal top border, badge yellow bbox.
"""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print('frame size', W, 'x', H)

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# red border: strong red, low green/blue
red = (r > 140) & (g < 90) & (b < 90)

# vertical red runs: count red pixels per column (excluding badge region rows for purity)
col_counts = red.sum(axis=0)
row_counts = red.sum(axis=1)

# candidate vertical border columns: many red pixels in a column
cand_cols = [x for x in range(W) if col_counts[x] > 200]
print('columns with >200 red px:', cand_cols)

# candidate horizontal border rows
cand_rows = [y for y in range(H) if row_counts[y] > 400]
print('rows with >400 red px:', cand_rows)

# restrict to left third / right third for panel borders
left_zone = [x for x in cand_cols if x < 300]
right_zone = [x for x in cand_cols if x > 660]
print('left border candidate cols:', left_zone)
print('right border candidate cols:', right_zone)

# top border rows: restrict to upper half, exclude title band later
top_zone = [y for y in cand_rows if y < 120]
print('top border candidate rows:', top_zone)

# badge: yellow fill FDFD96 (r>230,g>230,100<b<200)
yellow = (r > 225) & (g > 225) & (b > 90) & (b < 210)
ys, xs = np.where(yellow)
if len(xs):
    print('yellow bbox: x', xs.min(), '..', xs.max(), ' y', ys.min(), '..', ys.max(),
          ' count', len(xs))
    print('yellow center:', (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2)

# purple ring 6A5ACD (106,90,205)
purple = (abs(r - 106) < 45) & (abs(g - 90) < 45) & (abs(b - 205) < 45)
ys2, xs2 = np.where(purple)
if len(xs2):
    print('purple bbox: x', xs2.min(), '..', xs2.max(), ' y', ys2.min(), '..', ys2.max(),
          ' count', len(xs2))

# gray panel color check: sample a few points
for (px, py) in [(50, 300), (100, 100), (900, 500), (30, 30), (940, 520), (480, 530)]:
    print('sample', (px, py), a[py, px])
