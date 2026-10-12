#!/usr/bin/env python3
"""m5_bands.py — full-width row classification of slide_047.jpg (x 135..890)."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

X0, X1 = 135, 890
prev = None
print('y: [tan][barOrange][plum][paleY][darkLine][white]  (counts of 755)')
for y in range(40, 520):
    r, g, b = R[y, X0:X1], G[y, X0:X1], B[y, X0:X1]
    n = X1 - X0
    tan = int(((abs(r - 237) < 25) & (abs(g - 176) < 28) & (abs(b - 121) < 34)).sum())
    barO = int(((r > 205) & (g > 115) & (g < 205) & (b < 95)).sum())
    plum = int(((r > 100) & (r < 165) & (g < 90) & (b > 55) & (b < 135)).sum())
    paleY = int(((r > 235) & (g > 225) & (b > 150) & (b < 235) & (abs(r - g) < 30)).sum())
    dark = int(((r + g + b) < 330).sum())
    white = int(((r > 240) & (g > 240) & (b > 240)).sum())
    sig = (tan // 40, barO // 40, plum // 40, paleY // 40, dark // 40, white // 40)
    if sig != prev:
        print(f'y={y}: tan={tan} barO={barO} plum={plum} paleY={paleY} dark={dark} white={white}')
        prev = sig
