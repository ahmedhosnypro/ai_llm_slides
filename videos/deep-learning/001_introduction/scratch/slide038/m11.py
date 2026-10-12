#!/usr/bin/env python3
"""Slide 038 forensics pass 11: dark-mark hunt on stack, bottom 7, right 7, 735 weights bbox."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

print("=== stack region dark marks: lum<110 pixels (x392..560 y330..405), printed as map ===")
for y in range(330, 406, 2):
    row = ''
    for x in range(392, 561, 2):
        row += '#' if lum[y, x] < 110 else ('+' if lum[y, x] < 150 else '.')
    print(f"{y:3d} {row}")

print()
print("=== bottom-right of slab: x300..390 y415..470 (any ink lum<190) ===")
for y in range(415, 470, 2):
    row = ''
    for x in range(300, 391, 2):
        row += '#' if lum[y, x] < 110 else ('+' if lum[y, x] < 190 else '.')
    print(f"{y:3d} {row}")

print()
print("=== right of purple + below: x545..615 y300..470 (ink lum<190, excluding = region y360..376) ===")
for y in range(300, 470, 2):
    if 358 <= y <= 378: continue
    row = ''
    for x in range(545, 616, 2):
        row += '#' if lum[y, x] < 110 else ('+' if lum[y, x] < 190 else '.')
    if '+' in row or '#' in row:
        print(f"{y:3d} {row}")

print()
print("=== '735 weights' text: x360..560 y462..500 (lum<190) ===")
for y in range(462, 500, 2):
    row = ''
    for x in range(360, 561, 2):
        row += '#' if lum[y, x] < 110 else ('+' if lum[y, x] < 190 else '.')
    print(f"{y:3d} {row}")

print()
print("=== 'RGB' text bbox precise: x290..370 y262..292 ===")
for y in range(262, 293):
    row = ''
    for x in range(290, 371):
        row += '#' if lum[y, x] < 110 else ('+' if lum[y, x] < 190 else '.')
    print(f"{y:3d} {row}")
