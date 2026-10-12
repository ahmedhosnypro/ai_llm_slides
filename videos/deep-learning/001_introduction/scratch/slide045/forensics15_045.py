#!/usr/bin/env python3
"""forensics15_045.py — connected-component analysis of the eq(a) annotation zone.
Region x560..745, y300..375 frame px, original vs render_4.
Each component: class (RED/ink), bbox, size, centroid. Separates the arrow parts,
the dot, and the subscript glyphs rigorously."""
import numpy as np
from PIL import Image
from collections import deque

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
ren = np.asarray(Image.open(f"{QA}/render_4.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
s = ren.shape[0] / 540.0

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    lum = (r + g + b) / 3
    dark = (lum < 205) & (~red)
    return red, dark

X0, X1, Y0, Y1 = 560, 745, 300, 375
for nm, im, is_r in (("org", org, False), ("ren", ren, True)):
    k = s if is_r else 1
    R, D = masks(im)
    rwin = R[int(Y0*k):int(Y1*k)+1, int(X0*k):int(X1*k)+1]
    dwin = D[int(Y0*k):int(Y1*k)+1, int(X0*k):int(X1*k)+1]
    combo = (rwin | dwin)
    lab = np.zeros(combo.shape, dtype=int)
    comps = []
    for y in range(combo.shape[0]):
        for x in range(combo.shape[1]):
            if combo[y, x] and lab[y, x] == 0:
                cid = len(comps) + 1
                q = deque([(y, x)]); lab[y, x] = cid; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < combo.shape[0] and 0 <= nx < combo.shape[1] and combo[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = cid; q.append((ny, nx))
                comps.append(pts)
    print(f"== {nm}: {len(comps)} components (region x{X0}..{X1} y{Y0}..{Y1}) ==")
    rows = []
    for pts in comps:
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        bx0, bx1 = min(xs)/k + X0, max(xs)/k + X0
        by0, by1 = min(ys)/k + Y0, max(ys)/k + Y0
        nred = sum(1 for (y, x) in pts if rwin[y, x])
        cls = "RED" if nred > len(pts)*0.5 else "ink"
        rows.append((len(pts), cls, bx0, bx1, by0, by1))
    rows.sort(key=lambda t: (t[4], t[2]))
    for n, cls, bx0, bx1, by0, by1 in rows:
        if n < 6:
            continue
        print(f"  {cls:3s} n={n:5d}  x {bx0:6.1f}..{bx1:6.1f} ({bx1-bx0:5.1f}w)  y {by0:6.1f}..{by1:6.1f} ({by1-by0:5.1f}h)")
