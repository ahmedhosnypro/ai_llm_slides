#!/usr/bin/env python3
"""Micro-scan: V/K outcaps, role letters, side labels — exact bounds."""
from PIL import Image
im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()
def c(x, y): return px[x, y]
isw = lambda cc: cc[0] > 244 and cc[1] > 244 and cc[2] > 244

print("== V outcap: non-white columns x815..900 (y120..280) ==")
for x in range(815, 900):
    ys = [y for y in range(115, 295) if not isw(c(x, y))]
    if len(ys) > 60:
        reds = sum(1 for y in ys if c(x, y)[0] > 120 and c(x, y)[0] - c(x, y)[1] > 45 and c(x, y)[0] - c(x, y)[2] > 45)
        blues = sum(1 for y in ys if c(x, y)[2] > 110 and c(x, y)[2] - c(x, y)[0] > 40)
        mc = tuple(round(sum(cc[i] for cc in (c(x, y) for y in ys)) / len(ys)) for i in range(3))
        print(f"  x={x}: n={len(ys)} y {min(ys)}..{max(ys)} reds={reds} blues={blues} mean={mc}")
print("== V outcap white runs at y=200 (x800..900): ==")
runs = []; inw = False; start = 0
for x in range(790, 905):
    t = isw(c(x, 200))
    if t and not inw: inw = True; start = x
    elif not t and inw:
        inw = False
        if x - start >= 2: runs.append((start, x - 1))
if inw: runs.append((start, 904))
print("  ", runs)
print("== V outcap: vertical profile at x=845 ==")
runs = []; inw = False
for y in range(105, 305):
    t = isw(c(845, y))
    if t and not inw: inw = True; start = y
    elif not t and inw:
        inw = False
        if y - start >= 2: runs.append((start, y - 1))
if inw: runs.append((start, 304))
print("  white runs:", runs)
print("== K outcap: columns x408..462 (y340..500), green/red counts ==")
for x in range(408, 462):
    ys = [y for y in range(330, 510) if not isw(c(x, y))]
    if len(ys) > 100:
        reds = sum(1 for y in ys if c(x, y)[0] > 120 and c(x, y)[0] - c(x, y)[1] > 45 and c(x, y)[0] - c(x, y)[2] > 45)
        grns = sum(1 for y in ys if c(x, y)[1] > 100 and c(x, y)[1] - c(x, y)[0] > 25 and c(x, y)[1] - c(x, y)[2] > 25)
        print(f"  x={x}: n={len(ys)} y {min(ys)}..{max(ys)} reds={reds} greens={grns}")
print("== Q outcap cols x405..460 (y120..280) red counts ==")
for x in range(405, 460):
    ys = [y for y in range(115, 290) if not isw(c(x, y))]
    if len(ys) > 100:
        reds = sum(1 for y in ys if c(x, y)[0] > 120 and c(x, y)[0] - c(x, y)[1] > 45 and c(x, y)[0] - c(x, y)[2] > 45)
        print(f"  x={x}: n={len(ys)} reds={reds}")

print("== Role letters (tight) ==")
def bb(pred, x0, y0, x1, y1):
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(c(x, y)): xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None
pred_red = lambda cc: cc[0] > 120 and cc[0] - cc[1] > 45 and cc[0] - cc[2] > 45
pred_blue = lambda cc: cc[2] > 110 and cc[2] - cc[0] > 40 and cc[2] - cc[1] > 30
pred_grn = lambda cc: cc[1] > 95 and cc[1] - cc[0] > 20 and cc[1] - cc[2] > 20
print("  Q role:", bb(pred_red, 405, 88, 460, 120))
print("  V role:", bb(pred_blue, 790, 88, 875, 120))
print("  K role:", bb(pred_grn, 405, 298, 460, 330))
print("== Side labels exact ==")
print("  Q X2:", bb(pred_red, 110, 168, 165, 220))
print("  Q 1xd:", bb(lambda cc: sum(cc) < 430, 165, 168, 215, 200))
print("  V X2:", bb(pred_red, 525, 168, 585, 220))
print("  V 1xd:", bb(lambda cc: sum(cc) < 430, 585, 168, 640, 200))
print("  K X2:", bb(pred_red, 110, 385, 165, 440))
print("  K 1xd:", bb(lambda cc: sum(cc) < 430, 165, 385, 215, 420))
print("  Q WQ:", bb(pred_red, 190, 240, 260, 300))
print("  V WV:", bb(pred_red, 610, 240, 680, 300))
print("  K WK:", bb(pred_red, 190, 455, 260, 515))
print("  Q dxd:", bb(lambda cc: sum(cc) < 430, 325, 265, 380, 300))
print("  V dxd:", bb(lambda cc: sum(cc) < 430, 745, 265, 800, 300))
print("  K dxd:", bb(lambda cc: sum(cc) < 430, 325, 480, 380, 515))
print("== Q matrix rows: white-run map at x=300 (y105..300) ==")
runs = []; inw = False
for y in range(105, 300):
    t = isw(c(300, y))
    if t and not inw: inw = True; start = y
    elif not t and inw:
        inw = False
        if y - start >= 2: runs.append((start, y - 1))
if inw: runs.append((start, 299))
print("  white runs:", runs)
print("== Q matrix cols: white-run map at y=200 (x190..420) ==")
runs = []; inw = False
for x in range(190, 420):
    t = isw(c(x, 200))
    if t and not inw: inw = True; start = x
    elif not t and inw:
        inw = False
        if x - start >= 2: runs.append((start, x - 1))
if inw: runs.append((start, 419))
print("  white runs:", runs)
print("== V matrix cols: white-run map at y=200 (x600..840) ==")
runs = []; inw = False
for x in range(600, 840):
    t = isw(c(x, 200))
    if t and not inw: inw = True; start = x
    elif not t and inw:
        inw = False
        if x - start >= 2: runs.append((start, x - 1))
if inw: runs.append((start, 839))
print("  white runs:", runs)
print("== chip pale-yellow cols at Q y=145 (x215..380) ==")
pred_chip = lambda cc: cc[0] > 238 and cc[1] > 213 and 145 < cc[2] < 215 and cc[0] - cc[2] > 40
runs = []; inw = False
for x in range(210, 385):
    t = pred_chip(c(x, 145))
    if t and not inw: inw = True; start = x
    elif not t and inw:
        inw = False
        if x - start >= 3: runs.append((start, x - 1))
if inw: runs.append((start, 384))
print("  ", runs)
print("== chip pale-yellow rows at Q x=245 (y110..295) ==")
runs = []; inw = False
for y in range(110, 295):
    t = pred_chip(c(245, y))
    if t and not inw: inw = True; start = y
    elif not t and inw:
        inw = False
        if y - start >= 3: runs.append((start, y - 1))
if inw: runs.append((start, 294))
print("  ", runs)
