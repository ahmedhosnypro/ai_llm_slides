#!/usr/bin/env python3
"""Final decisive scans for slide_031.jpg."""
from PIL import Image
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

print("== A. left edge band at y=200 (x0..80 raw) ==")
prev = None
for x in range(0, 80):
    c = px[x, 200]
    b = "W" if all(v > 235 for v in c) else ("G" if all(190 < v < 225 for v in c) else ("P" if c[0] > 235 and 200 < c[1] < 240 and 185 < c[2] < 225 else "?"))
    if b != prev:
        print(f"  x={x}: {c} [{b}]")
        prev = b

print("\n== B. right region bands ==")
for y in [330, 376, 440, 470, 520, 533]:
    runs = []
    prev = None; s = 0
    for x in range(455, 935):
        c = px[x, y]
        b = "W" if all(v > 235 for v in c) else ("P" if c[0] > 235 and 200 < c[1] < 240 and 185 < c[2] < 225 else ("Y" if c[0] > 235 and c[1] > 215 and c[2] < 160 else "?"))
        if b != prev:
            if prev is not None: runs.append((prev, s, x-1))
            prev = b; s = x
    runs.append((prev, s, 934))
    print(f"  y={y}: " + " ".join(f"{c}{a}-{b}" for c, a, b in runs if b-a >= 1))

print("\n== C. K top border: green counts per row y296..320 (x70..450) ==")
for y in range(296, 321):
    n = sum(1 for x in range(70, 450) if (lambda c: c[1] > 110 and c[1]-c[0] > 30 and c[1]-c[2] > 30)(px[x, y]))
    raw = [px[x, y] for x in (100, 250, 400)]
    print(f"  y={y}: green={n} raw@100/250/400={raw}")

print("\n== D. title highlight rows/cols ==")
def pred_yel(c): r,g,b=c; return r>235 and g>215 and b<160
rows = [(y, sum(1 for x in range(430, 790) if pred_yel(px[x, y]))) for y in range(40, 80)]
print("  rows:", [(y, n) for y, n in rows if n > 30])
cols = [(x, sum(1 for y in range(42, 76) if pred_yel(px[x, y]))) for x in range(420, 800)]
xs = [x for x, n in cols if n > 8]
print(f"  cols extent: {min(xs)}..{max(xs)}" if xs else "  none")

print("\n== E. subtitle red/blue token extents (y70..94, x100..895) ==")
def pred_red(c): r,g,b=c; return r>130 and r-g>60 and r-b>60
def pred_blue(c): r,g,b=c; return b>110 and b-r>50 and b-g>40
red_cols = [x for x in range(100, 895) if any(pred_red(px[x, y]) for y in range(70, 94))]
blue_cols = [x for x in range(100, 895) if any(pred_blue(px[x, y]) for y in range(70, 94))]
def spans(cols):
    if not cols: return []
    out = []; s = cols[0]; p = cols[0]
    for x in cols[1:]:
        if x - p > 6:
            out.append((s, p)); s = x
        p = x
    out.append((s, p)); return out
print("  red spans:", spans(red_cols))
print("  blue spans:", spans(blue_cols))

print("\n== F. matrix cell zooms (fine classes) ==")
def cls(c):
    r, g, b = c
    if r > 238 and g > 238 and b > 238: return "."
    if r < 80 and g < 80 and b < 80: return "K"      # black
    if b > 60 and b-r > 30 and b-g > 30 and r < 120: return "N"  # navy
    if r > 60 and r-b > 30 and g < 90 and b < 90 and r < 150: return "M"  # magenta/maroon
    if r > 90 and r-b > 40 and g > 25 and g < 80 and b < 40: return "O"   # orange/brown
    if g > 90 and g-r > 25 and g-b > 25: return "V"  # green
    if r > 225 and 150 < g < 218 and 160 < b < 235 and r-g > 18: return "k"
    if r < 225 and g > 200 and g-r > 10: return "g"
    return "-"
