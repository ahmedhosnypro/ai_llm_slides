#!/usr/bin/env python3
"""m7_gaps.py — borders, word-color split, cyan arrowheads, refined fills, box extents."""
from PIL import Image
import numpy as np
from collections import Counter

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
SX = lambda fx: 42 + (fx - 58.5) * (919 - 42) / (901 - 58.5)
SY = lambda fy: 45 + (fy - 43.0) * (540 - 45) / (517.0 - 43.0)

print('=== box borders (row/col cross-sections)')
print('root top border, y=116..122 at x=420:', [tuple(im[y, 420]) for y in range(116, 123)])
print('root bottom border, y=167..172 at x=420:', [tuple(im[y, 420]) for y in range(167, 173)])
print('root left border, x=349..355 at y=140:', [tuple(im[140, x]) for x in range(349, 356)])
print('cyan1 top border, y=292..297 at x=380:', [tuple(im[y, 380]) for y in range(292, 298)])
print('cyan1 bottom border, y=332..337 at x=380:', [tuple(im[y, 380]) for y in range(332, 338)])
print('cyan1 left border, x=260..266 at y=315:', [tuple(im[315, x]) for x in range(260, 267)])
print('blue box border top, y=219..224 at x=200:', [tuple(im[y, 200]) for y in range(219, 225)])
print('green box left border, x=565..571 at y=245:', [tuple(im[245, x]) for x in range(565, 572)])
print('grnleaf top border, y=325..331 at x=640:', [tuple(im[y, 640]) for y in range(325, 332)])
print('grnleaf left border, x=558..564 at y=345:', [tuple(im[345, x]) for x in range(558, 565)])

print('=== leaf text: split bold "Weight" vs regular "Normalization"')
# grnleaf_txt frame[573,339 -> 776,358]; find word gap via column ink profile
dkg = (R < 130) & (G > 60) & (G < 180) & (B < 140)
sub = dkg[339:359, 573:777]
cols = sub.sum(axis=0)
runs, inr = [], False
for j, v in enumerate(cols):
    if v > 0 and not inr: inr, s = True, j
    elif v == 0 and inr:
        inr = False; runs.append((s, j - 1))
if inr: runs.append((s, len(cols) - 1))
print('word col runs (rel):', runs[:6], '...')
# biggest internal gap splits words
gaps = [(runs[i + 1][0] - runs[i][1], i) for i in range(len(runs) - 1)]
gaps.sort(reverse=True)
split = gaps[0][1]
w0, w1 = runs[0][0], runs[split][1]
n0, n1 = runs[split + 1][0], runs[-1][1]
print('bold word cols %d..%d, regular cols %d..%d (abs frame %d..%d, %d..%d)' % (
    w0, w1, n0, n1, 573 + w0, 573 + w1, 573 + n0, 573 + n1))
def corecensus(name, x0, y0, x1, y1):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    sel = px[(px[:, 0] < 140) & (px[:, 1] < 180) & (px[:, 2] < 150)]
    if len(sel) == 0: print(name, 'none'); return
    cnt = Counter(map(tuple, (sel // 4 * 4 + 2)))
    print('%-12s cores p25=%s median=%s n=%d mode=%s' % (
        name, np.percentile(sel, 25, axis=0).astype(int),
        np.median(sel, axis=0).astype(int), len(sel), cnt.most_common(2)))
corecensus('Weight_bold', 573 + w0, 341, 573 + w1 + 1, 357)
corecensus('Norm_regular', 573 + n0, 341, 573 + n1 + 1, 357)
# same split for one cyan box (bold Batch vs regular Normalization)
sub = dkg[305:324, 280:476]
cols = sub.sum(axis=0)
runs, inr = [], False
for j, v in enumerate(cols):
    if v > 0 and not inr: inr, s = True, j
    elif v == 0 and inr:
        inr = False; runs.append((s, j - 1))
if inr: runs.append((s, len(cols) - 1))
gaps = [(runs[i + 1][0] - runs[i][1], i) for i in range(len(runs) - 1)]
gaps.sort(reverse=True)
split = gaps[0][1]
print('cyan1 word runs:', runs[:4], 'gaps:', gaps[:3])
corecensus('Batch_bold', 280 + runs[0][0], 307, 280 + runs[split][1] + 1, 322)
corecensus('cNORM_regular', 280 + runs[split + 1][0], 307, 280 + runs[-1][1] + 1, 322)

print('=== cyan arrowheads (reddish, x 244..263)')
reddish = (R - G > 25) & (R - B > 25)
for i, (y0, y1) in enumerate([(304, 326), (357, 379), (409, 431), (462, 484)]):
    ys, xs = np.where(reddish[y0:y1, 244:264])
    if len(xs):
        print('arrow%d head frame x %d..%d y %d..%d -> slide x %.1f..%.1f y %.1f..%.1f n=%d' % (
            i + 1, 244 + xs.min(), 244 + xs.max(), y0 + ys.min(), y0 + ys.max(),
            SX(244 + xs.min()), SX(244 + xs.max()), SY(y0 + ys.min()), SY(y0 + ys.max()), len(xs)))
        # widest row
        for y in range(y0, y1):
            xs2 = np.where(reddish[y, 244:264])[0]
            if len(xs2):
                print('   y=%d x %d..%d (w=%d)' % (y, 244 + xs2.min(), 244 + xs2.max(), len(xs2)))

print('=== q=4 refined fills')
def q4(name, x0, y0, x1, y1):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    cnt = Counter(map(tuple, (px // 4 * 4 + 2)))
    print('%-13s mode=%s 2nd=%s n=%d' % (name, cnt.most_common(1)[0][0], cnt.most_common(2)[1][0], len(px)))
q4('cyan_fill', 300, 298, 470, 303)
q4('leaf_fill', 600, 331, 770, 337)
q4('blue_fill', 140, 240, 330, 268)
q4('green_fill', 590, 235, 770, 266)
q4('root_fill', 370, 122, 545, 130)

print('=== cyan box precise tops/bottoms (fill rows within x 280..460)')
cyan = (R > 195) & (R < 240) & (G > 243) & (B > 233)
rows = cyan[:, 280:460].sum(axis=1)
segs, inr = [], False
for y in range(280, 515):
    if rows[y] > 100 and not inr: inr, s = True, y
    elif rows[y] <= 100 and inr:
        inr = False; segs.append((s, y - 1))
if inr: segs.append((s, 514))
print('box fill row segments:', segs)
for i, (a, b) in enumerate(segs):
    print(' box%d frame y %d..%d -> slide y %.1f..%.1f (h %.1f)' % (i + 1, a, b, SY(a), SY(b), SY(b) - SY(a)))
