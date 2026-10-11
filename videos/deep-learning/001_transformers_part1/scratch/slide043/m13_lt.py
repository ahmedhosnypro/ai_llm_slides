#!/usr/bin/env python3
"""LT box borders + title line1 left edge + blue/red runs in LT band."""
import numpy as np
from PIL import Image
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
lum = (r+g+b)/3
dark = lum < 110
# horizontal dark lines y 80..125, x 300..700: rows where many dark px
for y in range(80, 126):
    n = dark[y, 300:700].sum()
    if n > 60: print(f"dark row y={y}: n={n}, x {300+np.where(dark[y,300:700])[0].min()}..{300+np.where(dark[y,300:700])[0].max()}")
# vertical dark lines x 300..700 in y 85..120
for x in range(300, 700):
    n = dark[85:120, x].sum()
    if n > 12: print(f"dark col x={x}: n={n}, y {85+np.where(dark[85:120,x])[0].min()}..{85+np.where(dark[85:120,x])[0].max()}")
# line1 left edge excluding vecbox: x 480..900, y 52..76
band = lum[52:76, 480:900]
cols = np.where((band<100).any(axis=0))[0]
print("line1 ink (x>=480):", 480+cols.min(), "..", 480+cols.max())
