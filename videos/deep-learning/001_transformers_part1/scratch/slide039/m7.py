#!/usr/bin/env python3
"""m7.py — W^q branch, bottom X row cells, green-stroked boxes census, sticker angle."""
from PIL import Image
import numpy as np
from collections import Counter

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

def census(name, x0, y0, x1, y1, top=6):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    q = (sub // 8 * 8)
    print(name, Counter(map(tuple, q)).most_common(top))

# green-stroked boxes at x200-224
census("greenbox1", 199, 289, 226, 310, 8)
# bottom X row zone
census("bottomrow-cell1", 262, 456, 320, 480, 8)
census("bottomrow-cell2", 320, 456, 375, 480, 6)
# pink highlight mask in bottom row
pink = (np.abs(R - 249) < 14) & (np.abs(G - 213) < 22) & (np.abs(B - 229) < 22) & (R - G > 18)
print("pink in bottom row y[450,485] x[240,500]:")
pz = pink[450:485, 240:500]
for s, e in runs(pz.sum(axis=1) > 5, 2):
    band = pz[s:e+1, :]
    rr = runs(band.sum(axis=0) > 1, 2)
    print(f"  y[{450+s},{450+e}]:", [(240+r0, 240+r1) for r0, r1 in rr][:8])
# green strokes in bottom row
green = (G - R > 25) & (G - B > 25) & (G > 90) & (G < 220)
gz = green[450:485, 240:520]
print("green strokes bottom row:")
for s, e in runs(gz.sum(axis=1) > 3, 2):
    band = gz[s:e+1, :]
    rr = runs(band.sum(axis=0) > 0, 2)
    print(f"  y[{450+s},{450+e}]:", [(240+r0, 240+r1) for r0, r1 in rr][:12])

# W^q red branch zone
census("wq-branch", 275, 400, 320, 450, 8)
# left X box zone fine scan: green X letters
print("green clusters x[120,200] y[270,430]:")
from scipy import ndimage
sub = np.zeros_like(green); sub[270:430, 120:200] = green[270:430, 120:200]
lab, n = ndimage.label(sub)
for sl in ndimage.find_objects(lab):
    cnt = sub[sl].sum()
    if cnt >= 5:
        print("   ", (sl[1].start, sl[0].start, sl[1].stop-1, sl[0].stop-1, int(cnt)))
# mint (W_k box) fill extent per row
mint = (np.abs(R - 232) < 10) & (np.abs(G - 248) < 8) & (np.abs(B - 232) < 12) & (G - R > 8)
print("mint rows x[120,200]:")
mz = mint[230:500, 120:200]
for s, e in runs(mz.sum(axis=1) > 12, 3):
    band = mz[s:e+1, :]
    rr = runs(band.sum(axis=0) > 3, 3)
    print(f"  y[{230+s},{230+e}]:", [(120+r0, 120+r1) for r0, r1 in rr][:8])
