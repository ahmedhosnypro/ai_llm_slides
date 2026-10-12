#!/usr/bin/env python3
"""Slide 045 — precise measurements: columns, row bands, cell colors, boxes, arrows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
SX, OX = 0.962329, 17.582
SY, OY = 0.957576, -0.0909
def S(fx, fy): return ((fx - OX) / SX, (fy - OY) / SY)

# --- 1) X-row bar: cell strip colors + full band + column centers.
# Row D pink band 481..496; full bar extends below pink. Sample col2 (frame cx~251.5)
# Print a vertical color profile at col2 center and a horizontal profile mid-bar.
print("== X row vertical profile at fx=250 (rows 470..510) ==")
for y in range(470, 512):
    print(y, tuple(img[y, 250]), tuple(img[y, 258]), tuple(img[y, 266]))
