#!/usr/bin/env python3
"""Measure the slide-38 delta inset (Figure-2-left, course style) from
unique_slides/slide_038.jpg (960x540, 1px = 1pt). Reports:
- green panel border bbox + stroke width
- colored flow boxes (bbox + core fill) via color clustering
- black text ink rows per box
- arrow segments (thin dark lines) + arrowheads
- Q/K/V label ink positions
"""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
im = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# region of interest (from the diff scan: x[770..930] y[90..330])
X0, X1, Y0, Y1 = 760, 935, 85, 340

def bbox_of(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] n={len(xs)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

# 1. green border: G clearly dominant and dark-green-ish
green = (G > R + 25) & (G > B + 15) & (G > 80) & (G < 200) & (R < 150)
gm = np.zeros_like(green); gm[Y0:Y1, X0:X1] = green[Y0:Y1, X0:X1]
bbox_of(gm, "green border (panel)")
# column profile of green inside ROI to find left/right border columns
gcols = gm.sum(axis=0); grows = gm.sum(axis=1)
gc = [(x, int(gcols[x])) for x in range(X0, X1) if gcols[x] > 20]
gr = [(y, int(grows[y])) for y in range(Y0, Y1) if grows[y] > 20]
print("green cols (>20px):", gc)
print("green rows (>20px):", gr)

# 2. flow boxes by color (JPEG-washed): sample color clusters
def cluster_bbox(cond, label, min_n=30):
    m = np.zeros((H, W), dtype=bool)
    m[Y0:Y1, X0:X1] = cond[Y0:Y1, X0:X1]
    ys, xs = np.where(m)
    if len(xs) < min_n:
        print(f"{label}: n={len(xs)} (skip)")
        return
    # split into row bands by y-histogram gaps
    order = np.argsort(ys)
    ys_s = ys[order]; xs_s = xs[order]
    bands = []
    start = 0
    for i in range(1, len(ys_s) + 1):
        if i == len(ys_s) or ys_s[i] - ys_s[i - 1] > 6:
            band_ys = ys_s[start:i]; band_xs = xs_s[start:i]
            if len(band_ys) >= min_n:
                bands.append((band_xs.min(), band_xs.max(), band_ys.min(), band_ys.max(), len(band_ys)))
            start = i
    for b in bands:
        cx0, cx1, cy0, cy1, n = b
        core = im[cy0+2:cy1-1, cx0+2:cx1-1] if cy1-cy0 > 4 else im[cy0:cy1+1, cx0:cx1+1]
        med = np.median(core.reshape(-1, 3), axis=0).astype(int)
        print(f"{label}: x[{cx0}..{cx1}] y[{cy0}..{cy1}] n={n} core={tuple(med)}")

lav = (np.abs(R - 179) < 45) & (np.abs(G - 157) < 45) & (np.abs(B - 219) < 45)
palegreen = (np.abs(R - 197) < 40) & (np.abs(G - 225) < 40) & (np.abs(B - 165) < 45)
lav2 = (np.abs(R - 209) < 40) & (np.abs(G - 196) < 40) & (np.abs(B - 233) < 40)
paleyellow = (np.abs(R - 255) < 35) & (np.abs(G - 245) < 40) & (np.abs(B - 157) < 60)
cluster_bbox(lav, "lavender#1(B39DDB)")
cluster_bbox(palegreen, "lightgreen(C5E1A5)")
cluster_bbox(lav2, "lavender#2(D1C4E9)")
cluster_bbox(paleyellow, "paleyellow(FFF59D)")

# 3. black ink (text/arrows) in ROI
ink = (R < 110) & (G < 110) & (B < 110)
imk = np.zeros((H, W), dtype=bool); imk[Y0:Y1, X0:X1] = ink[Y0:Y1, X0:X1]
irows = imk.sum(axis=1)
print("ink rows y:count (>4):", [(y, int(irows[y])) for y in range(Y0, Y1) if irows[y] > 4])
