#!/usr/bin/env python3
"""Pass F: fixed modals + ASCII shape maps (slab, siamese, tag column) + catmeme rows."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def modal(y0, y1, x0, x1, mask_fn, name):
    sub = im[y0:y1, x0:x1]
    m = mask_fn(sub)
    px = sub[m]
    if not len(px):
        print(f"  {name}: none")
        return
    q = (px // 16 * 16)
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    cnt = np.sort(counts)[::-1][:3]
    print(f"  {name}: n={len(px)} top {[[int(v) for v in t] for t in top]} counts {list(cnt)}")

red = lambda s: (s[:, :, 0] > 120) & (s[:, :, 1] < 110) & (s[:, :, 2] < 110)
print("== E. color modals (fixed) ==")
modal(62, 124, 100, 840, red, 'title red')
modal(168, 178, 450, 665, red, 'FC overline red')
modal(319, 330, 217, 251, red, 'Conv red')
modal(467, 480, 355, 575, red, 'caption red')
modal(462, 464, 60, 816, red, 'arrow red')
modal(268, 270, 60, 895, red, 'divider red')
modal(42, 45, 64, 896, red, 'top border')
modal(134, 137, 64, 895, red, 'rule')
modal(447, 450, 64, 895, red, 'bottom border')
modal(44, 516, 56, 60, red, 'left border')
modal(134, 450, 892, 896, red, 'right border')
blue_fn = lambda s: (s[:, :, 2] - s[:, :, 0] > 40) & (s[:, :, 2] > 110)
modal(416, 442, 260, 650, blue_fn, 'NonLinearity blue')
modal(158, 180, 250, 372, blue_fn, 'NN label text blue')

print("== F. ASCII map slab1 x215..300 y310..430 (3px) O=lt-orange o=dk-orange w=white .=bg ==")
orange = (r > 150) & (g > 80) & (g < 190) & (b < 110) & (r - b > 80)
whiteish = (r > 200) & (g > 200) & (b > 190)
darkor = (r > 120) & (r < 190) & (g > 60) & (g < 120) & (b < 60)
for y in range(310, 430, 3):
    line = ''
    for x in range(215, 300, 3):
        if darkor[y, x]: line += 'o'
        elif orange[y, x]: line += 'O'
        elif whiteish[y, x]: line += 'w'
        else: line += '.'
    print(f"  {y:3d} {line}")

print("== F2. slab top-face color samples ==")
for (x, y) in [(270, 320), (275, 325), (265, 318), (280, 330), (250, 322)]:
    print(f"  ({x},{y}): {tuple(int(v) for v in im[y, x])}")

print("== G. ASCII map siamese x120..235 y312..425 (3px) P=non-bg ==")
bg = ((r > 215) & (g > 215) & (b > 215)) | ((abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16))
for y in range(312, 425, 3):
    line = ''
    for x in range(120, 235, 3):
        line += '.' if bg[y, x] else 'P'
    print(f"  {y:3d} {line}")

print("== H. ASCII map tag+dotcol x385..430 y150..255 (2px) Y=yellow R=red B=blue G=green K=dark ' '=white ==")
yel = (r > 200) & (g > 200) & (b < 140)
redish = (r > 130) & (r - g > 50) & (r - b > 50)
blu = (b - r > 40) & (b > 110)
grn = (g - r > 30) & (g - b > 20) & (g > 90)
for y in range(150, 256, 2):
    line = ''
    for x in range(385, 430, 2):
        if yel[y, x]: line += 'Y'
        elif redish[y, x]: line += 'R'
        elif blu[y, x]: line += 'B'
        elif grn[y, x]: line += 'G'
        elif im[y, x].mean() < 120: line += 'K'
        elif im[y, x].mean() > 210: line += ' '
        else: line += '.'
    print(f"  {y:3d} {line}")

print("== I. catmeme row extents (all rows) ==")
for y in range(190, 254, 4):
    xs = np.where(~bg[y, 232:400])[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+232}..{xs.max()+232} n={len(xs)}")

print("== J. NN block white text x-extents (block1) ==")
sub = im[186:257, 450:476]
wt = sub.mean(axis=2) > 165
ys, xs = np.where(wt)
print(f"  block1 white: x {xs.min()+450}..{xs.max()+450} y {ys.min()+186}..{ys.max()+186}")
colsum = wt.sum(axis=0)
print(f"  per-col: {[int(v) for v in colsum]}")

print("== K. slab1 white text x-columns ==")
sub = im[316:425, 229:288]
wt = sub.mean(axis=2) > 175
ys, xs = np.where(wt)
print(f"  slab1 white: x {xs.min()+229}..{xs.max()+229} y {ys.min()+316}..{ys.max()+316} n={len(ys)}")
colsum = wt.sum(axis=0)
print(f"  per-col: {[int(v) for v in colsum]}")
