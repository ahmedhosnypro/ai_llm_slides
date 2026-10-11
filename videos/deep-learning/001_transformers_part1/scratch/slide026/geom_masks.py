#!/usr/bin/env python3
"""Precise geometry: color masks per element, connected components with scipy."""
import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def blobs(name, target, tol, minpx=120, limit=24):
    t = np.array(target)
    m = (np.abs(A - t).sum(axis=2) <= tol)
    m = ndimage.binary_closing(m, np.ones((3, 3)))
    L, n = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(L)):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if h * w < minpx: continue
        mm = L[sl] == i + 1
        real = int(mm.sum())
        if real < minpx: continue
        out.append((real, sl[1].start, sl[1].stop - 1, sl[0].start, sl[0].stop - 1))
    out.sort(reverse=True)
    print(f"--- {name} ({len(out)} blobs)")
    for real, x0, x1, y0, y1 in out[:limit]:
        print(f"    n={real:6d} x{x0:3d}..{x1:3d} (w{x1-x0+1:3d}) y{y0:3d}..{y1:3d} (h{y1-y0+1:3d})")

blobs("softmax_bar_pink", (249, 217, 248), 36)
blobs("sigma_cyan", (236, 252, 252), 24)
blobs("dotproduct_tan", (219, 204, 188), 30)
blobs("stack_mint", (229, 252, 236), 22)
blobs("pill_paleyellow", (250, 243, 155), 45)
blobs("vector_yellow", (255, 255, 160), 60)
blobs("vector_pink", (255, 160, 200), 70)
blobs("vector_lavender", (215, 180, 255), 70)
blobs("red_ink", (230, 20, 20), 150, minpx=40, limit=40)
blobs("blue_ink", (0, 60, 200), 150, minpx=30, limit=40)
blobs("dark_text", (40, 40, 40), 180, minpx=60, limit=40)
blobs("green_ink", (0, 170, 80), 120, minpx=30, limit=40)
blobs("purple_ink", (112, 48, 160), 150, minpx=25, limit=30)
blobs("brown_ink", (139, 69, 19), 160, minpx=25, limit=30)
blobs("magenta", (255, 0, 255), 170, minpx=20, limit=10)
