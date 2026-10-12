#!/usr/bin/env python3
# m14_asset.py — read the certified recolor asset (600dpi) along both column centers
# to get exact box boundaries under the highlights; asset px -> build pt: pt = origin + px*0.12
import numpy as np
from PIL import Image

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/slide015_fig1_color.png"
im = np.asarray(Image.open(A).convert("RGB"), dtype=np.float64)
print("asset size", im.shape)

def runs(a, x, y0, y1, tol=24):
    out, cur, start = [], None, y0
    for y in range(y0, y1):
        c = a[y, x]
        if cur is None: cur, start = c, y; continue
        if np.abs(c - cur).sum() > tol * 3:
            out.append((start, y - 1, cur)); cur, start = c, y
        else:
            cur = 0.7 * cur + 0.3 * c
    out.append((start, y1 - 1, cur))
    return [(s, e, "%02X%02X%02X" % tuple(int(round(q)) for q in c)) for s, e, c in out if e - s >= 2]

# encoder column center: build pt x 686.4 -> u = (686.4-575)/0.12 = 928
# decoder column center: build pt x 785.3 -> u = 1752
# y range of interest: pt 250..430 -> v 1192..2692
print("== ASSET encoder column u=928 (pt x 686.4), v 1192..2692 ==")
for s, e, c in runs(im, 928, 1192, 2692):
    print(f"  v {s}..{e} (pt y {107 + s * 0.12:.1f}..{107 + e * 0.12:.1f}) {c}")
print("== ASSET decoder column u=1752 (pt x 785.2), v 500..2692 ==")
for s, e, c in runs(im, 1752, 500, 2692):
    print(f"  v {s}..{e} (pt y {107 + s * 0.12:.1f}..{107 + e * 0.12:.1f}) {c}")

# horizontal runs through the two highlight bands to find the boxes' x extents
print("== ASSET horizontal u-run at encoder box mid v (pt y 370 -> v 2192), u 500..2650 ==")
row = im[2192]
segs, cur, start = [], None, 500
for u in range(500, 2650):
    c = row[u]
    if cur is None: cur, start = c, u; continue
    if np.abs(c - cur).sum() > 72:
        segs.append((start, u - 1, cur)); cur, start = c, u
    else:
        cur = 0.7 * cur + 0.3 * c
segs.append((start, 2649, cur))
for s, e, c in segs:
    if e - s >= 3:
        print(f"  u {s}..{e} (pt x {575 + s * 0.12:.1f}..{575 + e * 0.12:.1f}) {'%02X%02X%02X' % tuple(int(q) for q in c)}")
print("== ASSET horizontal u-run at decoder box mid (pt y 294 -> v 1558), u 500..2650 ==")
row = im[1558]
segs, cur, start = [], None, 500
for u in range(500, 2650):
    c = row[u]
    if cur is None: cur, start = c, u; continue
    if np.abs(c - cur).sum() > 72:
        segs.append((start, u - 1, cur)); cur, start = c, u
    else:
        cur = 0.7 * cur + 0.3 * c
segs.append((start, 2649, cur))
for s, e, c in segs:
    if e - s >= 3:
        print(f"  u {s}..{e} (pt x {575 + s * 0.12:.1f}..{575 + e * 0.12:.1f}) {'%02X%02X%02X' % tuple(int(q) for q in c)}")
