#!/usr/bin/env python3
"""Color-range component map for diagram elements in slide_017.jpg."""
import numpy as np
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape

def mask_range(lo, hi, region=None):
    m = np.ones((H, W), dtype=bool)
    for i in range(3):
        m &= (A[:, :, i] >= lo[i]) & (A[:, :, i] <= hi[i])
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros_like(m)
        mm[y0:y1+1, x0:x1+1] = m[y0:y1+1, x0:x1+1]
        m = mm
    return m

def components(mask, min_px=30):
    seen = np.zeros((H, W), dtype=bool)
    comps = []
    ys_all, xs_all = np.nonzero(mask)
    for (y, x) in zip(ys_all, xs_all):
        if seen[y, x]:
            continue
        q = deque([(y, x)])
        seen[y, x] = True
        pts = []
        while q:
            cy, cx = q.popleft()
            pts.append((cy, cx))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    q.append((ny, nx))
        if len(pts) >= min_px:
            pts = np.array(pts)
            comps.append((len(pts), int(pts[:,1].min()), int(pts[:,0].min()), int(pts[:,1].max()), int(pts[:,0].max())))
    return comps

def report(name, lo, hi, region, min_px=30, max_show=30):
    comps = components(mask_range(lo, hi, region), min_px)
    comps.sort(key=lambda c: (c[2], c[1]))
    print(f"== {name}: {len(comps)} comps")
    for n, x0, y0, x1, y1 in comps[:max_show]:
        print(f"   n={n:7d} x{x0:3d}..{x1:3d} y{y0:3d}..{y1:3d}  w={x1-x0+1:3d} h={y1-y0+1:3d}")

DIAG = (562, 95, 920, 536)

# tan node boxes (fill+border, generous): r 120..220, g 80..190, b 30..150
report("tan_nodes", (120, 80, 30), (225, 195, 150), DIAG, 250)
# light green boxes C5E0B4 (197,224,180): Linear/Softmax
report("lightgreen", (170, 205, 150), (230, 245, 215), DIAG, 200)
# purple B28FCE (178,143,206)
report("purple", (140, 110, 175), (220, 185, 235), DIAG, 150)
# dark red C0504D (192,80,77)
report("darkred", (150, 50, 45), (225, 125, 115), DIAG, 150)
# blue circles 0000FF
report("blue", (0, 0, 120), (110, 110, 255), DIAG, 30)
# pure red FF0000 (circles + block arrows) - separate from C00000 title
report("red", (140, 0, 0), (255, 120, 110), DIAG, 30)
# gray BFBFBF (N x circles)
report("gray_Nx", (150, 150, 150), (215, 215, 215), DIAG, 100)
# yellow highlights FFFF00
report("yellow_diag", (200, 200, 0), (255, 255, 170), DIAG, 100)
