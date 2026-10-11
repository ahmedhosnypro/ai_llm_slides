#!/usr/bin/env python3
"""Pass 3: fix wait2 bbox, per-row callout text analysis, leaders, title comparison s8 vs s6."""
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
    p_ = (img or im).load()
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
    ld = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = ld[x, y]
            if pred(p):
                c[p] += 1
    return c.most_common(6)

# wait2 box: column run (213,345) at wait rows
w2 = bbox(lightblue, 211, 250, 348, 300)
print("waitbox2 bbox:", w2)
t2 = bbox(blueink, w2[0], w2[1], w2[2] + 1, w2[3] + 1)
print("waitbox2 text ink bbox:", t2)
print("waitbox2 text mode:", mode(im, t2[0], t2[1], t2[2]+1, t2[3]+1, blueink)[:3])
rows2 = [(y, sum(1 for x in range(w2[0], w2[2]+1) if blueink(pxl[x, y]))) for y in range(w2[1], w2[3]+1)]
rows2 = [r for r in rows2 if r[1]]
ys2 = [y for y, _ in rows2]
g2 = [(ys2[i+1]-ys2[i], ys2[i]) for i in range(len(ys2)-1)]
print("waitbox2 line gaps:", sorted(g2, reverse=True)[:2], "rows", ys2[0], "..", ys2[-1])
# line split for wait2
split = sorted(g2, reverse=True)[0][1]
l2a = bbox(blueink, w2[0], w2[1], w2[2]+1, split+1)
l2b = bbox(blueink, w2[0], split+1, w2[2]+1, w2[3]+1)
print("waitbox2 line1 bbox:", l2a, " line2 bbox:", l2b)

# wait1 line split too (gap after y=270)
w1 = (52, 257, 184, 292)
l1a = bbox(blueink, w1[0], w1[1], w1[2]+1, 271)
l1b = bbox(blueink, w1[0], 271, w1[2]+1, w1[3]+1)
print("waitbox1 line1 bbox:", l1a, " line2 bbox:", l1b)

# callout per-line: line1 y183..199, line2 y202..212, underline 213..216
c_line1 = bbox(blueink, 43, 180, 330, 200)
c_line2 = bbox(blueink, 43, 201, 330, 213)
c_under = bbox(blueink, 43, 213, 330, 219)
print("callout line1 bbox:", c_line1)
print("callout line2 bbox:", c_line2)
print("callout underline bbox (y213..218):", c_under)
# underline exact rows
for y in range(210, 220):
    cnt = sum(1 for x in range(43, 330) if blueink(pxl[x, y]))
    row = [x for x in range(43, 330) if blueink(pxl[x, y])]
    print(f"  y={y}: n={cnt} x {min(row) if row else '-'}..{max(row) if row else '-'}")

# leaders
lA = bbox(blueink, 0, 231, 480, 256)
print("leader band y231..255:", lA)
if lA:
    for y in range(lA[1], lA[3]+1):
        row = [x for x in range(0, 480) if blueink(pxl[x, y])]
        if row:
            print(f"  y={y}: x {min(row)}..{max(row)} n={len(row)}")
lB = bbox(blueink, 0, 293, 480, 335)
print("leader band y293..334:", lB)
if lB:
    for y in range(lB[1], lB[3]+1, 2):
        row = [x for x in range(0, 480) if blueink(pxl[x, y])]
        if row:
            print(f"  y={y}: x {min(row)}..{max(row)} n={len(row)}")
# leader at callout right edge x 330..480, y 168..232 (the scissors/leader run)
lC = bbox(blueink, 326, 165, 480, 232)
print("blue ink right of callout (x326..480, y165..232):", lC)

# title: s8 vs s6, red ink in x 260..660 (avoid decoder caption x>660)
def rows_of(img, pred, x0, x1, y0, y1, tag):
    out = [(y, sum(1 for x in range(x0, x1) if pred(img.load()[x, y]))) for y in range(y0, y1)]
    out = [r for r in out if r[1]]
    print(tag, "rows:", out[0][0] if out else None, "..", out[-1][0] if out else None,
          "| first3:", out[:3], "last3:", out[-3:])
    bb = bbox(pred, x0, y0, x1, y1, img)
    print(tag, "bbox:", bb)
    return bb

r8 = rows_of(im, redink, 260, 660, 40, 115, "s8 red title")
r6 = rows_of(im6, redink, 260, 660, 40, 115, "s6 red title")
b8 = rows_of(im, blueink, 260, 660, 60, 130, "s8 blue line2")
b6 = rows_of(im6, blueink, 260, 660, 60, 130, "s6 blue line2")
# title fill modes
print("s8 title red mode:", mode(im, r8[0], r8[1], r8[2]+1, r8[3]+1, redink)[:3])
print("s8 challenges blue mode:", mode(im, b8[0], b8[1], b8[2]+1, b8[3]+1, blueink)[:3])
