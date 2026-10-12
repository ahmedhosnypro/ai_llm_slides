#!/usr/bin/env python3
"""Debug why ink extraction is empty inside the badge disc."""
from PIL import Image
import numpy as np
from scipy import ndimage
import os

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
a = np.array(Image.open(os.path.join(ROOT, "unique_slides", "slide_049.jpg")).convert("RGB"))
print("shape", a.shape, a.dtype)

r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
ym = (r > 215) & (g > 205) & (b < 215) & ((r - b) > 35) & ((g - b) > 35)
region = np.zeros(ym.shape, bool)
region[:170, 830:] = True
ym &= region
lab, n = ndimage.label(ym)
print("blobs:", n, "sizes:", [int((lab == i).sum()) for i in range(1, n + 1)])
sizes = [(lab == i).sum() for i in range(1, n + 1)]
lid = int(np.argmax(sizes)) + 1
blob = lab == lid
ys, xs = np.where(blob)
print("blob bbox", xs.min(), ys.min(), xs.max(), ys.max(), "area", blob.sum())

inner = ndimage.binary_erosion(blob, iterations=1)
print("inner px:", int(inner.sum()))

fill = np.median(a[blob].reshape(-1, 3), axis=0)
print("fill:", fill)
dist = np.sqrt(((a.astype(int) - fill.astype(int)) ** 2).sum(axis=2))
print("dist inside inner: min %.1f max %.1f  #>70: %d" % (dist[inner].min(), dist[inner].max(), int((dist[inner] > 70).sum())))
lum = 0.299 * r + 0.587 * g + 0.114 * b
print("lum inside inner: min %.1f max %.1f" % (lum[inner].min(), lum[inner].max()))

# raw grid over the badge bbox: luminance, 2 chars wide
x0, x1 = int(xs.min()), int(xs.max())
y0, y1 = int(ys.min()), int(ys.max())
print("luminance grid (rows %d..%d, cols %d..%d), darker = higher char:" % (y0, y1, x0, x1))
chars = "@%#*+=-:. "  # dark -> light
lmin, lmax = lum[y0:y1 + 1, x0:x1 + 1].min(), lum[y0:y1 + 1, x0:x1 + 1].max()
for y in range(y0, y1 + 1):
    row = ""
    for x in range(x0, x1 + 1):
        v = lum[y, x]
        idx = int((v - lmin) / (lmax - lmin + 1e-9) * (len(chars) - 1))
        row += chars[idx]
    print(f"{y:3d} |{row}|")
print("cols %d..%d" % (x0, x1))
