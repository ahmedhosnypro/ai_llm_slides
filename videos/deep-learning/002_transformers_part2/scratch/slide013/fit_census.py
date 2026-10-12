#!/usr/bin/env python3
"""Fit frame->slide mapping for slide_013 and census the shape colors."""
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_013.jpg').convert('RGB')
W, H = im.size
px = im.load()

# Mapping from my landmarks: left 58<->42, right 901<->919, top 43<->45, bottom 516.5<->540
sx = (901 - 58) / (919 - 42)          # 0.961232
ax = 58 - sx * 42                      # 17.628
sy = (516.5 - 43) / (540 - 45)         # 0.958502 (top: 43/45=0.95556 through origin)
# use through-origin fit like slide_002 (top 43/45 = 0.955556; bottom predicts 516.0 ~ measured 516.5-517)
sy2 = 43 / 45
print('sx=%.6f ax=%.4f  sy_twopt=%.6f sy_origin=%.6f' % (sx, ax, sy, sy2))
print('badge center frame (875.5,71) -> slide (%.1f, %.1f)' % ((875.5 - ax) / sx, 71 / sy2))

def to_slide(fx, fy):
    return ((fx - ax) / sx, fy / sy2)

# ---- color census inside the panel (exclude chrome/letterbox)
c = Counter()
for y in range(46, 516):
    for x in range(59, 901):
        c[px[x, y]] += 1
print('\nTop 40 colors inside panel:')
for col, n in c.most_common(40):
    print('#%02X%02X%02X' % col, n)
