#!/usr/bin/env python3
"""Profile rows/columns to find the red border lines and badge."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def redness(px):
    r, g, b = px
    return r - (g + b) / 2

# scan each column: max redness and count of redness>60
redmask = (a[:, :, 0] - (a[:, :, 1] + a[:, :, 2]) / 2) > 55
col_counts = redmask.sum(axis=0)
row_counts = redmask.sum(axis=1)

print('cols with >100 red px:', [x for x in range(W) if col_counts[x] > 100])
print()
print('rows with >200 red px:', [y for y in range(H) if row_counts[y] > 200])
