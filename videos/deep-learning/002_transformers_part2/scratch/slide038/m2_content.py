#!/usr/bin/env python3
"""Slide 038 — precise content regions: borders, title, defbox lines, panel, rows."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

# looser red mask for thin JPEG-softened borders
red = (R > 110) & (G < 110) & (B < 110)

# --- chrome borders, per-column/row probe
print("== chrome borders ==")
for x in range(50, 70):
    f_ = red[150:500, x].mean()
    if f_ > 0.5:
        print("left col", x, f"frac={f_:.2f}", "-> slide x", invx(x))
for x in range(895, 915):
    f_ = red[150:500, x].mean()
    if f_ > 0.5:
        print("right col", x, f"frac={f_:.2f}", "-> slide x", invx(x))
for y in range(35, 55):
    f_ = red[y, 200:800].mean()
    if f_ > 0.5:
        print("top row", y, f"frac={f_:.2f}", "-> slide y", invy(y))
for y in range(505, 519):
    f_ = red[y, 200:800].mean()
    if f_ > 0.5:
        print("bottom row", y, f"frac={f_:.2f}", "-> slide y", invy(y))

# --- title ink precise (row profile)
print("== title ==")
seg = (R[55:115, 150:850] > 130) & (G[55:115, 150:850] < 120) & (B[55:115, 150:850] < 120)
rows = np.where(seg.sum(axis=1) > 2)[0]
cols = np.where(seg.sum(axis=0) > 0)[0]
print("ink x", cols.min() + 150, cols.max() + 150, "y", rows.min() + 55, rows.max() + 55,
      "-> slide x", invx(cols.min() + 150), invx(cols.max() + 150),
      "y", invy(rows.min() + 55), invy(rows.max() + 55))
prof = seg.sum(axis=1)
for i, v in enumerate(prof):
    if v:
        print("  row", i + 55, v)

# --- defbox: blue border rect + text lines
print("== defbox ==")
blue = (B > 110) & (R < 110) & (G < 110)
seg = blue[95:245, 60:900]
rows = np.where(seg.sum(axis=1) > 3)[0]
# border rows = rows with very high count (long horizontal lines)
border_rows = [r + 95 for r in range(len(rows)) if seg[r].sum() > 400]
text_rows = [r + 95 for r in range(len(rows)) if 3 < seg[r].sum() <= 400]
print("border rows:", border_rows)
# group text rows
groups = []
cur = [text_rows[0]] if text_rows else []
for r in text_rows[1:]:
    if r - cur[-1] <= 2:
        cur.append(r)
    else:
        groups.append(cur); cur = [r]
if cur: groups.append(cur)
for g in groups:
    y0, y1 = g[0], g[-1]
    band = blue[y0:y1 + 1, 60:900]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"  text band y {y0}..{y1} x {cols.min()+60}..{cols.max()+60} -> slide y {invy(y0)}..{invy(y1)} x {invx(cols.min()+60)}..{invx(cols.max()+60)}")
# defbox border cols
segc = blue[100:240, 60:900]
colsum = segc.sum(axis=0)
bcols = [c + 60 for c in range(len(colsum)) if colsum[c] > 100]
print("border cols:", bcols)

# --- diagram panel red border
print("== diagram panel ==")
seg = red[245:519, 40:920]
rowsum = seg.sum(axis=1)
long_rows = [r + 245 for r in range(len(rowsum)) if rowsum[r] > 500]
print("long red rows:", long_rows)
colsum = seg.sum(axis=0)
long_cols = [c + 40 for c in range(len(colsum)) if colsum[c] > 150]
print("long red cols:", long_cols)
