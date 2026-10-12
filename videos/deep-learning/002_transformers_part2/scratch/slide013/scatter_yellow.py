#!/usr/bin/env python3
"""Yellow scatter in left region + K-vector/label search between ellipses."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

def yellowish(r, g, b):
    return r >= 235 and g >= 210 and 100 <= b <= 200 and (r - b) > 45

print('== yellow scatter x 195..270, y 200..400 (step1, cols=x) ==')
for y in range(200, 400):
    s = ''.join('Y' if yellowish(*px[x, y]) else ' ' for x in range(195, 270))
    if 'Y' in s:
        print('%4d %s' % (y, s))

print()
print('== dark-green text scatter (K labels?) x 195..270, y 200..400 ==')
for y in range(200, 400):
    s = ''.join('G' if (green_txt(r, g, b) or dkgreen_border(r, g, b)) else ' ' for x, (r, g, b) in ((x, px[x, y]) for x in range(195, 270)))
    if 'G' in s:
        print('%4d %s' % (y, s))
