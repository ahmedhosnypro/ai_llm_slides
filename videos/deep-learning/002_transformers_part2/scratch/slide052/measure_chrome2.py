#!/usr/bin/env python3
"""Chrome landmarks v2 for slide_052.jpg: looser red-border detection with
weighted centroids; verify slide_002 mapping on THIS frame."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
# looser red ink mask (border is thin + JPEG-soft)
red = (r > 100) & (r - g > 60) & (r - b > 60)

# vertical border lines: count red pixels per column over rows 120..400 (clean band,
# avoids callouts/bars), require long run
band = red[120:400, :]
colcnt = band.sum(axis=0)
cands = [(x, int(colcnt[x])) for x in range(W) if colcnt[x] > 200]
print("tall-ish red columns (rows120-400):", cands)

# For each side take weighted centroid over the connected peak
def centroid_x(xs_range):
    xs = np.arange(*xs_range)
    w = colcnt[xs_range[0]:xs_range[1]].astype(float)
    if w.sum() == 0:
        return None
    return float((xs * w).sum() / w.sum())

left = centroid_x((50, 70)) if colcnt[50:70].sum() else None
right = centroid_x((890, 915)) if colcnt[890:915].sum() else None
print("left border centroid x:", left, " right:", right)

# top border: rows with red over a wide x band that avoids badge (x 200..800)
rowcnt = red[:, 200:800].sum(axis=1)
topc = [(y, int(rowcnt[y])) for y in range(25, 60) if rowcnt[y] > 300]
print("top border rows:", topc)
if topc:
    ys = np.arange(25, 60)
    wv = rowcnt[25:60].astype(float)
    ty = float((ys * wv).sum() / wv.sum())
else:
    ty = None
print("top border centroid y:", ty)

# bottom red stroke: near letterbox top (rows 505..518)
botc = [(y, int(rowcnt[y])) for y in range(500, 519) if rowcnt[y] > 200]
print("bottom border rows:", botc)
if botc:
    ys = np.arange(500, 519)
    wv = rowcnt[500:519].astype(float)
    by = float((ys * wv).sum() / wv.sum())
else:
    by = None
print("bottom border centroid y:", by)

# badge cross-check through slide_002 mapping
def to_slide(fx, fy):
    return (fx - 18.63) / 0.96123, fy / 0.95556

bx, byy = 875.5, 69.5
sx, sy = to_slide(bx, byy)
print(f"badge center -> slide ({sx:.1f},{sy:.1f}) vs house (893,71): d=({sx-893:+.1f},{sy-71:+.1f})")

# verify landmarks map to slide chrome values
if left is not None:
    print(f"left {left} -> slide {to_slide(left,0)[0]:.1f} (expect 42)")
if right is not None:
    print(f"right {right} -> slide {to_slide(right,0)[0]:.1f} (expect 918.5)")
if ty is not None:
    print(f"top {ty} -> slide {to_slide(0,ty)[1]:.1f} (expect 45)")
if by is not None:
    print(f"bottom {by} -> slide {to_slide(0,by)[1]:.1f} (expect 539)")
