#!/usr/bin/env python3
"""m4_precise.py — strict re-measurement of slide_041.jpg content + color census."""
from PIL import Image
import numpy as np, json

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

SX = lambda fx: 42 + (fx - 58.5) * (919 - 42) / (901 - 58.5)
SY = lambda fy: 45 + (fy - 43.0) * (540 - 45) / (517.0 - 43.0)
def sl(bb):
    x0, y0, x1, y1 = bb
    return [round(SX(x0), 1), round(SY(y0), 1), round(SX(x1), 1), round(SY(y1), 1)]
def show(name, bb, extra=''):
    if bb is None: print(name, 'EMPTY'); return
    print('%-13s frame[%d,%d -> %d,%d] npx=%-6d slide[%s] %s' % (
        name, bb[0], bb[1], bb[2], bb[3], bb[4], ','.join(str(v) for v in sl(bb[:4])), extra))

# strict fill masks
peach  = (R > 238) & (G > 208) & (G < 246) & (B > 185) & (B < 228) & ((G - B) > 8) & ((R - G) > 12)
navy   = (R < 80) & (G < 80) & (B > 95)
green  = (R < 90) & (G > 85) & (G < 175) & (B < 110) & ((G - B) > 30)
lcyan  = (R > 195) & (R < 240) & (G > 243) & (B > 233)
lgreen = (R > 195) & (R < 240) & (G > 243) & (B > 195) & (B < 240) & ((G - B) > 10)
redink = (R > 120) & (G < 95) & (B < 95)
reddish = (R - G > 40) & (R - B > 40)
white  = (R > 215) & (G > 215) & (B > 215)
dkgreen = (R < 120) & (G > 70) & (G < 170) & (B < 120)

def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(len(xs))]

def lines_of(mask, x0, y0, x1, y1, gap=2):
    """split a text bbox into per-line runs via row-occupancy gaps"""
    sub = mask[y0:y1, x0:x1]
    rows = sub.sum(axis=1)
    runs, inr, s = [], False, 0
    for i, v in enumerate(rows):
        if v > 0 and not inr: inr, s = True, i
        elif v == 0 and inr:
            inr = False
            runs.append((y0 + s, y0 + i - 1))
    if inr: runs.append((y0 + s, y0 + len(rows) - 1))
    # merge runs separated by < gap rows
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], r[1])
        else: merged.append(list(r) if isinstance(r, tuple) else r)
    out = []
    for (a, b) in merged:
        out.append(bbox(mask, x0, a, x1, b + 1))
    return out

print('=== TITLE')
t = bbox(redink, 150, 55, 800, 112)
show('title', t)
for ln in lines_of(redink, 150, 55, 800, 112): show('  title_line', ln)

print('=== ROOT')
rb = bbox(peach, 300, 105, 640, 195)
show('root_box', rb)
for ln in lines_of(redink, rb[0] + 2, rb[1] + 2, rb[2] - 2, rb[3] - 2): show('  root_line', ln)

print('=== BLUE')
nb = bbox(navy, 100, 195, 400, 300)
show('blue_box', nb)
for ln in lines_of(white, nb[0] + 2, nb[1] + 2, nb[2] - 2, nb[3] - 2): show('  blue_line', ln)

print('=== GREEN parent')
gb = bbox(green, 520, 195, 830, 300)
show('green_box', gb)
for ln in lines_of(white, gb[0] + 2, gb[1] + 2, gb[2] - 2, gb[3] - 2): show('  green_line', ln)

print('=== CYAN STACK (strict)')
runs, inr = [], False
rowhas = lcyan[:, 240:540].sum(axis=1)
for y in range(280, 515):
    if rowhas[y] > 60 and not inr: inr, y0 = True, y
    elif rowhas[y] <= 60 and inr:
        inr = False; runs.append((y0, y - 1))
