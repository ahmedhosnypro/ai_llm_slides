#!/usr/bin/env python3
"""m2_struct.py — targeted measurement of slide_047.jpg structure."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def runs(mask_1d, min_len=1):
    out = []; i = 0; n = len(mask_1d)
    while i < n:
        if mask_1d[i]:
            j = i
            while j < n and mask_1d[j]: j += 1
            if j - i >= min_len: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# --- outer frame: dark red border. Probe column x=4,10,16,20 and row y=5,10,15,20
for x in [2, 5, 8, 12, 16, 20, 25, 940, 945, 950, 955, 958]:
    col = A[:, x]
    # find rows where pixel is reddish
    idx = [y for y in range(H) if col[y][0] > 120 and col[y][1] < 100 and col[y][2] < 100]
    print(f'x={x}: red rows count={len(idx)}', idx[:6], idx[-6:] if idx else '')
for y in [2, 5, 8, 12, 16, 20, 25, 520, 525, 530, 535]:
    row = A[y]
    idx = [x for x in range(W) if row[x][0] > 120 and row[x][1] < 100 and row[x][2] < 100]
    print(f'y={y}: red cols count={len(idx)}', idx[:6], idx[-6:] if idx else '')

print()
# --- tan container bounds: fill ~ (237,176,121). tolerance
tan = (abs(R - 237) < 25) & (abs(G - 176) < 25) & (abs(B - 121) < 30)
tc = tan.sum(axis=0); tr = tan.sum(axis=1)
print('TAN container cols (cnt>100):', runs(tc > 100))
print('TAN container rows (cnt>100):', runs(tr > 100))

# --- LN bars: orange F0A030-ish (240,160,48): scan rows 150-260 and 300-400 for wide orange rows
ln = (R > 215) & (abs(G - 160) < 40) & (B < 90)
lnc = ln.sum(axis=0); lnr = ln.sum(axis=1)
print('LN-bar orange rows (cnt>300):', runs(lnr > 300))

# --- lavender FFN fill F2E2F2 (242,226,242)
lav = (abs(R - 242) < 18) & (abs(G - 226) < 18) & (abs(B - 242) < 18)
lc = lav.sum(axis=0); lr = lav.sum(axis=1)
print('LAVENDER rows (cnt>200):', runs(lr > 200))
print('LAVENDER cols (cnt>30):', runs(lc > 30))

# --- purple border 7030A0 (112,48,160)
pur = (abs(R - 112) < 45) & (abs(G - 48) < 40) & (abs(B - 160) < 45)
pc = pur.sum(axis=0); pr = pur.sum(axis=1)
print('PURPLE rows (cnt>150):', runs(pr > 150))
print('PURPLE cols (cnt>20):', runs(pc > 20))
