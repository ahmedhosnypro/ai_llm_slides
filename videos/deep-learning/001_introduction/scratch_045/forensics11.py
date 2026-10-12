#!/usr/bin/env python3
"""forensics11.py — per-token segmentation of the 3 equations (lum ink, red excluded).
Prints col-clusters (gap>3) with per-cluster y-extent = token ink boxes.
Banked to qa/slide045/forensics11_out.txt."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (r + g + b) / 3
reddish = (r - g > 30) & (r - b > 20)
ink = (lum < 200) & (~reddish)

def clusters(x0, x1, y0, y1, label, gap=3):
    print(f"\n== {label} (x{x0}..{x1}, y{y0}..{y1}) ==")
    sub = ink[y0:y1 + 1, x0:x1 + 1]
    colprof = sub.sum(axis=0)
    cols = np.where(colprof > 0)[0]
    if len(cols) == 0:
        print(" EMPTY"); return
    segs, s, p = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - p > gap:
            segs.append((s, p)); s = c
        p = c
    segs.append((s, p))
    for (a, bb) in segs:
        band = sub[:, a:bb + 1]
        rows = np.where(band.any(axis=1))[0]
        print(f"  token x{a + x0}..{bb + x0} (w={bb - a + 1})  y{rows.min() + y0}..{rows.max() + y0} (h={rows.max() - rows.min() + 1})  n={int(band.sum())}")

clusters(465, 696, 295, 375, "EQ(a) tokens")
clusters(510, 650, 386, 418, "EQ(b) tokens")
clusters(425, 692, 418, 497, "EQ(c) tokens")

# fine row bands per equation for baseline pinning
def rowbands(x0, x1, y0, y1, label):
    sub = ink[y0:y1 + 1, x0:x1 + 1]
    rp = sub.sum(axis=1)
    rows = np.where(rp > 0)[0]
    segs, s, p = [], rows[0], rows[0]
    for c in rows[1:]:
        if c - p > 1:
            segs.append((s, p)); s = c
        p = c
    segs.append((s, p))
    print(f"\n{label} row-bands:", [(a + y0, bb + y0) for a, bb in segs])

rowbands(473, 694, 295, 375, "EQ(a)")
rowbands(522, 645, 386, 418, "EQ(b)")
rowbands(435, 680, 418, 497, "EQ(c)")
rowbands(515, 550, 295, 375, "EQ(a) sum1 zone")
rowbands(552, 592, 295, 375, "EQ(a) sum2 zone")
rowbands(540, 578, 418, 497, "EQ(c) sum1 zone")
rowbands(578, 617, 418, 497, "EQ(c) sum2 zone")
rowbands(435, 522, 418, 497, "EQ(c) fraction zone")
