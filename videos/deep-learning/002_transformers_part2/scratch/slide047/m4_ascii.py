#!/usr/bin/env python3
"""m4_ascii.py — ASCII color map of slide_047.jpg (each char = 8x6 px block)."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]

BX, BY = 8, 6  # block size -> 120 cols x 90 rows
def classify_block(y0, x0):
    blk = A[y0:y0+BY, x0:x0+BX].reshape(-1, 3)
    r = blk[:, 0].mean(); g = blk[:, 1].mean(); b = blk[:, 2].mean()
    sd = blk.std(axis=0).mean()
    if r > 244 and g > 244 and b > 244: return '.'
    if r < 50 and g < 50 and b < 50: return 'K'          # black
    if r > 140 and g < 95 and b < 95 and sd > 20: return 'R'   # red ink/text
    if r > 150 and g < 100 and b < 100: return 'r'       # dark red fill
    if r > 195 and 120 < g < 205 and b < 145: return 'o' # orange (LN bar / container)
    if 200 < r < 250 and 140 < g < 200 and 80 < b < 150: return 't'  # tan container fill
    if 100 < r < 165 and g < 85 and 60 < b < 135: return 'P'   # plum MHA
    if 85 < r < 145 and g < 80 and 125 < b < 195: return 'U'   # purple
    if r > 222 and g > 200 and b > 222: return 'l'       # lavender/pink pale
    if r > 238 and g > 236 and 195 < b < 240: return 'y' # pale yellow
    if r < 130 and g > 115 and b < 130: return 'g'       # green
    if r < 100 and g < 100 and b > 100: return 'b'       # blue
    if r > 180 and g > 140 and b < 120: return 'Y'       # yellow
    if abs(r-g) < 30 and abs(g-b) < 30 and 90 < r < 200: return 'w'  # gray
    return '?'

print('    ' + ''.join(str((x0*BX)//100 % 10) for x0 in range(W//BX)))
for y0 in range(0, H - BY + 1, BY):
    row = ''.join(classify_block(y0, x0) for x0 in range(0, W - BX + 1, BX))
    print(f'{y0:3d} {row}')
