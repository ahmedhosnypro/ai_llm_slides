#!/usr/bin/env python3
"""Scan encoder panel left region for faint gray strokes (curse of the diagonal line)."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

# gray stroke: low saturation, mid luminance, distinctly darker than peach (252,237,218)
def grayline(px):
    r, g, b = px
    if max(r,g,b) - min(r,g,b) > 25: return False      # not gray
    lum = (r+g+b)/3
    if lum > 225: return False                          # too light = peach-ish? peach lum=235
    if lum < 120: return False
    return True

print("gray-stroke pixels in x576..660, y110..530:")
rows = {}
for y in range(110, 531):
    xs = [x for x in range(576, 661) if grayline(A[y, x])]
    if len(xs) >= 1:
        rows[y] = (min(xs), max(xs), len(xs))
for y in sorted(rows):
    x0, x1, n = rows[y]
    if n >= 1:
        print(f"   y{y:3d}: x{x0}..{x1} n={n}")
