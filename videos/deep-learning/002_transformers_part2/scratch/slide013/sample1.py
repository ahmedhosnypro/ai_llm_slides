#!/usr/bin/env python3
"""Sample dominant colors in rectangles to decode translucent/overlaid fills."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *
from collections import Counter

def census(name, x0, x1, y0, y1, topn=12):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    tot = (x1 - x0) * (y1 - y0)
    print('%s (%dx%d):' % (name, x1 - x0, y1 - y0))
    for col, n in c.most_common(topn):
        print('   #%02X%02X%02X %5d %4.1f%%' % (col[0], col[1], col[2], n, 100.0 * n / tot))

# input ellipse interior bands (ellipse x69..197 y169..423); sample a left strip x 75..115
print('== INPUT ELLIPSE strip x75..115, y-bands ==')
for y0, y1 in ((175, 210), (210, 250), (250, 290), (290, 330), (330, 370), (370, 420)):
    census('y %d..%d' % (y0, y1), 75, 115, y0, y1, 6)
print()
# middle of ellipse x 115..165
print('== INPUT ELLIPSE strip x115..165 ==')
for y0, y1 in ((175, 215), (215, 255), (255, 295), (295, 335), (335, 375), (375, 415)):
    census('y %d..%d' % (y0, y1), 115, 165, y0, y1, 6)
print()
# mint ellipse interior: x 218..258, y bands
print('== MINT ELLIPSE x218..258 y-bands ==')
for y0, y1 in ((178, 215), (215, 260), (260, 305), (305, 350), (350, 395), (395, 418)):
    census('y %d..%d' % (y0, y1), 218, 258, y0, y1, 8)
