#!/usr/bin/env python3
"""Probe pixel colors near expected chrome landmarks (slide_002 mapping guess)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
).convert("RGB")).astype(int)

def probe(tag, pts):
    print(tag)
    for y, x in pts:
        print("  (%3d,%3d) = %s" % (x, y, tuple(im[y, x])))

# columns 50..70 at a row in the middle of the top border area (y=200, outside content?)
# take y=300 (middle-left, should cross left border near col ~59)
row = 300
print("row y=300, cols 50..75:", [(x, tuple(im[row, x])) for x in range(50, 76)])
print()
print("row y=300, cols 890..915:", [(x, tuple(im[row, x])) for x in range(890, 916)])
print()
col = 480  # middle: top border near row 43, bottom near 516
print("col x=480, rows 36..52:", [(y, tuple(im[y, col])) for y in range(36, 53)])
print()
print("col x=480, rows 508..528:", [(y, tuple(im[y, col])) for y in range(508, 529)])
