#!/usr/bin/env python3
"""Closed-loop measurement: render_1 vs original targets (frame px)."""
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide028/render_1.png"
im = Image.open(RENDER).convert("RGB")
W, H = im.size
s = W / 960.0
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
rm = (R > 110) & (R > G + 40) & (R > B + 40)

def band(y0, y1, x0=62, x1=918, name=""):
    sub = rm[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    rp = sub.sum(axis=1)
    cp = sub.sum(axis=0)
    ys = np.where(rp > 3 * s)[0]
    dense = np.where(rp > 40 * s)[0]
    xs = np.where(cp > 0)[0]
    if len(ys) == 0:
        print(f"{name}: NO INK")
        return
    print(f"{name}: ink y {ys.min()/s + y0:.1f}..{ys.max()/s + y0:.1f} dense {dense.min()/s + y0:.1f}..{dense.max()/s + y0:.1f} x {xs.min()/s + x0:.1f}..{xs.max()/s + x0:.1f} (w {(xs.max()-xs.min())/s:.1f})")

print("== render title bands (frame-px coords) ==")
band(110, 170, name="t1 'Introduction to'              target ink 119..158 x 301..660 w360")
band(226, 286, name="t2 'Convolutional Neural Network' target ink 235..274 x 112..847 w736")
band(284, 352, name="t3 '(CNN)'                        target ink 293..342 x 409..550 w142 bas 331.5")

# attribution (gray ink)
am = (R >= 45) & (R <= 200) & (np.abs(R - G) < 25) & (np.abs(G - B) < 25) & (G <= 200)
def gray_band(y0, y1, x0, x1, name):
    sub = am[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    rp = sub.sum(axis=1)
    cp = sub.sum(axis=0)
    ys = np.where(rp > 0)[0]
    xs = np.where(cp > 0)[0]
    if len(ys) == 0:
        print(f"{name}: NO INK")
        return
    # dense = rows near baseline: use >0.6*peak
    peak = rp.max()
    dense = np.where(rp > 0.6 * peak)[0]
    print(f"{name}: ink y {ys.min()/s + y0:.1f}..{ys.max()/s + y0:.1f} x {xs.min()/s + x0:.1f}..{xs.max()/s + x0:.1f} (w {(xs.max()-xs.min())/s:.1f}) dense-bottom {dense.max()/s + y0:.1f}")

print("\n== render attribution (frame-px coords) ==")
gray_band(455, 484, 150, 600, "a1 target ink ~467..481 x 99.. bas~477")
gray_band(484, 505, 150, 600, "a2 target ink 485..499 x 93..426 w334 bas~495")

# bar
dm = (R < 80) & (G < 80) & (B < 80)
sub = dm[int(510 * s):, :]
rp = sub.sum(axis=1)
rows = np.where(rp > 700 * s)[0]
xs_row = np.where(dm[int(525 * s), :] > 0)[0]
print(f"\nbar: rows {rows.min()/s + 510:.1f}..{rows.max()/s + 510:.1f} (target 519..537.5 drawn), x {xs_row.min()/s:.1f}..{xs_row.max()/s:.1f} (target 38..921)")

# colors
print("\ncolors: canvas", tuple(a[int(20 * s), int(20 * s)]), "panel", tuple(a[int(300 * s), int(700 * s)]),
      "bar", tuple(a[int(530 * s), int(480 * s)]))
# title modal
rr = a[int(240 * s):int(270 * s), int(200 * s):int(800 * s)][rm[int(240 * s):int(270 * s), int(200 * s):int(800 * s)]]
q = (rr // 4 * 4)
vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
print("title modal:", [list(map(int, v)) for v in vals[np.argsort(-counts)][:3]])
