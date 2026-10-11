#!/usr/bin/env python3
"""Measure: red bottom curve; salmon card exact bounds; swoosh path; q1 bar."""
import numpy as np
from PIL import Image
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
red = (r>140)&(g<110)&(b<110)   # CC0000-ish
darkred = (r>110)&(r<190)&(g<60)&(b<60)  # 8B0000-ish
# salmon card bounds: rows 275..528
salmon = (abs(r-241)<10)&(abs(g-139)<14)&(abs(b-150)<14)
ys,xs = np.where(salmon[260:535, 40:700])
print("salmon main bbox: x", 40+xs.min(),"..",40+xs.max(), " y", 260+ys.min(),"..",260+ys.max())
# salmon left edge per row
for y in range(272, 530, 25):
    row = np.where(salmon[y, 40:660])[0]
    if len(row): print(f"  salmon y={y}: x {40+row.min()}..{40+row.max()}")
# salmon bottom: last row with wide salmon
for y in range(535, 500, -1):
    row = np.where(salmon[y, 40:660])[0]
    if len(row) > 100:
        print("salmon bottom row:", y, "x", 40+row.min(),"..",40+row.max()); break
# red curve along bottom: red px below y 515, x 60..640
ys,xs = np.where(red[515:540, 40:660])
if len(xs):
    print("bottom red curve: x", 40+xs.min(),"..",40+xs.max(), " y", 515+ys.min(),"..",515+ys.max())
    for x in range(40+xs.min(), 40+xs.max()+1, 40):
        col = np.where(red[515:540, x])[0]
        if len(col): print(f"   curve x={x}: y {515+col.min()}..{515+col.max()}")
# dark red swoosh: right of x 480
ys,xs = np.where(darkred[150:540, 480:920])
if len(xs):
    print("swoosh bbox: x", 480+xs.min(),"..",480+xs.max(), " y", 150+ys.min(),"..",150+ys.max())
    for y in range(150, 540, 20):
        col = np.where(darkred[y, 480:920])[0]
        if len(col): print(f"   swoosh y={y}: x {480+col.min()}..{480+col.max()}")
# q1 red bar: horizontal red thick bar somewhere y 420..470 x 60..250?
ys,xs = np.where(red[400:480, 50:280])
if len(xs):
    # density per row
    for y in range(400, 480, 5):
        row = np.where(red[y, 50:280])[0]
        if len(row)>10: print(f"   red y={y}: x {50+row.min()}..{50+row.max()} n={len(row)}")
