#!/usr/bin/env python3
"""Measure slide_037.jpg pass 2 — yellow box, title, panel, diagram blocks."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_037.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def runs(mask, min_gap=2):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for v in idx[1:]:
        if v - p > min_gap:
            out.append((s, p))
            s = v
        p = v
    out.append((s, p))
    return out

# ---- pale-yellow box: high R,G, low-ish B (B < 242), across full width
ybox = (a[:, :, 0] > 243) & (a[:, :, 1] > 243) & (a[:, :, 2] < 242)
rsum = ybox.sum(axis=1)
rr = [(y, int(c)) for y, c in enumerate(rsum) if c > 300]
print("yellow rows:", rr[0], "...", rr[-1], f"({len(rr)} rows)")
y0, y1 = rr[0][0], rr[-1][0]
csum = ybox[y0:y1 + 1].sum(axis=0)
xs = np.where(csum > (y1 - y0) * 0.6)[0]
print(f"yellow box x{xs[0]}..{xs[-1]} y{y0}..{y1}  (w={xs[-1]-xs[0]+1} h={y1-y0+1})")
print("modal yellow fill:", Counter(map(tuple, a[y0:y1+1][ybox[y0:y1+1]])).most_common(3))

# ---- body text lines inside the yellow box
sub = a[y0:y1 + 1]
ink = sub.sum(axis=-1) < 420
rp = ink.sum(axis=1)
print("\nbody lines:")
for s, e in runs(rp > 2, min_gap=4):
    xs2 = np.where(ink[s:e + 1].sum(axis=0) > 0)[0]
    print(f"  line y{y0+s}..{y0+e} h={e-s+1} x{xs2[0]}..{xs2[-1]}  inkpx={int(ink[s:e+1].sum())}")

# red ink inside yellow box (bold dark-red 'same location')
redm = (sub[:, :, 0] > 130) & (sub[:, :, 1] < 100) & (sub[:, :, 2] < 100)
rp2 = redm.sum(axis=1)
for s, e in runs(rp2 > 2, min_gap=8):
    xs3 = np.where(redm[s:e + 1].sum(axis=0) > 0)[0]
    print(f"  RED span y{y0+s}..{y0+e} x{xs3[0]}..{xs3[-1]}")
print("modal body red:", Counter(map(tuple, sub[redm])).most_common(3))
# modal body black
darkm = sub.sum(axis=-1) < 240
print("modal body ink:", Counter(map(tuple, sub[darkm])).most_common(3))

# ---- title: red core (saturated) only
print("\ntitle:")
tb = a[70:120]
redc = (tb[:, :, 0] > 150) & (tb[:, :, 1] < 80) & (tb[:, :, 2] < 80)
rp3 = redc.sum(axis=1)
ys = np.where(rp3 > 2)[0]
print("core red rows:", ys[0] + 70, "..", ys[-1] + 70)
cp = redc.sum(axis=0)
xs4 = np.where(cp > 0)[0]
print(f"core red ink x{xs4[0]}..{xs4[-1]} center={(xs4[0]+xs4[-1])/2}")
print("modal title core:", Counter(map(tuple, tb[redc])).most_common(3))

# ---- diagram panel red border
print("\ndiagram panel:")
redl = (a[:, :, 0] > 140) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80)
# horizontal red runs: rows y255..520, count in x60..900
rr2 = redl[:, 60:900].sum(axis=1)
long_rows = [(y, int(c)) for y, c in enumerate(rr2) if c > 500]
print("panel border rows:", long_rows)
cc2 = redl[270:500, :].sum(axis=0)
long_cols = [(x, int(c)) for x, c in enumerate(cc2) if c > 150]
print("panel border cols:", long_cols)

# ---- inside panel: ink overview (non-white)
py0 = long_rows[0][0] if long_rows else 262
py1 = long_rows[-1][0] if long_rows else 510
print(f"panel inner y{py0}..{py1}")
inner = a[py0 + 2:py1 - 1]
nonwhite = inner.sum(axis=-1) < 690
print("row ink profile (runs>3):")
for s, e in runs(nonwhite.sum(axis=1) > 3, min_gap=3):
    xs5 = np.where(nonwhite[s:e + 1].sum(axis=0) > 0)[0]
    print(f"  y{py0+2+s}..{py0+2+e} h={e-s+1} x{xs5[0]}..{xs5[-1]} inkpx={int(nonwhite[s:e+1].sum())}")
