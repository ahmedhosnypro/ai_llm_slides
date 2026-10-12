#!/usr/bin/env python3
"""m6_final_measure.py — final precise numbers: arrowheads, spine, right arrow, mode colors."""
from PIL import Image
import numpy as np
from collections import Counter

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

SX = lambda fx: 42 + (fx - 58.5) * (919 - 42) / (901 - 58.5)
SY = lambda fy: 45 + (fy - 43.0) * (540 - 45) / (517.0 - 43.0)
def sl(bb):
    x0, y0, x1, y1 = bb
    return [round(SX(x0), 1), round(SY(y0), 1), round(SX(x1), 1), round(SY(y1), 1)]
def show(name, bb):
    if bb is None: print(name, 'EMPTY'); return
    print('%-14s frame[%d,%d -> %d,%d] slide[%s]' % (name, bb[0], bb[1], bb[2], bb[3], ','.join(str(v) for v in sl(bb[:4]))))

lum = (R + G + B) / 3.0
bg = (np.abs(R - 231) < 7) & (np.abs(G - 233) < 7) & (np.abs(B - 230) < 7)
ink = ~bg
reddish = (R - G > 25) & (R - B > 25)

def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(len(xs))]

print('=== top connector pieces')
show('drop_line', bbox(ink, 445, 173, 470, 206))
show('hbar', bbox(ink, 215, 202, 700, 207))
show('headL', bbox(reddish, 215, 207, 250, 220))
show('headR', bbox(reddish, 655, 207, 700, 220))
# head cross-sections
for y in (208, 210, 212, 214, 216, 218):
    xs = np.where(reddish[y, 215:250])[0]
    xs2 = np.where(reddish[y, 655:700])[0]
    print('headL y=%d x %s | headR y=%d x %s' % (
        y, (215 + xs.min(), 215 + xs.max()) if len(xs) else '-',
        y, (655 + xs2.min(), 655 + xs2.max()) if len(xs2) else '-'))

print('=== spine + 4 arrows')
show('spine_full', bbox(ink, 230, 276, 240, 505))
for i, (y0, y1) in enumerate([(305, 325), (358, 378), (410, 430), (463, 483)]):
    ab = bbox(ink, 228, y0, 263, y1)
    show('arrow%d' % (i + 1), ab)
    # column profile of arrow shaft vs head
    sub = ink[y0:y1, 228:263]
    cols = sub.sum(axis=0)
    prof = ''.join('#' if c >= (y1 - y0) * 0.6 else ('+' if c > 2 else '.') for c in cols)
    print('   arrow%d col profile x228..262: %s' % (i + 1, prof))
# spine below last arrow?
for y in range(477, 505):
    c = ink[y, 230:240].sum()
    if c > 1: print('spine tail y=%d ink=%d' % (y, c))

print('=== right arrow')
show('right_shaft', bbox(ink, 668, 274, 685, 312))
show('right_head', bbox(reddish, 660, 312, 695, 327))
for y in range(313, 326):
    xs = np.where(reddish[y, 660:695])[0]
    print('  headR y=%d x %s' % (y, (660 + xs.min(), 660 + xs.max()) if len(xs) else '-'))

print('=== MODE COLOR CENSUS')
def modecensus(name, x0, y0, x1, y1, q=8):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    qq = (px // q * q + q // 2)
    cnt = Counter(map(tuple, qq))
    (c, n), = cnt.most_common(1)
    print('%-15s mode(%d,%d,%d) n=%d/%d  top3=%s' % (
        name, c[0], c[1], c[2], n, len(px),
        [(tuple(int(v) for v in k), v) for k, v in cnt.most_common(3)]))
modecensus('title_red', 350, 70, 560, 90)
modecensus('root_fill', 360, 122, 550, 130)
modecensus('root_text_dark', 387, 124, 525, 140, q=16)
modecensus('blue_fill', 135, 226, 335, 270)
modecensus('green_fill', 575, 225, 775, 268)
modecensus('cyan_fill', 270, 298, 485, 305)
modecensus('cyan_fill2', 300, 325, 480, 332)
modecensus('grnleaf_fill', 570, 332, 780, 338)
modecensus('panel_bg', 90, 300, 115, 330)
modecensus('letterbox', 300, 525, 700, 535)
# text dark cores
def darkcore(name, x0, y0, x1, y1, cond):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    sel = px[cond(px)]
    if len(sel) == 0: print(name, 'none'); return
    cnt = Counter(map(tuple, (sel // 8 * 8 + 4)))
    (c, n), = cnt.most_common(1)
    print('%-15s dark-mode(%d,%d,%d) n=%d  p10=%s' % (
        name, c[0], c[1], c[2], n, np.percentile(sel, 10, axis=0).astype(int)))
darkcore('root_txt_core', 387, 124, 525, 163, lambda p: (p[:, 0] > 120) & (p[:, 1] < 80) & (p[:, 2] < 80))
darkcore('cyan_txt_core', 270, 300, 485, 335, lambda p: (p[:, 2] > 90) & (p[:, 0] < 70) & (p[:, 1] < 70))
darkcore('grnleaf_txt_core', 565, 340, 785, 360, lambda p: (p[:, 1] < 150) & (p[:, 0] < 120) & (p[:, 2] < 130))
darkcore('title_txt_core', 345, 68, 565, 93, lambda p: (p[:, 0] > 120) & (p[:, 1] < 80) & (p[:, 2] < 80))
# arrowhead red core
darkcore('headL_core', 224, 207, 245, 220, lambda p: (p[:, 0] > 120) & (p[:, 1] < 80) & (p[:, 2] < 80))
# shaft pixels along right arrow
print('right shaft px x676, y280..308:', [tuple(im[y, 676]) for y in range(280, 309, 7)])
print('drop line px x454, y190..202:', [tuple(im[y, 454]) for y in range(190, 203, 3)])
print('hbar px y204, x300..660:', [tuple(im[204, x]) for x in range(300, 661, 90)])
print('spine px x234, y280..460:', [tuple(im[y, 234]) for y in range(280, 461, 45)])
