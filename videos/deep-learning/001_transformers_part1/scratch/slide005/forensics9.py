#!/usr/bin/env python3
"""Forensics 9: remaining dev maps — FM2/FM4 fills, triangles 2-4, seq arrow, leader, caption, hatch."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def devmap(xa, xb, ya, yb, label, thr=26, step=1):
    print(f"--- {label} (x{xa}-{xb}, y{ya}-{yb}) ---")
    for y in range(ya, yb, step):
        row = []
        for x in range(xa, xb):
            px = im[y, x]
            d_panel = abs(int(px[0])-233)+abs(int(px[1])-233)+abs(int(px[2])-231)
            d_line = abs(int(px[0])-167)+abs(int(px[1])-175)+abs(int(px[2])-184)
            row.append("X" if min(d_panel, d_line) > thr else ".")
        print(f"{y:3d} " + "".join(row))

def devsum(xa, xb, ya, yb, label, thr=26):
    print(f"--- {label}: per-column deviation count ---")
    cols = []
    for x in range(xa, xb):
        n = 0
        ymin, ymax = None, None
        for y in range(ya, yb):
            px = im[y, x]
            d_panel = abs(int(px[0])-233)+abs(int(px[1])-233)+abs(int(px[2])-231)
            d_line = abs(int(px[0])-167)+abs(int(px[1])-175)+abs(int(px[2])-184)
            if min(d_panel, d_line) > thr:
                n += 1
                if ymin is None: ymin = y
                ymax = y
        cols.append((x, n, ymin, ymax))
    for x, n, ymin, ymax in cols:
        if n:
            print(f"  x={x}: n={n} y{ymin}..{ymax}")

# a. FM2 cyan cells: which y-band exactly (column through FM2 at x=496, y295-425)
print("=== FM2 column x=496 raw (y295-425, every 2) ===")
for y in range(295, 426, 2):
    px = im[y, 496]
    print(f"y{y}: {tuple(int(v) for v in px)}", end="  ")
    if (y - 295) % 6 == 5: print()
print()

# b. FM4: column x=777 raw y178-465
print("=== FM4 column x=777 raw (y178-465, every 2) ===")
for y in range(178, 466, 2):
    px = im[y, 777]
    print(f"y{y}: {tuple(int(v) for v in px)}", end="  ")
    if (y - 178) % 6 == 5: print()
print()

# c. triangles 2-4
devsum(246, 306, 330, 465, "gap1 lower (tri2?)")
devsum(539, 597, 176, 465, "gap2 (tri3?)")
devsum(681, 736, 176, 465, "gap3 (tri4?)")

# d. seq arrow zone: per-column deviation (x95-172, y165-470)
devsum(95, 172, 165, 470, "seq zone")

# e. leader line: devmap x365-470 y133-180
devmap(365, 470, 133, 180, "leader zone")

# f. caption underline check: rows y516-524 blue run pattern x181-810
print("=== caption rows y517-523 blue col positions ===")
blue = (b > 120) & (r < 110) & (g < 110)
for y in range(516, 524):
    xs = np.where(blue[y, 150:860])[0] + 150
    if len(xs):
        # runs
        runs = []
        s = p = xs[0]
        for x in xs[1:]:
            if x == p + 1: p = x
            else: runs.append((s, p)); s = p = x
        runs.append((s, p))
        longruns = [rn for rn in runs if rn[1] - rn[0] > 15]
        print(f"y={y}: n={len(xs)} runs>{15}px: {longruns}")

# g. bars modal + y extent
from collections import Counter
for lbl, xa, xb in [("bar1", 414, 427), ("bar2", 562, 575), ("bar3", 704, 717), ("bar4", 834, 847)]:
    patch = im[185:455, xa:xb].reshape(-1, 3)
    cnt = Counter(tuple(int(v) // 8 * 8 for v in p) for p in patch)
    print(f"{lbl} modal: {cnt.most_common(2)}")
# bar y extent at bar1 center x=420
col = im[:, 420]
ys = [y for y in range(170, 475) if abs(int(col[y][0])-233)+abs(int(col[y][1])-233)+abs(int(col[y][2])-231) > 30]
print(f"bar1 center col x=420 non-panel rows: {ys[0]}..{ys[-1]} n={len(ys)}")
