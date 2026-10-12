#!/usr/bin/env python3
"""Measure slide_052.jpg chrome landmarks -> frame->slide mapping.
House chrome (slide pts, 1px=1pt): panel border x 42..918(+1), y 45..540
(bottom stroke rows 538-539). Badge center (893,71) d36.
Frame is a ~0.958 zoomed-out capture with letterbox below.
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]

# red border mask: C00000-ish (allow JPEG noise)
red = (r > 120) & (g < 70) & (b < 70)

# Column profile of red pixels across rows 30..510 (avoid letterbox)
colcnt = red[30:510, :].sum(axis=0)
# find columns with count > 300 (full-height border lines)
cand = [x for x in range(W) if colcnt[x] > 300]
print("tall red columns:", cand)

rowcnt = red[:, 100:850].sum(axis=1)
candr = [y for y in range(H) if rowcnt[y] > 500]
print("wide red rows:", candr)

# badge: yellow FDFD96-ish circle near top-right. yellow: r>220,g>220,b<170
yel = (r > 215) & (g > 215) & (b < 190)
# search region x>820,y<130
ys, xs = np.where(yel[:140, 820:])
if len(xs):
    x0, x1 = xs.min() + 820, xs.max() + 820
    y0, y1 = ys.min(), ys.max()
    print(f"badge yellow bbox frame: x {x0}..{x1} y {y0}..{y1}  center {(x0+x1)/2:.1f},{(y0+y1)/2:.1f} d~{(x1-x0+y1-y0)/2}")

# letterbox: bottom black strip
dark_rows = [y for y in range(H) if (im[y, 100:850].sum(axis=1) < 90).mean() > 0.9]
print("letterbox rows (all-dark):", dark_rows[:5], "...", dark_rows[-5:] if dark_rows else "")
