#!/usr/bin/env python3
"""Refined PIL measurements for slide_029 (pass 2)."""
import numpy as np
from PIL import Image

ORIG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_029.jpg'
im = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 140) & (g < 90) & (b < 90)

print('--- content frame verticals (lower threshold) ---')
colcnt = red[210:475, :].sum(axis=0)
top = np.argsort(colcnt)[::-1][:12]
print('top red columns (x, count):', sorted([(int(x), int(colcnt[x])) for x in top if colcnt[x] > 20]))

print('--- title cap height: S column band ---')
tsub = red[60:150, 179:210]
rows = np.where(tsub.sum(axis=1) > 0)[0]
print(f'title S x179..210 ink y {60+rows.min()}..{60+rows.max()} (h={rows.max()-rows.min()+1})')

print('--- ring markers: sample colors left of text ---')
for y in range(230, 250):
    for x in range(125, 152):
        px = im[y, x]
        if abs(int(px[0]) - int(px[1])) > 30 or abs(int(px[1]) - int(px[2])) > 30:
            print(f'colored px ({x},{y}): #{px[0]:02X}{px[1]:02X}{px[2]:02X}')

print('--- bullet line cap heights (dark<160) ---')
dark = (r < 160) & (g < 160) & (b < 160)
for lbl, (y0, y1, x0, x1) in {
    'L1 Images(cap I x152..165)': (225, 255, 152, 166),
    'L2 k-D (k x154..166)': (248, 275, 154, 167),
    'L2 RGB (R x154..167)': (272, 296, 154, 168),
    'L1 What (W x151..170)': (328, 358, 151, 171),
    'L2 Neighboring (N x154..170)': (350, 378, 154, 171),
}.items():
    sub = dark[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) > 0)[0]
    if len(rows):
        print(f'{lbl}: y {y0+rows.min()}..{y0+rows.max()} (h={rows.max()-rows.min()+1})')
    else:
        print(f'{lbl}: NO INK')

print('--- ring marker bboxes (any saturated non-dark px left of text) ---')
sat = (np.abs(r - g) > 25) | (np.abs(g - b) > 25) | (np.abs(r - b) > 25)
for lbl, (yy0, yy1) in [('ring L1a', 228), ('ring L2a', 250), ('ring L2b', 273), ('ring L1b', 330), ('ring L2c', 352)]:
    sub = sat[yy0:yy0 + 26, 120:152]
    rows = np.where(sub.sum(axis=1) > 0)[0]
    cols = np.where(sub.sum(axis=0) > 0)[0]
    if len(rows):
        y0a, y1a = yy0 + rows.min(), yy0 + rows.max()
        x0a, x1a = 120 + cols.min(), 120 + cols.max()
        cy, cx = (y0a + y1a) // 2, (x0a + x1a) // 2
        print(f'{lbl}: x {x0a}..{x1a} y {y0a}..{y1a} (d={max(y1a-y0a, x1a-x0a)+1}) center ({cx},{cy}) color #{im[cy, x0a+1, 0]:02X}{im[cy, x0a+1, 1]:02X}{im[cy, x0a+1, 2]:02X}')
    else:
        print(f'{lbl}: NO INK in x120..152')

print('--- meme true bbox (exclude red frame strokes) ---')
bg = (np.abs(r - g) < 12) & (np.abs(g - b) < 12) & (r > 225)
nonbg = ~bg & ~red
sub = nonbg[195:350, 620:916]
rows = np.where(sub.sum(axis=1) > 20)[0]
cols = np.where(sub.sum(axis=0) > 10)[0]
print(f'meme: x {620+cols.min()}..{620+cols.max()} (w={cols.max()-cols.min()+1})  y {195+rows.min()}..{195+rows.max()} (h={rows.max()-rows.min()+1})')

