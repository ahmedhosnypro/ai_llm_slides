#!/usr/bin/env python3
"""m6_precise.py — color censuses + precise edges for slide_047.jpg."""
from PIL import Image
import numpy as np
from collections import Counter

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def census(y0, y1, x0, x1, label, topn=8):
    reg = A[y0:y1, x0:x1].reshape(-1, 3)
    q = (reg // 16) * 16 + 8
    cnt = Counter(map(tuple, q))
    print(f'-- {label} ({y0}:{y1},{x0}:{x1}) top colors:')
    for c, n in cnt.most_common(topn):
        print(f'   {c} x{n}')

def edges_row(y, x0, x1, thresh=150, label=''):
    """dark-ish column positions in a row band (min over y0..y1)."""
    band = A[y, x0:x1]
    s = band.sum(axis=1)
    m = s < thresh * 3
    idx = [x0 + i for i, v in enumerate(m) if v]
    # compress to runs
    runs = []
    for i in idx:
        if runs and i - runs[-1][1] <= 1: runs[-1][1] = i
        else: runs.append([i, i])
    print(f'-- dark cols at y={y} {label}: {[(a, b) for a, b in runs]}')

# 1) LN bar region color census (top bar 104..127, bottom bar 314..338)
census(105, 127, 170, 880, 'TOP LN bar interior')
census(315, 338, 170, 880, 'BOTTOM LN bar interior')
census(96, 98, 170, 880, 'dash row 96')
census(162, 167, 170, 880, 'dash row ~165')

# 2) FFN band census
census(208, 224, 170, 880, 'FFN header band')
census(232, 255, 170, 880, 'FFN units band')

# 3) row cell bands: output row and X row
census(58, 82, 200, 600, 'OUTPUT row cells')
census(484, 505, 200, 600, 'X row cells')
census(174, 188, 200, 600, 'post-FFN row cells (174..188?)')
census(280, 295, 200, 600, 'post-LN row cells (280..295?)')
census(385, 400, 200, 600, 'out-of-attention row cells (385..400?)')

# 4) MHA bar color
census(420, 435, 200, 600, 'MHA bar')

# 5) container border color: top border rows 87-88, bottom 476-477, left col 125-127
census(87, 89, 300, 700, 'container TOP border')
census(476, 478, 300, 700, 'container BOTTOM border')
census(300, 302, 124, 128, 'container LEFT border')

# 6) plus discs: around y 142-156 col1 (x~205) and y 352-367
census(143, 156, 196, 214, 'PLUS disc 1 (top unit)')
census(353, 367, 196, 214, 'PLUS disc 1 (bottom unit)')

# 7) output row / X row cell borders: dark cols at cell mid-row
edges_row(70, 150, 910, 160, '(output row mid)')
edges_row(496, 150, 910, 160, '(X row mid)')

# 8) horizontal dark lines: for x=250 (inside col1 cell) find dark rows 50..520
col = A[:, 250]
s = col.sum(axis=1)
print('-- dark rows at x=250 (sum<420):', [(y, tuple(A[y, 250])) for y in range(45, 520) if s[y] < 420])
