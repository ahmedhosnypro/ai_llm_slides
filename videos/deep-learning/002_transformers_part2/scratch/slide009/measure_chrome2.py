#!/usr/bin/env python3
"""Chrome landmarks v2 — softer thresholds, targeted regions."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# red-ish: r dominates g and b
red = (r > 110) & (r - g > 60) & (r - b > 60)

top_limit = 518  # black strip starts 519

# vertical border: scan columns in x 30..80 and x 880..930 for red runs
def col_red_run(x):
    col = red[:top_limit, x]
    return col.sum()

print('left region red-run per column x=30..90:')
print({x: int(col_red_run(x)) for x in range(30, 91) if col_red_run(x) > 30})
print('right region red-run per column x=870..930:')
print({x: int(col_red_run(x)) for x in range(870, 931) if col_red_run(x) > 30})

# top border: rows y=20..80 with wide red runs
print('top rows red-run y=20..90:')
print({y: int(red[y, :].sum()) for y in range(20, 91) if red[y, :].sum() > 200})

# bottom red border stroke: rows y=480..519
print('bottom rows red-run y=490..519:')
print({y: int(red[y, :].sum()) for y in range(490, 519) if red[y, :].sum() > 200})

# badge: yellow blob x 840..960 y 30..110
yellow = (r > 190) & (g > 190) & (b < 200) & (r - b > 20)
ys, xs = np.where(yellow[30:110, 840:960])
if len(xs):
    print('badge bbox: x', xs.min() + 840, '..', xs.max() + 840,
          ' y', ys.min() + 30, '..', ys.max() + 30,
          ' center', (xs.min() + xs.max()) / 2 + 840, (ys.min() + ys.max()) / 2 + 30)

# purple ring of badge: 6A5ACD-ish
purple = (abs(r - 106) < 60) & (abs(g - 90) < 50) & (abs(b - 205) < 60) & (b - r > 40) & (b - g > 40)
ys, xs = np.where(purple[30:110, 840:960])
if len(xs):
    print('badge ring bbox: x', xs.min() + 840, '..', xs.max() + 840,
          ' y', ys.min() + 30, '..', ys.max() + 30)
