#!/usr/bin/env python3
"""Measure remaining details: title metrics, callout text metrics, yellow band, block arrows, feedback arrow."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

# --- Title: glyph column profile to find cap height & text extent
def ink_cols(x0, x1, y0, y1, thr=150):
    cols = []
    for x in range(x0, x1+1):
        ys = [y for y in range(y0, y1+1) if all(A[y, x][i] < thr for i in range(3)) or A[y,x][0]>140 and A[y,x][1]<110 and A[y,x][2]<110]
        if ys: cols.append((x, min(ys), max(ys)))
    return cols

# Title red text: use red mask
def red_extent(x0, x1, y0, y1):
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            r, g, b = A[y, x]
            if r > 130 and g < 120 and b < 120 and r-g > 50:
                xs.append(x); ys.append(y)
    return (min(xs), max(xs), min(ys), max(ys)) if xs else None

e = red_extent(150, 820, 40, 100)
print("title red extent:", e)  # x0,x1,y0,y1

# 'E' of Encoder — first glyph: find leftmost red column band
# Cap height: measure 'E' column range
cols = {}
for y in range(50, 95):
    for x in range(200, 760):
        r, g, b = A[y, x]
        if r > 130 and g < 120 and b < 120 and r-g > 50:
            cols.setdefault(x, []).append(y)
xs_sorted = sorted(cols)
# first glyph cluster
first = [x for x in xs_sorted if x <= 232]
ys_first = [y for x in first for y in cols[x]]
print(f"'E' cluster x{min(first)}..{max(first)} y{min(ys_first)}..{max(ys_first)} capH={max(ys_first)-min(ys_first)+1}")

# --- Callout text metrics (dark text on fills)
def dark_extent(x0, x1, y0, y1, thr=120):
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if all(A[y, x][i] < thr for i in range(3)):
                xs.append(x); ys.append(y)
    return (min(xs), max(xs), min(ys), max(ys)) if xs else None

print("callout1 line1:", dark_extent(110, 520, 128, 152))
print("callout1 line2:", dark_extent(110, 520, 152, 178))
print("callout2 line1:", dark_extent(190, 480, 222, 245))
print("callout2 line2:", dark_extent(190, 480, 245, 272))
print("callout3 line1:", dark_extent(110, 515, 344, 363))
print("callout3 line2:", dark_extent(110, 515, 363, 388))
print("callout4 line1:", dark_extent(95, 525, 472, 494))
print("callout4 line2:", dark_extent(95, 525, 494, 514))

# colored text in callout2: purple line1 / red line2
def col_extent(x0, x1, y0, y1, test):
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if test(*A[y, x]):
                xs.append(x); ys.append(y)
    return (min(xs), max(xs), min(ys), max(ys)) if xs else None

purple = lambda r,g,b: 110 < r < 200 and g < 90 and b > 140
redtxt = lambda r,g,b: r > 130 and g < 80 and b < 80
print("callout2 line1 purple:", col_extent(190, 480, 222, 245, purple))
print("callout2 line2 red:", col_extent(190, 480, 245, 272, redtxt))
# dark red text in callouts 3/4 (943634-ish)
dr = lambda r,g,b: 120 < r < 180 and g < 90 and b < 90
print("callout3 line1 darkred:", col_extent(110, 515, 344, 363, dr))
# callout1 dark blue
db = lambda r,g,b: r < 90 and g < 90 and b > 90
print("callout1 line1 darkblue:", col_extent(110, 520, 128, 152, db))

# --- Yellow L-band precise geometry
def yellow_mask_region(x0, x1, y0, y1):
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            r, g, b = A[y, x]
            if r > 200 and g > 200 and b < 130:
                xs.append(x); ys.append(y)
    return xs, ys

xs, ys = yellow_mask_region(640, 800, 240, 340)
print(f"yellow L-band: x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} n={len(xs)}")
# row profile of the band
from collections import Counter
rows = Counter()
for x, y in zip(xs, ys):
    rows[y] += 1
print("  row counts:", {y: rows[y] for y in sorted(rows) if rows[y] > 3})

# yellow behind Outputs
xs2, ys2 = yellow_mask_region(740, 830, 485, 515)
print(f"yellow Outputs: x{min(xs2)}..{max(xs2)} y{min(ys2)}..{max(ys2)} n={len(xs2)}")
# yellow top (Output Probabilities)
xs3, ys3 = yellow_mask_region(740, 830, 105, 135)
print(f"yellow top: x{min(xs3)}..{max(xs3)} y{min(ys3)}..{max(ys3)} n={len(xs3)}")

# --- Red block arrows: 3 of them
def red_blocks(x0, x1, y0, y1, name):
    pts = [(x, y) for y in range(y0, y1+1) for x in range(x0, x1+1)
           if A[y,x][0] > 150 and A[y,x][1] < 90 and A[y,x][2] < 90]
    if not pts:
        print(f"{name}: none"); return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"{name}: x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} n={len(pts)}")

red_blocks(630, 700, 480, 520, "arrow1 enc bottom")
red_blocks(740, 830, 480, 520, "arrow2 dec bottom")
red_blocks(735, 760, 110, 145, "arrow3 dec top")
# feedback arrow right margin
red_blocks(880, 920, 100, 530, "feedback right")
red_blocks(850, 895, 430, 530, "feedback low")
