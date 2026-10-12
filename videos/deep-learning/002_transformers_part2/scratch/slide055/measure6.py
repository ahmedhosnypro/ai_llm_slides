#!/usr/bin/env python3
"""Last scan batch: mesh, fan, W_v, Y-rows, K zone, Z row, hatch borders."""
from PIL import Image
import numpy as np
from scipy import ndimage

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
A = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]

# 1. mesh: red pixel map inside DotProduct box [289..377, 210..385] as coarse ascii
sub = A[210:385, 289:377]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 45) & (r - b >= 35) & (r >= 150)
navy = (b - r >= 30) & (b >= 90) & (r < 120)
print("== DotProduct box ascii map (x 289..377 -> 44 cols of 2px, y 210..385 -> 35 rows of 5px) ==")
for yy in range(0, sub.shape[0], 5):
    row = ""
    for xx in range(0, sub.shape[1], 2):
        cell_r = redm[yy:yy+5, xx:xx+2].sum()
        cell_n = navy[yy:yy+5, xx:xx+2].sum()
        row += "O" if cell_n >= 6 else ("#" if cell_r >= 3 else ".")
    print(f"   y{210+yy:3d} {row}")

# 2. softmax fan: scan x 512..590, y 250..380
sub = A[250:380, 512:590]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 40) & (r - b >= 30) & (r >= 150)
print("== fan zone x 512..590 y 250..380 rows with red ==")
for yy in range(0, sub.shape[0], 4):
    xs = np.where(redm[yy])[0]
    if len(xs) > 2:
        print(f"   y={250+yy}: n={len(xs)} x {512+xs.min()}..{512+xs.max()}")

# 3. W_v boxes: light-blue census x 690..770, y 215..375
sub = A[215:375, 690:770]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
lb = (b - r >= 18) & (b - g >= 10) & (b >= 180) & (r >= 120)
lab, n = ndimage.label(lb)
print("== light-blue comps (W_v zone) ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 80: continue
    bb = [690 + int(xs.min()), 215 + int(ys.min()), 690 + int(xs.max()), 215 + int(ys.max())]
    print(f"   f={bb} {bb[2]-bb[0]+1}x{bb[3]-bb[1]+1} n={len(ys)}")
# fill samples
for (x, y) in [(712, 238), (730, 238), (750, 240), (712, 358), (735, 360), (755, 352), (745, 300)]:
    rr, gg, bb2 = A[y, x]
    print(f"   wv sample ({x},{y}): #{rr:02X}{gg:02X}{bb2:02X}")

# 4. Y container interior: red comps inside left container [101..180, 218..379]
sub = A[218:380, 101:181]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 45) & (r - b >= 35) & (r >= 140)
lab, n = ndimage.label(redm)
print("== red comps in left Y container ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 12: continue
    bb = [101 + int(xs.min()), 218 + int(ys.min()), 101 + int(xs.max()), 218 + int(ys.max())]
    print(f"   f={bb} n={len(ys)}")
# white cells inside container?
whm = (r >= 240) & (g >= 240) & (b >= 220)
lab, n = ndimage.label(whm)
print("== white-ish comps in left Y container ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 30: continue
    bb = [101 + int(xs.min()), 218 + int(ys.min()), 101 + int(xs.max()), 218 + int(ys.max())]
    print(f"   f={bb} n={len(ys)}")

# 5. K zone fill grid: x 232..272
print("== K zone grid samples ==")
for y in (230, 245, 260, 275, 300, 320, 350, 365):
    row = []
    for x in (235, 245, 255, 265):
        rr, gg, bb2 = A[y, x]
        row.append(f"({x},{y})#{rr:02X}{gg:02X}{bb2:02X}")
    print("   " + " ".join(row))

# 6. Z row: grid + border color
print("== Z row grid ==")
for y in (462, 470, 480, 490):
    row = []
    for x in (222, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 512):
        rr, gg, bb2 = A[y, x]
        row.append(f"{x}:#{rr:02X}{gg:02X}{bb2:02X}")
    print(f"   y={y}: " + " ".join(row))

# 7. hatch box: border scan — red per row x 95..195 (left box), y 170..220
print("== left hatch box red per-row (x 95..195) ==")
sub = A[170:220, 95:195]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 40) & (r - b >= 30) & (r >= 140)
for yy in range(0, sub.shape[0], 2):
    xs = np.where(redm[yy])[0]
    if len(xs) > 2:
        print(f"   y={170+yy}: n={len(xs)} x {95+xs.min()}..{95+xs.max()}")
# and per-col in text-free band y 176..182
sub2 = A[174:182, 90:200]
r, g, b = sub2[..., 0], sub2[..., 1], sub2[..., 2]
redm2 = (r - g >= 40) & (r - b >= 30) & (r >= 140)
colhits = [(90 + xx, int(redm2[:, xx].sum())) for xx in range(sub2.shape[1]) if redm2[:, xx].sum() >= 1]
print("   per-col red y174..182:", colhits[:40])

# 8. fraction zone fill: what's behind fraction (447..477, 185..217)?
for (x, y) in [(460, 190), (462, 200), (460, 212), (450, 195), (470, 210)]:
    rr, gg, bb2 = A[y, x]
    print(f"   frac zone ({x},{y}): #{rr:02X}{gg:02X}{bb2:02X}")

# 9. Scaling/Softmax column top/bottom exact + text strip extents
for x in (425, 501):
    col = A[185:392, x]
    r_, g_, b_ = col[..., 0], col[..., 1], col[..., 2]
    pinkish = (r_ - g_ >= 15) & (r_ >= 235)
    violet = (b_ - g_ >= 12) & (b_ >= 235) & (r_ >= 235)
    m = pinkish if x == 425 else violet
    ys = np.where(m)[0]
    if len(ys):
        print(f"   col x={x}: fill rows {185+ys.min()}..{185+ys.max()}")

# 10. O box interior: grid x 575..645, y 118..152
print("== O box grid ==")
for y in (122, 130, 138, 146):
    row = []
    for x in (580, 595, 610, 625, 638):
        rr, gg, bb2 = A[y, x]
        row.append(f"{x}:#{rr:02X}{gg:02X}{bb2:02X}")
    print(f"   y={y}: " + " ".join(row))
