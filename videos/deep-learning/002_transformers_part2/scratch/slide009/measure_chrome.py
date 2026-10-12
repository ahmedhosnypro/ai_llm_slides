#!/usr/bin/env python3
"""Chrome landmark measurement for slide_009.jpg (960x540).

Finds: red border verticals/horizontal, bottom border stroke above the black
letterbox, black strip rows, badge yellow bbox. Derives frame->slide mapping.
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# red-ish ink (border / title): strong red, low green/blue
red = (r > 120) & (g < 90) & (b < 90)

# 1) black letterbox strip: rows that are mostly near-black across full width
darkrow = ((r < 60) & (g < 60) & (b < 60)).mean(axis=1)
strip_rows = [y for y in range(H) if darkrow[y] > 0.8]
print('black strip rows:', (min(strip_rows), max(strip_rows)) if strip_rows else None)

# 2) red border verticals: columns with long red runs above the strip
top_limit = min(strip_rows) if strip_rows else H
redcol = red[:top_limit, :].mean(axis=0)
cand = [x for x in range(W) if redcol[x] > 0.5]
print('red-heavy columns (>50% of height):', cand)

# 3) red border horizontal: rows with wide red runs
redrow = red[:top_limit, :].mean(axis=1)
candh = [y for y in range(top_limit) if redrow[y] > 0.5]
print('red-heavy rows (>50% of width):', candh)

# 4) badge: yellow blob (FDFD96-ish) top-right quadrant
yellow = (r > 200) & (g > 200) & (b < 190) & (b > 90)
ys, xs = np.where(yellow[:150, 700:])
if len(xs):
    print('badge yellow bbox (abs): x', xs.min() + 700, '..', xs.max() + 700,
          ' y', ys.min(), '..', ys.max(),
          ' center', ((xs.min() + xs.max()) / 2 + 700, (ys.min() + ys.max()) / 2))
