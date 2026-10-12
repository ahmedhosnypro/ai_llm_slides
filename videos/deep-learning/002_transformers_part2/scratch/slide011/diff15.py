#!/usr/bin/env python3
"""Frame 011 chrome landmarks + diff vs certified sibling 015's frame."""
from PIL import Image, ImageChops
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
f11 = Image.open(f"{V}/unique_slides/slide_011.jpg").convert("RGB")
f15 = Image.open(f"{V}/unique_slides/slide_015.jpg").convert("RGB")
print("sizes:", f11.size, f15.size)
a11 = np.asarray(f11).astype(int)

# --- chrome landmark scan: red panel border columns/rows (C00000-ish) ---
def is_red(px):
    r, g, b = px
    return r > 130 and g < 90 and b < 90

# scan row y=200 (mid-slide) for vertical red borders (left/right of panel)
row = a11[200]
redcols = [x for x in range(960) if is_red(row[x])]
print("row200 red cols:", redcols[:12], "...", redcols[-12:] if len(redcols) > 12 else "")

# scan column x=480 for horizontal red borders (top border / bottom stroke)
col = a11[:, 480]
redrows = [y for y in range(540) if is_red(col[y])]
print("col480 red rows:", redrows[:14], "...", redrows[-14:] if len(redrows) > 14 else "")

# gray panel top edge: E9E9E7 run start; letterbox: black rows at bottom
gray = np.all(np.abs(a11 - np.array([233, 233, 231])) < 10, axis=2)
grayrows = np.where(gray[:, 100:200].mean(axis=1) > 0.8)[0]
print("gray rows range (x100..200):", grayrows.min() if len(grayrows) else None,
      grayrows.max() if len(grayrows) else None)
dark = np.all(a11 < 40, axis=2)
darkrows = np.where(dark[:, 100:800].mean(axis=1) > 0.9)[0]
print("black letterbox rows:", (darkrows.min(), darkrows.max()) if len(darkrows) else None)

# badge: yellow blob near top-right
yellow = (a11[:, :, 0] > 200) & (a11[:, :, 1] > 190) & (a11[:, :, 2] < 190)
ys, xs = np.where(yellow[:150, 700:])
if len(xs):
    print("badge bbox x", xs.min() + 700, xs.max() + 700, "y", ys.min(), ys.max(),
          "center", (xs.min() + xs.max()) / 2 + 700, (ys.min() + ys.max()) / 2)

# --- aligned diff vs 015 ---
d = ImageChops.difference(f11, f15)
da = np.asarray(d).astype(int).sum(axis=2)
hot = da > 90
print("hot px count 011-vs-015:", hot.sum(), "of", hot.size, f"({100*hot.sum()/hot.size:.1f}%)")
# hot map by 60x54 blocks to see where they differ
H, W = hot.shape
bs = 60
grid = hot[: H // bs * bs, : W // bs * bs].reshape(H // bs, bs, W // bs, bs).mean(axis=(1, 3))
np.set_printoptions(precision=1, suppress=True, linewidth=200)
print("hot fraction per 60px col-block (rows 0-9 top->bottom):")
print((grid * 100).astype(int))
