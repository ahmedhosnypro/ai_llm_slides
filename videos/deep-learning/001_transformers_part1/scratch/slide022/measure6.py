#!/usr/bin/env python3
"""measure6: sample pixels in the clusters; full left+right panel maps"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

# sample cluster interiors
print("cluster y167 x216..250:", [tuple(a[167, x]) for x in range(218, 248, 6)])
print("cluster y215 x183..210:", [tuple(a[215, x]) for x in range(184, 210, 5)])
print("cluster y380 x183..210:", [tuple(a[380, x]) for x in range(184, 210, 5)])
print("row y215 x175..255:", [tuple(a[215, x]) for x in range(175, 255, 8)])
print("row y167 x210..258:", [tuple(a[167, x]) for x in range(210, 258, 6)])
# what is between clusters (white?) and where do squares start/end per row
white = (a[:, :, 0] > 235) & (a[:, :, 1] > 235) & (a[:, :, 2] > 235)
for name, (x0, x1) in [("L-INPUT", (160, 258)), ("L-PROJ", (268, 362)), ("L-OUT", (375, 470)),
                        ("R-INPUT", (501, 570)), ("R-PROJ", (581, 657)), ("R-OUT", (668, 765))]:
    colw = white[:, x0:x1].sum(axis=1)
    runs = []
    inr = False
    for y in range(140, 470):
        v = colw[y] > (x1 - x0) * 0.55
        if v and not inr: s = y; inr = True
        elif not v and inr: runs.append((s, y - 1)); inr = False
    if inr: runs.append((s, 469))
    print(f"{name} white>55% rows: {runs}")
