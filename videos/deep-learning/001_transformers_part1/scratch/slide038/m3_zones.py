#!/usr/bin/env python3
"""Inspect the small scattered diff clusters: max channel diff + a sample of
pixel values in 37 vs 38, to separate JPEG/cursor noise from real content."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
a = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
b = np.asarray(Image.open(f"{V}/unique_slides/slide_037.jpg").convert("RGB")).astype(int)
d = np.abs(a - b).sum(axis=2)
mask = d > 60

zones = [
    ("badge", 875, 925, 55, 95),
    ("x660-700 y80-120", 655, 705, 75, 125),
    ("x360-420 y160-220", 355, 425, 155, 225),
    ("x380-420 y240-330", 375, 425, 235, 335),
    ("x360-420 y330-360", 355, 425, 325, 365),
    ("x690-740 y355-405", 685, 745, 350, 410),
    ("x355-425 y395-425", 350, 430, 390, 430),
]
for name, x0, x1, y0, y1 in zones:
    sub = mask[y0:y1, x0:x1]
    n = int(sub.sum())
    print(f"== {name}: {n} px")
    if n:
        dd = d[y0:y1, x0:x1]
        print(f"   max diff {int(dd.max())}, p99 {int(np.percentile(dd[sub], 99)) if n>4 else int(dd[sub].max())}")
        ys, xs = np.where(sub)
        # a few sample points
        for i in range(0, len(ys), max(1, len(ys)//4))[:4] if False else list(np.linspace(0, len(ys)-1, 4, dtype=int)):
            yy, xx = ys[i]+y0, xs[i]+x0
            print(f"   sample ({xx},{yy}): 38={tuple(a[yy,xx])} 37={tuple(b[yy,xx])} diff={int(d[yy,xx])}")
