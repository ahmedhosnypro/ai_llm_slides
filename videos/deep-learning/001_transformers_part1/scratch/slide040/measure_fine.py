#!/usr/bin/env python3
"""Fine measurements: cap heights, exact colors, border strokes for slide_040.jpg."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_040.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def ink_rows(mask, x0, x1, y0=0, y1=540):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return ys.min() + y0, ys.max() + y0, ys2 if False else (xs.min() + x0, xs.max() + x0)

red = (r > 130) & (g < 90) & (b < 90)
blue = (b > 110) & (r < 110) & (g < 110)

# Title 'M' cap height: columns 224..258
res = ink_rows(red, 224, 258)
print("title 'M' ink rows/cols:", res, "cap h =", res[1] - res[0] + 1 if res else None)
# 'd' ascender in Head: find columns of 'd' — measure full-word ink again precisely
res2 = ink_rows(red, 224, 707)
print("title full ink:", res2)

# Blue 'W' cap height: columns 166..200
resb = ink_rows(blue, 166, 200, 330, 380)
print("blue1 'W' ink:", resb, "cap h =", resb[1] - resb[0] + 1 if resb else None)
resb2 = ink_rows(blue, 166, 200, 410, 460)
print("blue2 'N' ink:", resb2, "cap h =", resb2[1] - resb2[0] + 1 if resb2 else None)

# lowercase 'i' dot vs x-height: measure 'i' in Wide (after W) — skip; use x-height of 'i','c','e'
# x-height measure: columns of 'ic' region in "Wide" ~ 200..230
resx = ink_rows(blue, 205, 235, 330, 380)
print("blue1 'de' ink (x-h):", resx, "x-h =", resx[1] - resx[0] + 1 if resx else None)

# Exact color samples ( darkest ink pixels )
def darkest(mask, x0, x1, y0, y1):
    sub = im[y0:y1, x0:x1]
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys):
        return None
    # average of the most saturated 30 pixels
    vals = sub[ys, xs]
    order = np.argsort(vals.sum(axis=1))
    sel = vals[order[:30]]
    return sel.mean(axis=0).round().astype(int)

print("title red avg (darkest 30):", darkest(red, 224, 707, 201, 237))
print("blue1 avg:", darkest(blue, 166, 468, 342, 368))
print("blue2 avg:", darkest(blue, 168, 505, 422, 448))

# Badge fill + ring + numeral colors
yel = (r > 200) & (g > 200) & (b < 190)
ys, xs = np.where(yel)
print("badge fill sample:", im[ys[len(ys)//2], xs[len(xs)//2]], "at", xs[len(xs)//2], ys[len(ys)//2])
ring_zone = im[53:90, 872:916]
rr, gg, bb = ring_zone[:, :, 0], ring_zone[:, :, 1], ring_zone[:, :, 2]
pur = (bb > 150) & (rr > 70) & (rr < 180) & (gg < 130)
pys, pxs = np.where(pur)
if len(pys):
    vals = ring_zone[pys, pxs]
    order = np.argsort(vals[:, 2] - vals[:, 0])
    print("ring avg (most purple 30):", vals[order[-30:]].mean(axis=0).round().astype(int), "count", len(pys))
dark = (r < 120) & (g < 120) & (b < 120)
subd = dark[57:87, 876:912]
dys, dxs = np.where(subd)
if len(dys):
    print("numeral ink h:", dys.max() - dys.min() + 1, "w:", dxs.max() - dxs.min() + 1)

# Border strokes: red-ish detection with wide threshold
reddish = (r - g > 40) & (r - b > 40) & (r > 120)
col_red = reddish.sum(axis=0)
row_red = reddish.sum(axis=1)
print("reddish cols >100 rows:", np.where(col_red > 100)[0])
print("reddish rows >300:", np.where(row_red > 300)[0])
print("reddish rows >50:", np.where(row_red > 50)[0])
# left border column values
for c in range(35, 46):
    print(f"col {c}: {im[300, c]}", end="  ")
print()
# top border rows
for rr_ in range(40, 52):
    print(f"row {rr_}: {im[rr_, 400]}", end="  ")
print()
# panel gray average in clean area
patch = im[280:320, 600:700]
print("panel gray avg:", patch.reshape(-1, 3).mean(axis=0).round(1))
# white margin avg
patch2 = im[5:40, 400:500]
print("white margin avg:", patch2.reshape(-1, 3).mean(axis=0).round(1))
