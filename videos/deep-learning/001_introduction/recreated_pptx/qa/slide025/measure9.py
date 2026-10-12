#!/usr/bin/env python3
# measure9.py - final pre-build probe for slide 025 (banked evidence)
from PIL import Image
import collections
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
p = im.load()

def darkbbox(x0, x1, y0, y1, thr=120):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = p[x, y]
            if r < thr and g < thr and b < thr:
                xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))

print("== A. magbox text ink ==")
print("IS l1:", darkbbox(64, 135, 98, 110))
print("IS l2:", darkbbox(64, 135, 110, 125))
print("SL l1:", darkbbox(612, 680, 98, 110))
print("SL l2:", darkbbox(612, 680, 110, 125))

def modal(x0, x1, y0, y1):
    c = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[p[x, y]] += 1
    return c.most_common(3)

print("== B. eq boxes ==")
print("b1 fill:", modal(120, 200, 475, 495))
print("b2 fill:", modal(340, 420, 470, 490))
print("b3 fill:", modal(600, 680, 465, 485))
def bordscan_row(y, x0, x1):
    return [(x, p[x, y]) for x in range(x0, x1) if sum(p[x, y]) < 560]
print("b1 row480:", bordscan_row(480, 60, 260)[:8])
print("b2 row480:", bordscan_row(480, 285, 510)[:8])
print("b3 row475:", bordscan_row(475, 535, 755)[:8])
def bordscan_col(x, y0, y1):
    return [(y, p[x, y]) for y in range(y0, y1) if sum(p[x, y]) < 560]
print("b1 col160:", bordscan_col(160, 440, 520)[:8])
print("b2 col340:", bordscan_col(340, 440, 520)[:8])
print("b3 col600:", bordscan_col(600, 435, 515)[:8])

def cls(r, g, b):
    if r < 100 and g < 100 and b < 100: return "K"
    if r > 180 and g < 110 and b < 110: return "R"
    if r > 190 and g > 190 and b > 190: return "W"
    if r > 140 and g < 120 and b > 140: return "M"
    if g > 150 and r < g - 30 and b < g: return "g"
    if 150 <= r <= 225 and 140 <= g <= 215 and 120 <= b <= 195: return "t"
    return "."

def zone(x0, x1, y0, y1, step=1):
    print(f"-- zone x{x0}..{x1} y{y0}..{y1}")
    for y in range(y0, y1):
        print(f"{y:4d} " + "".join(cls(*p[x, y]) for x in range(x0, x1, step)))

print("== C. outrow maps ==")
zone(440, 510, 172, 191)
zone(440, 510, 245, 263)
zone(440, 510, 326, 345)
print("== D. j arrow zone ==")
zone(402, 448, 362, 400)
print("== H. i arrow zone ==")
zone(244, 282, 362, 400)
print("== E. neuron col extents ==")
for (cx, y0, y1, tag) in [(261,150,220,"c1r1"),(426,150,220,"c2r1"),(261,230,285,"c1r2"),(261,310,365,"c1r3")]:
    rows = [y for y in range(y0, y1) if any((lambda c: c[1] > 150 and c[0] < c[1]-20 and c[2] < c[1])(p[cx+dx, y]) for dx in (-3,0,3))]
    print(tag, "green rows:", (min(rows), max(rows)) if rows else None)
print("== F/G. border modals ==")
print("class L:", p[612, 181], p[612, 182], " R:", p[674, 181], p[674, 182])
print("outbox L:", p[501, 182], p[501, 183], " T:", p[530, 174], p[530, 175])
print("== J. eq ink bboxes (dark px) ==")
print("eq1:", darkbbox(75, 245, 463, 500))
print("eq2:", darkbbox(295, 445, 458, 500, 130))
print("eq3:", darkbbox(543, 747, 450, 502, 130))
