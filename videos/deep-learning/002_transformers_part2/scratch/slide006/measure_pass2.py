#!/usr/bin/env python3
"""Pass 2 for slide_006.jpg: border stroke landmarks (lower threshold) for the
frame->slide mapping refit + badge with ring + cursor scan."""
from PIL import Image
import numpy as np

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
im = Image.open(p).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 110) & (G < 100) & (B < 100)
red_border = red.copy()
red_border[:115, 845:] = False  # exclude badge region

# vertical strokes near expected left (~59) and right (~902): look at column red mass
colsum = red_border.sum(axis=0)
rowsum = red_border.sum(axis=1)
print("cols with red mass > 30 (x<120):", [(x, int(colsum[x])) for x in range(0, 120) if colsum[x] > 30])
print("cols with red mass > 30 (x>860):", [(x, int(colsum[x])) for x in range(860, W) if colsum[x] > 30])
print("rows with red mass > 100 (y<80):", [(y, int(rowsum[y])) for y in range(0, 80) if rowsum[y] > 100])
print("rows with red mass > 100 (y>460):", [(y, int(rowsum[y])) for y in range(460, H) if rowsum[y] > 100])

def stroke_center(idxs, prof):
    groups, grp = [], []
    for i in idxs:
        if grp and i == grp[-1] + 1:
            grp.append(i)
        else:
            if grp: groups.append(grp)
            grp = [i]
    if grp: groups.append(grp)
    return [(round(sum(i * prof[i] for i in g) / sum(prof[i] for i in g), 2), g[0], g[-1]) for g in groups]

left_cols = [x for x in range(30, 90) if colsum[x] > 20]
right_cols = [x for x in range(880, 930) if colsum[x] > 20]
top_rows = [y for y in range(20, 70) if rowsum[y] > 100]
bot_rows = [y for y in range(480, 517) if rowsum[y] > 100]
print("\nleft stroke:", stroke_center(left_cols, colsum))
print("right stroke:", stroke_center(right_cols, colsum))
print("top stroke:", stroke_center(top_rows, rowsum))
print("bottom stroke:", stroke_center(bot_rows, rowsum))

# badge: yellow disc + ring 6A5ACD
yel = (R > 220) & (G > 215) & (B < 190) & (R > B + 40)
ys, xs = np.where(yel)
m = (ys < 130) & (xs > 820)
ys, xs = ys[m], xs[m]
print("\nbadge yellow bbox: x %d..%d, y %d..%d (cx %.1f cy %.1f, n=%d)" %
      (xs.min(), xs.max(), ys.min(), ys.max(), xs.mean(), ys.mean(), len(xs)))
pur = (np.abs(R - 106) < 55) & (np.abs(G - 90) < 55) & (np.abs(B - 205) < 60) & (B > R + 30) & (B > G + 40)
pys, pxs = np.where(pur)
m2 = (pys < 130) & (pxs > 820)
pys, pxs = pys[m2], pxs[m2]
if len(pxs):
    print("badge ring bbox: x %d..%d, y %d..%d (cx %.1f cy %.1f, n=%d)" %
          (pxs.min(), pxs.max(), pys.min(), pys.max(), pxs.mean(), pys.mean(), len(pxs)))

# cursor scan: white blob (r,g,b all >240) in the body, left half, below line-4 area
white = (R > 238) & (G > 238) & (B > 238)
# cursor is surrounded by gray panel (233) — white blob of size > 30 px
from scipy import ndimage  # may not exist; fallback manual
