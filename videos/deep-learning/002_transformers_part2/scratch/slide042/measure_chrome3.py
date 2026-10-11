#!/usr/bin/env python3
"""Precise chrome landmark extraction: border strokes have red frac ~1.0 over the
panel height/width; print profiles to separate borders from title glyph rows."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 130) & (r - g > 60) & (r - b > 60)

# full-panel-height vertical borders: frac over y 130..500 (below title, above letterbox)
band = red[130:500, :]
colfrac = band.mean(axis=0)
print("cols with colfrac>0.9 (y130..500):", [(x, round(colfrac[x], 3)) for x in range(W) if colfrac[x] > 0.9])
print("cols 55..65:", [(x, round(colfrac[x], 2)) for x in range(55, 66)])
print("cols 895..910:", [(x, round(colfrac[x], 2)) for x in range(895, 911)])

# full-width horizontal borders: frac over x 250..750 (avoid arrows at edges)
mid = red[:, 250:750]
rowfrac = mid.mean(axis=1)
print("rows with rowfrac>0.9:", [(y, round(rowfrac[y], 3)) for y in range(H) if rowfrac[y] > 0.9])
print("rows 40..50:", [(y, round(rowfrac[y], 2)) for y in range(40, 51)])
print("rows 512..520:", [(y, round(rowfrac[y], 2)) for y in range(512, 521)])

# title rows profile y 50..130 (x 150..820, red frac)
t = red[50:130, 150:820]
tf = t.mean(axis=1)
print("title region rowfrac y50..129:", [(50 + i, round(v, 3)) for i, v in enumerate(tf) if v > 0.02])
