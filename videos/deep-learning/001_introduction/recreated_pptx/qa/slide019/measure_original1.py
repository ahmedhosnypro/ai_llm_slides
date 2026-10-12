#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_019.jpg (960x540, 1px=1pt).
Pass 1: chrome bands, title ink, inner white panel, training ellipse, node boxes,
dashed container, vertical box, annotation box, bottom bands."""
from PIL import Image
import numpy as np

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")
a = np.asarray(IM).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        print(f"{label}: EMPTY")
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(f"{label}: x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) center=({(x0+x1)/2:.1f},{(y0+y1)/2:.1f})")
    return (x0, x1, y0, y1)

# ---- chrome ----
gray = (abs(r-233) < 14) & (abs(g-233) < 14) & (abs(b-231) < 16)
band = gray[80:520]
cols = np.where(band.sum(axis=0) > 300)[0]
print("chrome gray panel cols:", cols.min(), "..", cols.max())
rowsL = np.where(gray[:, 50:140].sum(axis=1) > 60)[0]
print("chrome gray rows (left band):", rowsL.min(), "..", rowsL.max())

red = (r > 120) & (g < 110) & (b < 110)
print("red rows at bottom (x500 col):", [y for y in range(500, H) if red[y, 500]])
black = (r < 60) & (g < 60) & (b < 60)
brows = np.where(black[:, 100].sum(axis=1) if False else black[:, 100])[0]
brows2 = np.where(black[:, 100])[0]
print("black@x100 rows:", brows2.min(), "..", brows2.max())
colsB = np.where(black[528])[0]
print("black@y528 cols:", (colsB.min(), colsB.max()) if len(colsB) else "none")
grayband = (abs(r-204) < 30) & (abs(g-204) < 30) & (abs(b-204) < 30)
gb = np.where(grayband[510, :])[0]
print("gray#cccc@y510 cols:", (gb.min(), gb.max()) if len(gb) else "none")
grows = np.where(grayband[:, 500])[0]
print("gray#cccc@x500 rows:", (grows.min(), grows.max()) if len(grows) else "none")

# ---- title ink (dark red on white, top region) ----
title_red = (r > 140) & (r < 230) & (g < 80) & (b < 80)
tmask = np.zeros_like(title_red)
tmask[50:110, 60:900] = title_red[50:110, 60:900]
tb = bbox(tmask, "title ink")
if tb:
    # column profile for cap-height estimation
    ys, xs = np.where(tmask)
    print("  title rows histogram:", np.bincount(ys)[50:110].nonzero()[0] + 50)

# ---- inner white panel (white surrounded by chrome gray / red border) ----
white = (r > 240) & (g > 240) & (b > 240)
inner = np.zeros_like(white)
inner[100:470, 60:900] = white[100:470, 60:900]
# find panel edges: scan rows/cols where long white runs exist
rowsum = white[:, 400:500].sum(axis=1)
wr = np.where(rowsum > 80)[0]
print("white@x400-500 rows:", wr.min(), "..", wr.max())
colsum = white[300:320, :].sum(axis=0)
wc = np.where(colsum > 15)[0]
print("white@y300-320 cols:", wc.min(), "..", wc.max())

# red frame of inner panel: vertical strokes
panel_red = np.zeros_like(red)
panel_red[80:480, :] = red[80:480, :]
colprof = panel_red.sum(axis=0)
strong_cols = [x for x in range(40, 930) if colprof[x] > 250]
print("inner-panel red vertical strokes cols:", strong_cols)
rowprof = panel_red[:, 60:900].sum(axis=1)
strong_rows = [y for y in range(80, 500) if rowprof[y] > 500]
print("inner-panel red horizontal strokes rows:", strong_rows)

# ---- training ellipse ----
# tan fill ~ (230,199,156)? sample around (425,135)
print("sample ellipse fill @(425,135):", a[135, 425], "@(430,140):", a[140, 430])
peachish = (abs(r-235) < 35) & (abs(g-200) < 35) & (abs(b-160) < 45)
em = np.zeros_like(peachish)
em[100:170, 360:500] = peachish[100:170, 360:500]
bbox(em, "training ellipse fill")

# ---- node boxes: sample fills at known-ish spots ----
spots = {
    "input_samples": (115, 236), "pre_processing": (240, 228), "feature_extraction": (360, 236),
    "feature_selection": (475, 236), "classification": (580, 236), "predicted_labels": (690, 236),
    "prediction_error": (765, 240), "samples_labels": (855, 236),
}
for k, (x, y) in spots.items():
    print(f"fill {k} @({x},{y}):", a[y, x])

# ---- annotation box (pale green bottom center) ----
ag = (abs(r-232) < 25) & (abs(g-245) < 20) & (abs(b-233) < 25)
am = np.zeros_like(ag)
am[340:400, 200:800] = ag[340:400, 200:800]
bbox(am, "annotation box fill")
print("sample annotation @(500,365):", a[365, 500])
