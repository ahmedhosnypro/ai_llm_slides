#!/usr/bin/env python3
"""Second-pass structural probes for slide_049.jpg: chip cells, bar colors (mode),
red arrow color/shape, word row, gray arrows, embedding bars, left column boxes."""
import numpy as np
from PIL import Image
from scipy import ndimage
from collections import Counter

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def mode_color(region):
    px = region.reshape(-1, 3)
    cnt = Counter(map(tuple, px))
    return cnt.most_common(3)

def colclass(c):
    r, g, b = c
    if r > 235 and g > 235 and b > 235: return "white"
    if r > 180 and g < 110 and b < 110: return "RED"
    if b > 110 and b - r > 45 and b - g > 40: return "BLUE"
    if g > 120 and g - r > 30 and g - b > 30: return "GREEN"
    if r > 200 and g > 170 and b < 190 and r - b > 40 and g - b > 30: return "TAN/YEL"
    if b > 190 and g > 190 and r < 215 and b - r > 15: return "CYAN"
    if r > 190 and b > 150 and g < 195 and r - g > 20: return "PINK"
    if abs(r-g) < 16 and abs(g-b) < 16 and 100 < r < 215: return "GRAY"
    if r < 100 and g < 100 and b < 100: return "BLACK"
    return f"other{c}"

# ---- 1. X chip cell structure: per-column class over chip 0 (x 168..246, y 374..402)
print("== X chip0 per-column classes (y378..398 mode) ==")
for x in range(166, 248, 2):
    col = a[378:398, x]
    cc = mode_color(col)[0][0]
    print(f"  x={x} {colclass(cc)} {cc}")

# ---- 2. Y chip0 (x 168..246, y 84..110)
print("== Y chip0 per-column classes (y88..106 mode) ==")
for x in range(166, 248, 2):
    col = a[88:106, x]
    cc = mode_color(col)[0][0]
    print(f"  x={x} {colclass(cc)} {cc}")

# ---- 3. Embedding bars: per-row dominant class x 300..700, y 405..470
print("== rows y405..472 dominant class (x 620..740, avoiding center text) ==")
for y in range(405, 473):
    row = a[y, 620:740]
    cc = mode_color(row)[0][0]
    print(f"  y={y} {colclass(cc)} {cc}")

# ---- 4. red arrow probe: gap 2-1 (y 266..285, x 195..235) full pixel dump classes
print("== gap Block2->Block1 y267..283, x195..235 ==")
for y in range(266, 285):
    row = a[y, 195:235:3]
    s = "".join({"w": ".", "R": "R", "B": "B", "G": "G", "g": "-"}.get(colclass(tuple(p))[0] if colclass(tuple(p)) not in ("BLACK",) else "K", "?") for p in row)
    print(f"  y={y} {s}")
print("sample colors:", mode_color(a[268:282, 196:232]))

# ---- 5. word row: box borders around word1 (x 205..280, y 470..515)
print("== word row structure x160..900 y470..515 red-border comps ==")
red = (a[:, :, 0] > 150) & (a[:, :, 1] < 120) & (a[:, :, 2] < 120)
lab, n = ndimage.label(red[470:518, :])
boxes = []
for sl in ndimage.find_objects(lab):
    y0, y1, x0, x1 = sl[0].start+470, sl[0].stop-1+470, sl[1].start, sl[1].stop-1
    if (x1-x0) > 40 and (y1-y0) > 15:
        boxes.append((x0, x1, y0, y1))
print("  big red comps (boxes):", boxes)
print("  word1 interior mode:", mode_color(a[487:500, 215:270]))
print("  word label ink mode:", mode_color(a[483:492, 215:268]))

# ---- 6. gray arrows shape: x 200..290, y 455..472
print("== gray arrows probe x196..286 y455..474 ==")
gray = (abs(a[:, :, 0]-a[:, :, 1]) < 18) & (abs(a[:, :, 1]-a[:, :, 2]) < 18) & (a[:, :, 0] < 215) & (a[:, :, 0] > 90)
for y in range(455, 475):
    row = gray[y, 196:286]
    xs = np.where(row)[0]
    print(f"  y={y} n={len(xs)} x={ (xs.min()+196, xs.max()+196) if len(xs) else None }")
print("  gray mode:", mode_color(a[466:470, 215:270]))

# ---- 7. blue arrows: x 195..215, y 396..420
print("== blue arrows probe x196..216 y396..421 ==")
blue = (a[:, :, 2] - a[:, :, 0] > 45) & (a[:, :, 2] - a[:, :, 1] > 35) & (a[:, :, 2] > 110)
for y in range(396, 421):
    row = blue[y, 190:225]
    xs = np.where(row)[0]
    print(f"  y={y} n={len(xs)} x={(xs.min()+190, xs.max()+190) if len(xs) else None}")
print("  blue arrow mode:", mode_color(a[405:414, 200:212]))

# ---- 8. green arrows: x 195..215, y 100..128
print("== green arrows probe ==")
green = (a[:, :, 1] - a[:, :, 0] > 30) & (a[:, :, 1] - a[:, :, 2] > 30)
for y in range(100, 128):
    row = green[y, 190:225]
    xs = np.where(row)[0]
    print(f"  y={y} n={len(xs)} x={(xs.min()+190, xs.max()+190) if len(xs) else None}")
print("  green mode:", mode_color(a[110:120, 200:210]))

# ---- 9. bars: mode colors of bar interiors + container
print("== bar/container modes ==")
print("  barM:", mode_color(a[135:157, 200:800]))
print("  bar0:", mode_color(a[333:355, 200:800]))
print("  container fill:", mode_color(a[200:230, 700:860]))
print("  container border top:", mode_color(a[125:130, 400:800]))
print("  dots:", mode_color(a[191:197, 200:209]))

# ---- 10. left column boxes: red border rows/cols in x55..165
print("== left column red structure ==")
lcred = red[:, 55:165]
for y in range(60, 520):
    xs = np.where(lcred[y])[0]
    if len(xs) > 25:
        print(f"  long red row y={y} x {xs.min()+55}..{xs.max()+55}")
for x in range(0, 110):
    ys = np.where(lcred[:, x])[0]
    if len(ys) > 25:
        print(f"  long red col x={x+55} y {ys.min()}..{ys.max()}")

# ---- 11. X/Y row full extents: red border comps full width
print("== X row red comps (full width, y370..404) ==")
lab, n = ndimage.label(red[370:404, :])
for sl in ndimage.find_objects(lab):
    y0, y1, x0, x1 = sl[0].start+370, sl[0].stop-1+370, sl[1].start, sl[1].stop-1
    npx = int(red[sl[0], sl[1]].sum())
    if npx >= 8:
        print(f"   x{x0}..{x1} y{y0}..{y1} npx={npx}")
print("== Y row red comps (full width, y76..114) ==")
lab, n = ndimage.label(red[76:114, :])
for sl in ndimage.find_objects(lab):
    y0, y1, x0, x1 = sl[0].start+76, sl[0].stop-1+76, sl[1].start, sl[1].stop-1
    npx = int(red[sl[0], sl[1]].sum())
    if npx >= 8:
        print(f"   x{x0}..{x1} y{y0}..{y1} npx={npx}")
