#!/usr/bin/env python3
"""Pass G: interior color grids, eroded red medians, per-slab geometry, label text color."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
orange = (r > 140) & (g > 70) & (g < 190) & (b < 100) & (r - b > 70)

print("== A. interior color grids ==")
def grid(x0, x1, y0, y1, name, dx=8, dy=12):
    print(f"  {name}:")
    for y in range(y0, y1, dy):
        row = []
        for x in range(x0, x1, dx):
            p = im[y, x]
            row.append(f"{x},{y}:{p[0]:3d},{p[1]:3d},{p[2]:3d}")
        print("    " + " | ".join(row))
grid(453, 474, 192, 252, "NN block1")
grid(232, 286, 340, 420, "slab1", dx=9, dy=10)
grid(737, 758, 338, 400, "L5 block", dx=7, dy=10)

print("== B. eroded red median (title) ==")
red = (r > 120) & (g < 110) & (b < 110)
core = red[62:124, 100:840]
er = core[1:-1, 1:-1] & core[:-2, 1:-1] & core[2:, 1:-1] & core[1:-1, :-2] & core[1:-1, 2:]
px = im[63:123, 101:839][er]
print(f"  title core n={len(px)} median {np.median(px, axis=0)}")
for (y0, y1, x0, x1, name) in [(447, 450, 100, 800, 'bottom border'), (57, 60, 100, 400, 'left border'),
                               (134, 137, 100, 800, 'rule'), (46, 49, 100, 800, 'top border')]:
    sub = red[y0:y1, x0:x1]
    er2 = sub[1:-1, 1:-1] & sub[:-2, 1:-1] & sub[2:, 1:-1] & sub[1:-1, :-2] & sub[1:-1, 2:]
    if er2.sum() > 20:
        p2 = im[y0+1:y1-1, x0+1:x1-1][er2]
        print(f"  {name}: n={len(p2)} median {np.median(p2, axis=0)}")

print("== C. label box text color (box1 interior darkest) ==")
sub = im[160:178, 250:370]
lum = sub.mean(axis=2)
idx = np.unravel_index(np.argsort(lum, axis=None)[:10], lum.shape)
for k in range(10):
    y, x = idx[0][k], idx[1][k]
    print(f"  ({x+250},{y+160}): {tuple(int(v) for v in sub[y, x])} lum={lum[y,x]:.0f}")

print("== D. per-slab geometry (orange extents at 5 rows each) ==")
slabs = [(228, 288), (310, 370), (398, 458), (476, 536), (553, 612), (634, 694)]
for i, (x0, x1) in enumerate(slabs):
    ext = []
    for y in (318, 330, 345, 360, 380, 400, 415, 423):
        xs = np.where(orange[y, x0-6:x1+7])[0]
        ext.append((y, xs.min()+x0-6 if len(xs) else -1, xs.max()+x0-6 if len(xs) else -1))
    print(f"  slab{i+1}: {ext}")

print("== E. per-block geometry NN + L5/L6/Loss ==")
for (x0, x1, y0, y1, name) in [(449, 476, 186, 256, 'NN1'), (685, 712, 186, 256, 'NN6-Loss'),
                               (734, 761, 333, 404, 'L5'), (829, 855, 333, 404, 'Loss')]:
    ext = []
    for y in (y0+2, (y0+y1)//2, y1-2):
        xs = np.where(orange[y, x0-4:x1+5])[0]
        ext.append((y, xs.min()+x0-4 if len(xs) else -1, xs.max()+x0-4 if len(xs) else -1))
    print(f"  {name}: {ext}")

print("== F. siamese vertices refinement ==")
bg = ((r > 215) & (g > 215) & (b > 215)) | ((abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16))
nb = ~bg
for y in (320, 324, 328, 340, 360, 370, 380, 390, 400, 410, 416):
    xs = np.where(nb[y, 122:226])[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+122}..{xs.max()+122}")

print("== G. slab top-face tone (light triangle) ==")
for (x, y) in [(282, 320), (270, 322), (258, 330), (246, 340), (238, 348)]:
    print(f"  ({x},{y}): {tuple(int(v) for v in im[y, x])}")
