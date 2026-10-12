#!/usr/bin/env python3
"""m1_frame.py — first structural measurement of slide_047.jpg (960x540, 1px=1pt)."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def runs(mask_1d, min_len=2):
    out = []
    i = 0
    n = len(mask_1d)
    while i < n:
        if mask_1d[i]:
            j = i
            while j < n and mask_1d[j]:
                j += 1
            if j - i >= min_len:
                out.append((i, j - 1))
            i = j
        else:
            i += 1
    return out

# 1) red-ish mask (outer frame): strong red, low green/blue
red = (R > 130) & (G < 90) & (B < 90)
# vertical borders: columns where red count is high
colcnt = red.sum(axis=0)
rowcnt = red.sum(axis=1)
print('RED frame candidate columns (cnt>300):', [(x, int(colcnt[x])) for x in range(W) if colcnt[x] > 300])
print('RED frame candidate rows (cnt>300):', [(y, int(rowcnt[y])) for y in range(H) if rowcnt[y] > 300])

# 2) orange container: sample around center
print('center px (480,270):', A[270, 480], '(480,100):', A[100, 480], '(480,500):', A[500, 480])
# orange-ish mask: R>200, 120<G<200, B<130
orange = (R > 200) & (G > 130) & (G < 210) & (B < 140)
oc = orange.sum(axis=0)
orr = orange.sum(axis=1)
print('ORANGE cols (cnt>200):', runs(oc > 200))
print('ORANGE rows (cnt>200):', runs(orr > 200))

# 3) dark plum MHA bar: R in 100..150, G<70, B in 70..120
plum = (R > 95) & (R < 160) & (G < 75) & (B > 70) & (B < 130)
pc = plum.sum(axis=0)
prr = plum.sum(axis=1)
print('PLUM rows (cnt>300):', runs(prr > 300))
print('PLUM cols (cnt>60):', runs(pc > 60))

# 4) vertical extent scan: classify each row by dominant non-white color between x=200..900
for y in range(0, H, 1):
    pass

# row band profile: for each y, count of strongly-colored px (not near-white/near-black)
ink = ((R > 180) | (R < 120)) & ~((R > 235) & (G > 235) & (B > 235))
print('\nrow ink profile (y: count) every 4px from 40:')
for y in range(40, H, 4):
    c = int(ink[y, 150:950].sum())
    if c > 30:
        print(f'  y={y}: {c}')
