#!/usr/bin/env python3
"""Measure slide 024's delta regions precisely (subtitle + rules box) in frame px,
then map to slide pts via the frame's own mapping (T=43, B=516 fit)."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)

# mapping: landmarks L=58, R=899, T=43, B=516 <-> slide (42, 919, 45, 540)
sx = (899 - 58) / (919.0 - 42.0)
a = 58 - sx * 42.0
sy = (516 - 43) / (540.0 - 45.0)
b = 43 - sy * 45.0
print(f"map24: fx = {a:.4f} + {sx:.6f} * slide_x ;  fy = {b:.4f} + {sy:.6f} * slide_y")
def to_slide(fx, fy):
    return (fx - a) / sx, (fy - b) / sy
def fr(v):
    return f"{v:.1f}"

# ---- A. subtitle band (frame y 75..115) ----
band = img[70:120, 200:800]
r, g, bl = band[..., 0], band[..., 1], band[..., 2]
# yellow highlight: r>230,g>230,b<190
yel = (r > 225) & (g > 225) & (bl < 200) & (bl < r - 30)
# blue text ink: b > r+40, b>120
blue = (bl > 120) & (bl > r + 40)
if yel.any():
    yx0, yx1 = np.where(yel.any(axis=0))[0][[0, -1]] + 200
    yy0, yy1 = np.where(yel.any(axis=1))[0][[0, -1]] + 70
    print(f"subtitle YELLOW strip frame x {yx0}..{yx1} y {yy0}..{yy1}  -> slide "
          f"x {fr(to_slide(yx0,0)[0])}..{fr(to_slide(yx1,0)[0])} y {fr(to_slide(0,yy0)[1])}..{fr(to_slide(0,yy1)[1])}")
    # sample the yellow
    print("yellow sample:", tuple(img[(yy0+yy1)//2, (yx0+yx1)//2]))
if blue.any():
    bx0, bx1 = np.where(blue.any(axis=0))[0][[0, -1]] + 200
    by0, by1 = np.where(blue.any(axis=1))[0][[0, -1]] + 70
    print(f"subtitle BLUE ink frame x {bx0}..{bx1} y {by0}..{by1}  -> slide "
          f"x {fr(to_slide(bx0,0)[0])}..{fr(to_slide(bx1,0)[0])} y {fr(to_slide(0,by0)[1])}..{fr(to_slide(0,by1)[1])}")
    print("blue ink sample:", tuple(img[(by0+by1)//2, bx0+2]))

# ---- B. rules box (frame y 355..535) ----
band2 = img[350:535, 30:930]
r2, g2, b2 = band2[..., 0], band2[..., 1], band2[..., 2]
# pale yellow fill FFFFCC: r>240,g>240,b 180..225
py = (r2 > 238) & (g2 > 238) & (b2 > 170) & (b2 < 235) & (r2 - b2 > 20)
if py.any():
    px0, px1 = np.where(py.any(axis=0))[0][[0, -1]] + 30
    py0, py1 = np.where(py.any(axis=1))[0][[0, -1]] + 350
    print(f"\nrules box FILL frame x {px0}..{px1} y {py0}..{py1}  -> slide "
          f"x {fr(to_slide(px0,0)[0])}..{fr(to_slide(px1,0)[0])} y {fr(to_slide(0,py0)[1])}..{fr(to_slide(0,py1)[1])}")
    print("fill sample:", tuple(img[(py0+py1)//2, (px0+px1)//2]))
# blue border of the box: strong blue line
bb = (b2 > 130) & (b2 > r2 + 50) & (g2 < b2)
# restrict to border candidates: rows/cols where blue count is long
colcount = bb.sum(axis=0)
rowcount = bb.sum(axis=1)
cols = [i + 30 for i, c in enumerate(colcount) if c > 100]
rows_ = [i + 350 for i, c in enumerate(rowcount) if c > 300]
print("blue border cols:", cols[:6], "...", cols[-6:] if len(cols) > 6 else "")
print("blue border rows:", rows_[:6], "...", rows_[-6:] if len(rows_) > 6 else "")

# ---- C. text lines inside rules box (blue ink rows) ----
ink = (b2 > 110) & (b2 > r2 + 40)
rows_ink = ink.sum(axis=1)
print("\nblue-ink rows in rules box (frame y: count):")
in_run = False
for yy in range(band2.shape[0]):
    if rows_ink[yy] > 3 and not in_run:
        start = yy; in_run = True
    elif rows_ink[yy] <= 3 and in_run:
        fy0, fy1 = start + 350, yy - 1 + 350
        sx0, _ = to_slide(0, 0)
        print(f"  frame y {fy0}..{fy1} (h {fy1-fy0+1})  slide y {fr(to_slide(0,fy0)[1])}..{fr(to_slide(0,fy1)[1])}")
        in_run = False
if in_run:
    print(f"  frame y {start+350}..{band2.shape[0]-1+350} (open)")
