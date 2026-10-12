#!/usr/bin/env python3
"""Palette clustering + exact edge scans for slide_026."""
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

# ---- palette of content area ----
cnt = Counter()
for y in range(185, 470):
    for x in range(400, 670):
        c = px[x, y]
        cnt[(c[0]//8*8, c[1]//8*8, c[2]//8*8)] += 1
print("--- TIDA-area palette top 18 (quantized/8) ---")
for c, n in cnt.most_common(18):
    print(c, n)

cnt2 = Counter()
for y in range(185, 470):
    for x in range(680, 860):
        c = px[x, y]
        cnt2[(c[0]//8*8, c[1]//8*8, c[2]//8*8)] += 1
print("--- right-panel palette top 14 ---")
for c, n in cnt2.most_common(14):
    print(c, n)

cnt3 = Counter()
for y in range(230, 395):
    for x in range(225, 390):
        c = px[x, y]
        cnt3[(c[0]//8*8, c[1]//8*8, c[2]//8*8)] += 1
print("--- blue-box palette top 10 ---")
for c, n in cnt3.most_common(10):
    print(c, n)

# ---- exact edge scans ----
def vscan(name, x, y0, y1):
    print(f"--- vscan {name} x={x} y={y0}..{y1} ---")
    prev = None
    for y in range(y0, y1):
        c = px[x, y]
        if c != prev:
            print(f"  y={y}: {c}")
            prev = c

def hscan(name, y, x0, x1):
    print(f"--- hscan {name} y={y} x={x0}..{x1} ---")
    prev = None
    for x in range(x0, x1):
        c = px[x, y]
        if c != prev:
            print(f"  x={x}: {c}")
            prev = c

# right panel top border thickness at x=760
vscan('rightpanel-top', 760, 184, 198)
# right panel left border at y=320
hscan('rightpanel-left', 320, 678, 700)
# right panel right border
hscan('rightpanel-right', 320, 845, 862)
# right panel bottom
vscan('rightpanel-bottom', 760, 458, 472)
# TIDA container top at x=450
vscan('tida-top', 450, 184, 196)
# TIDA container bottom
vscan('tida-bottom', 450, 460, 472)
# TIDA left/right edges at y=400
hscan('tida-left', 400, 395, 412)
hscan('tida-right', 400, 652, 672)
# blue box edges
vscan('blue-top', 300, 234, 246)
vscan('blue-bottom', 300, 382, 392)
hscan('blue-left', 300, 226, 238)
hscan('blue-right', 300, 374, 386)
# host box edges at y=300
hscan('host-left', 300, 390, 400)
hscan('host-right', 300, 410, 420)
vscan('host-top', 404, 248, 262)
vscan('host-bottom', 404, 378, 392)
