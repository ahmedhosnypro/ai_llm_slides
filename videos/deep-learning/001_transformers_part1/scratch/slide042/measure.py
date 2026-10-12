#!/usr/bin/env python3
"""PIL-measure slide_042.jpg (960x540, 1px=1pt) — title, subtitle, box, bullet lines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_042.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if not len(ys):
        print(label, "EMPTY")
        return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  (w {xs.max()-xs.min()+1}, h {ys.max()-ys.min()+1}) n={len(ys)}")
    return (xs.min(), xs.max(), ys.min(), ys.max())

# red-ish ink (title/subtitle) — broad
red = (r > 130) & (g < 100) & (b < 100)
# dark-red border (~990000) — darker
darkred = (r > 90) & (r < 190) & (g < 60) & (b < 60)
# blue body text
blue = (b > 120) & (r < 120) & (g < 120)
# green subscripts
green = (g > 110) & (r < 110) & (b < 110)

print("== red ink rows (row histogram, count>3) ==")
rows = np.where(red.sum(axis=1) > 3)[0]
bands = []
if len(rows):
    s = p = rows[0]
    for i in rows[1:]:
        if i == p + 1: p = i
        else: bands.append((s, p)); s = p = i
    bands.append((s, p))
for s, e in bands:
    m = red[s:e+1]
    xs = np.where(m.sum(axis=0) > 0)[0]
    print(f"  band y {s}..{e}: x {xs.min()}..{xs.max()} n={m.sum()}")

print("== blue ink bands (count>3) ==")
rows = np.where(blue.sum(axis=1) > 3)[0]
bands = []
if len(rows):
    s = p = rows[0]
    for i in rows[1:]:
        if i == p + 1: p = i
        else: bands.append((s, p)); s = p = i
    bands.append((s, p))
for s, e in bands:
    m = blue[s:e+1]
    xs = np.where(m.sum(axis=0) > 0)[0]
    print(f"  band y {s}..{e}: x {xs.min()}..{xs.max()} n={m.sum()}")

print("== green ink ==")
bbox(green, "green(all)")
print("== darkred (box border) ==")
bbox(darkred, "darkred(all)")

# box border: scan for long horizontal darkred runs
print("== darkred long horiz runs ==")
for y in range(H):
    xs = np.where(darkred[y])[0]
    if len(xs) > 300:
        print(f"  row {y}: x {xs.min()}..{xs.max()} n={len(xs)}")
print("== darkred long vert runs ==")
for x in range(W):
    ys = np.where(darkred[:, x])[0]
    if len(ys) > 100:
        print(f"  col {x}: y {ys.min()}..{ys.max()} n={len(ys)}")

# sample colors
print("== color samples ==")
for (x, y, lbl) in [(480, 60, "title ink?"), (300, 150, "subtitle?"), (100, 230, "body line1?"),
                    (80, 250, "box interior"), (30, 270, "panel left of box"), (20, 270, "canvas margin"),
                    (893, 71, "badge"), (893, 55, "badge ring top?")]:
    print(f"  ({x},{y}) {lbl}: {tuple(im[y, x])}")
