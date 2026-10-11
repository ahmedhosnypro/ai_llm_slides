#!/usr/bin/env python3
"""Measure pass 3: logo full extent (white panel incl.), badge numeral, title x-extents."""
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
px = im.load()
PPI = W / 13.33

def ih(x): return round(x / PPI, 3)
def iv(y): return round(y / (H / 7.5), 3)

# logo region: y 465..530, x 560..935 — find near-white and dark pixels (exclude frame stroke x>=918)
print("== logo: column profile of non-canvas pixels (y 466..528, x 560..917) ==")
run = None
for x in range(560, 918):
    n = 0
    for y in range(466, 529):
        r, g, b = px[x, y]
        if not (222 <= r <= 240 and 224 <= g <= 242 and 221 <= b <= 239):  # not canvas gray
            n += 1
    if n > 0:
        if run is None: run = [x, x]
        run[1] = x
    else:
        if run:
            print(f"  run x={run[0]}-{run[1]} ({ih(run[0])}-{ih(run[1])}in) w={(run[1]-run[0]+1)}px"); run = None
if run: print(f"  run x={run[0]}-{run[1]} ({ih(run[0])}-{ih(run[1])}in) w={(run[1]-run[0]+1)}px")

print("== logo: row profile of non-canvas pixels (x 560..917) ==")
run = None
for y in range(460, 535):
    n = 0
    for x in range(560, 918):
        r, g, b = px[x, y]
        if not (222 <= r <= 240 and 224 <= g <= 242 and 221 <= b <= 239):
            n += 1
    if n > 0:
        if run is None: run = [y, y]
        run[1] = y
    else:
        if run:
            print(f"  run y={run[0]}-{run[1]} ({iv(run[0])}-{iv(run[1])}in) h={(run[1]-run[0]+1)}px"); run = None
if run: print(f"  run y={run[0]}-{run[1]} ({iv(run[0])}-{iv(run[1])}in) h={(run[1]-run[0]+1)}px")

# white panel: count pure-white pixels per column
print("== logo: white-pixel column runs (y 470..525) ==")
run = None
for x in range(560, 918):
    n = sum(1 for y in range(470, 526) if all(c > 244 for c in px[x, y]))
    if n > 40:
        if run is None: run = [x, x]
        run[1] = x
    else:
        if run:
            print(f"  white run x={run[0]}-{run[1]} ({ih(run[0])}-{ih(run[1])}in)"); run = None
if run: print(f"  white run x={run[0]}-{run[1]} ({ih(run[0])}-{ih(run[1])}in)")

# teal panel exact bbox
xs, ys = [], []
for y in range(460, 535):
    for x in range(560, 918):
        r, g, b = px[x, y]
        if g > 90 and b > 90 and abs(g - b) < 45 and (g - r) > 30 and (b - r) > 20:
            xs.append(x); ys.append(y)
print(f"== teal bbox x={min(xs)}-{max(xs)} ({ih(min(xs))}-{ih(max(xs))}in) y={min(ys)}-{max(ys)} ({iv(min(ys))}-{iv(max(ys))}in)")

# badge numeral extent (dark pixels inside yellow)
xs, ys = [], []
for y in range(50, 95):
    for x in range(870, 915):
        r, g, b = px[x, y]
        if r < 120 and g < 120 and b < 120:
            xs.append(x); ys.append(y)
if xs:
    print(f"== badge numeral bbox x={min(xs)}-{max(xs)} y={min(ys)}-{max(ys)} h={(max(ys)-min(ys)+1)}px")

# title line1 exact word extents (red ink runs, gap>6px)
print("== title L1 red column runs (y 135..191, gap>6) ==")
run = None; runs = []
for x in range(240, 700):
    n = sum(1 for y in range(135, 192) if px[x, y][0] > 120 and px[x, y][1] < 90 and px[x, y][2] < 90)
    if n > 0:
        if run is None: run = [x, x]
        run[1] = x
    else:
        if run and (x - run[1]) > 6:
            runs.append(tuple(run)); run = None
if run: runs.append(tuple(run))
for a, b in runs: print(f"  run x={a}-{b} ({ih(a)}-{ih(b)}in) w={b-a+1}px")

# credit block center check: 'Prepared By' x extent recheck incl. antialiased
xs = [x for x in range(430, 610) for y in range(298, 325) if px[x, y][0] > 130 and px[x, y][1] < 110 and px[x, y][2] < 110]
print(f"== 'Prepared By' red x extent {min(xs)}-{max(xs)} ({ih(min(xs))}-{ih(max(xs))}in) center {ih((min(xs)+max(xs))/2)}in")

# canvas color stats
from collections import Counter
c = Counter()
for y in range(60, 500, 7):
    for x in range(50, 910, 7):
        c[px[x, y]] += 1
print("== canvas top colors:", c.most_common(3))
