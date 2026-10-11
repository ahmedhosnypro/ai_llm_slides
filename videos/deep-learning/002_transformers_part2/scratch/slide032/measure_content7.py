#!/usr/bin/env python3
"""v7: vector-box border check (maroon?), chevron color, callout text bbox, right navy border."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# any reddish/maroon px around the white box perimeter?
zone = (slice(94, 200), slice(80, 210))
z = a[zone]
redl = (z[:, :, 0] - z[:, :, 1] > 25) & (z[:, :, 0] - z[:, :, 2] > 25) & (z[:, :, 0] > 95)
ys, xs = np.where(redl)
print("reddish px near white box:", len(ys))
if len(ys):
    rr = np.bincount(ys, minlength=106); rc = np.bincount(xs, minlength=130)
    print("rows>2:", [(94 + i, int(rr[i])) for i in np.where(rr > 2)[0]])
    print("cols>2:", [(80 + i, int(rc[i])) for i in np.where(rc > 2)[0]])

# chevron pixels on L2 (y 290..312, x 80..95)
ch = a[290:313, 80:96]
dk = ch.sum(axis=2) < 600
ys, xs = np.where(dk)
print("\nchevron L2 dark px:", len(ys))
if len(ys):
    print(Counter(map(tuple, ch[ys, xs])).most_common(5))
    print("chevron bbox frame x", 80 + xs.min(), "..", 80 + xs.max(), " y", 290 + ys.min(), "..", 290 + ys.max())

# callout text ink bbox (dark px rows 118..172, cols 225..850)
ct = a[118:173, 225:851]
dk2 = ct.sum(axis=2) < 420
ys, xs = np.where(dk2)
print("\ncallout text dark px:", len(ys))
if len(ys):
    print("bbox frame x", 225 + xs.min(), "..", 225 + xs.max(), " y", 118 + ys.min(), "..", 118 + ys.max())
    # red chars inside callout
    redc = (ct[:, :, 0] - ct[:, :, 1] > 60) & (ct[:, :, 0] - ct[:, :, 2] > 60) & (ct[:, :, 0] > 110)
    ys3, xs3 = np.where(redc)
    if len(ys3):
        print("red chars bbox frame x", 225 + xs3.min(), "..", 225 + xs3.max(), " y", 118 + ys3.min(), "..", 118 + ys3.max(), " n=", len(ys3))

# callout text rows profile (to size the text band)
dk3 = (a[115:175, 225:851].sum(axis=2) < 420)
rp = dk3.sum(axis=1)
print("callout text rows:", [(115 + i, int(rp[i])) for i in np.where(rp > 3)[0]])

# main panel RIGHT navy border: 1px scan cols 874..890, rows 212..505
navy = (R < 110) & (G < 110) & (B > 85)
for c in range(872, 892):
    n = int(navy[212:506, c].sum())
    if n > 20:
        print(f"\nright navy col {c}: {n}")
print("\nleft navy col 74 core:", Counter(map(tuple, a[212:506, 74][navy[212:506, 74]])).most_common(3))
for c in [73, 74, 75, 76]:
    print(f"col {c} navy(212..506):", int(navy[212:506, c].sum()))
# top border row 208 core color
m = navy[208, 100:800]
print("top border row 208 core:", Counter(map(tuple, a[208, 100:800][m])).most_common(3))
# body-text right extent check on L3/L4: ink x max
ink = (a.sum(axis=2) < 430)
for (y0, y1, lbl) in [(227, 245, 'L1'), (292, 310, 'L2'), (324, 342, 'L3'), (356, 374, 'L4'), (388, 406, 'L5'), (452, 471, 'L6')]:
    xs2 = np.where(ink[y0:y1, 80:900].any(axis=0))[0]
    print(f"{lbl} ink x {80+xs2.min()}..{80+xs2.max()}")
