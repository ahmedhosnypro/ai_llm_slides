#!/usr/bin/env python3
"""Chrome landmarks, pass 2: sensitive red-border detection via redness."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

redness = np.clip(R - np.maximum(G, B), 0, 255)  # high for red/maroon ink

col_red = (redness > 60).sum(axis=0)
row_red = (redness > 60).sum(axis=1)
print("cols with >200 redness px:", [(int(c), int(col_red[c])) for c in np.where(col_red > 200)[0]])
print("rows with >300 redness px:", [(int(r), int(row_red[r])) for r in np.where(row_red > 300)[0]])
print("cols with >100:", [(int(c), int(col_red[c])) for c in np.where(col_red > 100)[0]])
print("rows with >150:", [(int(r), int(row_red[r])) for r in np.where(row_red > 150)[0]])

# For the top border: find rows 35..60 redness profile
print("\nrow profile 35..60 (redness>60 count):")
for r in range(35, 61):
    n = int((redness[r] > 60).sum())
    if n:
        xs = np.where(redness[r] > 60)[0]
        print(f"  row {r}: n={n} x {xs.min()}..{xs.max()}")
print("\ncol profile 45..75 (redness>60 count):")
for c in range(45, 76):
    n = int((redness[:, c] > 60).sum())
    if n > 50:
        ys = np.where(redness[:, c] > 60)[0]
        print(f"  col {c}: n={n} y {ys.min()}..{ys.max()}")
print("\ncol profile 880..915 (redness>60 count):")
for c in range(880, 916):
    n = int((redness[:, c] > 60).sum())
    if n > 50:
        ys = np.where(redness[:, c] > 60)[0]
        print(f"  col {c}: n={n} y {ys.min()}..{ys.max()}")
print("\nrow profile 505..530 (redness>60 count):")
for r in range(505, 531):
    n = int((redness[r] > 60).sum())
    if n > 50:
        xs = np.where(redness[r] > 60)[0]
        print(f"  row {r}: n={n} x {xs.min()}..{xs.max()}")

# Badge: yellow circle near top-right. Yellow = R,G high, B low.
yellow = (R > 200) & (G > 200) & (B < 140)
ys, xs = np.where(yellow)
if len(ys):
    # restrict to top-right region
    sel = (xs > 800) & (ys < 130)
    if sel.any():
        bx0, bx1, by0, by1 = xs[sel].min(), xs[sel].max(), ys[sel].min(), ys[sel].max()
        print(f"\nbadge yellow bbox x {bx0}..{bx1} y {by0}..{by1} center ({(bx0+bx1)/2},{(by0+by1)/2}) size {bx1-bx0+1}x{by1-by0+1}")
