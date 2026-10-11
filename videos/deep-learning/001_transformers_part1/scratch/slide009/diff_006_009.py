#!/usr/bin/env python3
"""Diff slide_006.jpg vs slide_009.jpg: block-level map of changed regions.

Slide 9 = slide 6's composition + delta (REMOVE pink context-vector callout;
encoder/decoder moved/resized; ADD blue callout, gray summary, backprop panel,
blue curve). This pass finds WHERE the frames differ so each region can be
PIL-measured individually.
"""
from PIL import Image
import numpy as np

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"

a = np.asarray(Image.open(A).convert("RGB"), dtype=np.int16)
b = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
d = np.abs(a - b).sum(axis=2)  # per-pixel abs diff sum

mask = d > 60  # significant pixel change
print("changed px:", int(mask.sum()), "of", mask.size, f"({100*mask.sum()/mask.size:.2f}%)")

# Row profile: how many changed px per row (in 10px bands)
print("\nrow bands (y0: count) with >200 changed px:")
rows = mask.sum(axis=1)
for y0 in range(0, 540, 10):
    c = rows[y0:y0+10].sum()
    if c > 200:
        print(f"  y{y0:3d}..{y0+9:3d}: {c}")

# Column profile
print("\ncol bands (x0: count) with >200 changed px:")
cols = mask.sum(axis=0)
for x0 in range(0, 960, 10):
    c = cols[x0:x0+10].sum()
    if c > 200:
        print(f"  x{x0:3d}..{x0+9:3d}: {c}")

# Connected-region-ish coarse clustering: label via simple grid flood
from scipy import ndimage
lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
print("\ncoarse diff components (area>400):")
objs = ndimage.find_objects(lab)
comps = []
for i, sl in enumerate(objs):
    ys, xs = sl
    area = int((lab[sl] == i + 1).sum())
    if area > 400:
        comps.append((area, xs.start, ys.start, xs.stop, ys.stop))
comps.sort(reverse=True)
for area, x0, y0, x1, y1 in comps[:40]:
    print(f"  area={area:7d} bbox x{x0}..{x1} y{y0}..{y1}  (w{x1-x0} h{y1-y0})")
