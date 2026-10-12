#!/usr/bin/env python3
"""measure1_chrome.py — slide 034 chrome landmark fit (P2 convention).
Red-weighted subpixel centroids of the four chrome border strokes, then the
family mapping fit. Also: letterbox extent + badge bbox cross-check."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(float)
H, W, _ = img.shape
print(f"frame {W}x{H}")

r, g, b = img[..., 0], img[..., 1], img[..., 2]
redness = r - np.maximum(g, b)

def stroke_centroid_x(x0, x1, y0, y1, thresh=60):
    win = redness[y0:y1, x0:x1]
    m = win > thresh
    if m.sum() == 0:
        return None, 0
    xs = np.arange(x0, x1)
    wsum = win.sum(axis=1)[m.any(axis=1)].sum() if False else win[m].sum()
    cx = (win * xs[None, :])[m].sum() / wsum
    return cx, m.sum()

def stroke_centroid_y(y0, y1, x0, x1, thresh=60):
    win = redness[y0:y1, x0:x1]
    m = win > thresh
    if m.sum() == 0:
        return None, 0
    ys = np.arange(y0, y1)
    wsum = win[m].sum()
    cy = (win * ys[:, None])[m].sum() / wsum
    return cy, m.sum()

# left stroke: scan x 50..70 in a quiet y band (no content) — pick y band free of other red
# first find rows of the left stroke: search columns 50..70 for redness
for band, y0, y1, x0, x1 in [("left", 200, 350, 50, 75), ("right", 200, 350, 885, 915),
                             ("top", 100, 300, 35, 60), ]:
    pass

# LEFT: for each y in a mid band, find red pixels in x 45..80
left_cols = redness[200:350, 45:80]
colsum = left_cols.sum(axis=0)
xs = np.arange(45, 80)
# weighted centroid over columns with redness
m = colsum > 0
cx = (colsum * xs)[m].sum() / colsum[m].sum()
print(f"LEFT stroke x-centroid: {cx:.2f} (cols {xs[m].min()}..{xs[m].max()})")

right_cols = redness[200:350, 880:920]
xs = np.arange(880, 920)
colsum = right_cols.sum(axis=0)
m = colsum > 0
cx = (colsum * xs)[m].sum() / colsum[m].sum()
print(f"RIGHT stroke x-centroid: {cx:.2f} (cols {xs[m].min()}..{xs[m].max()})")

top_rows = redness[35:60, 200:500]
ys = np.arange(35, 60)
rowsum = top_rows.sum(axis=1)
m = rowsum > 0
cy = (rowsum * ys)[m].sum() / rowsum[m].sum()
print(f"TOP stroke y-centroid: {cy:.2f} (rows {ys[m].min()}..{ys[m].max()})")

# BOTTOM letterbox: find black rows at bottom
dark = (r < 40) & (g < 40) & (b < 40)
rowdark = dark.mean(axis=1)
lb = [y for y in range(500, H) if rowdark[y] > 0.9]
print(f"letterbox rows: {min(lb) if lb else None}..{max(lb) if lb else None}")
# bottom red stroke just above letterbox (bottom edge of panel)
bot_rows = redness[500:520, 200:500]
ys = np.arange(500, 520)
rowsum = bot_rows.sum(axis=1)
m = rowsum > 0
if m.sum():
    cy = (rowsum * ys)[m].sum() / rowsum[m].sum()
    print(f"BOTTOM stroke y-centroid: {cy:.2f} (rows {ys[m].min()}..{ys[m].max()})")

# mapping fit (family: ay=0, sy=0.955556; fit ax from left; sx from left+right; bottom cross-check)
left_c, right_c, top_c = cx, 0, cy
# recompute right properly with centroid
rc_x = None
cols = redness[200:350, 880:920]
xs = np.arange(880, 920)
colsum = cols.sum(axis=0)
if (colsum > 0).sum():
    rc_x = (colsum * xs)[colsum > 0].sum() / colsum[colsum > 0].sum()
    right_c = rc_x
ax = left_c - 0.961231 * 42
sx = (right_c - left_c) / (918 - 42)
print(f"\nFIT: ax={ax:.3f}  sx={sx:.6f}  (family sx=0.961231, sy=0.955556)")
print(f"ax variants: 020={18.628:.3f} 021={18.13:.3f} 022={17.72:.3f}")

# badge bbox: yellow pixels (FDFD96-class) in top right
yellow = (r > 200) & (g > 200) & (b < 190) & (b > 100)
ys_, xs_ = np.where(yellow)
if len(xs_):
    # restrict to badge region (x>820, y<110)
    m = (xs_ > 820) & (xs_ < 920) & (ys_ > 30) & (ys_ < 110)
    if m.sum():
        bx0, bx1, by0, by1 = xs_[m].min(), xs_[m].max(), ys_[m].min(), ys_[m].max()
        print(f"badge yellow bbox: x {bx0}..{bx1} (cx {(bx0+bx1)/2:.1f}), y {by0}..{by1} (cy {(by0+by1)/2:.1f}), d~{(bx1-bx0+by1-by0)/2}")
