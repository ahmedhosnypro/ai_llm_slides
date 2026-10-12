#!/usr/bin/env python3
"""Probe anomalies: top border rows, badge region content, box border exact lines, ink colors."""
from PIL import Image
from collections import Counter

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_060.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

# 1) rows 35..55: reddish count per row + sample values
print("== rows 35..55 reddish counts ==")
for y in range(35, 56):
    xs = [x for x in range(0, W, 1) if reddish(px[x, y])]
    if xs:
        print(y, len(xs), (min(xs), max(xs)), "sample", px[xs[0], y])

# 2) badge region dump: classify colors in x 820..955, y 35..135
print("== badge region color classes ==")
c = Counter()
for y in range(35, 135):
    for x in range(820, 955):
        r, g, b = px[x, y]
        c[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
for k, v in c.most_common(12):
    print(k, v)

# purple ring pixels 6A5ACD ~ (106,90,205)
pur = [(x, y) for y in range(30, 140) for x in range(810, 960)
       if abs(px[x, y][0] - 106) < 45 and abs(px[x, y][1] - 90) < 45 and abs(px[x, y][2] - 205) < 50]
print("purple ring px count:", len(pur))
if pur:
    print("purple bbox:", min(p[0] for p in pur), min(p[1] for p in pur),
          max(p[0] for p in pur), max(p[1] for p in pur))

# yellow fill FDFD96 ~ (253,253,150)
yel = [(x, y) for y in range(30, 140) for x in range(810, 960)
       if px[x, y][0] > 235 and px[x, y][1] > 235 and 120 < px[x, y][2] < 200]
print("yellow px count:", len(yel))
if yel:
    print("yellow bbox:", min(p[0] for p in yel), min(p[1] for p in yel),
          max(p[0] for p in yel), max(p[1] for p in yel))

# what rows do 70..79 have red at? sample
print("== red px x-positions rows 70..77 ==")
for y in (70, 72, 74, 76):
    xs = [x for x in range(0, W) if reddish(px[x, y])]
    # summarize as ranges
    rngs = []
    for x in xs:
        if rngs and x - rngs[-1][1] <= 2:
            rngs[-1][1] = x
        else:
            rngs.append([x, x])
    print(y, rngs[:12])

# 3) box border: exact blue lines. Scan verticals: columns with long blue runs
def blueish(p):
    r, g, b = p
    return b > 110 and (b - r) > 40 and (b - g) > 30

print("== blue verticals ==")
for x in range(60, 900):
    ys = [y for y in range(60, 500) if blueish(px[x, y])]
    if len(ys) > 200:
        print("col", x, "n", len(ys), "range", min(ys), max(ys))
print("== blue horizontals ==")
for y in range(60, 520):
    xs = [x for x in range(60, 900) if blueish(px[x, y])]
    if len(xs) > 400:
        print("row", y, "n", len(xs), "range", min(xs), max(xs))

# 4) ink color censuses (saturated only)
def census(x0, y0, x1, y1, filt, n=8):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if filt(p):
                c[p] += 1
    return c.most_common(n)

print("== title core red (rows 78..92, x 275..630) ==")
print(census(275, 78, 630, 93, lambda p: reddish(p) and p[0] > 150))
print("== box fill interior (x 400..600, y 240..250 empty gap) ==")
print(census(400, 240, 600, 251, lambda p: True, 5))
print("== panel bg outside box (x 100..200, y 60..70?) row 60..64 ==")
print(census(100, 58, 220, 66, lambda p: True, 5))
print("== blue text core: row band 146..163 x 150..594 ==")
print(census(150, 146, 594, 164, lambda p: blueish(p) and p[2] > 140))
print("== red text core rows 210..227 (entry parenthetical) x 147..687 ==")
print(census(147, 210, 687, 228, lambda p: reddish(p) and p[0] > 150))
