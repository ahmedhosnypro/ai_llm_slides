#!/usr/bin/env python3
"""Refined landmark + ink measurement for slide_050.jpg."""
import json
from collections import Counter
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_050.jpg"
im = Image.open(FR).convert("RGB")
W, H = im.size
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 90 and r - max(g, b) > 50

# ---- vertical border strokes: columns x in 50..75 and 890..915
for zone in [(50, 75), (890, 915)]:
    cols = []
    for x in range(*zone):
        ys = [y for y in range(30, 520) if is_red(px[x, y])]
        if len(ys) > 200:
            cols.append((x, len(ys)))
    print(f"zone {zone}: red cols {cols}")
    if cols:
        cx = sum(n * x for x, n in cols) / sum(n for _, n in cols)
        print(f"  weighted stroke center x = {cx:.2f}")

# ---- horizontal strokes: rows y in 35..55 and 508..525
for zone in [(35, 55), (508, 525)]:
    rows = []
    for y in range(*zone):
        xs = [x for x in range(60, 900) if is_red(px[x, y])]
        if len(xs) > 200:
            rows.append((y, len(xs)))
    print(f"zone {zone}: red rows {rows}")
    if rows:
        cy = sum(n * y for y, n in rows) / sum(n for _, n in rows)
        print(f"  weighted stroke center y = {cy:.2f}")

# ---- top/bottom border stroke vertical extent at x=480 (for stroke width)
for x in [300, 480, 700]:
    ys = [y for y in range(30, 60) if is_red(px[x, y])]
    ys2 = [y for y in range(505, 525) if is_red(px[x, y])]
    print(f"x={x}: top stroke ys {ys}, bottom stroke ys {ys2}")
# left/right stroke horizontal extent at y=300
for y in [150, 300, 450]:
    xs1 = [x for x in range(45, 80) if is_red(px[x, y])]
    xs2 = [x for x in range(885, 920) if is_red(px[x, y])]
    print(f"y={y}: left stroke xs {xs1}, right stroke xs {xs2}")

# ---- title ink, subpixel-ish: strong red core only (r>140, r-max(g,b)>60)
def is_core_red(c):
    r, g, b = c
    return r > 140 and g < 80 and b < 80

txs, tys = [], []
for y in range(240, 330):
    for x in range(150, 800):
        if is_core_red(px[x, y]):
            txs.append(x); tys.append(y)
print(f"title core ink bbox: x {min(txs)}..{max(txs)} (w {max(txs)-min(txs)}), y {min(tys)}..{max(tys)} (h {max(tys)-min(tys)})")
print(f"  cx {(min(txs)+max(txs))/2}, cy {(min(tys)+max(tys))/2}")
# per-column profile: first/last ink col, and cap-top row vs baseline row at a T column
colprof = Counter()
for x in txs:
    ysx = [y for y in range(240, 330) if is_core_red(px[x, y])]
    colprof[x] = (min(ysx), max(ysx))
# T column = leftmost 20 columns: cap top
tcols = sorted(txs)[:20]
tcap = min(min(colprof[x]) for x in tcols)
rcols = sorted(txs)[-20:]
rbase = max(max(colprof[x]) for x in rcols)
print(f"  cap top (T cols) {tcap}, baseline (r cols) {rbase}, cap height {rbase - tcap}")

# title color census (core)
cc = Counter()
for y in range(min(tys), max(tys) + 1):
    for x in range(min(txs), max(txs) + 1):
        c = px[x, y]
        if is_core_red(c):
            cc[(c[0] // 8 * 8, c[1] // 8 * 8, c[2] // 8 * 8)] += 1
print("  title core color census (8-bin):", cc.most_common(5))

# ---- badge numeral ink: dark px inside badge circle
bxs, bys = [], []
for y in range(58, 85):
    for x in range(860, 892):
        c = px[x, y]
        if sum(c) < 330:
            bxs.append(x); bys.append(y)
if bxs:
    print(f"badge numeral ink bbox: x {min(bxs)}..{max(bxs)}, y {min(bys)}..{max(bys)}")

# ---- any other ink on the panel? scan interior for non-gray, non-red pixels
panel_y0, panel_y1 = 46, 515
panel_x0, panel_x1 = 60, 900
odd = Counter()
for y in range(panel_y0, panel_y1):
    for x in range(panel_x0, panel_x1):
        c = px[x, y]
        r, g, b = c
        is_gray = abs(r - g) < 12 and abs(g - b) < 12
        if not is_gray and not is_red(c):
            odd[(x // 40 * 40, y // 40 * 40, (r // 32, g // 32, b // 32))] += 1
print("non-gray/non-red cells (x,y 40px cell, color bin):", odd.most_common(12))

# pen cursor zone detail (gray strokes)
pen = [(x, y) for y in range(390, 440) for x in range(480, 560)
       if abs(px[x, y][0] - px[x, y][1]) < 14 and abs(px[x, y][1] - px[x, y][2]) < 14 and sum(px[x, y]) < 520]
if pen:
    pxs = [p[0] for p in pen]; pys = [p[1] for p in pen]
    print(f"pen cursor gray ink bbox: x {min(pxs)}..{max(pxs)}, y {min(pys)}..{max(pys)}, count {len(pen)}")
