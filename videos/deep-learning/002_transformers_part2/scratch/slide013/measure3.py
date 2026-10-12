#!/usr/bin/env python3
"""measure3: DP edges/dots clusters, multiply circles, Wv column, V labels,
right container, output box, sentence container, dimension note, title redo."""
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
        print('%-36s EMPTY (%d px)' % (name, len(xs)))
        return None
    print('%-36s x %3d..%3d  y %3d..%3d  n=%d' % (name, min(xs), max(xs), min(ys), max(ys), len(xs)))
    return (min(xs), max(xs), min(ys), max(ys))

print('== DP right edge (row y=250, x 340..385) ==')
prev = None
for x in range(340, 385):
    c = '#%02X%02X%02X' % px[x, 250]
    if c != prev and (prev is None or abs(px[x,250][0]-int(prev[1:3],16)) > 18):
        print('%d:%s' % (x, c), end=' ')
    prev = c
print()
print('== DP title text rows (x 275..345, y 192..220) ==')
for y in range(192, 220):
    s = ''.join('T' if (r <= 130 and g <= 110 and b <= 110) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(275, 350)))
    if 'T' in s:
        print('%4d %s' % (y, s))
print('== DP K.q rows (x 345..380, y 190..210) ==')
for y in range(190, 210):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(345, 380)))
    if 'R' in s:
        print('%4d %s' % (y, s))
print('== DP dots: navy cluster rows (x 275..350, y 225..375) ==')
for y in range(225, 375):
    s = ''.join('N' if navy(r, g, b) else ('h' if (140 <= r <= 190 and 185 <= g <= 215 and 225 <= b <= 250) else ' ') for x, (r, g, b) in ((x, px[x, y]) for x in range(275, 350)))
    if 'N' in s or 'h' in s:
        print('%4d %s' % (y, s))

print()
print('== multiply circles: white blobs x 495..625, y 225..395 ==')
for y in range(225, 395):
    s = ''.join('W' if white(r, g, b) else ('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ') for x, (r, g, b) in ((x, px[x, y]) for x in range(495, 625)))
    if 'W' in s:
        print('%4d %s' % (y, s))

print()
print('== Wv band: colors row y=300, x 680..745 ==')
prev = None
for x in range(680, 745):
    c = '#%02X%02X%02X' % px[x, 300]
    if c != prev:
        print('%d:%s' % (x, c), end=' ')
        prev = c
print()
print('== Wv band rows (x 690..735, y 210..390): yellow runs ==')
rp = [any(240 <= px[x,y][0] <= 255 and 238 <= px[x,y][1] <= 255 and 85 <= px[x,y][2] <= 135 for x in range(690, 735)) for y in range(210, 390)]
print([(a+210, b+210) for a, b in runs(rp, 2)])
print('== Wv box borders (dark olive) x 685..740 ==')
for y in range(215, 390):
    s = ''.join('G' if (55 <= r <= 115 and 100 <= g <= 155 and 55 <= b <= 110) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(685, 740)))
    if 'G' in s:
        print('%4d %s' % (y, s))
print('== V labels red (x 620..690, y 215..390) ==')
for y in range(215, 390):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(620, 690)))
    if 'R' in s:
        print('%4d %s' % (y, s))
