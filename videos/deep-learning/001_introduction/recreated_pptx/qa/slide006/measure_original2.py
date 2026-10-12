#!/usr/bin/env python3
# measure_original2.py — refined forensics: strict masks, border long-run detection,
# header line split + underline, bullet-12 hunt, cursor zone, full box edges.
from PIL import Image
import numpy as np

ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (r > 110) & (r - g > 45) & (r - b > 35)
strict_black = a.max(axis=2) < 100
dark = a.max(axis=2) < 150
blue = (b > 105) & (b - r > 55) & (b - g > 55)
blue_loose = (b - r > 25) & (b - g > 25) & (b > 110) & (r < 160)

def bbox(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (int(xs.min()) + x0, int(xs.max()) + x0, int(ys.min()) + y0, int(ys.max()) + y0)

print("== box borders via long runs ==")
# top border: rows 110..140, count red in x 95..875
for y in range(115, 142):
    c = red[y, 95:875].sum()
    if c > 400:
        print(f"  row {y}: red count {c}")
print("bottom:")
for y in range(495, 512):
    c = red[y, 95:875].sum()
    if c > 400:
        print(f"  row {y}: red count {c}")
print("left cols (x 80..100, red count in y 140..500):")
for x in range(80, 100):
    c = red[140:500, x].sum()
    if c > 200:
        print(f"  col {x}: {c}")
print("right cols (x 865..900):")
for x in range(865, 900):
    c = red[140:500, x].sum()
    if c > 200:
        print(f"  col {x}: {c}")

print("== header (strict black, y 136..205, x 91..878) ==")
hb = bbox(strict_black, 91, 878, 136, 205)
print("header strict-black bbox:", hb)
rows = strict_black[hb[2]:hb[3] + 1, hb[0]:hb[1] + 1].sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 0 and not inb:
        s = i; inb = True
    elif v == 0 and inb:
        bands.append((s + hb[2], i - 1 + hb[2])); inb = False
if inb:
    bands.append((s + hb[2], len(rows) - 1 + hb[2]))
print("header line bands:", bands)
for k, (y0, y1) in enumerate(bands):
    lb = bbox(strict_black, 91, 878, y0, y1 + 1)
    print(f"  L{k}: bbox {lb} adv {lb[1]-lb[0]+1}")
    # long horizontal runs (underline)
    for yy in range(y0, y1 + 1):
        seg = strict_black[yy, 91:878]
        if seg.sum() > 180:
            xs2 = np.where(seg)[0]
            print(f"    long-run row y={yy}: x {xs2.min()+91}..{xs2.max()+91} count {seg.sum()}")

print("== bullet 12 hunt (y 476..502, x 95..880) ==")
for name, m in [("dark", dark), ("strict_black", strict_black), ("blue", blue), ("blue_loose", blue_loose)]:
    bb2 = bbox(m, 95, 880, 476, 502)
    print(f"  {name}: {bb2}")
# row profile of any ink there
rows = (dark | blue_loose)[476:502, 95:880].sum(axis=1)
print("  ink row profile y476..501:", {476 + i: int(v) for i, v in enumerate(rows) if v > 0})

print("== recheck: blue bands with loose mask (y 195..502) ==")
rows = blue_loose[195:502, 95:880].sum(axis=1)
bands2 = []
inb = False
for i, v in enumerate(rows):
    if v > 2 and not inb:
        s = i; inb = True
    elif v <= 2 and inb:
        bands2.append((s + 195, i - 1 + 195)); inb = False
if inb:
    bands2.append((s + 195, len(rows) - 1 + 195))
print(f"n loose-blue bands: {len(bands2)}")
for k, (y0, y1) in enumerate(bands2):
    lb = bbox(blue_loose, 95, 880, y0, y1 + 1)
    print(f"  band {k+1}: y {y0}..{y1} x {lb[0]}..{lb[1]} adv {lb[1]-lb[0]+1}")

print("== cursor zone (strict dark, x 215..330, y 350..440) ==")
cb = bbox(strict_black, 215, 330, 350, 440)
print("strict-black bbox in cursor window:", cb)
if cb:
    # print row runs to see shape
    for yy in range(cb[2], cb[3] + 1, 3):
        xs2 = np.where(strict_black[yy, 215:330])[0]
        if len(xs2):
            print(f"  y={yy}: x {xs2.min()+215}..{xs2.max()+215} n={len(xs2)}")

print("== bullet text left edges (strict per band, loose mask, x>=195) ==")
for k, (y0, y1) in enumerate(bands2):
    lb = bbox(blue_loose, 195, 880, y0, y1 + 1)
    if lb:
        print(f"  band {k+1}: text-left {lb[0]}")

print("== colors (modal, saturated cores) ==")
def modal(mask, x0, x1, y0, y1, minsat=None):
    px = a[y0:y1, x0:x1][mask[y0:y1, x0:x1]]
    if minsat is not None:
        px = px[px.max(axis=1) - px.min(axis=1) > minsat]
    if not len(px):
        return None
    vals, counts = np.unique(px, axis=0, return_counts=True)
    order = np.argsort(-counts)[:3]
    return [(tuple(int(v) for v in vals[i]), int(counts[i])) for i in order]
print("title red modal (sat>60):", modal(red, 142, 833, 84, 125, 60))
print("border red modal (row 502-504):", modal(red, 95, 875, 502, 505, 40))
print("bullet blue modal (loose mask core, sat>80):", modal(blue_loose, 205, 570, 202, 476, 80))
print("header black modal (strict):", modal(strict_black, 91, 878, 136, 199))
