#!/usr/bin/env python3
"""Pass 1: precise card geometry via connected components + scanline runs."""
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def comps(mask, name, min_n=800):
    lab, n = ndimage.label(mask)
    print(f"== {name} ==")
    res = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_n: continue
        res.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(ys)))
        print(f"  comp: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")
    return res

def near(c, tol):
    return (abs(r-c[0])<tol) & (abs(g-c[1])<tol) & (abs(b-c[2])<tol)

# Cards — tight tolerance, biggest component each
comps(near((240,128,128), 22), 'h1 salmon S')
comps(near((200,200,240), 15), 'h2 lavender L')
comps(near((252,252,176), 18), 'h3 pale yellow Y')
comps(near((204,255,204), 14), 'h4 pale green N')
comps(near((255,228,196), 16), 'h5 peach P')

# scanline: for each card color, per-row leftmost/rightmost (to see the staircase)
print("\n== per-row extents (every 10 rows) ==")
for nm, c, tol in [('S',(240,128,128),22), ('L',(200,200,240),15), ('Y',(252,252,176),18), ('N',(204,255,204),14), ('P',(255,228,196),16)]:
    m = near(c, tol)
    print(f"-- {nm}")
    for y in range(180, 540, 10):
        xs = np.where(m[y])[0]
        if len(xs) > 5:
            print(f"   y={y}: x {xs.min()}..{xs.max()}")
