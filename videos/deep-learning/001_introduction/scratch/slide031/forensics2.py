#!/usr/bin/env python3
"""Forensics pass 2: exact box borders, text lines, matrix box, colors."""
from PIL import Image
import numpy as np
from collections import Counter

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
lum = a.mean(axis=2)

def modal(box, sel=None):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    if sel == "dark": sub = sub[sub.mean(axis=1) < 120]
    elif sel == "red": sub = sub[(sub[:,0] > 100) & (sub[:,1] < 90) & (sub[:,2] < 90)]
    elif sel == "blueish": sub = sub[(sub[:,2] - np.maximum(sub[:,0], sub[:,1])) > 35]
    if len(sub) == 0: return None, 0
    return Counter(map(tuple, sub)).most_common(1)[0], len(sub)

def vertical_line_scan(y0, y1, minrun=150):
    """columns whose pixels in [y0,y1) are mostly non-background (non gray/white)"""
    out = []
    for x in range(W):
        col = a[y0:y1, x]
        nonbg = ((np.abs(col[:,0]-233) > 40) | (np.abs(col[:,1]-233) > 40)).sum()
        if nonbg > minrun: out.append(x)
    return out

# 1. The vertical red lines at 58 and 841: where do they run?
for x in (58, 841, 842):
    col = a[:, x]
    red = (col[:,0] > 120) & (col[:,1] < 80) & (col[:,2] < 80)
    ys = np.where(red)[0]
    print(f"red col {x}: rows {ys.min()}..{ys.max()} count {red.sum()}")
# background modal
print("bg modal (60,400,70,120):", modal((60, 400, 70, 120)))
print("bg modal (200,40,300,42):", modal((200, 40, 300, 42)))

# 2. content box edges: scan y 140..350 for vertical border lines (any strong color)
vl = vertical_line_scan(140, 350, 150)
print("vertical non-bg cols in y140-350:", vl)

# 3. horizontal border lines: rows where many pixels differ from bg in x 100..900
for y in range(115, 540):
    row = a[y, 100:900]
    nonbg = ((np.abs(row[:,0]-233) > 45) | (np.abs(row[:,1]-233) > 45)).sum()
    if nonbg > 600:
        print("h-line row", y, "nonbg", nonbg, "modal:", modal((100, y, 900, y+1)))

# 4. text bands inside presumed content box y 150..360
inner = lum[145:360, 100:900]
prof = (inner < 190).sum(axis=1)
bands = []
y = 0
n = len(prof)
while y < n:
    if prof[y] > 2:
        y2 = y
        while y2 < n-1 and prof[y2+1] > 0: y2 += 1
        bands.append((y+145, y2+145)); y = y2+1
    else: y += 1
print("text bands y145-360:")
for b in bands:
    seg = lum[b[0]:b[1]+1, 100:900]
    xs = np.where((seg < 190).any(axis=0))[0]
    x0, x1 = 100+xs.min(), 100+xs.max()
    print(f"  y {b[0]}..{b[1]} (h {b[1]-b[0]+1}) x {x0}..{x1}")
    print("    modal dark:", modal((x0, b[0], x1+1, b[1]+1), "dark"))
    print("    modal blueish:", modal((x0, b[0], x1+1, b[1]+1), "blueish"))
    print("    modal red:", modal((x0, b[0], x1+1, b[1]+1), "red"))
