#!/usr/bin/env python3
"""Refined landmark measurement for slide_035.jpg: red border cols/rows, badge,
precise ink bboxes per text line (cap vs descender), letterbox extent."""
from PIL import Image
import numpy as np

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_035.jpg"
im = Image.open(P).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# loose red detector (JPEG-smeared thin border)
red = (R > 120) & (R - G > 60) & (R - B > 60)

# ---- vertical border columns: count red px per column over rows 60..500 (well inside)
sub_rows = slice(60, 500)
col_counts = red[sub_rows, :].sum(axis=0)
border_cols = [x for x in range(W) if col_counts[x] > 200]
print("vertical red border cols (count>200 over rows60..500):", border_cols)
for x in border_cols:
    ys = np.where(red[:, x])[0]
    print(f"  col {x}: red rows {ys.min()}..{ys.max()} n={col_counts[x]}")

# ---- horizontal border rows: count red px per row over cols 100..860
sub_cols = slice(100, 860)
row_counts = red[:, sub_cols].sum(axis=1)
border_rows = [y for y in range(H) if row_counts[y] > 300]
print("horizontal red border rows (count>300 over cols100..860):", border_rows)
for y in border_rows:
    xs = np.where(red[y, :])[0]
    print(f"  row {y}: red cols {xs.min()}..{xs.max()} n={row_counts[y]}")

# ---- title red band precise bbox (exclude border rows/cols)
red_text = red.copy()
for y in border_rows:
    red_text[y, :] = False
for x in border_cols:
    red_text[:, x] = False
ys, xs = np.where(red_text)
# exclude badge area (x>840, y<100)
keep = ~((xs > 840) & (ys < 100))
ys, xs = ys[keep], xs[keep]
print(f"TITLE red text bbox: x {xs.min()}..{xs.max()} (w {xs.max()-xs.min()+1})  y {ys.min()}..{ys.max()} (h {ys.max()-ys.min()+1})  cx {(xs.min()+xs.max())/2:.1f}")
# row histogram of title to find baseline vs descender (cap top, x-height)
rows_hist = red_text.sum(axis=1)
for y in range(ys.min(), ys.max() + 1):
    if rows_hist[y] > 0:
        pass
prof = [(y, int(rows_hist[y])) for y in range(ys.min(), ys.max() + 1)]
print("title row profile (y,count):", prof)

# ---- blue text precise per-line bboxes
blue = (B > 120) & (B - R > 60) & (B - G > 60)
ys, xs = np.where(blue)
rows_sorted = sorted(set(ys))
bands = []
start = prev = rows_sorted[0]
for y in rows_sorted[1:]:
    if y - prev > 4:
        bands.append((start, prev)); start = y
    prev = y
bands.append((start, prev))
print("\nBLUE line bands:")
for (y0, y1) in bands:
    m = (ys >= y0) & (ys <= y1)
    if m.sum() < 20:
        continue
    lx, ly = xs[m], ys[m]
    # column clusters (word gaps)
    xs_line = np.sort(lx)
    clusters = []
    cs = cp = xs_line[0]
    for x in xs_line[1:]:
        if x - cp > 10:
            clusters.append((cs, cp)); cs = x
        cp = x
    clusters.append((cs, cp))
    print(f"  y {y0}..{y1} x {lx.min()}..{lx.max()}  clusters={clusters}")
    # row profile to find descender
    rh = blue.sum(axis=1)
    prof = [(y, int(rh[y])) for y in range(y0, y1 + 1)]
    print(f"    profile: {prof}")
