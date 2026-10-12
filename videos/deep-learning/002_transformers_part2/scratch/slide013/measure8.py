#!/usr/bin/env python3
"""measure8: input ellipse rows 254-425, arrows, arrow/box borders, q2 vector, dot halo."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *
from collections import Counter

print('== INPUT ELLIPSE rows 254..425 (K/N/R/Y marks; x 66..214) ==')
for y in range(254, 425):
    s = ''.join('B' if bluegray(r, g, b) else ('C' if (160 <= r <= 185 and 195 <= g <= 215 and 205 <= b <= 225) else ('K' if black_ink(r, g, b) else ('N' if (navy(r, g, b) or blue_mid(r, g, b)) else ('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ('Y' if (235 <= r <= 255 and 210 <= g <= 245 and 100 <= b <= 190) else ' '))))) for x, (r, g, b) in ((x, px[x, y]) for x in range(66, 214)))
    if 'K' in s or 'N' in s or 'R' in s or 'Y' in s:
        print('%4d %s' % (y, s))
print()
print('== input ellipse row-1 cells: colors x 80..145, y 219..228 ==')
c = Counter()
for y in range(219, 229):
    for x in range(80, 146):
        c['#%02X%02X%02X' % px[x, y]] += 1
print([k for k, v in c.most_common(10)])
print('== rows y bands: dominant non-B color per band x 75..145 ==')
for y0, y1 in ((219, 228), (232, 244), (247, 258), (261, 272), (276, 288), (291, 302), (306, 318), (321, 332), (336, 348), (351, 362), (366, 378), (381, 392), (396, 407), (411, 422)):
    c = Counter()
    for y in range(y0, y1):
        for x in range(75, 146):
            r, g, b = px[x, y]
            if not bluegray(r, g, b) and not (160 <= r <= 185 and 195 <= g <= 215 and 205 <= b <= 225):
                c['#%02X%02X%02X' % (r, g, b)] += 1
    print('y %d..%d:' % (y0, y1), [k for k, v in c.most_common(5)])
print()
print('== sigma box border: col x=560, y 184..216 ==')
prev = None
for y in range(184, 216):
    c2 = '#%02X%02X%02X' % px[560, y]
    if c2 != prev:
        print('%d:%s' % (y, c2), end=' '); prev = c2
print()
print('== softmax border: row y=250, x 452..495 ==')
prev = None
for x in range(452, 495):
    c2 = '#%02X%02X%02X' % px[x, 250]
    if c2 != prev:
        print('%d:%s' % (x, c2), end=' '); prev = c2
print()
print('== pill border: Similarity row y=168, x 272..350 ==')
prev = None
for x in range(272, 350):
    c2 = '#%02X%02X%02X' % px[x, 168]
    if c2 != prev:
        print('%d:%s' % (x, c2), end=' '); prev = c2
print()
print('== mint ellipse border: row y=300, x 205..220 ==')
prev = None
for x in range(205, 220):
    c2 = '#%02X%02X%02X' % px[x, 300]
    if c2 != prev:
        print('%d:%s' % (x, c2), end=' '); prev = c2
print()
print('== dot1 halo: row y=238, x 328..350 ==')
prev = None
for x in range(328, 351):
    c2 = '#%02X%02X%02X' % px[x, 238]
    if c2 != prev:
        print('%d:%s' % (x, c2), end=' '); prev = c2
print()
print('== q2 vector: focused census x 286..320, y 400..416 ==')
c = Counter()
for y in range(400, 416):
    for x in range(286, 320):
        c['#%02X%02X%02X' % px[x, y]] += 1
print([k for k, v in c.most_common(12)])
