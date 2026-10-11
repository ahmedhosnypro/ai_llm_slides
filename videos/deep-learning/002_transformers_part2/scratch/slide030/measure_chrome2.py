#!/usr/bin/env python3
"""Looser border scan (thin JPEG-soft lines)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
# reddish: R noticeably above G,B
red = (R > 100) & (R - G > 50) & (R - B > 40)
col = red.sum(axis=0); row = red.sum(axis=1)
print("columns with red count>100:", [(x, int(col[x])) for x in range(W) if col[x] > 100])
print("rows with red count>100:", [(y, int(row[y])) for y in range(H) if row[y] > 100])
# print profiles near expected borders (slide032 said x 58..902, top 42-44, bottom 516-517)
print("\ncol profile 50..70:", [(x, int(col[x])) for x in range(50, 71)])
print("col profile 895..910:", [(x, int(col[x])) for x in range(895, 911)])
print("row profile 38..50:", [(y, int(row[y])) for y in range(38, 51)])
print("row profile 510..522:", [(y, int(row[y])) for y in range(510, 523)])
# sample actual colors on the strokes
for (x, y) in [(58, 300), (902, 300), (480, 43), (480, 516), (59, 100), (901, 100)]:
    print(f"px({x},{y}) = {tuple(im[y, x])}")
