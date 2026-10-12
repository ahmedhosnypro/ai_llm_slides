#!/usr/bin/env python3
"""measure5: title redo, output box, right container, input ellipse rows,
green arrow, q2/Wq, red arrow network endpoints, x2 highlight."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

def bb(name, x0, x1, y0, y1, fn, minpix=6):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if fn(*px[x, y]):
                xs.append(x)
                ys.append(y)
    if len(xs) < minpix:
        print('%-38s EMPTY (%d px)' % (name, len(xs)))
        return None
    print('%-38s x %3d..%3d  y %3d..%3d  n=%d' % (name, min(xs), max(xs), min(ys), max(ys), len(xs)))
    return (min(xs), max(xs), min(ys), max(ys))

print('== TITLE (excluding badge x>=845) ==')
anyink = lambda r, g, b: black_ink(r, g, b) or navy(r, g, b) or blue_mid(r, g, b) or red_ink(r, g, b) or dark_red(r, g, b)
l1 = bb('L1 ink', 60, 845, 44, 76, anyink)
l2 = bb('L2 ink', 60, 845, 76, 106, anyink)
bb('L1 black', 60, 845, 44, 76, black_ink)
bb('L1 blue', 60, 845, 44, 76, lambda r, g, b: navy(r, g, b) or blue_mid(r, g, b))
bb('L2 black', 60, 845, 76, 106, black_ink)
bb('L2 blue', 60, 845, 76, 106, lambda r, g, b: navy(r, g, b) or blue_mid(r, g, b))
bb('L2 red', 60, 845, 76, 106, lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))
bb('L1 red', 60, 845, 44, 76, lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))

print('== OUTPUT BOX + ARROW (x 480..680, y 105..215) ==')
dg = lambda r, g, b: dkgreen_border(r, g, b) or green_txt(r, g, b)
bb('output dashed green', 480, 680, 105, 215, dg)
for y in range(110, 200):
    s = ''.join('G' if dg(r, g, b) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(480, 680)))
    if 'G' in s:
        print('%4d %s' % (y, s))
print('-- bright green arrow fill (00B050-ish) --')
bg = lambda r, g, b: (30 <= r <= 110 and 150 <= g <= 210 and 50 <= b <= 120)
bb('green arrow', 480, 680, 105, 215, bg)
print('-- cells inside output box: census x 590..660, y 120..140 --')
from collections import Counter
c = Counter()
for y in range(118, 142):
    for x in range(585, 665):
        c['#%02X%02X%02X' % px[x, y]] += 1
for col, n in c.most_common(10):
    print('  ', col, n)
print('-- V label green text in output area --')
bb('V label', 480, 680, 110, 150, lambda r, g, b: green_txt(r, g, b) and not bg(r, g, b))
print('-- red arrowhead near arrow --')
bb('red head near arrow', 560, 640, 135, 175, lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))
print('-- gray guide line? --')
bb('gray line', 560, 640, 140, 200, lambda r, g, b: 150 <= r <= 185 and 150 <= g <= 185 and 145 <= b <= 185)

print('== RIGHT CONTAINER (x 740..900, y 180..420) ==')
bb('right container dashes', 740, 900, 180, 420, dg)
for y in range(185, 420):
    s = ''.join('G' if dg(r, g, b) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(740, 900)))
    if 'G' in s:
        print('%4d %s' % (y, s))
print('-- right container interior rows: cell colors x 800..880 --')
for y0, y1 in ((200, 240), (240, 280), (280, 320), (320, 360), (360, 400)):
    c = Counter()
    for y in range(y0, y1):
        for x in range(800, 880):
            c['#%02X%02X%02X' % px[x, y]] += 1
    print('  y %d..%d:' % (y0, y1), [k for k, v in c.most_common(5)])

print('== INPUT ELLIPSE rows (x 66..214, y 165..425) ==')
for y in range(165, 425):
    s = ''.join('B' if bluegray(r, g, b) else ('C' if (160 <= r <= 185 and 195 <= g <= 215 and 205 <= b <= 225) else ('K' if black_ink(r, g, b) else ('N' if (navy(r, g, b) or blue_mid(r, g, b)) else ('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ('Y' if (235 <= r <= 255 and 210 <= g <= 245 and 100 <= b <= 190) else ' '))))) for x, (r, g, b) in ((x, px[x, y]) for x in range(66, 214, 1)))
    if 'K' in s or 'N' in s or 'R' in s or 'Y' in s:
        print('%4d %s' % (y, s))
