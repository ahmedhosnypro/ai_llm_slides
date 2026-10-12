#!/usr/bin/env python3
"""Measure 002:8's frame chrome landmarks -> frame->slide transform (zoom fit).

Method (as slide_002.js / slide_013.js): find the gray panel's red border lines
(left/right/top) + bottom stroke + the yellow badge circle bbox, then fit
frame_x = AX + SX*slide_x, frame_y = SY*slide_y against the house chrome
(panel x 42..918(+1), y 45..540; badge center (893,71) d36).
"""
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# red border: strong red, low green/blue
red = (r > 130) & (g < 90) & (b < 90)

# columns with many red px (vertical borders)
colsum = red.sum(axis=0)
rowsum = red.sum(axis=1)
vcands = [x for x in range(W) if colsum[x] > 200]
hcands = [y for y in range(H) if rowsum[y] > 200]
print("vertical red cols:", vcands[:6], "...", vcands[-6:] if len(vcands) > 6 else "")
print("horizontal red rows:", hcands[:6], "...", hcands[-6:] if len(hcands) > 6 else "")

# yellow badge: FDFD96-ish
yellow = (r > 220) & (g > 220) & (b < 190) & (b > 110)
ys, xs = np.where(yellow)
# restrict to top-right quadrant
m = (xs > 700) & (ys < 160)
ys, xs = ys[m], xs[m]
if len(xs):
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(f"badge bbox frame: x {bx0}..{bx1} (cx {(bx0+bx1)/2}), y {by0}..{by1} (cy {(by0+by1)/2}), d~{(bx1-bx0+bx1-bx0)/2+1}")
else:
    print("badge not found")

# gray panel E9E9E7-ish columns: sample row 300 for panel left/right
row = a[300]
isgray = (abs(row[:,0]-233)<14) & (abs(row[:,1]-233)<14) & (abs(row[:,2]-231)<14)
gx = np.where(isgray)[0]
print("gray cols @row300:", gx.min(), gx.max())

# black letterbox at bottom
darkrow = (r < 40) & (g < 40) & (b < 40)
dr = darkrow.sum(axis=1)
rowsdark = [y for y in range(H) if dr[y] > 800]
print("letterbox rows:", rowsdark[:3], "..", rowsdark[-3:] if rowsdark else "")
