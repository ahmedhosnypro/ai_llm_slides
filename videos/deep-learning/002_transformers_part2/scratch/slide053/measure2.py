#!/usr/bin/env python3
"""Color census + precise badge + border subpixel positions for slide_053.jpg."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# ---- precise border columns: weighted center of red cols
redmask = (a[:, :, 0] - (a[:, :, 1] + a[:, :, 2]) / 2) > 55
col_counts = redmask.sum(axis=0)
# left border: cols 50..70; right: 890..910
for zone, lo, hi in [('left', 50, 70), ('right', 890, 912)]:
    tot = col_counts[lo:hi].sum()
    cx = sum(x * col_counts[x] for x in range(lo, hi)) / max(tot, 1)
    print(f'{zone} border weighted col-center: {cx:.2f} (counts {[int(col_counts[x]) for x in range(lo,hi)]})')
row_counts = redmask.sum(axis=1)
for zone, lo, hi in [('top', 35, 55), ('bottom', 508, 522)]:
    tot = row_counts[lo:hi].sum()
    cy = sum(y * row_counts[y] for y in range(lo, hi)) / max(tot, 1)
    print(f'{zone} border weighted row-center: {cy:.2f} (counts {[int(row_counts[y]) for y in range(lo,hi)]})')

# ---- badge: yellow in top-right corner zone x>820, y<130
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
yellow = (r > 225) & (g > 225) & (b > 90) & (b < 215)
zone = np.zeros_like(yellow); zone[30:130, 820:930] = True
ys, xs = np.where(yellow & zone)
print('badge yellow bbox: x', xs.min(), '..', xs.max(), ' y', ys.min(), '..', ys.max(),
      ' center', (xs.min()+xs.max())/2, (ys.min()+ys.max())/2, ' n', len(xs))

# badge fill exact color (center row of badge)
cy = int((ys.min()+ys.max())/2); cx = int((xs.min()+xs.max())/2)
print('badge fill sample:', a[cy, cx], a[cy-5, cx-5])

# purple ring in badge zone
purple = (abs(r-106) < 55) & (abs(g-90) < 55) & (abs(b-205) < 55)
ys2, xs2 = np.where(purple & zone)
if len(xs2):
    print('badge ring bbox: x', xs2.min(), '..', xs2.max(), ' y', ys2.min(), '..', ys2.max(), ' n', len(xs2))

# ---- global color census (quantized) excluding chrome/panel
cnt = Counter()
q = (a // 24) * 24
for y in range(0, H, 2):
    for x in range(0, W, 2):
        cnt[tuple(q[y, x])] += 1
print('\ntop 30 quantized colors:')
for c, n in cnt.most_common(30):
    print(c, n)
