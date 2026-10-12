#!/usr/bin/env python3
"""Remaining structures for slide_026."""
from PIL import Image
from collections import deque, Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def is_red(c):
    return c[0] > 150 and c[1] < 90 and c[2] < 90

# 1. arrow bbox: all red pixels x 120-230, y 285-325
minx = miny = 99999; maxx = maxy = -1
rows = {}
for y in range(285, 326):
    xs = [x for x in range(120, 235) if is_red(px[x, y])]
    if xs:
        rows[y] = (min(xs), max(xs))
        minx = min(minx, min(xs)); maxx = max(maxx, max(xs))
        miny = min(miny, y); maxy = max(maxy, y)
print("ARROW red bbox:", (minx, miny, maxx, maxy))
for y in sorted(rows):
    if y % 2 == 0 or y in (miny, maxy):
        print(f"  y={y}: x {rows[y][0]}..{rows[y][1]}")

# arrow label bbox (red text below)
minx = miny = 99999; maxx = maxy = -1
for y in range(318, 360):
    for x in range(120, 240):
        c = px[x, y]
        if c[0] > 130 and c[1] < 110 and c[2] < 110:
            minx = min(minx, x); maxx = max(maxx, x)
            miny = min(miny, y); maxy = max(maxy, y)
print("ARROW LABEL red-ish bbox:", (minx, miny, maxx, maxy))

# 2. title/subtitle exact ink bboxes
def ink_bbox(x0, y0, x1, y1, pred):
    mnx = mny = 99999; mxx = mxy = -1
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                mnx = min(mnx, x); mxx = max(mxx, x)
                mny = min(mny, y); mxy = max(mxy, y)
    return (mnx, mny, mxx, mxy)

print("title ink bbox:", ink_bbox(300, 50, 660, 85, lambda c: c[0] > 130 and c[1] < 110 and c[2] < 110))
print("subtitle ink bbox:", ink_bbox(150, 80, 800, 103, lambda c: c[2] > 120 and c[2] - c[0] > 30 and c[0] < 180))
print("caption1 bbox:", ink_bbox(300, 475, 820, 493, lambda c: c[0] > 130 and c[1] < 110 and c[2] < 110))
print("caption2 bbox:", ink_bbox(300, 493, 820, 510, lambda c: c[0] > 130 and c[1] < 110 and c[2] < 110))

# mode of dark pixels for text colors
def dark_mode(x0, y0, x1, y1, lmax=150):
    cnt = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if c[0]+c[1]+c[2] < lmax*3:
                cnt[(c[0]//16*16, c[1]//16*16, c[2]//16*16)] += 1
    return cnt.most_common(5)

print("title dark mode:", dark_mode(371, 58, 553, 79, 120))
print("subtitle dark mode:", dark_mode(207, 83, 722, 99, 140))
print("caption dark mode:", dark_mode(333, 479, 775, 505, 130))

# 3. TIDA interior dense: green triangle after Dual ADC (x 525-600, y 246-300)
print("--- hscan y=260 x=525..605 ---")
prev = None
for x in range(525, 606):
    c = px[x, 260]
    k = tuple(v//14 for v in c)
    if k != prev:
        print(f"  x={x}: {c}")
        prev = k
print("--- hscan y=290 x=525..615 ---")
prev = None
for x in range(525, 616):
    c = px[x, 290]
    k = tuple(v//14 for v in c)
    if k != prev:
        print(f"  x={x}: {c}")
        prev = k
print("--- vscan x=545 y=246..300 ---")
prev = None
for y in range(246, 301):
    c = px[545, y]
    k = tuple(v//14 for v in c)
    if k != prev:
        print(f"  y={y}: {c}")
        prev = k

# green comps in TIDA upper (triangles)
def comps_pred(x0, y0, x1, y1, pred, min_size=40):
    seen = set()
    out = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not pred(px[x, y]):
                continue
            q = deque([(x, y)]); seen.add((x, y))
            mnx = mxx = x; mny = mxy = y; n = 0
            while q:
                cx, cy = q.popleft(); n += 1
                mnx = min(mnx, cx); mxx = max(mxx, cx)
                mny = min(mny, cy); mxy = max(mxy, cy)
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    p = (cx+dx, cy+dy)
                    if p in seen or not (x0 <= p[0] < x1 and y0 <= p[1] < y1):
                        continue
                    if pred(px[p[0], p[1]]):
                        seen.add(p); q.append(p)
            if n >= min_size:
                out.append((n, mnx, mny, mxx, mxy))
    out.sort(reverse=True)
    return out

isgreen = lambda c: c[1] > 120 and c[1] - c[0] > 30 and c[1] - c[2] > 20
print("green comps TIDA:", comps_pred(403, 188, 659, 466, isgreen, 40)[:12])
is_orange = lambda c: c[0] > 180 and 100 < c[1] < 200 and c[2] < 150 and c[0]-c[2] > 60
print("orange comps TIDA:", comps_pred(403, 188, 659, 466, is_orange, 40)[:12])
