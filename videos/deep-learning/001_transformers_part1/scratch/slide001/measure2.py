#!/usr/bin/env python3
"""Fine measurement pass 2: frame strokes, logo region, crosshair, cap heights."""
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
px = im.load()
PPI = W / 13.33  # px per inch = 72

def inch_h(px_x): return round(px_x / PPI, 3)
def inch_v(px_y): return round(px_y / (H / 7.5), 3)

# 1. frame strokes: scan column x=480 and row y=270
print("== column x=480: rows differing from white (frame top) ==")
prev = None
for y in range(0, 60):
    r, g, b = px[480, y]
    if not (r > 245 and g > 245 and b > 245):
        print(f"  y={y} ({inch_v(y)}in) rgb=({r},{g},{b})")
print("== column x=480: rows near bottom differing from gray ==")
for y in range(H-40, H):
    r, g, b = px[480, y]
    if (r, g, b) != (231, 233, 230) and not (r > 245 and g > 245 and b > 245):
        pass
for y in range(H-30, H):
    r, g, b = px[480, y]
    print(f"  y={y} ({inch_v(y)}in) rgb=({r},{g},{b})")

print("== row y=270: cols differing from gray (frame left/right) ==")
runs = []
for x in range(0, 120):
    r, g, b = px[x, 270]
    if not (220 <= r <= 240 and 220 <= g <= 240 and 220 <= b <= 240):
        runs.append((x, (r, g, b)))
print("  left:", runs[:20])
runs = []
for x in range(W-120, W):
    r, g, b = px[x, 270]
    if not (220 <= r <= 240 and 220 <= g <= 240 and 220 <= b <= 240):
        runs.append((x, (r, g, b)))
print("  right:", runs[:20])

# 2. logo region detail: non-canvas, non-white-panel clusters in x 560-940, y 440-540
print("== logo region: column ink profile (x 560..940, y 440..540) ==")
cols = []
for x in range(560, min(940, W)):
    n = 0
    for y in range(440, min(540, H)):
        r, g, b = px[x, y]
        # canvas gray ~ (231,233,230); count anything that differs notably
        if abs(r-231) > 25 or abs(g-233) > 25 or abs(b-230) > 25:
            n += 1
    cols.append((x, n))
# print runs of n>0
run = None
for x, n in cols:
    if n > 0:
        if run is None: run = [x, x, 0]
        run[1] = x; run[2] = max(run[2], n)
    else:
        if run: print(f"  ink cols x={run[0]}-{run[1]} ({inch_h(run[0])}-{inch_h(run[1])}in) maxrows={run[2]}"); run = None
if run: print(f"  ink cols x={run[0]}-{run[1]} ({inch_h(run[0])}-{inch_h(run[1])}in) maxrows={run[2]}")

print("== logo region: row ink profile (y 440..540 over x 560..940) ==")
for y in range(440, min(540, H)):
    n = 0
    for x in range(560, min(940, W)):
        r, g, b = px[x, y]
        if abs(r-231) > 25 or abs(g-233) > 25 or abs(b-230) > 25:
            n += 1
    if n > 0:
        print(f"  y={y} ({inch_v(y)}in) ink={n}")

# 3. crosshair region x 130-220, y 170-240
print("== crosshair scan (pixels darker than canvas by >12) ==")
found = []
for y in range(170, 240):
    for x in range(130, 230):
        r, g, b = px[x, y]
        if (231 - r) > 12 and (233 - g) > 12 and (230 - b) > 12:
            found.append((x, y, (r, g, b)))
if found:
    xs = [f[0] for f in found]; ys = [f[1] for f in found]
    print(f"  n={len(found)} bbox x={min(xs)}-{max(xs)} ({inch_h(min(xs))}-{inch_h(max(xs))}in) y={min(ys)}-{max(ys)} ({inch_v(min(ys))}-{inch_v(max(ys))}in)")
    print(f"  sample colors: {found[:5]} ... {found[len(found)//2]}")
else:
    print("  none found in that window")

# 4. cap heights: per-column max ink extent for first letters
def col_extent(x0, x1, y0, y1, cls):
    """rows in [y0,y1] where any pixel in [x0,x1] matches cls"""
    rows = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if cls == "red":
                ok = r > 120 and g < 90 and b < 90
            else:
                ok = b > 100 and b - r > 60 and b - g > 40
            if ok:
                rows.append(y); break
    return (min(rows), max(rows)) if rows else None

print("== cap heights ==")
e = col_extent(254, 275, 120, 200, "red")   # 'D' of Deep
print(f"  title1 'D' rows {e} -> cap {e[1]-e[0]+1}px = {(e[1]-e[0]+1)}pt (72ppi)")
e = col_extent(341, 362, 195, 255, "red")   # 'D' of DSAI
print(f"  title2 'D' rows {e} -> cap {e[1]-e[0]+1}px")
e = col_extent(460, 480, 290, 330, "red")   # 'P' of Prepared
print(f"  'Prepared' 'P' rows {e} -> cap {e[1]-e[0]+1}px")
e = col_extent(56, 70, 400, 435, "red")     # 'I' of Instructors
print(f"  'Instructors:' 'I' rows {e} -> cap {e[1]-e[0]+1}px")
e = col_extent(373, 390, 315, 355, "blue")  # 'D' of Dr. (credit)
print(f"  credit 'Dr.' 'D' rows {e} -> cap {e[1]-e[0]+1}px")
e = col_extent(96, 112, 430, 462, "blue")   # 'D' of Dr. (instructors)
print(f"  instr 'Dr.' 'D' rows {e} -> cap {e[1]-e[0]+1}px")

# 5. darkest color samples per text band
def darkest(x0, x1, y0, y1):
    best = None
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            s = r + g + b
            if best is None or s < best[0]:
                best = (s, (r, g, b), (x, y))
    return best

print("== darkest text colors ==")
print("  title:", darkest(254, 677, 135, 190))
print("  prepared:", darkest(460, 571, 301, 320))
print("  instructors:", darkest(56, 175, 411, 425))
print("  credit name:", darkest(373, 659, 325, 347))
print("  credit email:", darkest(405, 624, 352, 365))
print("  instr name1:", darkest(96, 358, 438, 455))
print("  instr email2:", darkest(96, 293, 507, 519))
print("  badge fill:", darkest(885, 900, 65, 80), "badge center:", px[893, 72])
print("  arabic text:", darkest(698, 898, 489, 495))
