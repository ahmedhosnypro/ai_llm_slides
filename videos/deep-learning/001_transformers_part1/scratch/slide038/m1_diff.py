#!/usr/bin/env python3
"""Measure slide_038.jpg delta vs slide_037.jpg: locate the inset panel and
confirm the delta is confined to it (pure addition check)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
a = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
b = np.asarray(Image.open(f"{V}/unique_slides/slide_037.jpg").convert("RGB")).astype(int)
print("shapes:", a.shape, b.shape)
d = np.abs(a - b).sum(axis=2)
mask = d > 60  # strong-diff pixels
ys, xs = np.where(mask)
print("strong-diff pixel count:", len(xs))
if len(xs):
    print("diff bbox: x[%d..%d] y[%d..%d]" % (xs.min(), xs.max(), ys.min(), ys.max()))
# column/row histograms of the diff to see the zones
colsum = mask.sum(axis=0)
rowsum = mask.sum(axis=1)
cols = np.where(colsum > 3)[0]
rows = np.where(rowsum > 3)[0]
print("diff columns range:", (cols.min(), cols.max()) if len(cols) else None)
print("diff rows range:", (rows.min(), rows.max()) if len(rows) else None)
# is there diff outside x>780?
outside = mask[:, :780]
print("diff pixels with x<780:", int(outside.sum()))
if outside.sum():
    ys2, xs2 = np.where(outside)
    print("  bbox: x[%d..%d] y[%d..%d]" % (xs2.min(), xs2.max(), ys2.min(), ys2.max()))
