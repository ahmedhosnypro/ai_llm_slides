#!/usr/bin/env python3
"""measure1.py — slide_044 original-frame forensics, pass 1: chrome landmarks,
title, inner content frame, black bar, gray top line, note box, grid bboxes."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_044.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

R, G, B = a[..., 0], a[..., 1], a[..., 2]

# --- red mask (C00000-ish border/title) ---
red = (R > 120) & (G < 90) & (B < 90) & (R - G > 60) & (R - B > 60)

def runs(mask_1d, min_len=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            if p - s + 1 >= min_len:
                out.append((s, p))
            s = p = v
    if p - s + 1 >= min_len:
        out.append((s, p))
    return out

# red column profile: columns with many red pixels -> vertical border strokes
colcnt = red.sum(axis=0)
rowcnt = red.sum(axis=1)
print("RED col runs (count>=100):", [(s, e, int(colcnt[s:e+1].max())) for s, e in runs(colcnt >= 100)])
print("RED row runs (count>=100):", [(s, e, int(rowcnt[s:e+1].max())) for s, e in runs(rowcnt >= 100)])

# --- corner / canvas colors ---
for (x, y, label) in [(5, 5, "top-left corner"), (480, 3, "top edge mid"), (5, 270, "left edge mid"),
                      (955, 270, "right edge mid"), (20, 200, "left margin"), (940, 300, "right margin"),
                      (480, 20, "top band"), (480, 500, "bottom band"), (300, 500, "bottom band 2")]:
    print(f"px({x},{y}) {label}: {tuple(a[y, x])}")

# --- black bar at bottom ---
darkrow = ((R < 70) & (G < 70) & (B < 70)).mean(axis=1)
print("rows with >80% dark:", runs(darkrow > 0.8))

# --- top gray line ---
for y in range(0, 8):
    row = a[y]
    print(f"row {y}: mean {row.mean(axis=0).round(1)} min {row.min(axis=0)} max {row.max(axis=0)}")

# --- title ink bbox (red pixels, y 50..115) ---
tmask = red.copy()
tmask[:50] = False
tmask[115:] = False
ys, xs = np.where(tmask)
if len(xs):
    print(f"TITLE red ink bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} (w {xs.max()-xs.min()+1} h {ys.max()-ys.min()+1})")

# --- inner content frame: red rect inside y 110..420 ---
imask = red.copy()
imask[:110] = False
imask[420:] = False
# exclude title band columns from col profile: look at long vertical strokes
icol = imask.sum(axis=0)
irow = imask.sum(axis=1)
print("INNER red col runs (count>=150):", [(s, e) for s, e in runs(icol >= 150)])
print("INNER red row runs (count>=300):", [(s, e) for s, e in runs(irow >= 300)])

# --- note box: blue border (4472C4-ish: b > r, b > 120, r in 40..120) ---
blue = (B > 130) & (B - R > 40) & (B - G > 30) & (R < 160)
bmask = blue.copy()
bmask[:380] = False
bcol = bmask.sum(axis=0)
brow = bmask.sum(axis=1)
print("NOTEBOX blue col runs (count>=40):", [(s, e) for s, e in runs(bcol >= 40)])
print("NOTEBOX blue row runs (count>=150):", [(s, e) for s, e in runs(brow >= 150)])

# --- grids: dark pixels inside inner frame ---
dark = (R < 90) & (G < 90) & (B < 90)
g = dark.copy()
g[:150] = False
g[420:] = False
gcol = g.sum(axis=0)
grow = g.sum(axis=1)
print("GRID dark col runs (count>=120):", [(s, e) for s, e in runs(gcol >= 120)])
print("GRID dark row runs (count>=120):", [(s, e) for s, e in runs(grow >= 120)])

# grid cell fills: modal colors of grid regions
def modal(x0, x1, y0, y1, label):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    # quantize to /16 bins to beat JPEG noise
    q = (reg // 16) * 16
    vals, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:5]
    print(f"modal {label}:", [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order])

