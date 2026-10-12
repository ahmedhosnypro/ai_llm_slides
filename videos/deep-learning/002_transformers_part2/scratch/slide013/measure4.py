#!/usr/bin/env python3
"""measure4: multiply circles scatter, sentence container, dimension note,
output box, right container, input-ellipse rows, title redo, green arrow."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

print('== multiply circles red scatter x 495..625, y 225..395 ==')
for y in range(225, 395):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(495, 625)))
    if 'R' in s:
        print('%4d %s' % (y, s))
print()
print('== circle fill probe: census x 540..590, y 245..275 ==')
from collections import Counter
c = Counter()
for y in range(245, 275):
    for x in range(540, 590):
        c['#%02X%02X%02X' % px[x, y]] += 1
for col, n in c.most_common(8):
    print('  ', col, n)

print('== sentence container: dark-green dashed border scatter x 170..480, y 425..505 ==')
for y in range(425, 505):
    s = ''.join('G' if dkgreen_border(r, g, b) or green_txt(r, g, b) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(170, 480)))
    if 'G' in s:
        print('%4d %s' % (y, s))
print('== sentence container fill census x 200..260, y 450..490 ==')
c = Counter()
for y in range(450, 490):
    for x in range(200, 260):
        c['#%02X%02X%02X' % px[x, y]] += 1
for col, n in c.most_common(6):
    print('  ', col, n)
print('== X2 red-dashed highlight: red scatter x 240..330, y 430..505 ==')
for y in range(430, 505):
    s = ''.join('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(240, 330)))
    if 'R' in s:
        print('%4d %s' % (y, s))

print('== dimension note: white box + internals x 720..900, y 420..516 ==')
for y in range(420, 516):
    s = ''.join('W' if white(r, g, b) else ('G' if (dkgreen_border(r, g, b) or green_txt(r, g, b)) else ('R' if (red_ink(r, g, b) or dark_red(r, g, b)) else ('N' if (navy(r, g, b) or blue_mid(r, g, b)) else ('y' if yellowbox(r, g, b) else ('K' if black_ink(r, g, b) else ' '))))) for x, (r, g, b) in ((x, px[x, y]) for x in range(720, 900)))
    if s.strip():
        print('%4d %s' % (y, s))
