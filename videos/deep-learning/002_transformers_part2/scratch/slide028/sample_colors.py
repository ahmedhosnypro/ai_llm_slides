#!/usr/bin/env python3
"""Sample raw JPEG pixel values at known locations in frames 27/28 to calibrate masks."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"

for name in ("slide_027", "slide_028"):
    img = np.array(Image.open(f"{BASE}/unique_slides/{name}.jpg").convert("RGB")).astype(int)
    print("=====", name)
    print("row 300, cols 40..70 (left border zone):", [tuple(img[300, x]) for x in range(40, 70, 2)])
    print("row 300, cols 890..915 (right border zone):", [tuple(img[300, x]) for x in range(890, 915, 2)])
    print("col 480, rows 38..52 (top border zone):", [tuple(img[y, 480]) for y in range(38, 53, 1)])
    print("circle interior (581,297):", tuple(img[297, 581]), " (550,300):", tuple(img[300, 550]))
    print("chip Word0 interior (755,285):", tuple(img[285, 755]))
    print("chip Word6 interior f28 (400,285):", tuple(img[285, 400]))
    print("formula box interior (150,215):", tuple(img[215, 150]))
    # arrowhead: find darkest orange pixels in the whole frame
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    orange = (r > 180) & (g > 60) & (g < 160) & (b < 90)
    ys, xs = np.nonzero(orange)
    print("orange px count:", len(xs))
    if len(xs):
        print("orange sample colors:", [tuple(img[ys[i], xs[i]]) for i in range(0, min(len(xs), 8))])
    # red border column profile: count pixels per column with R-G>90 and R>120
    redish = (r > 120) & (r - g > 90) & (r - b > 90)
    cc = redish.sum(axis=0)
    rr = redish.sum(axis=1)
    print("redish col peaks (>300):", [(x, int(cc[x])) for x in np.nonzero(cc > 300)[0]][:12], "...",
          [(x, int(cc[x])) for x in np.nonzero(cc > 300)[0]][-12:])
    print("redish row peaks (>500):", [(y, int(rr[y])) for y in np.nonzero(rr > 500)[0]][:12], "...",
          [(y, int(rr[y])) for y in np.nonzero(rr > 500)[0]][-12:])
