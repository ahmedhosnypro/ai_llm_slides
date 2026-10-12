#!/usr/bin/env python3
"""Chrome landmark measurement v2 — looser red mask."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

red = (r - g > 45) & (r - b > 45) & (r > 120)

colprof = red[220:340, :].mean(axis=0)
redcols = [i for i in range(W) if colprof[i] > 0.6]
print("vert red border cols:", redcols)

rowprof = red[:, 150:750].mean(axis=1)
redrows = [i for i in range(80) if rowprof[i] > 0.6]
print("top red border rows:", redrows)

botprof = red[:, 60:900].mean(axis=1)
botrows = [i for i in range(480, min(545, H)) if botprof[i] > 0.3]
print("bottom red rows:", botrows, [(i, round(botprof[i],2)) for i in botrows])

# badge ring: purple 6A5ACD-ish? check colors around badge center (875.5,71)
c = a[71, 875]
print("badge center px:", c)
# sample ring: ring at d~34? sample points on circle radius 17
import math
for rad in (14, 16, 17, 18, 19):
    px_ = a[int(71 + rad), 875]
    print(f"badge sample r={rad}: {px_}")
# horizontal scan through badge center y=71: x 855..900
row = a[71, 855:900]
print("badge hscan y=71:", [f"{x+855}:{tuple(v)}" for x, v in enumerate(row) if not (v[0]>230 and v[1]>230 and v[2]>230)][:40])
