#!/usr/bin/env python3
"""Forensics pass 2 — slide_028.jpg: title bands (stroke-excluded), attribution
(cursor-excluded via intensity), bar extent, baseline/cap marks per band."""
import numpy as np
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_028.jpg"
im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
rm = (R > 110) & (R > G + 40) & (R > B + 40)

def band_profile(y0, y1, x0=62, x1=918, thr_low=3, thr_dense=40, name=""):
    sub = rm[y0:y1 + 1, x0:x1 + 1]
    rp = sub.sum(axis=1)
    cp = sub.sum(axis=0)
    xs = np.where(cp > 0)[0]
    ys = np.where(rp > thr_low)[0]
    dense = [y0 + i for i, n in enumerate(rp) if n > thr_dense]
    # modal color of strongly-red px
    rr = a[y0:y1 + 1, x0:x1 + 1, :][sub]
    q = (rr // 4 * 4)
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    top = vals[np.argsort(-counts)][:3]
    print(f"{name}: y {y0}..{y1}  x {xs.min()+x0}..{xs.max()+x0} (w {xs.max()-xs.min()+1}, center {(xs.min()+xs.max()+2*x0)/2:.1f})")
    print(f"    ink rows {ys.min()+y0}..{ys.max()+y0}; dense(>{thr_dense}) {dense[0]}..{dense[-1]} (n={len(dense)})")
    print(f"    modal rgb {[list(map(int, t)) for t in top]} counts {list(map(int, np.sort(counts)[::-1][:3]))}")
    # row-by-row profile tail (to find baseline vs descender)
    prof = {int(y0 + i): int(n) for i, n in enumerate(rp) if n > 0}
    print("    rowprofile:", {k: v for k, v in prof.items() if k >= y0 and (k < y0 + 4 or k > y1 - 10)})

print("== TITLE BANDS (x from 62, inset stroke excluded) ==")
band_profile(116, 162, name="band1 'Introduction to'")
band_profile(232, 278, name="band2 'Convolutional Neural Network'")
band_profile(290, 346, name="band3 '(CNN)'")

# band3: separate paren columns from letter columns
sub = rm[290:347, 62:918]
cp = sub.sum(axis=0)
xs = np.where(cp > 0)[0] + 62
print("\nband3 col profile (x:count):", {int(x): int(cp[x - 62]) for x in xs})

print("\n== BLACK BAR ==")
dm = (R < 80) & (G < 80) & (B < 80)
bar = dm[518:540, :]
cols = bar.sum(axis=0)
xs = np.where(cols >= 15)[0]
print(f"bar rows 518..539, x {xs.min()}..{xs.max()} (w {xs.max()-xs.min()+1})")

print("\n== ATTRIBUTION (text = gray 60..200; cursor = black <50) ==")
am = (R >= 45) & (R <= 200) & (np.abs(R - G) < 25) & (np.abs(G - B) < 25) & (G <= 200)
bm = (R < 50) & (G < 50) & (B < 50)
for (y0, y1, name) in [(460, 482, "attr line1"), (483, 502, "attr line2")]:
    sub = am[y0:y1 + 1, 62:600]
    rp = sub.sum(axis=1)
    cp = sub.sum(axis=0)
    xs = np.where(cp > 0)[0]
    ys = np.where(rp > 0)[0]
    rr = a[y0:y1 + 1, 62:600, :][sub]
    print(f"{name}: x {xs.min()+62}..{xs.max()+62} rows {ys.min()+y0}..{ys.max()+y0}")
    # darkest percentile (approximate true stroke color)
    lum = rr.mean(axis=1)
    print(f"    lum p05={np.percentile(lum,5):.0f} p25={np.percentile(lum,25):.0f} modal={(np.median(lum)):.0f}")
    # column gaps (word gaps + the wide Course-EFSTRATIOS gap)
    colink = np.where(cp > 0)[0]
    gaps = []
    if len(colink):
        run_start = colink[0]
        for i in range(1, len(colink)):
            if colink[i] != colink[i - 1] + 1:
                gaps.append((colink[i - 1] + 62, colink[i] + 62, colink[i] - colink[i - 1] - 1))
                run_start = colink[i]
    big = [g for g in gaps if g[2] >= 5]
    print(f"    gaps>=5px: {big}")
print("cursor black bbox:", end=" ")
ys, xs = np.where(bm[430:500, 200:400])
print(f"x {xs.min()+200}..{xs.max()+200} y {ys.min()+430}..{ys.max()+430} n={len(ys)}")

print("\n== bar rows precise ==")
for y in range(514, 522):
    print(f"  y={y} dark={int(dm[y, 100:900].sum())}")
