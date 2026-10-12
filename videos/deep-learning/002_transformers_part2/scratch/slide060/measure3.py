#!/usr/bin/env python3
"""Pass 3: top-border check vs slide_002, mapping fit from 4 landmarks, text bands, color census."""
from PIL import Image
from collections import Counter

S060 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_060.jpg"
S002 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_002.jpg"

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

def blueish(p):
    r, g, b = p
    return b > 110 and (b - r) > 40 and (b - g) > 30

for name, path in (("002", S002), ("060", S060)):
    img = Image.open(path).convert("RGB")
    px = img.load()
    print(f"== {name} rows 38..50: reddish count (x 60..900) + row mean ==")
    for y in range(38, 51):
        n = sum(1 for x in range(60, 901) if reddish(px[x, y]))
        vals = [px[x, y] for x in range(100, 900, 40)]
        mean = tuple(round(sum(v[i] for v in vals) / len(vals)) for i in range(3))
        print(y, n, mean)

# --- fit mapping for 060 from left/right/bottom borders + badge
img = Image.open(S060).convert("RGB")
W, H = img.size
px = img.load()
yel = [(x, y) for y in range(30, 140) for x in range(810, 960)
       if px[x, y][0] > 235 and px[x, y][1] > 235 and 120 < px[x, y][2] < 200]
byx = (min(p[0] for p in yel) + max(p[0] for p in yel)) / 2
byy = (min(p[1] for p in yel) + max(p[1] for p in yel)) / 2
print("badge yellow center frame:", byx, byy)

# landmarks: frame left col 59 <-> slide 42 (stroke center), right col 902 <-> slide 919,
# bottom row 516 <-> slide 539 (stroke center 538.5..539.5), badge (893,71)
sx = (902 - 59) / (919 - 42)
ix = 59 - sx * 42
# y fit from bottom border + badge center
sy1 = (516 - byy) / (539 - 71)
iy1 = 516 - sy1 * 539
print(f"fit x: frame_x = {ix:.2f} + {sx:.5f} * slide_x")
print(f"fit y (bottom+badge): frame_y = {iy1:.2f} + {sy1:.5f} * slide_y")
# alternative: bottom only with slide_002 scale
sy2 = 0.95556
iy2 = 516 - sy2 * 539
print(f"alt y (bottom only, slide_002 scale): frame_y = {iy2:.2f} + {sy2:.5f} * slide_y -> badge slide y = {(byy - iy2)/sy2:.1f}")
print(f"badge mapped (fit y): ({(byx-ix)/sx:.1f}, {(byy-iy1)/sy1:.1f}) vs house (893,71)")

def TX(fx): return (fx - ix) / sx
def TY(fy): return (fy - iy1) / sy1

# --- text bands inside box (exclude border cols 80-81, 878)
print("== bands inside box ==")
rows = []
for y in range(119, 481):
    b = sum(1 for x in range(83, 877) if blueish(px[x, y]))
    r = sum(1 for x in range(83, 877) if reddish(px[x, y]))
    rows.append((y, b, r))
bands = []
cur = None
for y, b, r in rows:
    if b + r > 2:
        if cur and y - cur[1] <= 4:
            cur[1] = y
        else:
            cur = [y, y]
            bands.append(cur)
for y0, y1 in bands:
    bxs = [x for y in range(y0, y1 + 1) for x in range(83, 877) if blueish(px[x, y])]
    rxs = [x for y in range(y0, y1 + 1) for x in range(83, 877) if reddish(px[x, y])]
    allx = sorted(bxs + rxs)
    print(f"band fy {y0}..{y1} (h{y1-y0+1}) slide_y {TY(y0):.1f}..{TY(y1):.1f} "
          f"ink x {min(allx)}..{max(allx)} slide_x {TX(min(allx)):.1f}..{TX(max(allx)):.1f} "
          f"blue {len(bxs)} red {len(rxs)}")

# --- color census per region
def census(x0, y0, x1, y1, filt):
    c = Counter()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            p = px[x, y]
            if filt(p):
                c[p] += 1
    return c

print("== title red census (fy 66..94, x 270..635) ==")
tc = census(270, 66, 635, 94, lambda p: p[0] > 130 and p[0] - p[1] > 60 and p[0] - p[2] > 50)
print(tc.most_common(8), "total", sum(tc.values()))
print("== entry name blue census (fy 143..165, x 145..600) ==")
bc = census(145, 143, 600, 165, blueish)
print(bc.most_common(8), "total", sum(bc.values()))
print("== entry parenthetical red census (fy 143..165, x 145..600) ==")
rc = census(145, 143, 600, 165, lambda p: p[0] > 130 and p[0] - p[1] > 60 and p[0] - p[2] > 50)
print(rc.most_common(8), "total", sum(rc.values()))
print("== citation blue census (fy 170..195, x 100..600) ==")
cc = census(100, 170, 600, 195, blueish)
print(cc.most_common(8), "total", sum(cc.values()))
print("== box border blue census (col 80-81, fy 120..480) ==")
xc = census(80, 120, 81, 480, blueish)
print(xc.most_common(8), "total", sum(xc.values()))
print("== box fill mean (x 300..500, fy 240..260) ==")
fc = census(300, 240, 500, 260, lambda p: True)
tot = sum(fc.values())
mean = tuple(round(sum(k[i] * v for k, v in fc.items()) / tot) for i in range(3))
print("mean fill:", mean, "top:", fc.most_common(4))
print("== panel bg mean (x 100..200, fy 55..65) ==")
gc = census(100, 55, 200, 65, lambda p: True)
tot = sum(gc.values())
print("panel mean:", tuple(round(sum(k[i] * v for k, v in gc.items()) / tot) for i in range(3)))
print("== badge numeral dark px bbox ==")
dark = [(x, y) for y in range(56, 86) for x in range(859, 893) if sum(px[x, y]) < 340]
if dark:
    print("numeral bbox:", min(p[0] for p in dark), min(p[1] for p in dark),
          max(p[0] for p in dark), max(p[1] for p in dark))
