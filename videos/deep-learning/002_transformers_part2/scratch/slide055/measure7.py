#!/usr/bin/env python3
"""Gap scans: K strip y-extents, right Y rows, W_v arrows, O flanking cells,
green arrow map, legend interior, Scaling/Softmax text strips."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
A = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]

# 1. K strips: pale-yellow rows at x=245..265, y 215..380
print("== K strip bands: per-row pale-yellow count x 232..272 ==")
sub = A[215:380, 232:272]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
pale = (r >= 248) & (g >= 245) & (b >= 195) & (b <= 230)
for yy in range(sub.shape[0]):
    cnt = int(pale[yy].sum())
    if cnt > 8:
        xs = np.where(pale[yy])[0]
        print(f"   y={215+yy}: n={cnt} x {232+xs.min()}..{232+xs.max()}")

# 2. right Y container rows: red + white comps inside [780..859, 218..380]
sub = A[218:380, 780:860]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 45) & (r - b >= 35) & (r >= 140)
whm = (r >= 240) & (g >= 240) & (b >= 220)
from scipy import ndimage
for nm, m in (("red", redm), ("white", whm)):
    lab, n = ndimage.label(m)
    print(f"== {nm} comps in right Y container ==")
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 10: continue
        bb = [780 + int(xs.min()), 218 + int(ys.min()), 780 + int(xs.max()), 218 + int(ys.max())]
        print(f"   f={bb} n={len(ys)}")

# 3. W_v arrows: red/dark comps x 755..785, y 220..375
sub = A[220:375, 755:785]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
dark = (r < 150) & (g < 150) & (b < 150)
redm = (r - g >= 40) & (r - b >= 30) & (r >= 140)
print("== dark/red per-row x 755..785 ==")
for yy in range(0, sub.shape[0], 3):
    nd, nr = int(dark[yy].sum()), int(redm[yy].sum())
    if nd + nr > 3:
        xs = np.where(dark[yy] | redm[yy])[0]
        print(f"   y={220+yy}: dark={nd} red={nr} x {755+xs.min()}..{755+xs.max()}")

# 4. O flanking cells: white/yellow comps x 545..580 and 640..680, y 118..155
for x0, x1, nm in ((545, 580, "left-of-O"), (640, 685, "right-of-O")):
    sub = A[118:155, x0:x1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    whm = (r >= 235) & (g >= 235) & (b >= 200)
    yel = (r >= 235) & (g >= 235) & (b <= 190)
    lab, n = ndimage.label(whm | yel)
    print(f"== {nm} cell comps ==")
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 15: continue
        bb = [x0 + int(xs.min()), 118 + int(ys.min()), x0 + int(xs.max()), 118 + int(ys.max())]
        print(f"   f={bb} n={len(ys)}")

# 5. green arrow pixel map x 550..680, y 135..195 (coarse)
sub = A[135:195, 550:680]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
grn = (g - r >= 30) & (g - b >= 30) & (g >= 110)
print("== green map (x 550..680 -> 26 cols of 5px, y 135..195 -> 12 rows of 5px) ==")
for yy in range(0, sub.shape[0], 5):
    row = ""
    for xx in range(0, sub.shape[1], 5):
        row += "#" if grn[yy:yy+5, xx:xx+5].sum() >= 4 else "."
    print(f"   y{135+yy:3d} {row}")

# 6. legend interior: comps of yellow/white/dark/blue inside [735..880, 432..500]
sub = A[432:500, 735:882]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
masks = {
    "yellow": (r >= 235) & (g >= 235) & (b <= 190),
    "white": (r >= 240) & (g >= 240) & (b >= 240),
    "dark": (r < 110) & (g < 110) & (b < 110),
    "blue": (b - r >= 60) & (b >= 130) & (r < 160),
    "red": (r - g >= 60) & (r - b >= 50) & (r >= 140),
}
for nm, m in masks.items():
    lab, n = ndimage.label(m)
    print(f"== legend {nm} comps ==")
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 8: continue
        bb = [735 + int(xs.min()), 432 + int(ys.min()), 735 + int(xs.max()), 432 + int(ys.max())]
        print(f"   f={bb} n={len(ys)}")

# 7. Scaling text strip: exact red rows at x 412..438; Softmax purple rows at x 488..514
sub = A[185:395, 412:439]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 140)
ys, xs = np.where(redm)
print(f"== Scaling red text rows {185+ys.min()}..{185+ys.max()}, x {412+xs.min()}..{412+xs.max()}, n={len(ys)}")
sub = A[185:395, 488:515]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
vio = (b - g >= 25) & (r - g >= 20) & (r >= 120) & (b >= 150)
ys, xs = np.where(vio)
if len(ys):
    print(f"== Softmax purple text rows {185+ys.min()}..{185+ys.max()}, x {488+xs.min()}..{488+xs.max()}, n={len(ys)}")
# per-row to see text vs separate glyph
rows = {}
for yy in set(185 + ys):
    rows[yy] = int(vio[yy - 185].sum())
bands = []
prev = None
for yy in sorted(rows):
    if prev is None or yy - prev > 3:
        bands.append([yy, yy])
    else:
        bands[-1][1] = yy
    prev = yy
print("   purple bands:", bands)
