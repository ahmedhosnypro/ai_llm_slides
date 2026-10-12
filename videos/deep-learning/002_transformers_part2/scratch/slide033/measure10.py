#!/usr/bin/env python3
"""slide033 measure-10: general pair text (loose maroon mask) + index strip fine scan."""
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556

# general pair box: text = pixels notably darker than the whitish interior and reddish
sub = a[126:214, 96:186]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
m = (r < 200) & (r - g > 25) & (r - b > 20)  # reddish-dark
ys, xs = np.where(m)
print("general pair reddish ink count:", len(ys))
if len(ys):
    rows = np.bincount(ys, minlength=sub.shape[0])
    for y in range(sub.shape[0]):
        if rows[y] > 0 and (y == 0 or rows[y - 1] == 0):
            print(f"  ink row-start frame y={y+126} slide={MAPY(y+126):.1f}")
        if rows[y] > 0 and (y == sub.shape[0] - 1 or rows[y + 1] == 0):
            print(f"  ink row-end   frame y={y+126} slide={MAPY(y+126):.1f}")
    # line bands
    lab, n = ndimage.label(rows[:, None].repeat(2, 1) > 0)
    print("  row bands:")
    for i in range(1, n + 1):
        yy = np.where(lab[:, 0] == i)[0]
        xsel = xs[(ys >= yy.min()) & (ys <= yy.max())]
        print(f"    f y {yy.min()+126}..{yy.max()+126} x {xsel.min()+96}..{xsel.max()+96}"
              f"  slide y {MAPY(yy.min()+126):.1f}..{MAPY(yy.max()+126):.1f} x {MAPX(xsel.min()+96):.1f}..{MAPX(xsel.max()+96):.1f}")

# box border hunt: vertical dark strokes around x 88..100 and x 178..190, rows 130..205
print("border scan (cols with dark counts in y130..205):")
for x in list(range(86, 104)) + list(range(178, 196)):
    col = a[130:206, x]
    dk = (col.mean(axis=1) < 190).sum()
    if dk > 20:
        print(f"  x={x} darkrows={dk} med={tuple(int(v) for v in np.median(col[col.mean(axis=1)<190], axis=0)) if dk else '-'}")
print("border scan (rows with dark counts in x96..184):")
for y in list(range(118, 130)) + list(range(204, 218)):
    row = a[y, 96:185]
    dk = (row.mean(axis=1) < 190).sum()
    if dk > 20:
        print(f"  y={y} darkcols={dk} med={tuple(int(v) for v in np.median(row[row.mean(axis=1)<190], axis=0)) if dk else '-'}")

# index strip: red-ish ink rows (loose)
print("index strip red rows (x 270..308, y 124..514):")
sub = a[124:515, 270:309]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
m = (r > 140) & (r - g > 35) & (r - b > 30)
rows = m.sum(axis=1)
y = 0
while y < len(rows):
    if rows[y] > 0:
        y2 = y
        while y2 < len(rows) - 1 and rows[y2 + 1] > 0:
            y2 += 1
        xs = np.where(m[y:y2 + 1].any(axis=0))[0]
        print(f"  f y {y+124}..{y2+124} x {xs.min()+270}..{xs.max()+270}  slide y {MAPY(y+124):.1f}..{MAPY(y2+124):.1f} x {MAPX(xs.min()+270):.1f}..{MAPX(xs.max()+270):.1f}")
        y = y2 + 1
    else:
        y += 1