if inr: runs.append((y0, 514))
print('cyan runs:', runs)
cyans = []
for i, (y0, y1) in enumerate(runs):
    cb = bbox(lcyan, 200, y0 - 2, 560, y1 + 3)
    show('cyan%d_box' % (i + 1), cb)
    cyans.append(cb)
    tb = bbox(navy, cb[0] + 2, cb[1] + 2, cb[2] - 2, cb[3] - 2)
    show('  cyan%d_txt' % (i + 1), tb)

print('=== GREEN LEAF')
gl = bbox(lgreen, 500, 300, 850, 400)
show('grnleaf_box', gl)
gt = bbox(dkgreen, gl[0] + 2, gl[1] + 2, gl[2] - 2, gl[3] - 2)
show('  grnleaf_txt', gt)
# split text into bold word + rest via column profile inside the text bbox
if gt:
    sub = dkgreen[gt[1]:gt[3] + 1, gt[0]:gt[2] + 1]
    cols = sub.sum(axis=0)
    gaps = [j for j in range(len(cols)) if cols[j] == 0]
    print('  text col-gap runs (first 10):', gaps[:10])

print('=== CONNECTORS (loose reddish)')
# top connector region between root bottom and parents top
ct = bbox(reddish, 200, 168, 700, 219)
show('conn_top', ct)
# row/col profile of the top connector
sub = reddish[168:219, 200:700]
rows = sub.sum(axis=1)
print('conn_top row occupancy y168..218:', {168 + i: int(v) for i, v in enumerate(rows) if v > 0})
# spine + arrows: region left of cyan boxes
sp = bbox(reddish, 215, 276, 265, 500)
show('conn_spine', sp)
sub2 = reddish[276:500, 215:265]
rows2 = sub2.sum(axis=1)
print('spine row occupancy (first/last 12):', {276 + i: int(v) for i, v in enumerate(rows2) if v > 0})
# right arrow
ra = bbox(reddish, 640, 274, 720, 330)
show('conn_right', ra)
sub3 = reddish[274:330, 640:720]
rows3 = sub3.sum(axis=1)
print('right arrow row occupancy:', {274 + i: int(v) for i, v in enumerate(rows3) if v > 0})

print('=== COLOR CENSUS (deep interior cores)')
def census(name, x0, y0, x1, y1):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    med = np.median(px, axis=0).astype(int)
    print('%-14s median(%d,%d,%d) hex #%02X%02X%02X  n=%d' % (name, med[0], med[1], med[2], med[0], med[1], med[2], len(px)))
census('title_red', 400, 75, 420, 88)
census('root_fill', 360, 118, 390, 130)
census('root_text', 400, 128, 410, 138)  # may mix fill
census('blue_fill', 140, 230, 170, 240)
census('cyan_fill', 300, 298, 340, 306)
census('grnleaf_fill', 600, 332, 640, 338)
census('green_fill', 580, 228, 610, 238)
census('panel_bg', 100, 300, 120, 320)
# red connector core
ys, xs = np.where(reddish[168:219, 200:700])
if len(xs): census('conn_red', 200 + xs.min(), 168, 200 + xs.max() + 1, 219)
# navy text core
ys, xs = np.where(navy[307:322, 282:474])
if len(xs):
    px = im[307:322, 282:474][navy[307:322, 282:474]]
    dk = px[px[:, 2] < 150]
    print('cyan text dark-core median:', np.median(dk, axis=0).astype(int), 'n=%d/%d' % (len(dk), len(px)))
# green leaf text core
ys, xs = np.where(dkgreen[339:359, 573:777])
if len(xs):
    px = im[339:359, 573:777][dkgreen[339:359, 573:777]]
    print('grnleaf text median:', np.median(px, axis=0).astype(int), 'n=%d' % len(px))
# root text red core
ys, xs = np.where(redink[124:163, 387:525])
if len(xs):
    px = im[124:163, 387:525][redink[124:163, 387:525]]
    print('root text red-core median:', np.median(px, axis=0).astype(int), 'n=%d' % len(px))
# title red core
ys, xs = np.where(redink[68:93, 345:565])
if len(xs):
    px = im[68:93, 345:565][redink[68:93, 345:565]]
    print('title red-core median:', np.median(px, axis=0).astype(int), 'n=%d' % len(px))
