#!/usr/bin/env python3
"""ASCII maps of brackets, white-text confirmation, pill pure colors, underline."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
mx = np.maximum(np.maximum(R, G), B)

def amap(name, x0, x1, y0, y1, mask, step=1):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1}")
    hdr = "     " + "".join(str((x0 + x) % 10) for x in range(0, x1 - x0, step))
    print(hdr)
    for y in range(y0, y1):
        row = "".join("#" if mask[y, x0 + x] else "." for x in range(0, x1 - x0, step))
        print(f"y{y:3d} {row}")

dark = mx < 150
redd = (R > 110) & (R - G > 40) & (R - B > 30)
navyd = (B - R > 30) & (B - G > 20) & (B > 80)
amap("v1 Lbracket red", 238, 258, 54, 140, redd, 1)
amap("mtx Lbracket navy", 276, 300, 350, 362, navyd, 1)
amap("mtx Lbracket navy bottom", 276, 300, 420, 434, navyd, 1)
amap("v2 Lbracket black", 238, 260, 148, 165, dark, 1)
amap("mLv Lbracket black", 114, 134, 348, 365, dark, 1)
amap("rvec Lbracket red", 478, 500, 350, 365, redd, 1)

# white text confirmation in matrix col2: B-channel profile — pill B low, white text B high
def bimodal(name, x0, y0, x1, y1):
    sub = im[y0:y1, x0:x1]
    w = ((sub[:, :, 0] > 235) & (sub[:, :, 1] > 235) & (sub[:, :, 2] > 235)).sum()
    yl = ((sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] < 180)).sum()
    dk = (sub.sum(axis=2) < 330).sum()
    print(f"{name}: white={w} yellowish={yl} dark={dk}")
bimodal("mtx r1c2", 425, 356, 462, 378)
bimodal("mtx r2c2", 420, 398, 462, 422)
bimodal("L1 tail", 596, 249, 644, 268)
bimodal("L2 mid cos(wd)", 450, 295, 516, 314)
bimodal("L1 green cos(wd) (control)", 432, 250, 492, 266)

# dark pixel locations in L2 cos(wd)
sub = im[295:314, 450:516]
dk = np.argwhere(sub.sum(axis=2) < 330)
print("L2 cos(wd) dark pixel coords (first 20):", [(450 + int(c), 295 + int(r)) for r, c in dk[:20]])

# pill pure interiors (avoid text): sample corners
def pure(name, x0, y0, x1, y1):
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    keep = sub[(sub.sum(axis=1) > 350)]
    print(f"{name} bright-mode: {np.median(keep, axis=0)} n={len(keep)}")
pure("vivid pill L1(t+d) top strip", 149, 246, 187, 250)
pure("vivid pill vecbox r1", 305, 154, 343, 158)
pure("pale pill L1 tail strip", 598, 250, 642, 254)
pure("pale pill mtx r1c2 top", 426, 356, 460, 360)
pure("green pill L1 strip", 433, 249, 491, 252)
pure("green pill mtx r1c1 strip", 305, 355, 372, 359)
pure("remember fill", 620, 132, 840, 142)
pure("note fill", 640, 455, 860, 468)

# underline: raw scan
navy2 = (B - R > 15) & (B > 110)
print("underline loose scan:", [(y, int(navy2[y, 505:605].sum())) for y in range(110, 132)])
# where is navy in row 121?
xs = np.where(navy2[121, 505:605])[0]
print("row121 navy x:", (505 + xs.min(), 505 + xs.max()) if len(xs) else "none", "count", len(xs))
xs = np.where(navy2[123, 505:605])[0]
print("row123 navy x:", (505 + xs.min(), 505 + xs.max()) if len(xs) else "none", "count", len(xs))
xs = np.where(navy2[124, 505:605])[0]
print("row124 navy x:", (505 + xs.min(), 505 + xs.max()) if len(xs) else "none", "count", len(xs))
