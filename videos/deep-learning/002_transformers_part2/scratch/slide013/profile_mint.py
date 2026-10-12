#!/usr/bin/env python3
"""Vertical profile inside mint ellipse + blue-gray ellipse interiors."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *
from collections import Counter

def profile(name, x0, x1, y0, y1, dom, minfrac=0.15):
    print('== %s ==' % name)
    for y in range(y0, y1):
        c = Counter()
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if dom(r, g, b):
                c['DOM'] += 1
            else:
                c['#%02X%02X%02X' % (r, g, b)] += 1
        domn = c.pop('DOM', 0)
        tot = x1 - x0
        if tot - domn > tot * 0.25:  # rows with >25% non-dominant
            tops = ', '.join('%s:%d' % (k, v) for k, v in c.most_common(4))
            print('y=%d dom=%3d%% | %s' % (y, 100 * domn // tot, tops))

mintf = lambda r, g, b: mint(r, g, b)
profile('MINT ellipse x224..252', 224, 252, 172, 422, mintf)
