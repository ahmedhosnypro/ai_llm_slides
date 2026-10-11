#!/usr/bin/env python3
"""Pass 5: leader tracing in restricted windows; callout edge/border check; fill modes."""
from PIL import Image
import collections

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
ld = im.load()

def bluish(p):
    r, g, b = p
    return b - r > 35 and b > 140 and g < 220

# window A: right of callout, above wait2 top (x 330..500, y 165..254)
print("A: callout leader (x330..500, y165..254):")
for y in range(165, 254):
    row = [x for x in range(330, 500) if bluish(ld[x, y])]
    if len(row) >= 1:
        print(f"  y={y}: {min(row)}..{max(row)} n={len(row)}")

# window B: below wait boxes to h-arrows (x 0..500, y 290..334), excluding box interiors
print("B: wait leaders (y290..334):")
for y in range(290, 334):
    row = [x for x in range(0, 500) if bluish(ld[x, y])]
    if len(row) >= 1:
        # split into runs
        runs, s = [], None
        prev = -10
        for x in row:
            if x - prev > 4:
                if s is not None: runs.append((s, prev))
                s = x
            prev = x
        runs.append((s, prev))
        print(f"  y={y}: runs={runs}")

# window C: right of wait2 (x 348..500, y 255..290)
print("C: right of wait2 (x348..500, y255..290):")
for y in range(255, 290):
    row = [x for x in range(348, 500) if bluish(ld[x, y])]
    if len(row) >= 1:
        print(f"  y={y}: {min(row)}..{max(row)} n={len(row)}")

# callout top edge profile at y=167..170, x 60..320 (border check)
print("callout top edge colors (y=167,168,169 at x=100,200,300):")
for y in (166, 167, 168, 169, 170):
    print(f"  y={y}: {ld[100, y]} {ld[200, y]} {ld[300, y]}")
# left edge at x=43..47, y=200
print("callout left edge x=42..48 at y=200:", [ld[x, 200] for x in range(42, 49)])

# clean fill modes
def mode(x0, y0, x1, y1):
    c = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[ld[x, y]] += 1
    return c.most_common(4)
print("callout fill (y215..222, x250..320):", mode(250, 215, 320, 222))
print("wait1 fill (y271..274, x60..170):", mode(60, 271, 170, 274))
print("wait2 fill (y268..271, x225..335):", mode(225, 268, 335, 271))

# encoder h1/h2 arrows in MY frame (verify parent geometry still holds): dark olive ink at y~329
def olive(p):
    r, g, b = p
    return 100 < r < 180 and 90 < g < 170 and b < 110 and r > b + 30 and g > b + 30
for y in (328, 329, 330):
    row = [x for x in range(46, 480) if olive(ld[x, y])]
    runs, s = [], None
    prev = -10
    for x in row:
        if x - prev > 5:
            if s is not None: runs.append((s, prev))
            s = x
        prev = x
    if s is not None: runs.append((s, prev))
    print(f"h-arrow row y={y}: runs={runs}")
