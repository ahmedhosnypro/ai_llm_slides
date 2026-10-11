#!/usr/bin/env python3
"""Cluster the strong-diff pixels to see the delta zones in detail."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
a = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
b = np.asarray(Image.open(f"{V}/unique_slides/slide_037.jpg").convert("RGB")).astype(int)
d = np.abs(a - b).sum(axis=2)
mask = d > 60

# coarse 20px-grid cluster report
H, W = mask.shape
cell = 20
print("grid counts (col=x20px, row=y20px), only cells with >5 px:")
for gy in range(0, H, cell):
    for gx in range(0, W, cell):
        c = int(mask[gy:gy+cell, gx:gx+cell].sum())
        if c > 5:
            print(f"  x{gx:3d}-{gx+cell:3d} y{gy:3d}-{gy+cell:3d}: {c}")
