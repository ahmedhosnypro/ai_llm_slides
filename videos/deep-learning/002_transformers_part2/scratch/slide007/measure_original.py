#!/usr/bin/env python3
"""Measure slide_007.jpg original frame (960x540): chrome landmarks -> frame->slide
mapping, title ink bboxes, color census. Slide coords: 960x540, 1px = 1pt."""
from PIL import Image
import collections

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_007.jpg"
im = Image.open(IM).convert("RGB")
W, H = im.size
px = im.load()
print(f"size {W}x{H}")

def is_red(p):    # C00000-family border/title ink (JPEG-muted: core ~ (184..193,13..16,29..35))
    r, g, b = p
    return r > 90 and (r - g) > 50 and (r - b) > 40

def is_yellow(p): # badge fill FDFD96
    r, g, b = p
    return r > 215 and g > 215 and 110 < b < 210

# --- 1. vertical border columns: count red in y 330..500 (below title, above bottom border)
colcount = {}
for x in range(W):
    c = sum(1 for y in range(330, 500) if is_red(px[x, y]))
    if c > 100:
        colcount[x] = c
cols = sorted(colcount)
print("red cols(y330-500):", cols)
left = cols[0]; right = cols[-1]

# --- 2. horizontal border rows: count red in x 100..180 (left of title, clear of badge)
rowcount = {}
for y in range(H):
    c = sum(1 for x in range(100, 180) if is_red(px[x, y]))
    if c > 50:
        rowcount[y] = c
rows = sorted(rowcount)
print("red rows(x100-180):", rows)
top = rows[0]; bottom = rows[-1]

# --- 3. mapping fit: frame landmarks <-> slide chrome (42, 919, 45, 540)
sx = (right - left) / (919 - 42)
ox = left - 42 * sx
sy = (bottom - top) / (540 - 45)
oy = top - 45 * sy
print(f"mapping: frame_x = {ox:.3f} + {sx:.5f}*slide_x ; frame_y = {oy:.3f} + {sy:.5f}*slide_y")
def to_slide(fx, fy):
    return ((fx - ox) / sx, (fy - oy) / sy)

# --- 4. badge yellow bbox
ys = [ (x, y) for y in range(H) for x in range(W) if is_yellow(px[x, y]) ]
xs_b = [p[0] for p in ys]; ys_b = [p[1] for p in ys]
bx0, bx1, by0, by1 = min(xs_b), max(xs_b), min(ys_b), max(ys_b)
bcx, bcy = (bx0 + bx1) / 2, (by0 + by1) / 2
print(f"badge yellow bbox frame ({bx0},{by0})..({bx1},{by1}) center ({bcx:.1f},{bcy:.1f})")
print(f"badge center -> slide ({bcx:.1f} -> {to_slide(bcx, bcy)[0]:.1f}, {bcy:.1f} -> {to_slide(bcx, bcy)[1]:.1f})  [house badge (893,71)]")

# --- 5. title ink: red pixels in x 120..860, y (top+8)..(bottom-8), excluding border cols
x0t, x1t = left + 8, right - 8
y0t, y1t = top + 8, bottom - 8
ink = []
for y in range(y0t, y1t):
    for x in range(x0t, x1t):
        if is_red(px[x, y]):
            ink.append((x, y))
# cluster into lines by y histogram
yhist = collections.Counter(p[1] for p in ink)
ys_ink = sorted(yhist)
# find gap(s) > 5 rows
lines = []
cur = [ys_ink[0]]
for y in ys_ink[1:]:
    if y - cur[-1] > 5:
        lines.append(cur); cur = [y]
    else:
        cur.append(y)
lines.append(cur)
print(f"title ink rows: {len(lines)} line cluster(s)")
for i, ly in enumerate(lines):
    lset = set(ly)
    lpts = [p for p in ink if p[1] in lset]
    lx = [p[0] for p in lpts]
    x_min, x_max = min(lx), max(lx)
    y_min, y_max = min(ly), max(ly)
    scx0, scy0 = to_slide(x_min, y_min)
    scx1, scy1 = to_slide(x_max, y_max)
    print(f"  line{i+1}: frame ink x {x_min}..{x_max} (w {x_max-x_min+1}) y {y_min}..{y_max} (h {y_max-y_min+1})"
          f" -> slide x {scx0:.1f}..{scx1:.1f} (w {scx1-scx0:.1f}) y {scy0:.1f}..{scy1:.1f} (h {scy1-scy0:.1f})"
          f" cx {(scx0+scx1)/2:.1f} cy {(scy0+scy1)/2:.1f}")

# --- 6. color census
def census(name, pts):
    c = collections.Counter(px[x, y] for x, y in pts)
    print(f"  {name}: top {c.most_common(4)}")
title_pts = ink
print("census:")
census("title red core", title_pts)
census("badge fill", [(x, y) for x in range(bx0+6, bx1-6) for y in range(by0+6, by1-6) if is_yellow(px[x,y])])
# ring: purple pixels near badge bbox edge
ring = [(x, y) for y in range(max(0,by0-4), by1+5) for x in range(max(0,bx0-4), bx1+5)
        if (lambda p: p[2] > 140 and p[0] < 160 and p[1] < 130 and p[2] > p[0] > p[1])(px[x, y])]
census("badge ring", ring) if ring else print("  badge ring: none found")
print(f"  canvas @(20,20): {px[20,20]}  @(940,300): {px[940,300]}")
print(f"  panel @(480,430): {px[480,430]}  @(200,120): {px[200,120]}")
print(f"  letterbox @(480,530): {px[480,530]}  @(480,525): {px[480,525]}")
# cursor artifact check region (~35% x, 58% y of frame)
cur_reg = [(x, y) for y in range(280, 340) for x in range(300, 380)
           if (lambda p: sum(p) < 180)(px[x, y])]
print(f"  cursor dark pixels in (300..380,280..340): {len(cur_reg)}", cur_reg[:5])
