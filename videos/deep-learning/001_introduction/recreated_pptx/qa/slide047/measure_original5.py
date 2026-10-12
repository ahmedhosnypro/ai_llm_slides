#!/usr/bin/env python3
"""PIL forensics pass 5 — remaining details (fixed)."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_047.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

def amap(x0, x1, y0, y1, pred, label=""):
    print(f"  {label} x {x0}..{x1} y {y0}..{y1}:")
    for y in range(y0, y1):
        row = "".join("#" if bool(pred(a[y, x])) else "." for x in range(x0, x1))
        print(f"  y={y:3d} {row}")

blueish = lambda p: (p[2] > 100) & (p[2] - p[0] > 25)
reddish = lambda p: (p[0] > 120) & (p[0] - p[1] > 40)

# 1. label box1 text (blue ink)
amap(113, 315, 288, 314, blueish, "box1 'Activation function:' blue ink")
# 2. label box2 text
amap(113, 315, 322, 352, blueish, "box2 'Gradient w.r.t. input' blue ink")
# 3. intro line 2 (red ink) left half
amap(78, 330, 154, 180, reddish, "intro line2 red ink (left)")
# 4. intro line 2 right half
amap(330, 540, 154, 180, reddish, "intro line2 red ink (right)")

# 5. darkest pixel on marker ring
seg = a[228:240, 90:104]
s = seg.sum(axis=2)
iy, ix = np.unravel_index(np.argmin(s), s.shape)
print("ring darkest px:", seg[iy, ix].tolist(), "at", (90 + ix, 228 + iy))
# ring pixels above threshold
m = s < 560
ys, xs = np.nonzero(m)
if len(xs):
    print("ring ink mean color:", seg[m].mean(axis=0).round().tolist(), "n=", len(xs))

# 6. x=58 red line endpoints + width
redm = lambda p: (p[0] > 120) & (p[0] - p[1] > 60) & (p[0] - p[2] > 60)
for x in (56, 57, 58, 59, 60, 61):
    ys = [y for y in range(200, 510) if redm(a[y, x])]
    print(f"x={x}: red n={len(ys)}", f"y {min(ys)}..{max(ys)}" if ys else "")
# does it start/end exactly?
for y in (208, 209, 210, 211, 498, 499, 500, 501):
    row = [x for x in range(54, 64) if redm(a[y, x])]
    print(f"y={y}: red x {row}")

# 7. label box borders color (rows/cols)
print("\nlabel box1 border samples:")
for (yy, xx) in [(287, 200), (288, 200), (312, 200), (313, 200), (300, 109), (300, 110), (300, 310), (300, 311)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())
print("label box2 border samples:")
for (yy, xx) in [(323, 200), (324, 200), (350, 200), (351, 200), (337, 109), (337, 311)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 8. legend border samples
print("\nlegend border samples:")
for (yy, xx) in [(348, 500), (349, 520), (474, 500), (475, 520), (400, 455), (400, 456), (400, 565), (400, 566)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 9. content box border colors
print("\ncontent box border samples:")
for (yy, xx) in [(220, 300), (220, 600), (486, 300), (487, 600), (350, 82), (350, 874)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 10. title + intro core colors
print("\ntitle/intro core stroke samples:")
for lbl, (yy, xx) in [("title-red", (80, 148)), ("title-blue", (75, 460)), ("intro1", (138, 90)),
                      ("intro2", (165, 90)), ("intro3", (195, 90)), ("legend-header", (362, 470)),
                      ("legend-row", (382, 468)), ("eq3-ink", (298, 320)), ("eq4-ink", (330, 330))]:
    print(f"  {lbl} ({xx},{yy}) =", a[yy, xx].tolist())

# 11. grid: exact column boundaries (colored col profile)
green = lambda p: (p[1] > 120) & (p[1] - p[0] > 40) & (p[1] - p[2] > 40)
yellow = lambda p: (p[0] > 180) & (p[1] > 170) & (p[2] < 130)
redf = lambda p: (p[0] > 180) & (p[1] < 90) & (p[2] < 90)
cyan = lambda p: (p[2] > 150) & (p[1] > 120) & (p[0] < 140) & (p[2] - p[0] > 60)
def colprofile(y0, y1):
    counts = []
    for x in range(560, 740):
        n = sum(1 for y in range(y0, y1) if green(a[y, x]) or yellow(a[y, x]) or redf(a[y, x]) or cyan(a[y, x]))
        counts.append((x, n))
    return counts
print("\ngrid col profile rows3-4 (y 426..483): gaps:")
cp = colprofile(426, 484)
gap = [x for x, n in cp if n < 5]
print("  gap cols:", gap)
print("grid col profile rows1-2 (y 365..423): gaps:")
cp = colprofile(365, 424)
gap = [x for x, n in cp if n < 5]
print("  gap cols:", gap)
# row boundaries precise (rows 1-2 vs 3-4)
for y in range(390, 400):
    n = sum(1 for x in range(571, 727) if green(a[y, x]) or yellow(a[y, x]) or redf(a[y, x]) or cyan(a[y, x]))
    print(f"  y={y}: colored n={n}")

# 12. output grid precise gaps
print("\noutput grid gaps:")
for x in range(792, 876):
    n = sum(1 for y in range(394, 456) if green(a[y, x]) or yellow(a[y, x]) or redf(a[y, x]) or cyan(a[y, x]))
    if n < 4:
        print(f"  x={x}: n={n}", end=";")
print()
for y in range(392, 458):
    n = sum(1 for x in range(794, 874) if green(a[y, x]) or yellow(a[y, x]) or redf(a[y, x]) or cyan(a[y, x]))
    if n < 4:
        print(f"  y={y}: n={n}", end=";")
print()

# 13. eq3 'a' region + subscript exact (to size mathtext): main glyph height
# 'a' x-height: rows 294..303 (from map) -> x-height ~10px, subscript to 313
# 14. underline of 'average' in line2
amap(240, 330, 266, 271, lambda p: sum(p) < 500, "line2 underline region")
