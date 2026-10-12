#!/usr/bin/env python3
"""Chrome landmark detection for slide_013.jpg (002 video, ~0.958 zoomed capture).
Finds: gray panel left/right/top red borders, bottom red stroke, yellow badge.
Fits frame->slide mapping against the playlist chrome constants (42,919,45,540 px,
badge center (893,71)). 1px=1pt on the TRUE slide."""
from PIL import Image
import json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_013.jpg').convert('RGB')
W, H = im.size
px = im.load()

def is_red(p):
    r, g, b = p
    return r > 130 and g < 90 and b < 90 and (r - max(g, b)) > 60

# --- vertical red borders: count red pixels per column in y 60..500
colcount = [0] * W
for x in range(W):
    c = 0
    for y in range(60, 500):
        if is_red(px[x, y]):
            c += 1
    colcount[x] = c

# candidate border columns: high count
cands = [x for x in range(W) if colcount[x] > 200]
print('red-column candidates:', cands)

# --- horizontal red rows: count red pixels per row in x 100..850
rowcount = [0] * H
for y in range(H):
    c = 0
    for x in range(100, 851):
        if is_red(px[x, y]):
            c += 1
    rowcount[y] = c
rows = [(y, rowcount[y]) for y in range(H) if rowcount[y] > 300]
print('red-row candidates (>300):', rows[:10], '...' if len(rows) > 10 else '')

# bottom stroke: strongest red row below y=480
bottom = None
best = 0
for y in range(480, H):
    if rowcount[y] > best:
        best = rowcount[y]
        bottom = y
print('bottom stroke row:', bottom, 'count', best)

# --- badge: yellow-ish FDFD96 in top-right region x>820, y<120
ys = []
xs = []
for y in range(0, 130):
    for x in range(820, W):
        r, g, b = px[x, y]
        if r > 225 and g > 225 and 90 < b < 200:
            xs.append(x)
            ys.append(y)
if xs:
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    print('badge yellow bbox: x %d..%d y %d..%d center (%.1f, %.1f) d~%.1f' % (
        bx0, bx1, by0, by1, (bx0 + bx1) / 2, (by0 + by1) / 2, (bx1 - bx0 + bx1 - bx0) / 2))

# --- sample colors along a horizontal line through the panel (y=300) to see panel edges
line = []
prev = None
for x in range(30, 70):
    p = px[x, 300]
    if p != prev:
        line.append((x, p))
        prev = p
print('y=300 x30..70 color changes:', line[:12])
line = []
prev = None
for x in range(880, 920):
    p = px[x, 300]
    if p != prev:
        line.append((x, p))
        prev = p
print('y=300 x880..920 color changes:', line[:12])
# top border: color changes along x=500, y 30..60
line = []
prev = None
for y in range(30, 60):
    p = px[500, y]
    if p != prev:
        line.append((y, p))
        prev = p
print('x=500 y30..60 color changes:', line[:12])
# bottom: x=500, y 505..530
line = []
prev = None
for y in range(505, 532):
    p = px[500, y]
    if p != prev:
        line.append((y, p))
        prev = p
print('x=500 y505..531 color changes:', line[:14])
