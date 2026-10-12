#!/usr/bin/env python3
"""Fine profiles: mint ellipse center column + horizontal cuts through W_k boxes."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

print('== column x=237, y 215..385 (mint ellipse center) ==')
prev = None
for y in range(215, 385):
    r, g, b = px[237, y]
    s = '#%02X%02X%02X' % (r, g, b)
    if s != prev:
        print('y=%d %s' % (y, s))
        prev = s

print()
print('== row y=230 (through W_k text band 1), x 210..266 ==')
prev = None
for x in range(210, 266):
    r, g, b = px[x, 230]
    s = '#%02X%02X%02X' % (r, g, b)
    if s != prev:
        print('x=%d %s' % (x, s))
        prev = s

print()
print('== row y=245 (between text bands), x 210..266 ==')
prev = None
for x in range(210, 266):
    r, g, b = px[x, 245]
    s = '#%02X%02X%02X' % (r, g, b)
    if s != prev:
        print('x=%d %s' % (x, s))
        prev = s

print()
print('== row y=258, x 210..266 ==')
prev = None
for x in range(210, 266):
    r, g, b = px[x, 258]
    s = '#%02X%02X%02X' % (r, g, b)
    if s != prev:
        print('x=%d %s' % (x, s))
        prev = s
