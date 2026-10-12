#!/usr/bin/env python3
"""m8.py — complete top-zone inventory: every ink cluster that is neither white canvas
nor peach panel fill, y[46,245] x[40,960]."""
from PIL import Image
import numpy as np
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 238) & (G > 238) & (B > 238)
peach = (np.abs(R - 240) < 14) & (np.abs(G - 224) < 14) & (np.abs(B - 200) < 16)
ink = ~(white | peach)
# restrict to top zone
zone = np.zeros_like(ink)
zone[46:246, 40:960] = ink[46:246, 40:960]
lab, n = ndimage.label(zone, structure=np.ones((3, 3)))
cl = []
for sl in ndimage.find_objects(lab):
    cnt = zone[sl].sum()
    if cnt >= 25:
        x0, y0, x1, y1 = sl[1].start, sl[0].start, sl[1].stop - 1, sl[0].stop - 1
        # mean color of the cluster
        m = a[y0:y1+1, x0:x1+1][zone[y0:y1+1, x0:x1+1]]
        cl.append((x0, y0, x1, y1, int(cnt), tuple(m.mean(axis=0).astype(int))))
cl.sort(key=lambda t: (t[1], t[0]))
print("top-zone ink clusters (x0,y0,x1,y1,count,meanRGB):")
for c in cl:
    print("   ", c)
