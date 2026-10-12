#!/usr/bin/env python3
"""m4_core.py — comprehensive measurement of slide_047.jpg: chrome landmarks, container,
rows, cells, LN bars, MHA bar, FFN, plus discs, boxes, badge."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def runs(m, min_len=1):
    out = []; i = 0; n = len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[i]: j += 1
            if j - i >= min_len: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# ---- 1) chrome landmarks: red border (dark red C00000-ish) ----
# probe columns 50..70 and 890..912 across rows 44..514: count reddish px
redm = (R > 110) & (G < 90) & (B < 90)
print('== chrome: left border candidates (col, redcount rows 44..514) ==')
for x in range(50, 72):
    c = int(redm[44:515, x].sum())
    if c > 30: print(f'  x={x}: {c}')
print('== chrome: right border candidates ==')
for x in range(892, 912):
    c = int(redm[44:515, x].sum())
    if c > 30: print(f'  x={x}: {c}')
print('== chrome: top border rows (y, redcount cols 60..898) ==')
for y in range(38, 52):
    c = int(redm[y, 60:899].sum())
    if c > 30: print(f'  y={y}: {c}')
print('== chrome: bottom stroke rows ==')
for y in range(510, 522):
    c = int(redm[y, 60:899].sum())
    print(f'  y={y}: {c}')

# ---- 2) tan container precise bounds + border color ----
tan = (abs(R - 237) < 22) & (abs(G - 176) < 25) & (abs(B - 121) < 32)
print('== container: col extent at y=300 ==')
row = tan[300]
print('  tan runs y=300:', runs(row, 5)[:3], runs(row, 5)[-3:] if runs(row,5) else '')
print('  px at y=300 x=120..132:', [tuple(A[300, x]) for x in range(120, 133)])
print('  px at y=300 x=892..904:', [tuple(A[300, x]) for x in range(892, 905)])
print('== container: row extent at x=500 ==')
col = tan[:, 500]
rr = runs(col, 5)
print('  tan runs x=500:', rr[:2], rr[-2:] if rr else '')
print('  px x=500 y=84..92:', [tuple(A[y, 500]) for y in range(84, 93)])
print('  px x=500 y=472..482:', [tuple(A[y, 500]) for y in range(472, 483)])

# ---- 3) row bands: cell vertical border lines. Use x=204 (between cells? or inside cell 1) ----
# find dark-ish horizontal lines inside the container at a token-column center x=205
print('== row bands: darkness profile at x=205 (col1 center) y=90..480 ==')
for y in range(88, 482):
    px = A[y, 205]
    s = int(px[0]) + int(px[1]) + int(px[2])
    if s < 480:
        print(f'  y={y}: {tuple(px)}')
