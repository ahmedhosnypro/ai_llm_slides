#!/usr/bin/env python3
"""Classify slide_017.jpg into named colors, print 3px-block ASCII map of the diagram."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape

def classify(px):
    r, g, b = px
    if abs(r-233) <= 10 and abs(g-232) <= 10 and abs(b-227) <= 10: return '.'   # gray panel
    if r > 246 and g > 246 and b > 246: return ' '                                # white
    # yellow highlight / callout
    if r > 210 and g > 210 and b < 190: return 'Y'
    # peach panel
    if r > 238 and 222 <= g <= 246 and 202 <= b <= 230: return 'p'
    # pale green panel
    if 195 <= r <= 232 and g > 232 and 202 <= b <= 232: return 'g'
    # tan box (darker tan in diagram)
    if 120 <= r <= 225 and 80 <= g <= 200 and 20 <= b <= 160 and r > g > b: return 'T'
    # light green box
    if 160 <= r <= 232 and 200 <= g <= 248 and 140 <= b <= 220 and g > r >= b: return 'L'
    # purple
    if 130 <= r <= 225 and 100 <= g <= 190 and 165 <= b <= 240 and b > r > g: return 'P'
    # dark red box / red arrow
    if r > 130 and g < 135 and b < 135 and r - g > 60: return 'R'
    # blue
    if b > 140 and b - r > 60 and b - g > 40: return 'B'
    # gray (N x)
    if 150 <= r <= 225 and abs(r-g) <= 12 and abs(g-b) <= 14: return 'N'
    # dark ink (text/black)
    if r < 130 and g < 130 and b < 130: return '#'
    return '?'

B = 3
rows = []
for y0 in range(90, 537, B):
    line = []
    for x0 in range(560, 957, B):
        # majority vote in block
        from collections import Counter
        c = Counter()
        for dy in range(B):
            for dx in range(B):
                c[classify(A[y0+dy, x0+dx])] += 1
        line.append(c.most_common(1)[0][0])
    rows.append((y0, ''.join(line)))

hdr = '     ' + ''.join(str((560 + i*B) // 100 % 10) if (560 + i*B) % 100 < B else ' ' for i in range(len(rows[0][1])))
print(hdr)
for y0, line in rows:
    print(f"{y0:3d}  {line}")
