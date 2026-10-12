#!/usr/bin/env python3
"""m18_ffdiff.py — frame-vs-frame diff: slide_046.jpg vs slide_047.jpg.
Coarse grid RMS map + per-band row/col profiles of where they differ."""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/"
A = np.asarray(Image.open(D + "slide_046.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(D + "slide_047.jpg").convert("RGB")).astype(int)
print("shapes", A.shape, B.shape)
d = np.abs(A - B).sum(axis=2)  # 0..765

# grid map 16x30
H, W = d.shape
gh, gw = H // 15, W // 30
print("grid RMS (rows=y bands of 36px, cols=x bands of 32px), '.' <20 'o' <60 'O' <120 '#' >=120:")
for gy in range(15):
    row = ""
    for gx in range(30):
        blk = d[gy * gh:(gy + 1) * gh, gx * gw:(gx + 1) * gw]
        r = np.sqrt((blk ** 2).mean())
        row += "." if r < 20 else ("o" if r < 60 else ("O" if r < 120 else "#"))
    print(f" y{gy*gh:3d}-{(gy+1)*gh:3d} {row}")

# column profile of mean diff (which x are unchanged)
cp = d.mean(axis=0)
same_cols = [i for i in range(W) if cp[i] < 8]
print("nearly-identical column ranges:", end=" ")
runs = []
for xs in same_cols:
    if runs and xs - runs[-1][1] <= 2: runs[-1][1] = xs
    else: runs.append([xs, xs])
print([(a, b) for a, b in runs if b - a > 5])
rp = d.mean(axis=1)
same_rows = [i for i in range(H) if rp[i] < 8]
runs = []
for ys in same_rows:
    if runs and ys - runs[-1][1] <= 2: runs[-1][1] = ys
    else: runs.append([ys, ys])
print("nearly-identical row ranges:", [(a, b) for a, b in runs if b - a > 2])