def zoom(x0, x1, y0, y1, label):
    print(f"  -- {label} x{x0}..{x1} y{y0}..{y1}")
    print("      " + "".join(str((x//10) % 10) if x % 10 == 0 else " " for x in range(x0, x1)))
    for y in range(y0, y1):
        print(f"  {y:4d} " + "".join(cls(px[x, y]) for x in range(x0, x1)))
zoom(222, 300, 128, 152, "Q matrix r1c1+r1c2")
zoom(260, 300, 250, 275, "Q matrix r4c2")

print("\n== G. callout border dashes ==")
def ring_scan(y0, y1, x0, x1, lbl):
    # count non-white, non-fill pixels per row (border candidates)
    def borderish(c):
        r, g, b = c
        white = r > 235 and g > 235 and b > 235
        pink = r > 235 and 165 < g < 215 and 175 < b < 230 and r-g > 30
        peach = r > 235 and 200 < g < 240 and 185 < b < 225
        ltgreen = g > 225 and r < 245 and b < 245 and g-r > 8
        return not (white or pink or peach or ltgreen)
    rows = [(y, sum(1 for x in range(x0, x1) if borderish(px[x, y]))) for y in range(y0, y1)]
    print(f"  {lbl} rows:", [(y, n) for y, n in rows if n > 6])
ring_scan(262, 316, 438, 632, "callout1")
ring_scan(300, 350, 688, 895, "callout2")
ring_scan(324, 382, 438, 632, "callout3")
def col_scan(x0, x1, y0, y1, lbl):
    def borderish(c):
        r, g, b = c
        white = r > 235 and g > 235 and b > 235
        pink = r > 235 and 165 < g < 215 and 175 < b < 230 and r-g > 30
        peach = r > 235 and 200 < g < 240 and 185 < b < 225
        ltgreen = g > 225 and r < 245 and b < 245 and g-r > 8
        return not (white or pink or peach or ltgreen)
    cols = [(x, sum(1 for y in range(y0, y1) if borderish(px[x, y]))) for x in range(x0, x1)]
    print(f"  {lbl} cols:", [(x, n) for x, n in cols if n > 5])
col_scan(430, 645, 268, 312, "callout1")
col_scan(685, 900, 303, 347, "callout2")
col_scan(430, 645, 328, 378, "callout3")

print("\n== H. emphasis + notebox line bands ==")
def pred_red(c): r,g,b=c; return r>130 and r-g>60 and r-b>60
def pred_blue(c): r,g,b=c; return b>110 and b-r>50 and b-g>40
print("  emphasis red rows:", [(y, sum(1 for x in range(648, 880) if pred_red(px[x, y]))) for y in range(386, 436) if sum(1 for x in range(648, 880) if pred_red(px[x, y])) > 8])
print("  notebox red rows:", [(y, sum(1 for x in range(495, 890) if pred_red(px[x, y]))) for y in range(450, 516) if sum(1 for x in range(495, 890) if pred_red(px[x, y])) > 5])
for y in [462, 485, 503]:
    reds = [x for x in range(495, 890) if pred_red(px[x, y])]
    blues = [x for x in range(495, 890) if pred_blue(px[x, y])]
    def spans(cols):
        if not cols: return []
        out = []; s = cols[0]; p = cols[0]
        for x in cols[1:]:
            if x - p > 8: out.append((s, p)); s = x
            p = x
        out.append((s, p)); return out
    print(f"  y={y} red spans:", spans(reds))
    print(f"  y={y} blue span extent:", (min(blues), max(blues)) if blues else None)

print("\n== I. matrix bg samples away from text ==")
for x, y, lbl in [(230, 120, "Q r1c1 corner"), (300, 190, "Q r2 gap"), (350, 280, "Q r4 low"),
                  (650, 120, "V r1c1"), (700, 190, "V r2"), (230, 340, "K r1c1"), (300, 410, "K r2"),
                  (350, 495, "K r4 low")]:
    print(f"  {lbl} ({x},{y}): {px[x, y]}")

print("\n== J. badge zone raw ==")
print("  (893,71):", px[893, 71], " (880,58):", px[880, 58], " (906,84):", px[906, 84])
