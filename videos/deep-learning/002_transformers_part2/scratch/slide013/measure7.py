#!/usr/bin/env python3
"""measure7: right-container full dash map, dimension note internals, W label colors, arrows."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *
from collections import Counter

dg = lambda r, g, b: dkgreen_border(r, g, b) or green_txt(r, g, b)

print('== G-dash map x 730..900, y 205..400 (step1, mark G) ==')
for y in range(205, 400):
    s = ''.join('G' if dg(r, g, b) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(730, 900)))
    if 'G' in s:
        print('%4d %s' % (y, s))

print()
print('== dimension note internals x 724..884, y 446..511 (wide buckets) ==')
for y in range(446, 512):
    s = ''
    for x in range(724, 884):
        r, g, b = px[x, y]
        if dg(r, g, b): s += 'G'
        elif 235 <= r <= 255 and 200 <= g <= 245 and 120 <= b <= 200: s += 'Y'   # yellow cell
        elif 180 <= r <= 215 and 140 <= g <= 180 and 200 <= b <= 235: s += 'L'   # lavender cell
        elif 240 <= r <= 255 and 100 <= g <= 170 and 100 <= b <= 170: s += 'S'   # salmon cell
        elif red_ink(r, g, b) or dark_red(r, g, b): s += 'R'
        elif black_ink(r, g, b): s += 'K'
        elif navy(r, g, b) or blue_mid(r, g, b): s += 'N'
        elif white(r, g, b): s += 'W'
        else: s += '.'
    print('%4d %s' % (y, s))
