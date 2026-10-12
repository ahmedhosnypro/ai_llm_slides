#!/usr/bin/env python3
"""slide033 measure-5: raw medians + exact x extents of pair boxes and columns."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556

print("--- raw row medians, sin/cos col x 332..394 ---")
for y in [100, 120, 130, 150, 170, 190, 200, 220, 240, 250, 265, 290, 320, 340, 360, 380, 400, 430, 460, 480, 505]:
    med = tuple(int(v) for v in np.median(a[y, 332:395], axis=0))
    print(f"  y={y:3d} slideY={MAPY(y):6.1f}  med={med}")

print("--- raw row medians, vector pairs col x 228..248 ---")
for y in [110, 130, 150, 170, 190, 200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500]:
    med = tuple(int(v) for v in np.median(a[y, 228:249], axis=0))
    print(f"  y={y:3d} slideY={MAPY(y):6.1f}  med={med}")

print("--- raw row medians, index col x 282..302 ---")
for y in [110, 130, 150, 170, 190, 200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500]:
    med = tuple(int(v) for v in np.median(a[y, 282:303], axis=0))
    print(f"  y={y:3d} slideY={MAPY(y):6.1f}  med={med}")

def xext(y, lo=200, hi=470, thresh=40):
    """find runs of non-background columns at row y"""
    row = a[y, lo:hi]
    nb = (np.abs(row - np.array([235, 235, 233])).sum(axis=1)) > thresh
    runs, cur = [], None
    for i, v in enumerate(nb):
        if v and cur is None: cur = [i + lo, i + lo]
        elif v: cur[1] = i + lo
        elif cur is not None:
            if cur[1] - cur[0] >= 1: runs.append(cur)
            cur = None
    if cur: runs.append(cur)
    return runs

print("--- x-extent runs (non-bg) at key rows ---")
for y in [130, 155, 170, 205, 220, 240, 270, 290, 315, 365, 385, 405, 480, 500]:
    runs = xext(y)
    rs = ", ".join(f"[{r0}..{r1}] x{MAPX(r0):.0f}..{MAPX(r1):.0f}" for r0, r1 in runs)
    print(f"  y={y:3d} slideY={MAPY(y):6.1f}: {rs}")
