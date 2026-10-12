#!/usr/bin/env python3
"""Targeted stroke scans: right border, top border; then fit mapping."""
from PIL import Image
import numpy as np

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(p).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
red = (R - G > 40) & (R - B > 40) & (R > 100)

# right border: columns 880..920, count red over y 110..510
for thr in (100, 60, 40, 20, 10):
    colprof = red[110:510, :].sum(axis=0)
    cand = [x for x in range(880, 920) if colprof[x] >= thr]
    if cand:
        ws = np.array([colprof[x] for x in cand], float)
        c = float((np.array(cand) * ws).sum() / ws.sum())
        print(f"RIGHT stroke thr={thr}: cols {cand} center {c:.2f}")
        break
    else:
        print(f"RIGHT stroke thr={thr}: none")

# top border: rows 30..60, count red over x 70..890
for thr in (100, 60, 40, 20, 10):
    rowprof = red[:, 70:890].sum(axis=1)
    cand = [y for y in range(30, 60) if rowprof[y] >= thr]
    if cand:
        ws = np.array([rowprof[y] for y in cand], float)
        c = float((np.array(cand) * ws).sum() / ws.sum())
        print(f"TOP stroke thr={thr}: rows {cand} center {c:.2f}")
        break
    else:
        print(f"TOP stroke thr={thr}: none")

# left stroke redness check with loose mask too
colprof = red[110:510, :].sum(axis=0)
cand = [x for x in range(40, 75) if colprof[x] >= 20]
ws = np.array([colprof[x] for x in cand], float)
c = float((np.array(cand) * ws).sum() / ws.sum())
print(f"LEFT stroke loose: cols {cand} center {c:.2f}")
cand = [x for x in range(880, 920) if colprof[x] >= 20]
if cand:
    ws = np.array([colprof[x] for x in cand], float)
    c = float((np.array(cand) * ws).sum() / ws.sum())
    print(f"RIGHT stroke loose: cols {cand} center {c:.2f}")
