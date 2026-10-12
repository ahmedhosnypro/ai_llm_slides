#!/usr/bin/env python3
"""Pass 9: bracket tick geometry + per-row entry runs in the original matrix."""
from PIL import Image
import numpy as np
import os

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(os.path.join(D, "unique_slides/slide_031.jpg")).convert("RGB")).astype(int)
lum = a.mean(axis=2)

def runs_in(y0, y1, x0, x1, thr=150, gap=2):
    seg = lum[y0:y1 + 1, x0:x1 + 1]
    colink = (seg < thr).sum(axis=0)
    out, x, n = [], 0, len(colink)
    while x < n:
        if colink[x] > 0:
            x2, g = x, 0
            while x2 < n - 1:
                if colink[x2 + 1] > 0: g = 0; x2 += 1
                else:
                    g += 1
                    if g > gap: break
                    x2 += 1
            out.append((x0 + x, x0 + x2)); x = x2 + 1
        else: x += 1
    return out

print("top tick rows (395..399), x 625..850:")
for y in range(395, 400):
    print(f"  row {y}:", runs_in(y, y, 625, 850))
print("bottom tick rows (491..496):")
for y in range(491, 497):
    print(f"  row {y}:", runs_in(y, y, 625, 850))
print("stroke col 634..638 y-extent per col:")
for x in range(632, 640):
    ys = np.where(lum[390:500, x] < 150)[0]
    print(f"  col {x}: {390+ys.min()}..{390+ys.max()}" if len(ys) else f"  col {x}: none")
print("row bands per-entry runs:")
for y0, y1 in ((401, 424), (433, 456), (466, 489)):
    print(f"  band {y0}..{y1}:", runs_in(y0, y1, 640, 828, gap=3))
# vertical extents of theta vs subscript in an entry: rows of ink in x 718..747 (theta_5)
seg = lum[400:430, 718:734]
rows = np.where((seg < 150).any(axis=1))[0]
print("theta_5 glyph rows:", 400 + rows.min(), "..", 400 + rows.max())
seg = lum[400:430, 735:750]
rows = np.where((seg < 150).any(axis=1))[0]
print("sub_5 rows:", 400 + rows.min(), "..", 400 + rows.max())
