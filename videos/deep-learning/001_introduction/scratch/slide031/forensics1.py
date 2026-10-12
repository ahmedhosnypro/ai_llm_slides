#!/usr/bin/env python3
"""PIL forensics on slide_031.jpg (960x540, 1px = 1pt). Pure measurement, no vision."""
from PIL import Image
import numpy as np
from collections import Counter

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"size {W}x{H}")
lum = a.mean(axis=2)

def modal(box, mask=None):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    if mask == "dark":
        sub = sub[sub.mean(axis=1) < 120]
    if mask == "red":
        sub = sub[(sub[:, 0] > 100) & (sub[:, 1] < 90) & (sub[:, 2] < 90)]
    if mask == "blue":
        sub = sub[(sub[:, 2] > 100) & (sub[:, 0] < 90)]
    if len(sub) == 0:
        return None, 0
    c = Counter(map(tuple, sub))
    return c.most_common(1)[0], len(sub)

def ink_bbox(box, thr=200):
    x0, y0, x1, y1 = box
    sub = lum[y0:y1, x0:x1]
    ys, xs = np.where(sub < thr)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

# ---- 1. chrome panel border: scan for the red border lines
red = (a[:, :, 0] > 120) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80)
col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
strong_cols = [x for x in range(W) if col_red[x] > 100]
strong_rows = [y for y in range(H) if row_red[y] > 100]
print("strong red cols:", strong_cols[:12], "...", strong_cols[-6:] if strong_cols else "")
print("strong red rows:", strong_rows[:12], "...", strong_rows[-6:] if strong_rows else "")

# ---- 2. black bottom bar
dark_rows = [y for y in range(H) if (lum[y] < 60).sum() > 500]
print("dark bar rows:", dark_rows[:4], dark_rows[-4:] if dark_rows else "")

# ---- 3. title: ink band y 55..130
tb = ink_bbox((100, 50, 880, 130), thr=200)
print("title ink bbox:", tb)
if tb:
    print("title modal (red):", modal((tb[0], tb[1], tb[2] + 1, tb[3] + 1), "red"))
    # cap-top / baseline: rows with ink
    sub = lum[tb[1]:tb[3] + 1, tb[0]:tb[2] + 1]
    prof = (sub < 200).sum(axis=1)
    rows = [i for i, v in enumerate(prof) if v > 0]
    print("title ink rows(first,last):", rows[0] + tb[1], rows[-1] + tb[1])

# ---- 4. content box: search for blue border lines in y 120..380
blue = (a[:, :, 2] > 110) & (a[:, :, 0] < 90) & (a[:, :, 1] < 90)
col_blue = blue[120:380].sum(axis=0)
row_blue = blue.sum(axis=1)
strong_bcols = [x for x in range(W) if col_blue[x] > 80]
print("strong blue cols (y120-380):", strong_bcols)
# horizontal blue border rows across x 100..880
row_blue_band = blue[:400, 100:880].sum(axis=1)
strong_brows = [y for y in range(400) if row_blue_band[y] > 300]
print("strong blue rows (x100-880, y<400):", strong_brows)

# ---- 5. inside content box: find text ink bands
if strong_bcols and strong_brows:
    cbx0, cbx1 = strong_bcols[0], strong_bcols[-1]
    cby0, cby1 = strong_brows[0], strong_brows[-1]
    print("content box:", cbx0, cby0, cbx1, cby1)
    inner = lum[cby0 + 4:cby1 - 3, cbx0 + 4:cbx1 - 3]
    prof = (inner < 180).sum(axis=1)
    bands = []
    y = 0
    n = len(prof)
    while y < n:
        if prof[y] > 2:
            y2 = y
            while y2 < n - 1 and prof[y2 + 1] > 0:
                y2 += 1
            bands.append((y + cby0 + 4, y2 + cby0 + 4))
            y = y2 + 1
        else:
            y += 1
    print("text bands in content box (abs y ranges):")
    for b in bands:
        seg = lum[b[0]:b[1] + 1, cbx0 + 4:cbx1 - 3]
        xs = np.where((seg < 180).any(axis=0))[0]
        print(f"  y {b[0]}..{b[1]} (h {b[1]-b[0]+1})  x {cbx0+4+xs.min()}..{cbx0+4+xs.max()}")
        # modal dark color
        yy0, yy1 = b
        print("    modal dark:", modal((cbx0 + 4, yy0, cbx1 - 3, yy1 + 1), "dark"))
    # bullet glyphs: leftmost ink columns per band
