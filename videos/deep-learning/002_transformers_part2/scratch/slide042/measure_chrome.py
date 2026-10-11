#!/usr/bin/env python3
"""Measure chrome landmarks + badge in slide_042.jpg (960x540, 1px=1pt frame space).

Chrome law (playlist): slide-space panel x 42..918, y 45..540 (bottom stroke 538-539);
badge circle d36 centered (893,71). Slide_002 established the zoomed-out mapping:
frame = a + s * slide, fit from 4 landmarks (panel left/right/top/bottom).
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"frame {W}x{H}")

def is_red(px):  # C00000-ish (or CC0000-ish) border red
    r, g, b = px
    return r > 120 and g < 90 and b < 90

# --- red border verticals: scan each column, count strongly-red pixels ---
red = (a[:, :, 0] > 120) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
# columns with long red runs = panel left/right borders
cand_cols = [x for x in range(W) if colcount[x] > 300]
cand_rows = [y for y in range(H) if rowcount[y] > 500]
print("long-red columns:", cand_cols)
print("long-red rows:", cand_rows)

# horizontal profile: average redness per row to find top border & bottom stroke
# sample middle band x 200..800
mid = red[:, 200:800]
rowfrac = mid.mean(axis=1)
top_band = [(y, round(rowfrac[y], 3)) for y in range(0, 120) if rowfrac[y] > 0.5]
bot_band = [(y, round(rowfrac[y], 3)) for y in range(H - 80, H) if rowfrac[y] > 0.5]
print("top border rows (frac>0.5):", top_band[:10])
print("bottom rows (frac>0.5):", bot_band[:10])

# left/right border columns frac within y 100..400
band = red[100:400, :]
colfrac = band.mean(axis=0)
lcols = [(x, round(colfrac[x], 3)) for x in range(0, 200) if colfrac[x] > 0.5]
rcols = [(x, round(colfrac[x], 3)) for x in range(W - 200, W) if colfrac[x] > 0.5]
print("left border cols (frac>0.5):", lcols[:10])
print("right border cols (frac>0.5):", rcols[:10])

# --- badge: find yellow FDFD96-ish pixels (high R, high G, low-mid B) ---
yel = (a[:, :, 0] > 220) & (a[:, :, 1] > 220) & (a[:, :, 2] < 190) & (a[:, :, 2] > 90)
ys, xs = np.nonzero(yel)
if len(xs):
    # restrict to top-right quadrant
    m = (xs > W * 0.8) & (ys < H * 0.4)
    if m.any():
        print(f"yellow badge bbox x {xs[m].min()}..{xs[m].max()} y {ys[m].min()}..{ys[m].max()} "
              f"center ({(xs[m].min()+xs[m].max())/2},{(ys[m].min()+ys[m].max())/2}) n={m.sum()}")
        cx = (xs[m].min() + xs[m].max()) / 2
        cy = (ys[m].min() + ys[m].max()) / 2
        # map to slide space with slide_002 transform for cross-check
        s = 0.96123
        ax_, ay_ = 18.63, 0.95556
        sx = (cx - ax_) / s
        sy = cy / ay_
        print(f"badge center -> slide ({sx:.1f},{sy:.1f}) vs house (893,71)")
        # numeral ink inside badge (dark pixels)
        x0, x1, y0, y1 = xs[m].min(), xs[m].max(), ys[m].min(), ys[m].max()
        sub = a[y0:y1 + 1, x0:x1 + 1]
        dark = (sub[:, :, 0] < 120) & (sub[:, :, 1] < 120) & (sub[:, :, 2] < 120)
        dys, dxs = np.nonzero(dark)
        if len(dxs):
            print(f"numeral ink bbox in-badge x {dxs.min()}..{dxs.max()} y {dys.min()}..{dys.max()} n={len(dxs)}")
            # column profile to guess digit count: gaps
            colhas = dark.any(axis=0)
            runs = []
            inr = False
            for i, v in enumerate(colhas):
                if v and not inr:
                    st = i; inr = True
                elif not v and inr:
                    runs.append((st, i - 1)); inr = False
            if inr: runs.append((st, len(colhas) - 1))
            print("numeral ink column runs:", runs)
else:
    print("no yellow badge found")
