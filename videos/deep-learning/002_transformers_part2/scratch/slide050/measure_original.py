#!/usr/bin/env python3
"""Measure original frame slide_050.jpg (960x540) — chrome landmarks, badge, title ink.

Frame->slide mapping derived like certified slide_002/003/056: the capture is zoomed
OUT (~0.958) with a black letterbox strip below. Landmarks: panel border stroke
centers (left/right/top/bottom-border) <-> slide chrome 42 / 919 / 45 / 540 pt.
Badge cross-check: yellow-fill bbox center vs house badge (893, 71).
"""
import json
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_050.jpg"
im = Image.open(FR).convert("RGB")
W, H = im.size
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 120 and g < 90 and b < 90

def col_red_ink(x):
    """count red pixels in column x, return (count, ymin, ymax)"""
    ys = [y for y in range(H) if is_red(px[x, y])]
    if not ys:
        return 0, None, None
    return len(ys), min(ys), max(ys)

def row_red_ink(y):
    xs = [x for x in range(W) if is_red(px[x, y])]
    if not xs:
        return 0, None, None
    return len(xs), min(xs), max(xs)

# ---- 1. find vertical border strokes: columns with many red pixels (long runs)
col_counts = []
for x in range(W):
    n, y0, y1 = col_red_ink(x)
    col_counts.append((x, n, y0, y1))

long_cols = [c for c in col_counts if c[1] > 300]
print("long red columns (x, count, ymin, ymax):", long_cols)

# ---- 2. find horizontal border strokes: rows with many red pixels
long_rows = []
for y in range(H):
    n, x0, x1 = row_red_ink(y)
    if n > 300:
        long_rows.append((y, n, x0, x1))
print("long red rows (y, count, xmin, xmax):", long_rows)

# stroke centers: take contiguous groups of long cols/rows, weight by count
def groups(items):
    out = []
    cur = [items[0]]
    for it in items[1:]:
        if it[0] - cur[-1][0] <= 2:
            cur.append(it)
        else:
            out.append(cur)
            cur = [it]
    out.append(cur)
    return out

if long_cols:
    for g in groups(long_cols):
        s = sum(it[1] * it[0] for it in g)
        n = sum(it[1] for it in g)
        print(f"vertical stroke group: center={s/n:.2f} members={[it[0] for it in g]}")
if long_rows:
    for g in groups(long_rows):
        s = sum(it[1] * it[0] for it in g)
        n = sum(it[1] for it in g)
        print(f"horizontal stroke group: center={s/n:.2f} members={[it[0] for it in g]}")

# ---- 3. letterbox: find black rows near bottom
def is_black(c):
    return c[0] < 40 and c[1] < 40 and c[2] < 40
black_rows = [y for y in range(H) if sum(1 for x in range(W) if is_black(px[x, y])) > 500]
print("black letterbox rows:", black_rows[:5], "...", black_rows[-5:] if len(black_rows) > 5 else "")

# ---- 4. badge: yellow fill bbox in top-right quadrant
def is_yellow(c):
    r, g, b = c
    return r > 200 and g > 200 and b < 160
ys, xs = [], []
for y in range(0, 160):
    for x in range(700, 960):
        if is_yellow(px[x, y]):
            xs.append(x); ys.append(y)
if xs:
    print(f"badge yellow bbox: x {min(xs)}..{max(xs)} (cx {(min(xs)+max(xs))/2}), y {min(ys)}..{max(ys)} (cy {(min(ys)+max(ys))/2})")
    # purple ring bbox
    def is_purple(c):
        r, g, b = c
        return 80 <= r <= 160 and 60 <= g <= 120 and b > 150
    ys2, xs2 = [], []
    for y in range(0, 200):
        for x in range(700, 960):
            if is_purple(px[x, y]):
                xs2.append(x); ys2.append(y)
    if xs2:
        print(f"badge ring bbox: x {min(xs2)}..{max(xs2)}, y {min(ys2)}..{max(ys2)}")

# ---- 5. title ink: red pixels NOT part of the border/badge — middle region
# (exclude border columns/rows found above and badge zone)
bcx = set()
if long_cols:
    for g in groups(long_cols):
        for it in g:
            bcx.add(it[0])
title_xs, title_ys = [], []
from collections import Counter
title_cols = Counter()
for y in range(H):
    for x in range(W):
        if x in bcx:
            continue
        if is_red(px[x, y]) and 100 < y < 400:
            title_xs.append(x); title_ys.append(y)
            title_cols[x] += 1
if title_xs:
    print(f"title ink bbox: x {min(title_xs)}..{max(title_xs)} (w {max(title_xs)-min(title_xs)+1}), y {min(title_ys)}..{max(title_ys)} (h {max(title_ys)-min(title_ys)+1})")
    print(f"title ink center: cx {(min(title_xs)+max(title_xs))/2}, cy {(min(title_ys)+max(title_ys))/2}")
    # color census of title ink
    cc = Counter()
    for y in range(min(title_ys), max(title_ys)+1):
        for x in range(min(title_xs), max(title_xs)+1):
            c = px[x, y]
            if is_red(c):
                cc[c] += 1
    print("title ink top colors:", cc.most_common(6))

# ---- 6. panel interior color (gray) — sample center-left away from title
samples = [px[200, 300], px[250, 350], px[150, 250], px[700, 300], px[700, 400]]
print("interior samples:", samples)
# outside canvas (above panel)
print("outside samples (above panel):", [px[100, 10], px[480, 10], px[900, 20]])
# below border, above letterbox
if black_rows:
    lb_top = min(black_rows)
    print(f"strip between border-bottom and letterbox (row ~{(516+lb_top)//2}):", [px[100, (516+lb_top)//2], px[480, (516+lb_top)//2]])

# ---- 7. pen cursor: dark pixels in lower-middle region (y 380..470, x 400..600)
dark = [(x, y, px[x, y]) for y in range(380, 470) for x in range(380, 620) if sum(px[x, y]) < 250]
print(f"pen-cursor candidate dark px count: {len(dark)}")
if dark:
    xs3 = [d[0] for d in dark]; ys3 = [d[1] for d in dark]
    print(f"pen cursor bbox: x {min(xs3)}..{max(xs3)}, y {min(ys3)}..{max(ys3)}")
