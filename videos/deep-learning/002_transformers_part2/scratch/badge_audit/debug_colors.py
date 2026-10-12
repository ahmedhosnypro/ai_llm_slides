#!/usr/bin/env python3
"""Sample actual RGB values: digit cores vs ring AA vs guards, on 047/049."""
from PIL import Image
import numpy as np
from scipy import ndimage
import os, collections

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"

def blob_of(a):
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    ym = (r > 215) & (g > 205) & (b < 215) & ((r - b) > 35) & ((g - b) > 35)
    region = np.zeros(ym.shape, bool); region[:170, 830:] = True
    ym &= region
    lab, n = ndimage.label(ym)
    sizes = [(lab == i).sum() for i in range(1, n + 1)]
    return lab == (int(np.argmax(sizes)) + 1)

for name in ("slide_047", "slide_049", "slide_048"):
    a = np.array(Image.open(os.path.join(ROOT, "unique_slides", f"{name}.jpg")).convert("RGB"))
    blob = blob_of(a)
    ys, xs = np.where(blob)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    zone = np.zeros(a.shape[:2], bool)
    zone[max(0,y0-4):y1+5, max(0,x0-4):x1+5] = True
    # darkest pixels in the zone = digit cores
    lum = (0.299*a[:,:,0] + 0.587*a[:,:,1] + 0.114*a[:,:,2]).astype(int)
    dark = zone & (lum < 150)
    cols = collections.Counter(map(tuple, a[dark].reshape(-1,3)))
    print(name, "darkest-zone colors (top 12):", cols.most_common(12))
    # ring AA band: pixels within 2px of blob but not blob and lum>150
    band = ndimage.binary_dilation(blob, iterations=2) & ~blob & (lum >= 150) & (lum < 215)
    cols2 = collections.Counter(map(tuple, a[band].reshape(-1,3)))
    print(name, "ring-AA band colors (top 8):", cols2.most_common(8))
    # how many dark pixels by location relative to disc bbox
    print(name, "dark px:", int(dark.sum()))
    # print digit-zone RGB grid rows y0..y1 only inside x0+2..x1-2, luminance<150 marked
    print()
