#!/usr/bin/env python3
"""Connected-component analysis of each ink mask over the whole slide_053 frame."""
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def sxy(fx, fy):
    return (fx - 18.45) / 0.95991, (fy + 0.29) / 0.95600

masks = {
    'red':   (r - (g + b) / 2 > 55),
    'blue':  (b - (r + g) / 2 > 55),
    'green': (g > r + 6) & (g > b + 6) & (g > 195) & (r > 150),
    'mauve': (r > 140) & (r < 230) & (g > 90) & (g < 190) & (b > 90) & (b < 190) & (r > g + 15) & (r > b + 15),
    'yellow': (r > 228) & (g > 228) & (b > 150) & (b < 220),
    'dark':  (r < 100) & (g < 100) & (b < 100),
}

for name, m in masks.items():
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    print(f'=== {name}: {n} components ===')
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) < 25:
            continue
        comps.append((len(xs), xs.min(), xs.max(), ys.min(), ys.max()))
    comps.sort(key=lambda c: (-c[0]))
    for npx, x0, x1, y0, y1 in comps[:60]:
        sx0, sy0 = sxy(x0, y0); sx1, sy1 = sxy(x1, y1)
        print(f'  n={npx:6d} frame x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d}  slide x {sx0:6.1f}..{sx1:6.1f} y {sy0:6.1f}..{sy1:6.1f}')
