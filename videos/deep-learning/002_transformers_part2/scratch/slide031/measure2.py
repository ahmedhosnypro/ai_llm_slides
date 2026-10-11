#!/usr/bin/env python3
"""Precise measurements part 2: chrome, panels, footer, banner, badge."""
import numpy as np
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(m, minlen=1):
    out, i, n = [], 0, len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[i if False else j] if False else (j < n and m[j]): j += 1
            if j - i >= minlen: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# gray E9E9E7 chrome panel
gray = (np.abs(R - 233) < 14) & (np.abs(G - 233) < 14) & (np.abs(B - 231) < 14)
ys, xs = np.where(gray)
print(f"gray px count={len(ys)}", f"bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}" if len(ys) else "")
gcol = gray.sum(axis=0); grow = gray.sum(axis=1)
print("gray cols>100:", runs(gcol > 100)[:12])
print("gray rows>100:", runs(grow > 100)[:12])

# red C00000-ish border: r>150, g<80, b<80
red = (R > 150) & (G < 90) & (B < 90)
ys, xs = np.where(red)
print(f"\nred px count={len(ys)} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}" if len(ys) else "\nno red")
rc = red.sum(axis=0)
print("red cols>40:", [(c, int(rc[c])) for c in np.where(rc > 40)[0]][:24])
rr_ = red.sum(axis=1)
print("red rows>40:", [(r, int(rr_[r])) for r in np.where(rr_ > 40)[0]][:24])

# black footer
black = (R < 70) & (G < 70) & (B < 70)
foot = black[515:540, :]
fc = foot.sum(axis=0)
cols = np.where(fc > 10)[0]
print(f"\nfooter black cols x{cols.min()}..{cols.max()}" if len(cols) else "no footer")
frows = np.where(black[:, 400:500].sum(axis=1) > 80)[0]
print("footer rows:", frows.min(), "..", frows.max())

# badge region crop analysis
print("\nbadge crop 840..940 x 40..110:")
sub = a[40:110, 840:940]
# find saturated yellowish (fill) and purple ring and red
sy = (sub[:, :, 0] > 230) & (sub[:, :, 1] > 230) & (sub[:, :, 2] > 120) & (sub[:, :, 2] < 200)
ys, xs = np.where(sy)
if len(ys): print(f"  pale-yellow fill bbox x{840+xs.min()}..{840+xs.max()} y{40+ys.min()}..{40+ys.max()} count={len(ys)}")
purple = (sub[:, :, 2] > 120) & (sub[:, :, 0] > 80) & (sub[:, :, 0] < 160) & (sub[:, :, 1] < 110)
ys, xs = np.where(purple)
if len(ys): print(f"  purple ring bbox x{840+xs.min()}..{840+xs.max()} y{40+ys.min()}..{40+ys.max()} count={len(ys)}")
reddish = (sub[:, :, 0] > 150) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110)
ys, xs = np.where(reddish)
if len(ys): print(f"  red ink bbox x{840+xs.min()}..{840+xs.max()} y{40+ys.min()}..{40+ys.max()} count={len(ys)}")
darkink = (sub[:, :, 0] < 90) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
ys, xs = np.where(darkink)
if len(ys): print(f"  dark ink bbox x{840+xs.min()}..{840+xs.max()} y{40+ys.min()}..{40+ys.max()} count={len(ys)}")

# banner strip: rows 215..260 — sample fill at several x
print("\nbanner fill samples:", [(x, tuple(a[230, x])) for x in (100, 200, 300, 470, 500, 620, 700)])
# banner border rows: scan rows 210..265 for long horizontal non-white strokes
for y in range(210, 268):
    row = a[y, 60:900]
    nw = ((np.abs(row - np.array([255, 255, 255])).sum(axis=1) > 60)).sum()
    if nw > 700: print(f"  banner-ish row y{y} nonwhite={nw} sample x60={tuple(a[y,60])} x450={tuple(a[y,450])}")