print('--- close-up photo proper (column/row profiles) ---')
sub = nonbg[380:505, 180:510]
colsum = sub.sum(axis=0)
photocols = [i for i, v in enumerate(colsum) if v > 25]
rowsum = sub.sum(axis=1)
photorows = [i for i, v in enumerate(rowsum) if v > 40]
print(f'photo cols x {180+photocols[0]}..{180+photocols[-1]}  rows y {380+photorows[0]}..{380+photorows[-1]}')
# corner check: photo is tilted; measure ink bbox of strong-photo region
strong = nonbg[380:505, 180:510]
rows2 = np.where(strong.sum(axis=1) > 5)[0]
cols2 = np.where(strong.sum(axis=0) > 5)[0]
print(f'closeup full ink: x {180+cols2.min()}..{180+cols2.max()} (w={cols2.max()-cols2.min()+1})  y {380+rows2.min()}..{380+rows2.max()} (h={rows2.max()-rows2.min()+1})')

print('--- cards clean bboxes (y336..477) ---')
redc = (r > 130) & (g < 95) & (b < 95)
greenc = (g > 105) & (r < 115) & (b < 115)
bluec = (b > 100) & (r < 115) & (g < 115)
for nm, m in [('red', redc), ('green', greenc), ('blue', bluec)]:
    sub = m[336:478, 605:902]
    rows = np.where(sub.sum(axis=1) > 3)[0]
    cols = np.where(sub.sum(axis=0) > 3)[0]
    print(f'{nm} card: x {605+cols.min()}..{605+cols.max()} (w={cols.max()-cols.min()+1})  y {336+rows.min()}..{336+rows.max()} (h={rows.max()-rows.min()+1})')

print('--- arrows: saturated stroke pixels in arrow zone, excluding closeup photo cols ---')
zone = im[385:500, 190:510]
rr, gg, bb = zone[:, :, 0], zone[:, :, 1], zone[:, :, 2]
# arrow strokes: saturated, not dark, not white
arr = ((np.abs(rr - gg) > 40) | (np.abs(gg - bb) > 40)) & ~((rr < 90) & (gg < 90) & (bb < 90))
ys, xs = np.where(arr)
pts = [(190 + x, 385 + y, int(rr[y, x]), int(gg[y, x]), int(bb[y, x])) for y, x in zip(ys, xs)]
# cluster by hue
import collections
def hueclass(R, G, B):
    if R > 200 and G > 190 and B < 150: return 'yellow'
    if R > 180 and G > 90 and B < 90 and G < 190: return 'orange'
    if B > 140 and G > 120 and R < 130: return 'cyan'
    if R > 150 and G < 100 and B < 100: return 'red'
    return None
clusters = collections.defaultdict(list)
for (x, y, R, G, B) in pts:
    h = hueclass(R, G, B)
    if h: clusters[h].append((x, y))
for h, lst in clusters.items():
    xs2 = [p[0] for p in lst]; ys2 = [p[1] for p in lst]
    cx = lst[len(lst) // 2]
    print(f'arrow {h}: n={len(lst)} x {min(xs2)}..{max(xs2)} y {min(ys2)}..{max(ys2)} mid color #{cx[2]:02X}{cx[3]:02X}{cx[4]:02X}')

print('--- cursor whites over cards (looser) ---')
wt = (r > 200) & (g > 200) & (b > 200)
sub = wt[350:430, 740:830]
rows = np.where(sub.sum(axis=1) > 0)[0]
cols = np.where(sub.sum(axis=0) > 0)[0]
if len(rows):
    print(f'cursor: x {740+cols.min()}..{740+cols.max()} y {350+rows.min()}..{350+rows.max()}')

print('--- bullet left edges (dark<160, per band, full x from 120) ---')
bands = [(228, 248), (250, 272), (272, 298), (328, 352), (352, 372)]
for (y0, y1) in bands:
    sub = dark[y0:y1, 120:600]
    cols = np.where(sub.sum(axis=0) > 0)[0]
    rows = np.where(sub.sum(axis=1) > 0)[0]
    if len(cols):
        print(f'band y{y0}-{y1}: x {120+cols.min()}..{120+cols.max()}  y {y0+rows.min()}..{y0+rows.max()}')
