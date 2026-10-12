#!/usr/bin/env python3
"""m1.py — slide 039 frame measurements, part 1.
Panel detection: find the 4 peach panel rects via the tan border color + peach fill.
Original frame: videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg (960x540, 1px=1pt).
"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print("frame size", W, H)

def runs(mask_1d, min_len=3):
    out = []
    s = None
    for i, v in enumerate(mask_1d):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= min_len:
                out.append((s, i - 1))
            s = None
    if s is not None and len(mask_1d) - s >= min_len:
        out.append((s, len(mask_1d) - 1))
    return out

def near(px, ref, tol):
    return all(abs(int(px[i]) - ref[i]) <= tol for i in range(3))

# peach FCE4C8 = (252,228,200); JPEG-washed range guess
peach = (np.abs(a[:, :, 0] - 250) < 14) & (np.abs(a[:, :, 1] - 227) < 16) & (np.abs(a[:, :, 2] - 198) < 20)
print("peach px count:", peach.sum())

# column profile of peach: which x-ranges contain peach
colsum = peach.sum(axis=0)
rowsum = peach.sum(axis=1)
print("peach col presence runs (x):", runs(colsum > 30, 5))
print("peach row presence runs (y):", runs(rowsum > 30, 5))

# Scan a few horizontal lines to find panel left/right edges at various heights
for y in [240, 300, 360, 420, 470]:
    m = peach[y]
    print(f"peach runs row y={y}:", runs(m, 8))

# Scan vertical lines for panel top/bottom edges
for x in [140, 300, 500, 700, 850, 920]:
    m = peach[:, x]
    print(f"peach runs col x={x}:", runs(m, 8))

# Title block: dark ink above y<130, x<600
dark = (a[:, :, 0] < 100) & (a[:, :, 1] < 100) & (a[:, :, 2] < 100)
tzone = dark[30:130, :]
print("title rows (y offset +30):", [(s + 30, e + 30) for s, e in runs(tzone.sum(axis=1) > 4, 3)])
for y0, y1 in runs(tzone.sum(axis=1) > 4, 3):
    band = dark[30 + y0:31 + y1, :640]
    cols = band.sum(axis=0)
    rr = runs(cols > 0, 2)
    print(f"  title band y[{30+y0},{30+y1}] x-extent:", (rr[0][0], rr[-1][1]) if rr else None)

# Sticker: yellow region bottom-right
yellow = (a[:, :, 0] > 200) & (a[:, :, 1] > 200) & (a[:, :, 2] < 120)
ys, xs = np.where(yellow)
if len(xs):
    print("yellow ink bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "count", len(xs))

# bottom red arrows: strong red in y>440
red = (a[:, :, 0] > 150) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
bz = red[430:540, :]
print("red rows in bottom (y+430):", [(s + 430, e + 430) for s, e in runs(bz.sum(axis=1) > 3, 2)])
# arrow columns
bcols = bz.sum(axis=0)
print("bottom red col runs:", runs(bcols > 8, 3))
