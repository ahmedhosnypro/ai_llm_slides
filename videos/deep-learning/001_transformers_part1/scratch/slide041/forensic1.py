#!/usr/bin/env python3
"""Forensics pass 1 on original slide_041.jpg (960x540, 1px=1pt).
Verify crop-compare findings with pixel numbers:
 A. center zoom: Concat fill, top Linear fill, SDPA stack geometry,
    green inner rectangle, bottom Linear stacked copies, circle/box collision
 B. right panel: Add&Norm fills (blue vs gray), olive containers, green loops,
    Softmax/Linear boxes, V/K/Q circle fills, encoder MHA fill, sine icons
"""
from PIL import Image
import sys

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
print(f"orig size {W}x{H}")
px = im.load()

def sample(name, x, y):
    r, g, b = px[x, y]
    print(f"  {name:38s} ({x:3d},{y:3d}) = #{r:02X}{g:02X}{b:02X}")

def region_hist(name, x0, y0, x1, y1, top=8):
    from collections import Counter
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            c[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
    tot = (x1 - x0) * (y1 - y0)
    print(f"  {name} [{x0},{y0}..{x1},{y1}] n={tot}")
    for (r, g, b), n in c.most_common(top):
        print(f"    #{r:02X}{g:02X}{b:02X}  {100*n/tot:5.1f}%")

print("\n== A. CENTER ZOOM ==")
print("-- Concat box region (build: 364,300..412,345):")
sample("concat center", 388, 322)
sample("concat upper", 388, 310)
sample("concat lower", 388, 335)
region_hist("concat hist", 370, 305, 405, 340)
print("-- top Linear box (build: 366,258..410,296):")
sample("topLinear center", 388, 277)
region_hist("topLinear hist", 372, 262, 404, 292)
print("-- area above Concat (300..345 replaced? scan x=388 col y 240..350):")
for y in range(240, 352, 4):
    r, g, b = px[388, y]
    print(f"    y={y:3d} #{r:02X}{g:02X}{b:02X}")

print("\n-- SDPA stack: red-border pixels in center zoom (x 286..521, y 330..430):")
reds = []
for y in range(330, 432):
    for x in range(286, 522):
        r, g, b = px[x, y]
        if r > 150 and g < 90 and b < 90:
            reds.append((x, y))
if reds:
    xs = [p[0] for p in reds]; ys = [p[1] for p in reds]
    print(f"    red px n={len(reds)} bbox x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)}")
    # row profile to see distinct stacked borders
    from collections import Counter
    rowc = Counter(y for _, y in reds)
    ys_sorted = sorted(rowc)
    bands = []
    start = prev = ys_sorted[0]
    for y in ys_sorted[1:]:
        if y - prev > 3:
            bands.append((start, prev)); start = y
        prev = y
    bands.append((start, prev))
    print(f"    red horizontal-line y-bands: {bands}")
    # column extent for the topmost and bottom band
    for (a, bnd) in bands:
        xs_b = [x for x, y in reds if a <= y <= bnd]
        print(f"      band y{a}..{bnd}: x {min(xs_b)}..{max(xs_b)} n={len(xs_b)}")

print("\n-- green pixels in center zoom (x 286..521, y 208..525):")
greens = []
for y in range(208, 526):
    for x in range(286, 522):
        r, g, b = px[x, y]
        if g > 70 and g > r + 30 and g > b + 20 and r < 160:
            greens.append((x, y))
print(f"    green px n={len(greens)}")
if greens:
    xs = [p[0] for p in greens]; ys = [p[1] for p in greens]
    print(f"    bbox x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)}")
    # vertical strokes: column histogram
    from collections import Counter
    colc = Counter(x for x, _ in greens)
    common = colc.most_common(12)
    print(f"    top green columns: {common}")
    rowc = Counter(y for _, y in greens)
    print(f"    top green rows: {rowc.most_common(12)}")

print("\n-- bottom Linear boxes row: scan x=360 col y 440..510 and x=444:")
for xx in (360, 388, 417, 444, 475):
    runs = []
    cur = None
    for y in range(430, 515):
        r, g, b = px[xx, y]
        # brownish border?
        isb = (120 < r < 200 and 60 < g < 140 and b < 90)
        if isb and cur is None:
            cur = y
        elif not isb and cur is not None:
            runs.append((cur, y - 1)); cur = None
    if cur is not None:
        runs.append((cur, 514))
    print(f"    x={xx}: brown-border y-runs {runs}")

print("\n-- circles row: scan y=496 for circle fills x 300..470:")
row = []
for x in range(300, 472):
    r, g, b = px[x, 496]
    row.append((x, f"#{r:02X}{g:02X}{b:02X}"))
# compress: show color transitions
prev = None
for x, c in row:
    if c != prev:
        print(f"    x={x} {c}")
        prev = c

print("\n== B. RIGHT PANEL ==")
print("-- encoder column scanline x=687, y 110..510 (block bands):")
prev = None
for y in range(108, 512):
    r, g, b = px[687, y]
    c = f"#{r:02X}{g:02X}{b:02X}"
    # quantize to reduce JPEG noise
    q = (r // 24, g // 24, b // 24)
    if q != prev:
        print(f"    y={y:3d} {c}")
        prev = q
