#!/usr/bin/env python3
"""m8_likeforlike.py — like-for-like census: frame_046 vs frame_047 at the same mapped
positions (both frames share mapping SX=0.962329 OX=17.582 SY=0.955556 OY=0, landmark-
verified on 047: L58/R901/T43/B517). Slide-pt probe boxes -> frame px, census both."""
from PIL import Image
import numpy as np
from collections import Counter

F46 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg'
F47 = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
A46 = np.asarray(Image.open(F46).convert('RGB')).astype(int)
A47 = np.asarray(Image.open(F47).convert('RGB')).astype(int)

SX, OX, SY, OY = 0.962329, 17.582, 0.955556, 0.0

def box(sx, sy0, sy1, w=8):
    """slide x (center), slide y band -> frame box (x0,x1,y0,y1) with w frame px half-width"""
    fx = OX + SX * sx
    fy0, fy1 = SY * sy0, SY * sy1
    return (int(fx - w), int(fx + w), int(fy0), int(fy1))

def census(A, b, topn=5):
    x0, x1, y0, y1 = b
    reg = A[y0:y1, x0:x1].reshape(-1, 3)
    q = (reg // 16) * 16 + 8
    return Counter(map(tuple, q)).most_common(topn)

probes = [
    # label, slide x, slide y0, y1
    ('output row cells (col1)', 194.9, 67.3, 84.8),
    ('post-FFN row cells (col1)', 194.9, 180.4, 197.4),
    ('post-LN row cells (col1)', 194.9, 290.3, 307.8),
    ('out-of-attention row (col1)', 194.9, 401.2, 418.2),
    ('X row cells (col1)', 194.9, 509.0, 526.5),
    ('MHA bar', 500.0, 440.0, 460.0),
    ('top LN bar', 500.0, 107.0, 134.0),
    ('bottom LN bar', 500.0, 328.6, 356.0),
    ('plus disc top unit (col1)', 194.9, 148.0, 162.0),
    ('plus disc bottom unit (col1)', 194.9, 369.0, 383.0),
    ('FFN tile 1', 193.5, 240.7, 270.1),
    ('gap right of FFN tile 6', 640.0, 240.7, 270.1),
    ('green arrows top unit (col1)', 194.9, 135.1, 147.0),
    ('navy arrows top unit (col1)', 194.9, 163.2, 179.0),
    ('red arrows top unit (col1)', 194.9, 86.0, 105.0),
    ('orange curve col1 top unit', 194.9 - 26.0, 150.0, 300.0),
    ('block arrow zone2 (col1)', 194.9, 489.0, 509.0),
    ('block arrow FFN gap (col1)', 194.9, 198.8, 215.6),
    ('caption band', 412.2, 526.5, 540.0),
    ('callout', 100.0, 54.4, 105.7),
    ('badge zone', 875.0, 30.0, 80.0),
    ('container interior (empty spot)', 640.0, 296.0, 310.0),
    ('container interior 2', 350.0, 200.0, 205.0),
]
print(f"{'probe':38s} | frame_046 top colors | frame_047 top colors")
for label, sx, y0, y1 in probes:
    b = box(sx, y0, y1)
    c46, c47 = census(A46, b), census(A47, b)
    f46 = ' '.join(f'{r},{g},{b_}x{n}' for (r, g, b_), n in c46[:4])
    f47 = ' '.join(f'{r},{g},{"b"}x{n}'.replace(',b x', ',') for (r, g, b_), n in c47[:4])
    f47 = ' '.join(f'{r},{g},{bb}x{n}' for (r, g, bb), n in c47[:4])
    print(f'{label:38s} | {f46} | {f47}')
