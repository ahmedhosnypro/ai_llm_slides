#!/usr/bin/env python3
"""Fine structure: white boxes in TIDA, columns/rows scans, text cores, arrow, connector."""
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def is_white(c):
    return c[0] > 243 and c[1] > 243 and c[2] > 240

# ---- 1. white components inside TIDA container (x 402-660, y 187-467) ----
def white_comps(x0, y0, x1, y1, min_size=200):
    seen = set()
    comps = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not is_white(px[x, y]):
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
                    if is_white(px[p[0], p[1]]):
                        seen.add(p); q.append(p)
            if n >= min_size:
                comps.append((n, mnx, mny, mxx, mxy))
    comps.sort(reverse=True)
    return comps

print("--- white comps in TIDA (x402-660 y187-467) ---")
for c in white_comps(403, 188, 659, 466)[:16]:
    print(c)
print("--- white comps in right panel (x690-850 y192-462) ---")
for c in white_comps(695, 195, 849, 460)[:12]:
    print(c)
print("--- white comps in blue box (x233-379 y240-386) ---")
for c in white_comps(234, 241, 378, 385, 100)[:10]:
    print(c)

# ---- 2. column scans ----
def vscan(name, x, y0, y1, step=1):
    print(f"--- vscan {name} x={x} ---")
    prev = None
    for y in range(y0, y1, step):
        c = px[x, y]
        key = tuple(v//12 for v in c)
        if key != prev:
            print(f"  y={y}: {c}")
            prev = key

def hscan(name, y, x0, x1, step=1):
    print(f"--- hscan {name} y={y} ---")
    prev = None
    for x in range(x0, x1, step):
        c = px[x, y]
        key = tuple(v//12 for v in c)
        if key != prev:
            print(f"  x={x}: {c}")
            prev = key

vscan('upper-TIDA x=470 (16bit box?)', 470, 214, 248)
vscan('mid-TIDA x=500 (adc/triangle)', 500, 246, 300)
vscan('mid-TIDA x=500 (analog path)', 500, 316, 395)
vscan('lower-TIDA x=500 (comparators/psu)', 500, 395, 467)
vscan('encoder-conn x=657', 657, 275, 400)
vscan('24v x=425', 425, 420, 460)
vscan('blue sub-blocks x=300', 300, 250, 390)
hscan('upper-TIDA y=235', 235, 440, 620, 2)
hscan('psu-row y=437', 437, 404, 660, 2)
hscan('arrow y=306', 306, 135, 225)
vscan('arrow x=200', 200, 292, 322)
vscan('arrow-tip x=160', 160, 292, 322)

# ---- 3. text cores ----
def core_color(x0, y0, x1, y1, pick='dark'):
    best = None
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            l = c[0]+c[1]+c[2]
            if pick == 'dark':
                if best is None or l < best[0]:
                    best = (l, c)
            else:
                if best is None or l > best[0]:
                    best = (l, c)
    return best

print("title core:", core_color(371, 60, 553, 78))
print("subtitle core:", core_color(207, 84, 722, 98))
print("caption1 core:", core_color(333, 480, 775, 492))
print("caption2 core:", core_color(434, 494, 679, 505))
print("arrowlabel core:", core_color(142, 322, 197, 355))
print("arrow red core:", core_color(156, 298, 214, 314))
print("badge numeral core:", core_color(862, 60, 888, 82))
print("tida tag text core:", core_color(578, 194, 650, 208))
