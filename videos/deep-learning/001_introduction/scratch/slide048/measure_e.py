#!/usr/bin/env python3
"""Pass E: gray-panel extents, ASCII shape maps, color samples."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
gray = (abs(r - 232) < 10) & (abs(g - 232) < 10) & (abs(b - 232) < 10)

print("== A. gray extents ==")
for y in (60, 100, 145, 270, 470, 500, 515):
    xs = np.where(gray[y, :])[0]
    if len(xs):
        rr = []
        s = p = xs[0]
        for i in xs[1:]:
            if i <= p + 3: p = i
            else: rr.append((s, p)); s = p = i
        rr.append((s, p))
        print(f"  y={y}: gray spans {rr}")
for x in (50, 480, 700, 900, 910):
    ys = np.where(gray[:, x])[0]
    if len(ys):
        rr = []
        s = p = ys[0]
        for i in ys[1:]:
            if i <= p + 3: p = i
            else: rr.append((s, p)); s = p = i
        rr.append((s, p))
        print(f"  x={x}: gray spans {rr}")

print("== B. edge color samples ==")
for (x, y, tag) in [(42, 300, 'x42'), (44, 300, 'x44'), (46, 300, 'x46'), (50, 300, 'x50'), (54, 300, 'x54'),
                    (916, 300, 'x916'), (918, 300, 'x918'), (920, 300, 'x920'),
                    (880, 60, '880,60'), (890, 60, '890,60'), (896, 60, '896,60'), (900, 60, '900,60'),
                    (905, 60, '905,60'), (912, 60, '912,60'), (917, 60, '917,60'),
                    (400, 448, 'bottom border'), (400, 135, 'rule'), (300, 155, 'labelbox top border'),
                    (242, 168, 'labelbox left border'), (400, 43, 'top border dark')]:
    print(f"  ({x},{y}) {tag}: {tuple(int(v) for v in im[y, x])}")

print("== C. tag text color: darkest 10 px in x388..422 y158..180 ==")
sub = im[158:181, 388:423]
lum = sub.mean(axis=2)
flat = [(lum[i, j], i + 158, j + 388, tuple(int(v) for v in sub[i, j])) for i in range(sub.shape[0]) for j in range(sub.shape[1])]
flat.sort()
for f in flat[:12]:
    print(f"  lum={f[0]:.0f} ({f[2]},{f[1]}): {f[3]}")

print("== D. dot centers ==")
for (y0, y1, tag) in [(193, 198, 'dot1'), (202, 206, 'dot2'), (210, 215, 'dot3'), (227, 231, 'dot5'), (235, 240, 'dot6'), (244, 248, 'dot7')]:
    px = im[(y0 + y1) // 2, 403:409]
    best = max(px, key=lambda p: p.mean() if tag in ('dot6',) else -p.mean())
    print(f"  {tag}: row{(y0+y1)//2} x403..408 {[tuple(int(v) for v in p) for p in px]}")

print("== E. color modals ==")
def modal(mask, name):
    px = im[mask]
    if not len(px):
        print(f"  {name}: none")
        return
    q = (px // 16 * 16)
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    cnt = np.sort(counts)[::-1][:3]
    print(f"  {name}: n={len(px)} top {[[int(v) for v in t] for t in top]} counts {list(cnt)}")
red = (r > 120) & (g < 110) & (b < 110)
modal(red[62:124, 100:840], 'title red')
modal(red[168:178, 450:665], 'FC overline red')
modal(red[319:330, 217:251], 'Conv red')
modal(red[467:480, 355:575], 'caption red')
modal(red[462:464, 60:816], 'arrow red')
modal(red[268:270, 60:895], 'divider red')
modal(red[42:45, 64:896], 'top border')
modal(red[134:137, 64:895], 'rule')
modal(red[447:450, 64:895], 'bottom border')
modal(red[44:516, 56:60], 'left border')
modal(red[134:450, 892:896], 'right border')

print("== F. ASCII map slab1 x215..300 y310..430 (3px) O=orange w=white .=bg ==")
orange = (r > 150) & (g > 80) & (g < 190) & (b < 110) & (r - b > 80)
whiteish = (r > 200) & (g > 200) & (b > 190)
darkor = (r > 120) & (r < 190) & (g > 60) & (g < 120) & (b < 60)
for y in range(310, 430, 3):
    line = ''
    for x in range(215, 300, 3):
        if orange[y, x]: line += 'O'
        elif darkor[y, x]: line += 'o'
        elif whiteish[y, x]: line += 'w'
        else: line += '.'
    print(f"  {y:3d} {line}")

print("== G. ASCII map siamese x120..235 y312..425 (3px) P=photo(non-bg) ==")
bg = ((r > 215) & (g > 215) & (b > 215)) | ((abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16))
for y in range(312, 425, 3):
    line = ''
    for x in range(120, 235, 3):
        line += '.' if bg[y, x] else 'P'
    print(f"  {y:3d} {line}")

print("== H. ASCII map tag+col x385..430 y150..255 (2px) Y=yellow R=red-ish B=blue G=green K=dark W=white ==")
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

print("== I. catmeme rows extent (excluding arrow band y215..227) ==")
for y in (193, 200, 210, 230, 240, 248, 251):
    xs = np.where(~bg[y, 232:400])[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+232}..{xs.max()+232}")
