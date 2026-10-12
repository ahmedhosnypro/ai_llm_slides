#!/usr/bin/env python3
"""Precise region measurements for slide_017.jpg via connected components + scanlines."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def cc_bboxes(mask, min_area=80):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_area: continue
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs)))
    return out

def near(target, tol):
    return np.abs(a - np.array(target)).max(axis=2) <= tol

def report(name, target, tol, region=None, min_area=80, max_results=14):
    m = near(target, tol)
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; m = mm
    bbs = sorted(cc_bboxes(m, min_area), key=lambda b: -b[4])[:max_results]
    print(f"{name}: " + " ; ".join(f"({x0},{y0})-({x1},{y1}) n={n}" for x0, y0, x1, y1, n in bbs))
    return bbs

# --- the five cascade cards: use scanline-derived cores
report("card h1 (salmon F08C96)", (240, 140, 150), 14)
report("card h2 (lavender C5C1F4)", (197, 193, 244), 12)
report("card h3 (pale yellow F8FF9A)", (248, 255, 154), 14)
report("card h4 (pale mint D4FFE5)", (212, 255, 229), 12)
report("card h5 (peach F7E2CD)", (247, 226, 205), 12)

# --- black pills (h tags) inside card zone
report("black pills", (25, 25, 25), 45, region=(100, 150, 920, 520), min_area=150)

# --- gold W boxes
report("gold F5C242", (245, 194, 66), 35, min_area=100)

# --- concat bar: find its exact extent. scan rows 118..150 for the bar's left/right edge
# bar interior: label zone + 5 segments. Use "not background" run analysis per row
print("\n-- concat bar rows (y=120..152) full-width nonbg runs (len>=30) --")
for y in range(118, 154, 2):
    row = a[y]
    sat = row.max(axis=1) - row.min(axis=1)
    dark = row.max(axis=1) < 150
    nb = ~((sat < 24) & ~dark)
    runs = []; s = None
    for x in range(W):
        if nb[x] and s is None: s = x
        elif not nb[x] and s is not None:
            if x - s >= 30: runs.append((s, x - 1))
            s = None
    if s is not None and W - s >= 30: runs.append((s, W - 1))
    print(f"y={y}: {runs}")

# --- top pipeline: embedding strip zone. y 45..75, x 330..480
print("\n-- top strip zone rows y=45..75 (x330..480), runs len>=6 --")
for y in range(45, 76, 3):
    row = a[y, 330:480]
    med_run = []
    s = None
    for x in range(150):
        r, g, b = row[x]
        sat = max(r, g, b) - min(r, g, b)
        if sat >= 25 and s is None: s = x
        elif sat < 25 and s is not None:
            if x - s >= 6:
                med = np.median(row[s:x], axis=0).astype(int)
                med_run.append((s + 330, x - 1 + 330, "#%02X%02X%02X" % tuple(med)))
            s = None
    if s is not None:
        med = np.median(row[s:], axis=0).astype(int)
        med_run.append((s + 330, 149 + 330, "#%02X%02X%02X" % tuple(med)))
    print(f"y={y}: {med_run}")

# --- LT box zone y 80..118 x 250..520: border+fill
print("\n-- LT box: vertical border columns (dark-ish) in y95..110 --")
sub = a[95:110, 250:520]
for x in range(sub.shape[1]):
    col = sub[:, x]
    if (col.max(axis=1) < 190).sum() >= 12:
        print(f"  col x={x+250}")
