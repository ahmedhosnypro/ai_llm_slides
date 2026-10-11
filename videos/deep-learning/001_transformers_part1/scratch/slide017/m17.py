#!/usr/bin/env python3
"""Scan for feedback arrow + decoder bottom arrow + right-margin ink."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def scan(name, x0, x1, y0, y1, test, minrun=1):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1}")
    rows = {}
    for y in range(y0, y1+1):
        xs = [x for x in range(x0, x1+1) if test(*A[y, x])]
        if len(xs) >= minrun:
            rows[y] = (min(xs), max(xs), len(xs))
    for y in sorted(rows):
        x0r, x1r, n = rows[y]
        print(f"   y{y:3d}: x{x0r}..{x1r} n={n}")

# any strongly non-panel ink in right margin x850..920
nonpanel = lambda r, g, b: not (r > 190 and g > 230 and b > 195) and not (r > 240 and g > 240 and b > 240)
scan("right margin ink", 840, 920, 105, 530, nonpanel, 2)
# decoder bottom: red-ish
reddish = lambda r, g, b: r > 140 and g < 130 and b < 130 and r-g > 40
scan("dec bottom red", 738, 840, 470, 500, reddish, 1)
# what color is the feedback bits (sample)
for pt in [(869, 200), (873, 210), (875, 240), (871, 180), (866, 160), (890, 300), (895, 400)]:
    x, y = pt
    print(f"   sample ({x},{y}) = {tuple(int(v) for v in A[y, x])}")
