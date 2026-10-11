#!/usr/bin/env python3
"""Measure strokes (borders) + fill regions + derivation line bands."""
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
            while j < n and m[j]: j += 1
            if j - i >= minlen: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# reddish incl. pink jpeg bleed: r - g > 25 and r - b > 25 and r > 180
reddish = (R - G > 25) & (R - B > 25) & (R > 170)
# bluish: b - r > 25 and b > 130
bluish = (B - R > 25) & (B > 130)
# greenish fill (mint/lime): g - r > 15, g - b > 15, g > 200
greenfill = (G - R > 15) & (G - B > 15) & (G > 200)
# cream/yellow fill: r>230,g>230,b<225 and (r-b>18)
cream = (R > 225) & (G > 225) & (R - B > 18) & (G - B > 18)

rc = reddish.sum(axis=0)
print("reddish vertical strokes (cols>35):", [(c, int(rc[c])) for c in np.where(rc > 35)[0]])
rr = reddish.sum(axis=1)
print("reddish horizontal strokes (rows>35):", [(r, int(rr[r])) for r in np.where(rr > 35)[0]])

bc = bluish.sum(axis=0)
print("\nbluish vertical strokes (cols>35):", [(c, int(bc[c])) for c in np.where(bc > 35)[0]])
br = bluish.sum(axis=1)
print("bluish horizontal strokes (rows>35):", [(r, int(br[r])) for r in np.where(br > 35)[0]])

for name, m in [("greenfill", greenfill), ("cream", cream)]:
    ys, xs = np.where(m)
    print(f"\n{name}: count={len(ys)} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
    # connected regions via row-band clustering
    rowhas = m.sum(axis=1)
    print(f"  {name} row bands:", runs(rowhas > 20, 2))

# per-stroke extent check: vertical reddish strokes — for each col, y-extent
print("\nvertical reddish stroke extents:")
for c, _ in [(c, 0) for c in np.where(rc > 35)[0]]:
    ys = np.where(reddish[:, c])[0]
    print(f"  col {c}: y{ys.min()}..{ys.max()} n={len(ys)}")
print("\nhorizontal reddish stroke extents:")
for r in np.where(rr > 35)[0]:
    xs = np.where(reddish[r, :])[0]
    print(f"  row {r}: x{xs.min()}..{xs.max()} n={len(xs)}")
print("\nvertical bluish stroke extents:")
for c in np.where(bc > 35)[0]:
    ys = np.where(bluish[:, c])[0]
    print(f"  col {c}: y{ys.min()}..{ys.max()} n={len(ys)}")
print("\nhorizontal bluish stroke extents:")
for r in np.where(br > 35)[0]:
    xs = np.where(bluish[r, :])[0]
    print(f"  row {r}: x{xs.min()}..{xs.max()} n={len(xs)}")
