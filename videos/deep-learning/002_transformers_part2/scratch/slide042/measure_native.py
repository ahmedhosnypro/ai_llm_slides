#!/usr/bin/env python3
"""Native-element scans: pure red (arrows + labels, orange excluded), label box
borders (muted red rects), green/blue text bits inside label boxes, stacking sliver."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

S = 0.96055; AX = 18.66; SY = 0.95556
def mp(x, y): return ((x - AX) / S, y / SY)

def show(name, mask, min_px=6, region=None):
    lab, n = ndimage.label(mask)
    print(f"--- {name}")
    items = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px: continue
        items.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs)))
    for x0, y0, x1, y1, npx in sorted(items, key=lambda t: (t[1], t[0])):
        sx0, sy0 = mp(x0, y0); sx1, sy1 = mp(x1, y1)
        print(f"  f({x0},{y0})..({x1},{y1}) w{x1-x0+1} h{y1-y0+1} n{npx} -> s({sx0:.0f},{sy0:.0f})..({sx1:.0f},{sy1:.0f})")
    if not items: print("  (none)")

# PURE RED: exclude orange (orange has g 60..180); red text/border g<100
pure_red = (r > 130) & (r - g > 70) & (r - b > 70) & (g < 110)
m = np.zeros((H, W), bool); m[280:520, 570:910] = pure_red[280:520, 570:910]
show("PURE RED comps in right region (arrows + red text)", m, 4)

# label text under horizontal arrow region y460..510 x600..820: red text lines
m = np.zeros((H, W), bool); m[455:515, 600:830] = pure_red[455:515, 600:830]
rows = m.sum(axis=1)
print("--- red row profile y455..514 (x600..830):")
for y in range(455, 515):
    if rows[y] > 0:
        xs = np.nonzero(m[y])[0]
        print(f"  y{y}: n={int(rows[y])} x {xs.min()}..{xs.max()}")

# vertical arrow + rotated label: column profile
m = np.zeros((H, W), bool); m[300:480, 570:680] = pure_red[300:480, 570:680]
cols = m.sum(axis=0)
print("--- red col profile x570..679 (y300..480):")
for x in range(570, 680):
    if cols[x] > 3:
        ys = np.nonzero(m[:, x])[0]
        print(f"  x{x}: n={int(cols[x])} y {ys.min()}..{ys.max()}")

# LABEL BOX BORDERS: muted dark red (like chrome border (105,44,52)) — thin lines
mutred = (r > 70) & (r - g > 30) & (r - b > 30) & (g < 110)
print("--- label box horizontal borders: rows with mutred runs >120px, y150..300, x60..900")
for y in range(150, 301):
    xs = np.nonzero(mutred[y, 60:900])[0]
    if len(xs) < 120: continue
    runs = []
    st = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x > prev + 6:
            if prev - st > 60: runs.append((60 + st, 60 + prev))
            st = x
        prev = x
    if prev - st > 60: runs.append((60 + st, 60 + prev))
    if runs: print(f"  y{y}: {runs}")
print("--- label box vertical borders: cols with mutred runs >25px, y150..300")
for x in range(60, 900):
    ys = np.nonzero(mutred[150:300, x])[0]
    if len(ys) < 25: continue
    runs = []
    st = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y > prev + 6:
            if prev - st > 20: runs.append((150 + st, 150 + prev))
            st = y
        prev = y
    if prev - st > 20: runs.append((150 + st, 150 + prev))
    if runs: print(f"  x{x}: {runs}")

# GREEN text bits (One/FIVE) and BLUE text bits inside label boxes y150..300
grn = (g > 120) & (g - r > 50) & (g - b > 60)
m = np.zeros((H, W), bool); m[150:300, 60:900] = grn[150:300, 60:900]
show("GREEN text comps y150..300", m, 4)
blu = (b > 110) & (b - r > 50) & (b - g > 30)
m = np.zeros((H, W), bool); m[150:300, 60:900] = blu[150:300, 60:900]
show("BLUE text comps y150..300", m, 4)

# MAGENTA text bit ([mini-Batch]) in right box
mag = (r > 110) & (b > 110) & (g < 100)
m = np.zeros((H, W), bool); m[150:300, 60:900] = mag[150:300, 60:900]
show("MAGENTA text comps y150..300", m, 4)

# BLACK text (Using) in right box line 3
blk = (r < 90) & (g < 90) & (b < 90)
m = np.zeros((H, W), bool); m[195:230, 600:900] = blk[195:230, 600:900]
show("BLACK text comps right box area", m, 4)
