#!/usr/bin/env python3
"""m6.py — dot box rect, pale-yellow cell stacks, pale-blue sigma boxes, white W boxes."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(m, min_len=2):
    out = []; s = None
    for i, v in enumerate(m):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_len: out.append((s, i - 1))
            s = None
    if s is not None and len(m) - s >= min_len: out.append((s, len(m) - 1))
    return out

# Dot Product box fill (216,200,184)
dot = (np.abs(R - 216) < 10) & (np.abs(G - 200) < 10) & (np.abs(B - 184) < 10)
print("== dot-fill rows x[240,340]:")
dz = dot[240:500, 240:340]
for s, e in runs(dz.sum(axis=1) > 25, 4):
    band = dz[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 10, 4)
    print(f"  y[{240+s},{240+e}] x-runs:", [(240+r0, 240+r1) for r0, r1 in rr][:6])

# pale-yellow cells #FFF6BF
py = (R > 240) & (G > 232) & (B > 150) & (B < 225) & (R - B > 35)
print("== pale-yellow clusters (panel1 zone x[110,700] y[230,500]):")
sub = np.zeros_like(py); sub[230:500, 110:700] = py[230:500, 110:700]
from scipy import ndimage
lab, n = ndimage.label(sub)
cl = []
for sl in ndimage.find_objects(lab):
    cnt = sub[sl].sum()
    if cnt >= 12:
        cl.append((sl[1].start, sl[0].start, sl[1].stop-1, sl[0].stop-1, int(cnt)))
cl.sort(key=lambda t: (t[1], t[0]))
for c in cl[:40]: print("   ", c)

# pale blue #C9DFF5 sigma boxes
pb = (np.abs(R - 201) < 25) & (np.abs(G - 223) < 22) & (np.abs(B - 245) < 18) & (B - R > 22)
print("== pale-blue clusters:")
sub = np.zeros_like(pb); sub[130:500, 100:960] = pb[130:500, 100:960]
lab, n = ndimage.label(sub)
cl = []
for sl in ndimage.find_objects(lab):
    cnt = sub[sl].sum()
    if cnt >= 25:
        cl.append((sl[1].start, sl[0].start, sl[1].stop-1, sl[0].stop-1, int(cnt)))
cl.sort(key=lambda t: -t[4])
for c in cl[:20]: print("   ", c)

# white boxes (near pure white) in panel1 left zone
wh = (R > 246) & (G > 246) & (B > 246)
print("== white rows x[165,265] y[280,400] (W^k boxes?):")
wz = wh[280:400, 165:265]
for s, e in runs(wz.sum(axis=1) > 15, 3):
    band = wz[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 3, 3)
    print(f"  y[{280+s},{280+e}] x-runs:", [(165+r0, 165+r1) for r0, r1 in rr][:8])
