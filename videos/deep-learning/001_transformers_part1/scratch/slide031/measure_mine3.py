#!/usr/bin/env python3
"""Fine scans: peach bounds, matrix grids, capsules, output-label forensics, callouts, boxes."""
from PIL import Image
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()
def c(x, y): return px[x, y]

def pred_peach(cc):
    r, g, b = cc
    return 235 <= r <= 258 and 205 <= g <= 240 and 185 <= b <= 225 and r - b > 25 and r - g > 12

def bbox(pred, x0, y0, x1, y1):
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(c(x, y)):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None

print("=== A. PEACH CANVAS BOUNDS ===")
print("peach bbox:", bbox(pred_peach, 0, 60, W, H))
# edges via scanlines
row = 300
xs = [x for x in range(0, W) if pred_peach(c(x, row))]
print(f"row300 peach x: {min(xs)}..{max(xs)}")
col = 480
ys = [y for y in range(60, H) if pred_peach(c(col, y))]
print(f"col480 peach y: {min(ys)}..{max(ys)}")
col = 100
ys = [y for y in range(60, H) if pred_peach(c(col, y))]
print(f"col100 peach y: {min(ys)}..{max(ys)}")
print("peach core:", c(500, 330), c(700, 420), c(60, 250))

print("\n=== B. Q INPUT CAPSULE: pill + circles ===")
pred_pinkpill = lambda cc: abs(cc[0]-250) < 14 and abs(cc[1]-190) < 30 and abs(cc[2]-208) < 30 and cc[0]-cc[1] > 30
print("Q pill pink bbox (x56..230,y125..175):", bbox(pred_pinkpill, 56, 125, 230, 175))
# circles: dark ring pixels
pred_darkring = lambda cc: sum(cc) < 400 and cc[0]-cc[2] > -30
# input capsule label ink per cell: scan 4 circles approx x83..202
print("Q input circle region ink rows (x80..205, y130..180):")
for y in range(130, 180):
    n = sum(1 for x in range(80, 205) if sum(c(x, y)) < 330)
    if n > 3: print(f"  y={y}: {n}")

