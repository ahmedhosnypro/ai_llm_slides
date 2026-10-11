#!/usr/bin/env python3
"""Pass 2: per-box bboxes, text lines, underline, leaders, color modes; compare title vs slide 6."""
from PIL import Image
import collections

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
im6 = Image.open(BASE + "unique_slides/slide_006.jpg").convert("RGB")
pxl = im.load()

def lightblue(p):
    r, g, b = p
    return b > 200 and b - r > 12 and g > 190 and r > 170

def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140

def redink(p):
    r, g, b = p
    return r > 120 and r - g > 60 and r - b > 60

def bbox(pred, x0, y0, x1, y1, img=None):
    p_ = img if img else pxl
    minx, miny, maxx, maxy, n = 10**9, 10**9, -1, -1, 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(p_[x, y]):
                n += 1
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    return (minx, miny, maxx, maxy, n) if n else None

def mode(img, x0, y0, x1, y1, pred):
    c = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = img.load()[x, y]
            if pred(p):
                c[p] += 1
    return c.most_common(6)

def col_runs(pred, y0, y1, x0=0, x1=480, minrun=8):
    runs, start = [], None
    for x in range(x0, x1):
        hit = any(pred(pxl[x, y]) for y in range(y0, y1))
        if hit and start is None: start = x
        if not hit and start is not None:
            if x - start >= minrun: runs.append((start, x - 1))
            start = None
    if start is not None and x1 - start >= minrun: runs.append((start, x1 - 1))
    return runs

# callout box columns (y 171..228 core rows)
print("callout col runs (y171..228):", col_runs(lightblue, 171, 228))
# wait boxes columns (y 257..292)
print("waitbox col runs (y257..292):", col_runs(lightblue, 257, 292))

# callout bbox precise
cb = bbox(lightblue, 0, 160, 480, 245)
print("callout box bbox:", cb)
print("callout fill mode:", mode(im, cb[0]+5, cb[1]+5, cb[2]-4, cb[3]-4, lambda p: not blueink(p))[:3])

# callout text lines: blue ink rows inside callout
text_rows = []
for y in range(cb[1], cb[3] + 1):
    cnt = sum(1 for x in range(cb[0], cb[2] + 1) if blueink(pxl[x, y]))
    if cnt: text_rows.append((y, cnt))
print("callout text rows:", text_rows[:3], "...", text_rows[-3:] if len(text_rows) > 3 else "")
# gaps
prev = None
for y, cnt in text_rows:
    if prev is not None and y - prev > 1:
        print(f"  callout text gap between y={prev} and y={y}")
    prev = y
# line 1 bbox / line 2 bbox: split at the biggest gap
ys = [y for y, _ in text_rows]
gaps = [(ys[i+1] - ys[i], ys[i]) for i in range(len(ys) - 1)]
gaps.sort(reverse=True)
print("callout top-3 gaps (size, after_y):", gaps[:3])

# text ink bbox inside callout (full)
tb = bbox(blueink, cb[0], cb[1], cb[2] + 1, cb[3] + 1)
print("callout text ink bbox:", tb)
print("callout text ink mode:", mode(im, tb[0], tb[1], tb[2]+1, tb[3]+1, blueink)[:3])

# underline detection: bottom-most blue rows spanning wide horizontally
for y in range(cb[3] - 2, cb[1], -1):
    cnt = sum(1 for x in range(cb[0], cb[2] + 1) if blueink(pxl[x, y]))
    if cnt > 40:
        print(f"  underline candidate row y={y} count={cnt}")
        ub = bbox(blueink, cb[0], y, cb[2] + 1, y + 1)
        print("  underline bbox at that row:", ub)
        break

# wait boxes: split columns
wb = bbox(lightblue, 0, 250, 480, 300)
print("wait boxes combined bbox:", wb)
# two column runs at wait rows
wr = col_runs(lightblue, 257, 292, minrun=5)
print("waitbox column runs (minrun5):", wr)
if len(wr) >= 2:
    (b1x0, b1x1), (b2x0, b2x1) = wr[0], wr[1]
    w1 = bbox(lightblue, b1x0 - 2, 250, b1x1 + 3, 300)
    w2 = bbox(lightblue, b2x0 - 2, 250, b2x1 + 3, 300)
    print("waitbox1 bbox:", w1)
    print("waitbox2 bbox:", w2)
    for name, bx in (("wait1", w1), ("wait2", w2)):
        t = bbox(blueink, bx[0], bx[1], bx[2] + 1, bx[3] + 1)
        print(f"{name} text ink bbox:", t)
        print(f"{name} text mode:", mode(im, t[0], t[1], t[2]+1, t[3]+1, blueink)[:3])
        rows = [(y, sum(1 for x in range(bx[0], bx[2]+1) if blueink(pxl[x, y]))) for y in range(bx[1], bx[3]+1)]
        rows = [r for r in rows if r[1]]
        ys = [y for y, _ in rows]
        g = [(ys[i+1] - ys[i], ys[i]) for i in range(len(ys)-1)]
        print(f"{name} line gaps:", sorted(g, reverse=True)[:2], f"rows {ys[0]}..{ys[-1]}")

# leaders: blue ink BELOW the callout (y 230..255) and BELOW wait boxes (y 293..330)
l1 = bbox(blueink, 0, 230, 480, 256)
print("leader ink between callout & wait boxes:", l1)
l2 = bbox(blueink, 0, 293, 480, 340)
print("leader ink below wait boxes:", l2)
# leader below callout right edge going down-right: trace per row
if l1:
    for y in range(l1[1], min(l1[3] + 1, 256)):
        row = [x for x in range(0, 480) if blueink(pxl[x, y])]
        if row:
            print(f"  y={y}: x {min(row)}..{max(row)} n={len(row)}")

# title red-ink row profile (slide 8 vs slide 6) in band x 260..810
def rows_of(img, pred, x0, x1, y0, y1, tag):
    out = []
    for y in range(y0, y1):
        cnt = sum(1 for x in range(x0, x1) if pred(img.load()[x, y]))
        if cnt: out.append((y, cnt))
    print(tag, "first:", out[0] if out else None, "last:", out[-1] if out else None)
    return out

rows_of(im, redink, 260, 810, 40, 115, "s8 red title rows")
rows_of(im6, redink, 260, 810, 40, 115, "s6 red title rows")
rows_of(im, blueink, 260, 810, 60, 130, "s8 blue title rows")
rows_of(im6, blueink, 260, 810, 60, 130, "s6 blue title rows")
