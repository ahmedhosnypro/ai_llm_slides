#!/usr/bin/env python3
"""Slide 038 forensics pass 12: last gaps — below slab diagonal, seam lines zoom."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

print("=== gap below slab bottom-right diagonal: x258..362 y392..448 ===")
for y in range(392, 449):
    row = ''
    for x in range(258, 363):
        v = lum[y, x]
        row += '#' if v < 110 else ('+' if v < 190 else ('o' if (r[y, x] > 150 and g[y, x] > 95 and b[y, x] < 115) else '.'))
    if '#' in row or '+' in row:
        print(f"{y:3d} {row}")

print()
print("=== seam zoom x444..458 y362..390 (1px) ===")
for y in range(362, 390):
    print(f"{y:3d} " + ''.join('#' if lum[y, x] < 110 else ('+' if lum[y, x] < 170 else '.') for x in range(444, 459)))

print()
print("=== seam zoom x503..517 y355..392 (1px) ===")
for y in range(355, 392):
    print(f"{y:3d} " + ''.join('#' if lum[y, x] < 110 else ('+' if lum[y, x] < 170 else '.') for x in range(503, 518)))

print()
print("=== top sliver check: x420..552 y330..342 lum<190 (7 above stack?) ===")
for y in range(330, 343):
    row = ''
    for x in range(420, 553):
        v = lum[y, x]
        row += '#' if v < 110 else ('+' if v < 190 else '.')
    if '#' in row or '+' in row:
        print(f"{y:3d} {row}")
