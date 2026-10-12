#!/usr/bin/env python3
"""m6_bands.py — band census: pale box rows, dark-red (plus) blobs, box columns."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def runs(m, min_len=1):
    out=[];i=0;n=len(m)
    while i<n:
        if m[i]:
            j=i
            while j<n and m[j]: j+=1
            if j-i>=min_len: out.append((i,j-1))
            i=j
        else: i+=1
    return out

# pale box fill: high green vs container. r>225 & g>205 & b>185 (excludes container g~176)
pale = (R>225)&(G>205)&(B>180)
pr = pale[:, 130:900].sum(axis=1)
print('--- pale-box rows (count>150), y 40..520 ---')
for y in range(40, 520):
    if pr[y] > 150: print(f'y={y}: {int(pr[y])}')

print()
print('--- dark red plus-disc color (150<r<225, g<100, b<85) blobs ---')
plus = (R>150)&(R<228)&(G<100)&(B<85)
pc = plus[:, 130:900].sum(axis=1)
for y in range(84, 480):
    if pc[y] > 40: print(f'y={y}: {int(pc[y])}')

print()
print('--- x=897 red line: rows where red-ish ---')
redm = (R>140)&(G<110)&(B<110)
col = redm[:, 897]
print(runs(col, 5))
