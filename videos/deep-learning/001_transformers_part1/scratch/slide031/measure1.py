#!/usr/bin/env python3
"""Measure slide_031.jpg (960x540, 1px = 1pt = 1/72 in) for the recreation build.

Strategy: color-region scanning. The frame has:
- peach background FCE4CF (rounded rect covering ~98%)
- white content canvas
- three panels with red/blue/green rounded borders
- pink capsules F5B8D0, matrix backgrounds (rose F2B9C6 / periwinkle B9C2F2 / green C7E8C7)
- yellow FFFF00 highlight box + badge
Print all measured bboxes in frame px.
"""
from PIL import Image
import sys

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def near(c, ref, tol):
    return all(abs(c[i] - ref[i]) <= tol for i in range(3))

def bbox_of(pred, x0=0, y0=0, x1=W, y1=H):
    minx, miny, maxx, maxy, n = None, None, None, None, 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                n += 1
                if minx is None or x < minx: minx = x
                if maxx is None or x > maxx: maxx = x
                if miny is None or y < miny: miny = y
                if maxy is None or y > maxy: maxy = y
    return (minx, miny, maxx, maxy, n)

def report(name, bb):
    print(f"{name}: x {bb[0]}..{bb[2]}  y {bb[1]}..{bb[3]}  w={bb[2]-bb[0]+1} h={bb[3]-bb[1]+1} n={bb[4]}")

print("== corner samples (bg colors) ==")
for (x, y, lbl) in [(3,3,"slide corner"), (20,270,"left edge mid"), (480,60,"top mid"), (480,270,"center"),
                    (480,30,"above peach?"), (950,530,"bottom right"), (480,535,"bottom mid")]:
    print(f"({x},{y}) {lbl}: {px[x,y]}")

PEACH = (252, 228, 207)
print("\n== peach background bbox ==")
report("peach", bbox_of(lambda c: near(c, PEACH, 14)))

print("\n== panel borders (strong red / blue / green runs) ==")
# scan for saturated colors
RED = lambda c: c[0] > 190 and c[1] < 90 and c[2] < 90
BLUE = lambda c: c[2] > 190 and c[0] < 90 and c[1] < 90
GREEN = lambda c: c[1] > 120 and c[0] < 110 and c[2] < 110 and c[1] - max(c[0], c[2]) > 40

# Panel borders: red border of Q panel — search whole frame but restrict to long runs.
# Simpler: for each of a set of columns, find rows where the color appears, then cluster.
def color_rows(pred, x, y0=0, y1=H):
    rows = [y for y in range(y0, y1) if pred(px[x, y])]
    return rows

def color_cols(pred, y, x0=0, x1=W):
    cols = [x for x in range(x0, x1) if pred(px[x, y])]
    return cols

# Find horizontal red border lines (rows with many red px)
def rows_with(pred, mincount, x0=0, x1=W, y0=0, y1=H):
    out = []
    for y in range(y0, y1):
        cnt = sum(1 for x in range(x0, x1) if pred(px[x, y]))
        if cnt >= mincount:
            out.append((y, cnt))
    return out

def cols_with(pred, mincount, x0=0, x1=W, y0=0, y1=H):
    out = []
    for x in range(x0, x1):
        cnt = sum(1 for y in range(y0, y1) if pred(px[x, y]))
        if cnt >= mincount:
            out.append((x, cnt))
    return out

print("-- red rows (>=150 red px across full width):")
print(rows_with(RED, 150)[:12], "..." if len(rows_with(RED,150)) > 12 else "")
print("-- red rows in left half (x 40..470):")
print(rows_with(RED, 120, 40, 470))
print("-- blue rows (>=150):")
print(rows_with(BLUE, 150))
print("-- green rows (>=150):")
print(rows_with(GREEN, 150))
print("-- red cols (y 90..310, left half) >=80:")
print(cols_with(RED, 80, 30, 480, 90, 310))
print("-- blue cols (y 90..310, right half) >=80:")
print(cols_with(BLUE, 80, 470, 940, 90, 310))
print("-- green cols (y 300..540, left half) >=80:")
print(cols_with(GREEN, 80, 30, 480, 300, 540))

print("\n== pink capsule fill F5B8D0 ==")
PINK = (245, 184, 208)
report("pink_all", bbox_of(lambda c: near(c, PINK, 22)))

print("\n== matrix backgrounds ==")
ROSE = (242, 185, 198)
PERI = (185, 194, 242)
MGRN = (199, 232, 199)
report("rose(Q matrix bg)", bbox_of(lambda c: near(c, ROSE, 16)))
report("peri(V matrix bg)", bbox_of(lambda c: near(c, PERI, 16)))
report("mgrn(K matrix bg)", bbox_of(lambda c: near(c, MGRN, 16)))

print("\n== yellow (badge + title highlight + emphasis box) ==")
YEL = lambda c: c[0] > 230 and c[1] > 220 and c[2] < 120
report("yellow_all", bbox_of(YEL))
print("-- yellow rows (>=40):")
print(rows_with(YEL, 40))
print("-- yellow cols (>=40):")
print(cols_with(YEL, 40))

print("\n== white canvas bounds (row/col scans) ==")
# white vs peach transition on a horizontal line through the canvas
y = 350
runs = []
prev = None
for x in range(0, W):
    c = px[x, y]
    w = near(c, (255, 255, 255), 12)
    if w != prev:
        runs.append((x, w))
        prev = w
print(f"row y={y} white runs (first 12):", runs[:12])

# vertical: peach top edge at x=480
col = []
prev = None
for y in range(0, 140):
    c = px[480, y]
    p = near(c, PEACH, 18)
    if p != prev:
        col.append((y, p))
        prev = p
print("col x=480 peach transitions y<140:", col)
