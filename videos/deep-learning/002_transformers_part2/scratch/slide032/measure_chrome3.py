#!/usr/bin/env python3
"""Chrome landmarks, pass 3: badge with pale-yellow fill, top border hunt."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# pale yellow FDFD96 (253,253,150): R>230 G>230 100<B<200
badge = (R > 225) & (G > 225) & (B > 100) & (B < 205) & (np.abs(R - G) < 25)
ys, xs = np.where(badge)
sel = (xs > 820) & (ys < 130)
if sel.any():
    bx0, bx1, by0, by1 = xs[sel].min(), xs[sel].max(), ys[sel].min(), ys[sel].max()
    print(f"badge pale-yellow bbox x {bx0}..{bx1} y {by0}..{by1} center ({(bx0+bx1)/2},{(by0+by1)/2}) size {bx1-bx0+1}x{by1-by0+1}")
    # dark numeral inside badge
    num = (R < 120) & (G < 120) & (B < 120)
    inner = num[by0:by1+1, bx0:bx1+1]
    iys, ixs = np.where(inner)
    if len(iys):
        print(f"  numeral ink bbox in badge: x {bx0+iys.min()}..{bx0+iys.max()} y {by0+iys.min()}..{by0+iys.max()}")

redness = np.clip(R - np.maximum(G, B), 0, 255)
print("\nrows 36..58 any redness>30 count (x<910):")
for r in range(36, 59):
    n = int((redness[r, :910] > 30).sum())
    if n > 5:
        xs2 = np.where(redness[r, :910] > 30)[0]
        print(f"  row {r}: n={n} x {xs2.min()}..{xs2.max()}")

# purple ring 6A5ACD: R~106 G~90 B~205
purple = (np.abs(R - 106) < 70) & (np.abs(G - 90) < 70) & (B > 150) & (B - R > 40)
ys, xs = np.where(purple)
sel = (xs > 820) & (ys < 130)
if sel.any():
    print(f"purple-ring bbox x {xs[sel].min()}..{xs[sel].max()} y {ys[sel].min()}..{ys[sel].max()}")
