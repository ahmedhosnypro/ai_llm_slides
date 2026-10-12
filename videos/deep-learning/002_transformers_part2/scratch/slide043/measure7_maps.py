#!/usr/bin/env python3
"""Slide 043 — stack color-band maps, callout structure, arrow zone scans."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R < 100 and G < 100 and B < 140: return 'N'      # navy/dark
    if R > 150 and G < 90 and B > 150: return 'M'       # magenta
    if R > 180 and G > 90 and B < 90: return 'O'        # orange
    if R > 200 and G > 200 and B < 130: return 'Y'      # yellow
    if G > 120 and G - R > 30 and G - B > 30: return 'g' # green
    if B > 150 and B - R > 25 and G > 110: return 'L'   # light blue
    if R > 245 and G > 245 and 200 < B < 248: return 'C' # cream
    if R > 245 and G > 245 and B >= 248: return 'W'     # white
    if abs(R - 231) < 8 and abs(G - 233) < 8: return '.'  # gray panel
    if R > 140 and R - G > 60 and R - B > 60 and G < B + 35: return 'R'  # red
    return '?'

print('=== LEFT STACK map (x100..340 step 4, y95..350 step 5) ===')
hdr = '     ' + ''.join(str((100 + i * 4) // 100 % 10) for i in range(61))
print(hdr)
for y in range(95, 351, 5):
    print(f'y{y:3d} ' + ''.join(cls(a[y, 100 + i * 4]) for i in range(61)))

print('=== RIGHT STACK map (x590..940 step 4, y95..350 step 5) ===')
print(hdr)
for y in range(95, 351, 5):
    print(f'y{y:3d} ' + ''.join(cls(a[y, 590 + i * 4]) for i in range(89)))

print('=== CALLOUT zone map (x320..700 step 4, y160..340 step 4) ===')
print('     ' + ''.join(str((320 + i * 4) // 100 % 10) for i in range(96)))
for y in range(160, 341, 4):
    print(f'y{y:3d} ' + ''.join(cls(a[y, 320 + i * 4]) for i in range(96)))
