#!/usr/bin/env python3
"""Slide 038 forensics pass 13: slab bottom-right corner + in-slab 7, 1px."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

print("=== slab bottom region 1px: x246..335 y384..446 ===")
print("     " + ''.join(str((x // 10) % 10) for x in range(246, 336)))
for y in range(384, 447):
    row = ''
    for x in range(246, 336):
        rr, gg, bb = a[y, x]
        v = lum[y, x]
        if v < 100: c = '#'
        elif v < 165: c = 'd'
        elif rr > 195 and gg > 105: c = 'L'   # light tan strip
        elif rr > 145 and gg > 80 and bb < 120: c = 'o'  # main brown
        else: c = '.'
        row += c
    print(f"{y:3d} {row}")
