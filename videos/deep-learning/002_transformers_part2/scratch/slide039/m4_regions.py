#!/usr/bin/env python3
"""Per-region line measurement for slide_039."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()

SH, DH = 0.96123, 18.63
SV = 0.95556
def to_slide(fx, fy):
    return ((fx - DH) / SH, fy / SV)

def ink(p): return sum(p) < 640
def classify(p):
    r, g, b = p
    if r > 120 and r - g > 50 and r - b > 50: return "red"
    if b > 110 and b - r > 60 and b - g > 40: return "blue"
    if sum(p) < 260: return "black"
    return "?"

def lines_in(x0, x1, y0, y1, label, gap=2, minpx=2):
    rows = {}
    for y in range(y0, y1 + 1):
        xs = [x for x in range(x0, x1 + 1) if ink(px[x, y])]
        if len(xs) >= minpx: rows[y] = (min(xs), max(xs))
    segs = []
    cur = None
    for y in sorted(rows):
        if cur and y <= cur[1] + gap:
            cur[1] = y; cur[2].append(rows[y])
        else:
            if cur: segs.append(cur)
            cur = [y, y, [rows[y]]]
    if cur: segs.append(cur)
    print(f"--- {label} (x{x0}..{x1}, y{y0}..{y1}) ---")
    out = []
    for y0s, y1s, sl in segs:
        fx0 = min(s[0] for s in sl); fx1 = max(s[1] for s in sl)
        colors = {}
        for y in range(y0s, y1s + 1):
            for x in range(fx0, fx1 + 1):
                if ink(px[x, y]):
                    c = classify(px[x, y])
                    if c != "?": colors[c] = colors.get(c, 0) + 1
        tot = sum(colors.values()) or 1
        colstr = ",".join(f"{c}:{round(100*v/tot)}%" for c, v in sorted(colors.items(), key=lambda kv: -kv[1]))
        a = to_slide(fx0, y0s); b = to_slide(fx1, y1s)
        print(f"  frame[{fx0},{y0s},{fx1},{y1s}] h={y1s-y0s+1} slide[{a[0]:.1f},{a[1]:.1f},{b[0]:.1f},{b[1]:.1f}] {colstr}")
        out.append([fx0, y0s, fx1, y1s])
    return out

# 1. Title (exclude badge x>=850)
lines_in(62, 849, 47, 95, "TITLE")

# 2. Quote box interior (borders 96-97/152-153, cols 74-75/878-880)
lines_in(78, 876, 98, 151, "QUOTE-BOX")

# 3. Big container interior (borders 162-163/396-397, cols 72-73/877-878)
lines_in(76, 875, 165, 395, "CONTAINER", gap=3)

# 4. Summary box interior (borders 410-411/501-503)
lines_in(76, 875, 413, 500, "SUMMARY-BOX")

# 5. Yellow fills (flowchart boxes): FFFFCC-ish
ypts = [(x, y) for y in range(165, 395) for x in range(76, 875)
        if px[x, y][0] > 235 and px[x, y][1] > 235 and 190 < px[x, y][2] < 225]
if ypts:
    print("--- YELLOW fill bbox:", min(p[0] for p in ypts), min(p[1] for p in ypts),
          max(p[0] for p in ypts), max(p[1] for p in ypts))
    # column profile of yellow to find 3 boxes
    colcount = {}
    for x, y in ypts: colcount[x] = colcount.get(x, 0) + 1
    xs = sorted(colcount)
    runs = []
    x0 = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x - prev > 3:
            runs.append((x0, prev)); x0 = x
        prev = x
    runs.append((x0, prev))
    print("  yellow column runs:", runs)
    rowcount = {}
    for x, y in ypts: rowcount[y] = rowcount.get(y, 0) + 1
    ys = sorted(rowcount)
    runsy = []
    y0 = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y - prev > 3:
            runsy.append((y0, prev)); y0 = y
        prev = y
    runsy.append((y0, prev))
    print("  yellow row runs:", runsy)

# 6. sample fill colors
print("bg samples:", px[500, 70], px[500, 260], px[500, 460])
print("quote fill:", px[400, 120], " summary fill:", px[400, 450], px[400, 480])
