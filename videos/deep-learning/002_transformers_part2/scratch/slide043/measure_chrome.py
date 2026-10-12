#!/usr/bin/env python3
"""Slide 043 chrome landmarks: border strokes have red frac ~1.0 over the panel
height/width (loose red mask — chroma-destroyed thin borders, per slide042 lesson)."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 130) & (r - g > 30) & (r - b > 30)  # LOOSE mask for borders (4:2:0 chroma)

# vertical borders: frac over y 140..380 (below title, above bottom box)
band = red[140:380, :]
colfrac = band.mean(axis=0)
print("cols colfrac>0.85 (y140..380):", [(x, round(colfrac[x], 3)) for x in range(W) if colfrac[x] > 0.85])
print("cols 45..70:", [(x, round(colfrac[x], 2)) for x in range(45, 71)])
print("cols 890..915:", [(x, round(colfrac[x], 2)) for x in range(890, 916)])

# horizontal borders: frac over x 250..750 (middle; avoid arrows/diagram edges)
mid = red[:, 250:750]
rowfrac = mid.mean(axis=1)
print("rows rowfrac>0.85:", [(y, round(rowfrac[y], 3)) for y in range(H) if rowfrac[y] > 0.85])
print("rows 38..55:", [(y, round(rowfrac[y], 2)) for y in range(38, 56)])
print("rows 505..525:", [(y, round(rowfrac[y], 2)) for y in range(505, 526)])

# badge: yellow circle bbox (top-right)
yel = (r > 200) & (g > 200) & (b < 180)
ys, xs = np.where(yel[40:120, 820:940])
if len(xs):
    print("yellow bbox x", xs.min() + 820, "..", xs.max() + 820, " y", ys.min() + 40, "..", ys.max() + 40,
          " center", (xs.min() + xs.max()) / 2 + 820, (ys.min() + ys.max()) / 2 + 40)

# title rows profile y 45..130 (x 150..820, strict red-text mask)
tred = (r > 150) & (r - g > 60) & (r - b > 60)
t = tred[45:130, 150:820]
tf = t.mean(axis=1)
print("title rows>0.02:", [(45 + i, round(v, 3)) for i, v in enumerate(tf) if v > 0.02])
cols = t.mean(axis=0)
nz = [150 + i for i, v in enumerate(cols) if v > 0.02]
print("title ink x-extent:", (nz[0], nz[-1]) if nz else None)
