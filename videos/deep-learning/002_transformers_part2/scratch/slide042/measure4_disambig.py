#!/usr/bin/env python3
# measure4_disambig.py — left-box divider, Channels/(4 Filters) extents, diagonal-arrow
# components, stack arrow, face color cores, block bbox (attempt 3)
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
R, G, B = img[..., 0], img[..., 1], img[..., 2]
reddish = (R - G > 25) & (R - B > 25) & (R > 100)
dark = img.sum(axis=-1) < 560

# 1. LEFT BOX: vertical extent of the x299/300 and x330/331 strokes; border x-extents
print("--- left box strokes")
for x in [299, 300, 330, 331, 76, 77]:
    ys = np.nonzero(reddish[185:245, x])[0]
    print(f"  x={x}: reddish rows {[185 + y for y in ys]}")
for y in [195, 196, 236, 237]:
    xs = np.nonzero(reddish[y, 70:345])[0]
    runs = []
    if len(xs):
        s = p = xs[0]
        for v in xs[1:]:
            if v - p > 2:
                runs.append((70 + s, 70 + p)); s = v
            p = v
        runs.append((70 + s, 70 + p))
    print(f"  y={y}: border x-runs {runs}")

# 2. Channels / (4 Filters) text-only columns (rows below shaft)
print("--- h-arrow label columns (y468..482 / y484..498)")
for y0, y1, tag in [(467, 483, "Channels"), (483, 500, "(4 Filters)")]:
    seg = img[y0:y1, 640:770]
    dk = seg.sum(axis=-1) < 560
    cols = np.nonzero(dk.any(axis=0))[0]
    runs, s, p = [], None, None
    for c in cols:
        if s is None:
            s = p = c; continue
        if c - p > 3:
            runs.append((640 + s, 640 + p)); s = c
        p = c
    if s is not None:
        runs.append((640 + s, 640 + p))
    print(f"  {tag}: runs {runs}")
# shaft y position: rows with long dark-red runs x660..780
print("--- h-arrow shaft rows")
for y in range(452, 472):
    n = int(reddish[y, 660:780].sum())
    if n > 20:
        print(f"  y={y} n={n}")

# 3. diagonal region connected components (dark ink x795..900 y375..485)
print("--- diagonal region components")
from scipy import ndimage
seg = dark[375:485, 795:900]
lab, n = ndimage.label(seg)
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 12:
        continue
    print(f"  comp n={len(xs)} x{795+xs.min()}..{795+xs.max()} y{375+ys.min()}..{375+ys.max()}")

# 4. stack arrow: white-ish pixels with colored neighbors in top staircase
print("--- stack arrow candidates (sum>690, neighbors colored), y265..315 x655..810")
cands = []
for y in range(265, 316):
    for x in range(655, 811):
        if img[y, x].sum() > 690:
            nb = [img[y + dy, x + dx] for dy in (-2, 0, 2) for dx in (-2, 0, 2)]
            colored = sum(1 for p in nb if p.sum() < 620)
            if colored >= 5:
                cands.append((x, y))
if cands:
    xs = [c[0] for c in cands]; ys = [c[1] for c in cands]
    print(f"  n={len(cands)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
    print("  sample:", cands[:12], "...", cands[-6:] if len(cands) > 12 else "")

# 5. face color cores per layer (bright front vs dark top) + green cube faces
def core(x0, y0, x1, y1, tag, bright=True):
    seg = img[y0:y1, x0:x1].reshape(-1, 3)
    s = seg.sum(axis=1)
    pick = seg[s >= np.percentile(s, 75)] if bright else seg[s <= np.percentile(s, 25)]
    m = pick.mean(axis=0).round(0)
    print(f"  {tag}: {'bright' if bright else 'dark'}-quartile ({m[0]:.0f},{m[1]:.0f},{m[2]:.0f})")

print("--- face colors")
core(390, 275, 430, 292, "midgrid front green")
core(390, 257, 430, 267, "midgrid top green", bright=False)
core(180, 285, 195, 300, "leftstack front")
core(203, 282, 209, 296, "leftstack right-face", bright=False)
core(700, 325, 770, 340, "magenta front")
core(700, 307, 770, 315, "magenta top", bright=False)
core(795, 310, 800, 320, "green L1 front")
core(810, 285, 825, 298, "orange front")
core(760, 260, 800, 266, "yellow top", bright=False)
core(830, 290, 840, 305, "yellow front")
core(841, 285, 850, 300, "bluegray right/front")

# 6. block global bbox (any strong color in x600..900 y230..480)
colored = ((np.abs(R - G) > 50) | (np.abs(G - B) > 50) | (np.abs(R - B) > 50)) & (img.sum(axis=-1) < 720)
ys, xs = np.nonzero(colored[230:480, 600:900])
print("block colored bbox:", 600 + xs.min(), 230 + ys.min(), 600 + xs.max(), 230 + ys.max(), "n", len(xs))
# top edge per x (first colored row) for staircase shape
prof = []
for x in range(655, 890, 15):
    col = np.nonzero(colored[230:480, x])[0]
    prof.append((x, 230 + col.min()) if len(col) else (x, -1))
print("block top profile:", prof)
