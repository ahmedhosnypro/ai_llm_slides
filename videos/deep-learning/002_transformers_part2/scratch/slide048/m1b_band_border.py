#!/usr/bin/env python3
"""m1b_band_border.py — precise outer border + black bottom band on slide_048.jpg."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_048.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
H, W = A.shape[:2]
out = []
def p(*a):
    s = ' '.join(str(x) for x in a); out.append(s); print(s)

# --- outer border: scan row y=300 and column x=480 for the first non-white runs ---
row = A[300]
p('row 300, x 36..70:', [(x, tuple(row[x])) for x in range(36, 70) if not all(row[x] > 235)])
p('row 300, x 900..925:', [(x, tuple(row[x])) for x in range(900, 925) if not all(row[x] > 235)])
col = A[:, 480]
p('col 480, y 36..60:', [(y, tuple(col[y])) for y in range(36, 60) if not all(col[y] > 235)])
p('col 480, y 505..540:', [(y, tuple(col[y])) for y in range(505, 540)])

# reddish mask (looser): R significantly above G,B
redish = (A[..., 0] > 150) & (A[..., 0] - A[..., 1] > 40) & (A[..., 0] - A[..., 2] > 40)
rc = redish.sum(axis=0); rr = redish.sum(axis=1)
sc = [int(x) for x in range(W) if rc[x] > 250]
sr = [int(y) for y in range(H) if rr[y] > 250]
p('redish cols cnt>250:', sc[:6], '...', sc[-6:] if sc else [])
p('redish rows cnt>250:', sr[:10])
# per-row counts in border zone
p('redish row counts y 40..60:', [(y, int(rr[y])) for y in range(40, 60)])
p('redish col counts x 38..60:', [(x, int(rc[x])) for x in range(38, 60)])
p('redish col counts x 905..925:', [(x, int(rc[x])) for x in range(905, 925)])

# --- black band precise ---
blk = (A.max(axis=2) < 60)
p('black full-row-extent per row (rows 505..539):')
for y in range(505, 540):
    xs = np.where(blk[y])[0]
    if len(xs) > 30:
        p(f'  y={y}: x {xs.min()}..{xs.max()} count={len(xs)}')
p('black rows 505..539 col-480 sample:', [tuple(A[y, 480]) for y in (510, 515, 520, 530, 538)])
# is the band under the gray panel? gray row span vs band rows
p('NOTE: gray panel rows 46..514 (m1); band covers ~515..539')

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide048/m1b_output.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
