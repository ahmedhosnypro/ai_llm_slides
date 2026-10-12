#!/usr/bin/env python3
"""Frame 011 chrome landmarks: panel borders + badge, refit mapping."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
a = np.asarray(Image.open(f"{V}/unique_slides/slide_011.jpg").convert("RGB")).astype(int)

def reddish(r, g, b):
    return r > 120 and g < 100 and b < 100 and (r - max(g, b)) > 50

# left/right borders: scan several clean rows (y=30..40 above content, y=505..515 below)
for y in [30, 35, 500, 508, 512]:
    cols = [x for x in range(960) if reddish(*a[y, x])]
    print(f"y={y} red cols:", cols)
# top border: scan clean columns (x=100..150, x=300)
for x in [100, 130, 300, 700, 850]:
    rows = [y for y in range(60) if reddish(*a[y, x])]
    print(f"x={x} red rows(0..60):", rows)
# bottom stroke: scan x=300, x=700 in 500..525
for x in [300, 700]:
    rows = [y for y in range(495, 525) if reddish(*a[y, x])]
    print(f"x={x} red rows(495..525):", rows)

# badge bbox: strong yellow FDFD96-ish
yl = (a[:, :, 0] > 230) & (a[:, :, 1] > 220) & (a[:, :, 2] > 120) & (a[:, :, 2] < 210)
ys, xs = np.where(yl[:130, 780:])
if len(xs):
    print("badge yellow bbox x", xs.min() + 780, xs.max() + 780, "y", ys.min(), ys.max())
