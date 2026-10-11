#!/usr/bin/env python3
# measure3_bands.py — precise raw-RGB band dumps + arrows + line bboxes (attempt 3)
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[..., 0], img[..., 1], img[..., 2]

def col_dump(x, y0, y1, tag):
    print(f"--- col x={x} {tag}")
    prev = None
    for y in range(y0, y1):
        px = tuple(img[y, x])
        if prev is None or max(abs(px[i] - prev[i]) for i in range(3)) > 28:
            print(f"  y={y}: {px}")
            prev = px

def row_dump(y, x0, x1, tag):
    print(f"--- row y={y} {tag}")
    prev = None
    for x in range(x0, x1):
        px = tuple(img[y, x])
        if prev is None or max(abs(px[i] - prev[i]) for i in range(3)) > 28:
            print(f"  x={x}: {px}")
            prev = px

# RIGHT BLOCK structure: raw dumps
for x in [658, 680, 700, 730, 760, 790, 815, 835]:
    col_dump(x, 255, 480, "right block")
for y in [300, 340, 400, 440, 465]:
    row_dump(y, 630, 895, "right block")

# LEFT STACK: row profile of green + col dump
gm = (G - R > 40) & (G - B > 40)
print("--- left stack row profile (count in x165..215)")
runs = []
prev = 0
for y in range(255, 435):
    n = int(gm[y, 165:215].sum())
    if (n > 6) != (prev > 6):
        print(f"  y={y} n={n}")
    prev = n
col_dump(185, 255, 435, "left stack")
row_dump(300, 160, 220, "left stack")

# MIDDLE GRID: row bands via col dump at x=400 (inside col 1) and x=505 (col 4 right edge)
col_dump(400, 248, 430, "mid grid c1")
col_dump(490, 248, 430, "mid grid c4")
row_dump(280, 370, 525, "mid grid")
row_dump(262, 370, 525, "mid grid top faces")

# LABEL BOX borders: 1px scans
print("--- box border scans")
row_dump(210, 70, 105, "left box left border")
row_dump(210, 290, 345, "left box right border + mid box left")
row_dump(210, 590, 612, "mid box right border")
row_dump(195, 620, 640, "right box left border")
row_dump(195, 865, 895, "right box right border + blue frame")
col_dump(150, 185, 245, "left box top/bottom")
col_dump(450, 185, 245, "mid box top/bottom")
col_dump(700, 155, 235, "right box top/bottom")

# blue frame core color: darkest pixels on the border lines
seg = img[133:137, 200:800].reshape(-1, 3)
d = seg.sum(axis=1)
idx = np.argsort(d)[:30]
print("blue frame top-line darkest:", seg[idx].mean(axis=0).round(1))
seg = img[300:460, 68:71].reshape(-1, 3)
d = seg.sum(axis=1)
idx = np.argsort(d)[:30]
print("blue frame left-line darkest:", seg[idx].mean(axis=0).round(1))
# red border color of label boxes: darkest on leftbox top border row
seg = img[194:197, 100:300].reshape(-1, 3)
d = seg.sum(axis=1)
idx = np.argsort(d)[:30]
print("labelbox border darkest:", seg[idx].mean(axis=0).round(1))
# title core color
seg = img[72:112, 204:780].reshape(-1, 3)
dk = seg[seg.sum(axis=1) < 320]
print("title ink n,darkest-quartile:", len(dk), dk[np.argsort(dk.sum(axis=1))[: len(dk) // 4]].mean(axis=0).round(1) if len(dk) else None)

# TEXT LINE bboxes (dark ink) per box line
def ink_bbox(x0, y0, x1, y1, tag):
    seg = img[y0:y1, x0:x1]
    dk = seg.sum(axis=-1) < 560
    ys, xs = np.nonzero(dk)
    if len(xs) == 0:
        print(tag, "none"); return
    print(tag, f"x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")

print("--- text line bboxes")
ink_bbox(80, 192, 330, 214, "L-L1")
ink_bbox(80, 214, 330, 234, "L-L2")
ink_bbox(340, 192, 600, 214, "M-L1")
ink_bbox(340, 214, 600, 234, "M-L2")
ink_bbox(630, 165, 880, 186, "R-L1")
ink_bbox(630, 186, 880, 204, "R-L2")
ink_bbox(630, 203, 880, 224, "R-L3")

# ARROWS (red-ish mask, loose)
rm = (R - G > 40) & (R - B > 40) & (R > 110)
def rbbox(x0, y0, x1, y1, tag):
    sub = rm[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        print(tag, "none"); return
    print(tag, f"x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")

print("--- arrows")
rbbox(630, 315, 660, 345, "v-arrow top head")
rbbox(630, 450, 660, 475, "v-arrow bottom head")
rbbox(636, 340, 650, 445, "v-arrow shaft strip")
rbbox(640, 455, 700, 472, "h-arrow left part")
rbbox(700, 455, 812, 472, "h-arrow right part")
rbbox(786, 380, 896, 480, "d-arrow region")
rbbox(620, 320, 645, 465, "v-rot-label strip")
# rotated label text bboxes (dark ink)
def dkbox(x0, y0, x1, y1, tag):
    seg = img[y0:y1, x0:x1]
    dk = seg.sum(axis=-1) < 560
    ys, xs = np.nonzero(dk)
    if len(xs) == 0:
        print(tag, "none"); return
    print(tag, f"x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")
dkbox(622, 330, 642, 460, "rot 'Feature Vector'")
dkbox(648, 465, 745, 483, "'Channels'")
dkbox(648, 482, 745, 502, "'(4 Filters)'")
dkbox(806, 400, 870, 470, "rot '(5 samples)'")
dkbox(830, 395, 895, 465, "rot 'Batch size' zone")
# stacking arrow (white pixels surrounded by color, near top between magenta & yellow)
seg = img[270:330, 640:820]
wt = seg.sum(axis=-1) > 735
ys, xs = np.nonzero(wt)
if len(xs):
    print("white-ish px in top-staircase zone bbox:", 640 + xs.min(), 270 + ys.min(), 640 + xs.max(), 270 + ys.max(), "n", len(xs))
row_dump(296, 690, 800, "stack arrow zone")
