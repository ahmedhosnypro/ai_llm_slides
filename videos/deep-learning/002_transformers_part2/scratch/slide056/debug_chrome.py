#!/usr/bin/env python3
# debug_chrome.py — profile the red border rows/cols to find exact chrome landmarks.
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_056.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 120) & (g < 90) & (b < 90)

col = red[60:500, :].sum(axis=0)   # vertical lines span the panel
row = red[:, 200:800].sum(axis=1)  # horizontal lines span the middle

print("TOP cols 50..100:", [(x, int(col[x])) for x in range(50, 100) if col[x] > 50])
print("RIGHT cols 880..925:", [(x, int(col[x])) for x in range(880, 925) if col[x] > 50])
print("TOP rows 25..60:", [(y, int(row[y])) for y in range(25, 60) if row[y] > 100])
print("BOTTOM rows 500..540:", [(y, int(row[y])) for y in range(500, 540) if row[y] > 100])

# badge: yellow + ring; scan x 850..915, y 45..100
yellow = (r > 200) & (g > 200) & (b < 180)
ys, xs = np.nonzero(yellow[40:110, 845:920])
print("badge yellow bbox frame:", xs.min() + 845, xs.max() + 845, ys.min() + 40, ys.max() + 40)

# sample the border pixel color at the found landmarks
def sample(x, y):
    return tuple(a[y, x])
print("sample left border:", [sample(x, 300) for x in range(56, 64)])
print("sample top border:", [sample(400, y) for y in range(40, 48)])
print("sample bottom border:", [sample(400, y) for y in range(513, 521)])
