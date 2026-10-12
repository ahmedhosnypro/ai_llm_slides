#!/usr/bin/env python3
"""measure6: Wq box, X2 highlight, container rows, note internals, W labels, arrows."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *
from collections import Counter

print('== Wq box top edge: red pixels x 285..335, y 395..445 ==')
for y in range(395, 445):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(285, 335)))
    if 'R' in s:
        print('%4d %s' % (y, s))

print('== q2 label red x 275..300, y 390..420 ==')
for y in range(390, 420):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(270, 300)))
    if 'R' in s:
        print('%4d %s' % (y, s))
print('== q2 vector cells census x 295..330, y 405..425 ==')
c = Counter()
for y in range(405, 425):
    for x in range(295, 330):
        c['#%02X%02X%02X' % px[x, y]] += 1
print([k for k, v in c.most_common(8)])

print('== sentence container rows: cell colors per band x 215..455 ==')
for y0, y1 in ((456, 468), (468, 478), (478, 488), (488, 497)):
    c = Counter()
    for y in range(y0, y1):
        for x in range(215, 455):
            c['#%02X%02X%02X' % px[x, y]] += 1
    print('y %d..%d:' % (y0, y1), [k for k, v in c.most_common(7)])
print('== X2 dashed highlight scan x 240..340, y 455..500 ==')
for y in range(455, 500):
    s = ''.join('R' if (150 <= r <= 220 and g <= 90 and b <= 110) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(240, 340)))
    if 'R' in s:
        print('%4d %s' % (y, s))
print('== sentence X labels red x 200..470, y 456..497 ==')
for y in range(456, 497):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(200, 470)))
    if 'R' in s:
        print('%4d %s' % (y, s))

print('== right container rows: cell colors per band x 755..825 ==')
for y0, y1 in ((220, 240), (240, 260), (260, 280), (280, 300), (300, 320), (320, 340), (340, 360), (360, 381)):
    c = Counter()
    for y in range(y0, y1):
        for x in range(755, 825):
            c['#%02X%02X%02X' % px[x, y]] += 1
    print('y %d..%d:' % (y0, y1), [k for k, v in c.most_common(6)])
print('== right container X labels red x 790..830, y 217..381 ==')
for y in range(217, 381):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(790, 830)))
    if 'R' in s:
        print('%4d %s' % (y, s))
