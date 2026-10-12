#!/usr/bin/env python3
"""Pass D: rerun crashed sections + structural probes (backgrounds, borders, Conv, skew)."""
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

loose = (r > 150) & (r - g > 25) & (r - b > 25)
reddish = (r > 130) & (r - g > 40) & (r - b > 40)
blue = (b - r > 40) & (b - g > 30) & (b > 110)
orange = (r > 150) & (g > 80) & (g < 180) & (b < 90) & (r - b > 90)

def runs(idx, gap=2):
    out = []; s = p = None
    for i in idx:
        if s is None: s = p = i
        elif i <= p + gap: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

print("== A. raw RGB samples ==")
for (x, y, tag) in [(400, 41, 'above top border'), (400, 42, 'top border'), (400, 43, 'below top border'),
                    (894, 60, 'right border y60'), (894, 80, 'right y80'), (894, 110, 'right y110'),
                    (894, 130, 'right y130'), (58, 300, 'left border y300'), (58, 480, 'left y480'),
                    (100, 200, 'inside box NN row'), (480, 145, 'title band between lines'),
                    (700, 220, 'inside box right'), (480, 470, 'below box'), (480, 500, 'below box2'),
                    (480, 512, 'just above strip'), (30, 270, 'left of box'), (930, 270, 'right of box'),
                    (480, 30, 'above box'), (100, 470, 'below box left'), (850, 470, 'below box right')]:
    print(f"  ({x},{y}) {tag}: {tuple(int(v) for v in im[y, x])}")

print("== B. ultra-loose right border rows 43..134 (r-g>12, r>170) ==")
ul = (r > 170) & (r - g > 12) & (r - b > 12)
for y in range(43, 135, 6):
    xs = np.where(ul[y, 880:910])[0]
    print(f"  y={y}: n={len(xs)} {'x ' + str(xs.min()+880) + '..' + str(xs.max()+880) if len(xs) else ''}")

print("== C. white text in NN block1: luminance & bands ==")
sub = im[186:257, 450:476]
lum = sub.mean(axis=2)
wt = lum > 165
rowsum = wt.sum(axis=1)
bands = runs(list(np.where(rowsum > 0)[0]), gap=2)
print(f"  white bands y(+186): {[(s+186, e+186) for s, e in bands]}, total n={int(wt.sum())}")

print("== D. slab1 orange x-extent by row (skew) ==")
for y in (316, 330, 350, 370, 390, 410, 424):
    xs = np.where(orange[y, 215:300])[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+215}..{xs.max()+215}")

print("== E. label box1 border: blue pixels rows 154..184 x 235..385 ==")
for y in (154, 155, 156, 168, 181, 182, 183):
    xs = np.where(blue[y, 235:390])[0]
    if len(xs):
        rr = runs(list(xs), gap=3)
        print(f"  y={y}: n={len(xs)} runs {[(s+235, e+235) for s, e in rr][:6]}")

print("== F. Conv texts: loose red comps y 310..335 x 200..700 ==")
sub = loose[310:336, 200:700]
lab, n = ndimage.label(sub)
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) >= 8:
        print(f"  comp x {xs.min()+200}..{xs.max()+200} y {ys.min()+310}..{ys.max()+310} n={len(ys)}")

print("== G. divider pattern fixed: row 268 & 269 col runs ==")
for y in (268, 269):
    xs = np.where(reddish[y, 55:900])[0]
    rr = runs(list(xs), gap=1)
    print(f"  y={y}: n={len(xs)} nruns={len(rr)} widths {[e-s+1 for s, e in rr][:14]} gaps {[rr[i+1][0]-rr[i][1]-1 for i in range(min(13, len(rr)-1))]}")
    print(f"    x {xs.min()+55}..{xs.max()+55}")

print("== H. dark arrows between NN blocks (gaps) ==")
darkish = (r < 130) & (g < 130) & (b < 130)
for (x0, x1, tag) in [(477, 497, 'NN1-2'), (524, 544, 'NN2-3'), (571, 591, 'NN3-4'), (618, 638, 'NN4-5'), (666, 685, 'NN5-Loss'),
                      (375, 402, 'photo-dots'), (408, 449, 'dots-blk1')]:
    sub = darkish[200:250, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  {tag}: n={len(ys)} x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+200}..{ys.max()+200}")
    else:
        print(f"  {tag}: none")

print("== I. dark arrows between CNN slabs y 350..400 ==")
for (x0, x1, tag) in [(289, 310, 's1-2'), (371, 398, 's2-3'), (459, 476, 's3-4'), (537, 553, 's4-5'), (613, 634, 's5-6'), (695, 734, 's6-L5'), (762, 781, 'L5-L6'), (809, 829, 'L6-Loss')]:
    sub = darkish[340:410, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  {tag}: n={len(ys)} x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+340}..{ys.max()+340}")
    else:
        print(f"  {tag}: none")

print("== J. photo bboxes precise ==")
bg = ((r > 215) & (g > 215) & (b > 215)) | ((abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16))
for (x0, x1, y0, y1, name) in [(232, 385, 184, 258, 'catmeme'), (120, 225, 310, 425, 'siamese')]:
    sub = ~bg[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    print(f"  {name}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
    # column/row fill to detect parallelogram skew
    for frac in (0.1, 0.5, 0.9):
        yy = int(y0 + frac * (y1 - y0))
        xs2 = np.where(~bg[yy, x0:x1])[0]
        if len(xs2):
            print(f"    row y={yy}: x {xs2.min()+x0}..{xs2.max()+x0}")

print("== K. Non Linearity blue comps y 405..448 x 250..660 ==")
lab, n = ndimage.label(blue[405:448, 250:660])
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) >= 6:
        print(f"  comp x {xs.min()+250}..{xs.max()+250} y {ys.min()+405}..{ys.max()+405} n={len(ys)}")

print("== L. tag text red rows ==")
sub = reddish[155:186, 387:423]
rowsum = sub.sum(axis=1)
print(f"  per-row n: {list(enumerate([int(v) for v in rowsum], start=155))}")
ys, xs = np.where(sub)
if len(ys):
    print(f"  red bbox x {xs.min()+387}..{xs.max()+387} y {ys.min()+155}..{ys.max()+155}")

print("== M. caption bbox loose ==")
ys, xs = np.where(loose[464:483, 55:900])
print(f"  x {xs.min()+55}..{xs.max()+55} y {ys.min()+464}..{ys.max()+464} n={len(ys)}")

print("== N. white vertical text in CNN slab1 & L5/L6/Loss ==")
for (x0, x1, y0, y1, tag) in [(229, 288, 316, 424, 'slab1'), (735, 761, 334, 404, 'L5'), (782, 808, 334, 404, 'L6'), (830, 855, 334, 404, 'Loss')]:
    sub = im[y0:y1, x0:x1]
    lum = sub.mean(axis=2)
    wt = lum > 165
    rowsum = wt.sum(axis=1)
    bands = runs(list(np.where(rowsum > 0)[0]), gap=3)
    ys, xs = np.where(wt)
    if len(ys):
        print(f"  {tag}: white n={len(ys)} bands(y+{y0}) {[(s+y0, e+y0) for s, e in bands]}")

print("== O. arrow shaft detail: row 462 & 463 runs (x 55..845) ==")
for y in (462, 463):
    xs = np.where(loose[y, 55:845])[0]
    rr = runs(list(xs), gap=3)
    print(f"  y={y}: n={len(xs)} nruns={len(rr)} x {xs.min()+55}..{xs.max()+55} widths sample {[e-s+1 for s, e in rr[:8]]}")
