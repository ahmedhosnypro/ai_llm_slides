#!/usr/bin/env python3
"""m9.py — panel1 zone ink inventory (y[246,500] x[110,690]) excluding fills;
plus per-row content strips between x188-268 (K-row zone)."""
from PIL import Image
import numpy as np
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 243) & (G > 243) & (B > 243)
grayp = (np.abs(R - 233) < 7) & (np.abs(G - 233) < 7) & (np.abs(B - 231) < 8)
peach = (np.abs(R - 240) < 14) & (np.abs(G - 224) < 14) & (np.abs(B - 200) < 16)
dotf = (np.abs(R - 216) < 10) & (np.abs(G - 200) < 10) & (np.abs(B - 184) < 10)
mint = (np.abs(R - 232) < 12) & (np.abs(G - 248) < 8) & (np.abs(B - 232) < 14) & (G - R > 6)
cyan = (np.abs(R - 232) < 14) & (np.abs(G - 248) < 10) & (np.abs(B - 248) < 10) & (B - R > 8)
ink = ~(white | grayp | peach | dotf | mint | cyan)
zone = np.zeros_like(ink)
zone[246:500, 110:690] = ink[246:500, 110:690]
lab, n = ndimage.label(zone)
cl = []
for sl in ndimage.find_objects(lab):
    cnt = zone[sl].sum()
    if cnt >= 35:
        x0, y0, x1, y1 = sl[1].start, sl[0].start, sl[1].stop - 1, sl[0].stop - 1
        m = a[y0:y1+1, x0:x1+1][zone[y0:y1+1, x0:x1+1]]
        cl.append((x0, y0, x1, y1, int(cnt), tuple(m.mean(axis=0).astype(int))))
cl.sort(key=lambda t: (t[1], t[0]))
print("panel1 ink clusters (x0,y0,x1,y1,count,meanRGB):")
for c in cl:
    print("   ", c)
