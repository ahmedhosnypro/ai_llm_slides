#!/usr/bin/env python3
"""m7_cols.py — box columns in top/bottom rows, segmented cells, plus-disc x census."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def runs(m, min_len=2):
    out=[];i=0;n=len(m)
    while i<n:
        if m[i]:
            j=i
            while j<n and m[j]: j+=1
            if j-i>=min_len: out.append((i,j-1))
            i=j
        else: i+=1
    return out

# --- top row: pale box fill at y=52 (above text) and y=80 (below text)
for yy in [50, 52, 80, 82]:
    pale = (R[yy] > 225) & (G[yy] > 205) & (B[yy] > 180)
    rr = runs(pale, 8)
    print(f'top row y={yy} pale runs:', rr)

# --- bottom row: pale at y=485 and y=505
for yy in [485, 505]:
    pale = (R[yy] > 225) & (G[yy] > 205) & (B[yy] > 180)
    rr = runs(pale, 8)
    print(f'bottom row y={yy} pale runs:', rr)

# --- segmented cells: scan rows 90..475 for cyan/yellow/pink cell colors
cyan = (B > 185) & (R < 205) & (G > 120) & (G < 215)
yellow = (R > 225) & (G > 215) & (B < 140)
pink = (R > 225) & (G > 130) & (G < 215) & (B > 130) & (B < 225) & (B <= G + 40)
print()
print('--- per-row counts: cyan / yellow / pink (x130..905) ---')
for y in range(88, 478, 2):
    c, yl, p = int(cyan[y,130:905].sum()), int(yellow[y,130:905].sum()), int(pink[y,130:905].sum())
    if c > 60 or yl > 60 or p > 60:
        print(f'y={y}: cyan={c} yellow={yl} pink={p}')

print()
print('--- plus discs: dark-red blobs at y=142..156 and y=353..367: x-runs ---')
plus = (R>150)&(R<228)&(G<105)&(B<90)
for y0,y1 in [(142,157),(353,368)]:
    band = plus[y0:y1+1, :].sum(axis=0)
    print(f'y{y0}-{y1}:', runs(band > 6, 4))
