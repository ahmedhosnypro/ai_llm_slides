#!/usr/bin/env python3
"""m5_connectors.py — trace thin connector lines with a sensitive detector."""
from PIL import Image
import numpy as np

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# sensitive: any pixel meaningfully darker than the panel bg (231,233,230) OR reddish
lum = (R + G + B) / 3.0
bg = (np.abs(R - 231) < 7) & (np.abs(G - 233) < 7) & (np.abs(B - 230) < 7)
ink = ~bg
reddish = (R - G > 25) & (R - B > 25)

def colprofile(x0, x1, y0, y1, name):
    print('--- %s: per-column ink counts (y %d..%d)' % (name, y0, y1))
    for x in range(x0, x1):
        c = ink[y0:y1, x].sum()
        if c > 3:
            rr = reddish[y0:y1, x].sum()
            print('  x=%d ink=%d reddish=%d' % (x, c, rr))

def rowprofile(y0, y1, x0, x1, name):
    print('--- %s: per-row ink spans (x %d..%d)' % (name, x0, x1))
    for y in range(y0, y1):
        xs = np.where(ink[y, x0:x1])[0]
        if len(xs) > 2:
            print('  y=%d span %d..%d (n=%d)' % (y, x0 + xs.min(), x0 + xs.max(), len(xs)))

# 1. top connector band between root bottom (169) and boxes top (220)
rowprofile(170, 220, 215, 700, 'TOP-CONN')
# 2. spine region left of cyan boxes, below blue box
rowprofile(276, 500, 222, 262, 'SPINE')
# 3. right arrow between green box bottom (272) and leaf top (328)
rowprofile(274, 328, 640, 712, 'RIGHT-ARR')