print("\n=== C. MATRIX CELL GRIDS (chip fill + text color per row) ===")
def grid_scan(x0, x1, y0, y1, label):
    # classify each pixel; find chip fill color and cell boundaries via non-white columns
    fills = Counter()
    for y in range(y0, y1, 2):
        for x in range(x0, x1, 2):
            cc = c(x, y)
            r, g, b = cc
            if r > 244 and g > 244 and b > 244: continue
            fills[(r // 24 * 24, g // 24 * 24, b // 24 * 24)] += 1
    print(f"  {label} top fill buckets: {fills.most_common(6)}")
grid_scan(200, 410, 112, 296, "Q matrix")
grid_scan(620, 832, 112, 296, "V matrix")
grid_scan(200, 410, 330, 512, "K matrix")
# column profile of chip edges: white gaps along row through cells
def colgaps(y, x0, x1, label):
    runs = []; inw = False; start = 0
    for x in range(x0, x1):
        w = c(x, y)
        isw = w[0] > 244 and w[1] > 244 and w[2] > 244
        if isw and not inw: inw = True; start = x
        elif not isw and inw:
            inw = False
            if x - start >= 3: runs.append((start, x - 1))
    if inw: runs.append((start, x1 - 1))
    print(f"  {label} white runs at y={y}: {runs}")
colgaps(140, 195, 470, "Q matrix row1")
colgaps(172, 195, 470, "Q matrix row2")
colgaps(204, 195, 470, "Q matrix row3")
colgaps(236, 195, 470, "Q matrix row4")
colgaps(460, 195, 470, "K matrix row4")
# row gaps down a column through cells
def rowgaps(x, y0, y1, label):
    runs = []; inw = False; start = 0
    for y in range(y0, y1):
        w = c(x, y)
        isw = w[0] > 244 and w[1] > 244 and w[2] > 244
        if isw and not inw: inw = True; start = y
        elif not isw and inw:
            inw = False
            if y - start >= 3: runs.append((start, y - 1))
    if inw: runs.append((start, y1 - 1))
    print(f"  {label} white runs at x={x}: {runs}")
rowgaps(240, 105, 300, "Q matrix col1")
rowgaps(660, 105, 300, "V matrix col1")
rowgaps(240, 320, 515, "K matrix col1")

print("\n=== D. OUTPUT CAPSULES: bounds + label forensics ===")
# Q output capsule: outline red cols near x409..455
for x in range(405, 462):
    ys = [y for y in range(100, 300) if c(x, y)[0] > 130 and c(x, y)[0] - c(x, y)[1] > 55 and c(x, y)[0] - c(x, y)[2] > 55]
    if len(ys) > 100:
        print(f"  Q outcap red col x={x}: n={len(ys)} y {min(ys)}..{max(ys)}")
pred_pinkish = lambda cc: cc[0] > 235 and 150 < cc[1] < 225 and 150 < cc[2] < 230 and cc[0] - cc[1] > 25
print("Q outcap pink bbox:", bbox(pred_pinkish, 400, 95, 470, 300))
print("V outcap pink bbox:", bbox(pred_pinkish, 820, 95, 900, 300))
print("K outcap pink bbox:", bbox(pred_pinkish, 400, 320, 470, 520))
# tiles inside Q outcap: yellow chip rows
pred_chip = lambda cc: cc[0] > 240 and cc[1] > 215 and 150 < cc[2] < 215
print("Q outcap chip bbox:", bbox(pred_chip, 405, 95, 465, 300))
print("V outcap chip bbox:", bbox(pred_chip, 825, 95, 900, 300))
print("K outcap chip bbox:", bbox(pred_chip, 405, 320, 470, 520))
# INPUT cell chips for width comparison
print("Q incap chip bbox:", bbox(pred_chip, 60, 125, 230, 180))

print("\n--- OUTPUT LABEL INK FORENSICS (per tile) ---")
def ink_forensics(x0, y0, x1, y1, label):
    xs = []; ys = []; reds = 0; darks = 0
    red_xs = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            cc = c(x, y)
            r, g, b = cc
            if r > 120 and r - g > 55 and r - b > 55:
                reds += 1; red_xs.append(x)
            elif sum(cc) < 340:
                darks += 1
                xs.append(x); ys.append(y)
    if xs:
        print(f"  {label}: dark ink x {min(xs)}..{max(xs)} (w={max(xs)-min(xs)+1}) y {min(ys)}..{max(ys)} darks={darks} reds={reds} redx={min(red_xs) if red_xs else '-'}..{max(red_xs) if red_xs else '-'}")
    else:
        print(f"  {label}: no dark ink; reds={reds} redx={min(red_xs) if red_xs else '-'}..{max(red_xs) if red_xs else '-'}")

print("Q INPUT cells (4) label ink:")
for i, (cx0, cx1) in enumerate([(83, 113), (114, 144), (145, 175), (176, 206)]):
    ink_forensics(cx0, 138, cx1, 172, f"Q-incell{i+1}")
print("Q OUTPUT tiles (4) label ink (tiles x~412..452):")
for i, (ty0, ty1) in enumerate([(118, 165), (168, 215), (218, 265), (250, 296)]):
    ink_forensics(413, ty0, 452, ty1, f"Q-outtile{i+1}")
print("V OUTPUT tiles (4) label ink (capsule x~830..884):")
for i, (ty0, ty1) in enumerate([(118, 165), (168, 215), (218, 265), (250, 296)]):
    ink_forensics(834, ty0, 882, ty1, f"V-outtile{i+1}")
print("K OUTPUT tiles (4) label ink (capsule x~412..455):")
for i, (ty0, ty1) in enumerate([(334, 378), (382, 426), (430, 474), (458, 502)]):
    ink_forensics(413, ty0, 456, ty1, f"K-outtile{i+1}")
print("K INPUT cells label ink (capsule y~352..426):")
for i, (cx0, cx1) in enumerate([(83, 113), (114, 144), (145, 175), (176, 206)]):
    ink_forensics(cx0, 360, cx1, 400, f"K-incell{i+1}")
