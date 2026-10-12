#!/usr/bin/env python3
"""Stage 6: precise highlight/outline inventory via colored-pixel connected components."""
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
colored = (mx - mn) > 22   # excludes white/gray/black text

# panel interior
PX0, PX1, PY0, PY1 = 148, 551, 206, 500
lab, n = ndimage.label(colored[PY0:PY1, PX0:PX1], structure=np.ones((3,3)))
print(f'{n} components')
out = []
for i in range(1, n+1):
    ys, xs = np.where(lab == i)
    if len(xs) < 25: continue
    x0, x1, y0, y1 = xs.min()+PX0, xs.max()+PX0, ys.min()+PY0, ys.max()+PY0
    area = len(xs)
    fill = area / ((x1-x0+1) * (y1-y0+1))
    mr = r[ys+PY0, xs+PX0].mean(); mg = g[ys+PY0, xs+PX0].mean(); mb = b[ys+PY0, xs+PX0].mean()
    # core color: mode-ish (median)
    medr = np.median(r[ys+PY0, xs+PX0]); medg = np.median(g[ys+PY0, xs+PX0]); medb = np.median(b[ys+PY0, xs+PX0])
    out.append((y0, x0, x1, y1, area, fill, medr, medg, medb))
out.sort()
for (y0, x0, x1, y1, area, fill, mr, mg, mb) in out:
    kind = 'FILL' if fill > 0.55 else ('OUTLINE' if fill < 0.25 else 'MIXED')
    print(f'y {y0}..{y1}  x {x0}..{x1}  area {area:5d} fill {fill:.2f} {kind}  medRGB=({mr:.0f},{mg:.0f},{mb:.0f}) hex=#{int(mr):02X}{int(mg):02X}{int(mb):02X}')
