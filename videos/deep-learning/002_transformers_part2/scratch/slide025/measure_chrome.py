#!/usr/bin/env python3
"""Measure slide_025.jpg: chrome landmarks + fit frame->slide mapping.
Chrome law (playlist): slide coords: panel x 42..918 (left border outer 42,
right border outer 919), top border outer y=45, bottom border stroke at 538-539
(half-visible), badge center (893,71) d36.
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"frame {W}x{H}")

r, g, b = a[..., 0], a[..., 1], a[..., 2]

# red border mask: strong red, low green/blue
red = (r > 120) & (g < 90) & (b < 90)

# Panel left border: scan columns 40..90 at rows 200..400, find red columns
rows = slice(200, 400)
colprof = red[rows, :].mean(axis=0)
redcols = [i for i in range(W) if colprof[i] > 0.8]
print("red vertical border columns (colprof>0.8):", redcols[:10], "...", redcols[-10:] if len(redcols) > 10 else "")

# Panel top border: scan rows 30..70 at cols 200..800
cols = slice(200, 800)
rowprof = red[:, cols].mean(axis=1)
redrows = [i for i in range(60) if rowprof[i] > 0.8]
print("red horizontal border rows (top):", redrows)

# Bottom border: scan rows 500..540 full width
rowprof2 = red[:, :].mean(axis=1)
botrows = [i for i in range(500, H) if rowprof2[i] > 0.5]
print("red rows near bottom (>0.5 width):", botrows)

# black strip rows (letterbox)
dark = (r < 40) & (g < 40) & (b < 40)
dprof = dark.mean(axis=1)
darkrows = [i for i in range(H) if dprof[i] > 0.9]
print("full-width dark rows:", darkrows[:5], "...", darkrows[-3:] if darkrows else "")

# badge: yellow FDFD96-ish circle top right. search x 840..910, y 45..100
sub = a[40:105, 830:920]
sr, sg, sb = sub[...,0], sub[...,1], sub[...,2]
yel = (sr > 220) & (sg > 220) & (sb < 180) & (sb > 120)
ys, xs = np.nonzero(yel)
if len(xs):
    print(f"badge yellow bbox: x {830+xs.min()}..{830+xs.max()} y {40+ys.min()}..{40+ys.max()}  center ({830+(xs.min()+xs.max())/2}, {40+(ys.min()+ys.max())/2})")
else:
    print("no yellow badge found in search window")

# gray panel region: sample far inside
print("panel color @ (100,300):", a[300, 100], " @ (500,450):", a[450, 500])
print("outer canvas @ (10,10):", a[10, 10], " @ (5,480):", a[480, 5])
