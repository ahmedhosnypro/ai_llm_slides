#!/usr/bin/env python3
"""Stage 3b: paragraph lines via dark-ink profile; panel border via lower thresholds."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r + g + b) / 3

# text ink inside intro box: luminance < 175 (glyphs incl colored ones; highlights are light)
text = lum < 175
inner = np.zeros_like(text); inner[107:182, 92:888] = text[107:182, 92:888]
prof = inner.sum(axis=1)
lines, in_line = [], False
for y in range(107, 182):
    if prof[y] > 2 and not in_line: start, in_line = y, True
    elif prof[y] <= 2 and in_line: lines.append((start, y-1)); in_line = False
if in_line: lines.append((start, 181))
print('paragraph dark-ink line bands:', lines)
for (a, bb) in lines:
    ys, xs = np.where(inner[a:bb+1])
    print(f'  band y {a}..{bb}: x {xs.min()}..{xs.max()}')

# panel border: blackish strokes, print profiles
blackish = (r < 110) & (g < 110) & (b < 110)
sub = blackish[195:505, 120:580]
rowsum = sub.sum(axis=1)
print('panel rows with >100 black px:', [195+i for i,v in enumerate(rowsum) if v > 100])
colsum = sub.sum(axis=0)
print('panel cols with >60 black px:', [120+i for i,v in enumerate(colsum) if v > 60])
