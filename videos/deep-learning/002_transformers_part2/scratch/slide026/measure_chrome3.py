#!/usr/bin/env python3
"""Sample pixel colors along expected border lines + refine landmarks."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# Border detection: red-dominant pixels (r - max(g,b) > 40), any darkness
redish = (r - np.maximum(g, b) > 40) & (r > 100)

def vprofile(x0, x1, y0=120, y1=400, label=""):
    out = []
    for x in range(x0, x1):
        cnt = redish[y0:y1, x].sum()
        if cnt > 30:
            out.append((x, int(cnt)))
    print(label, out)

def hprofile(y0, y1, x0=200, x1=750, label=""):
    out = []
    for y in range(y0, y1):
        cnt = redish[x0:x1, y].sum()
        if cnt > 30:
            out.append((y, int(cnt)))
    print(label, out)

vprofile(40, 80, label="LEFT cols:")
vprofile(880, 920, label="RIGHT cols:")
hprofile(25, 65, label="TOP rows:")
hprofile(495, 540, label="BOTTOM rows:")

# what does the border color look like? sample at known spots once found
# also sample bottom black strip
black = (r < 60) & (g < 60) & (b < 60)
rowb = black.sum(axis=1)
print("black-heavy rows (count>400):", [(y, int(c)) for y, c in enumerate(rowb) if c > 400])
