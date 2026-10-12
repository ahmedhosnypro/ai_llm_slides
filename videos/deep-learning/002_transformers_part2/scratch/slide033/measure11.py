#!/usr/bin/env python3
"""slide033 measure-11: equation sub-box internal ink geometry by color."""
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556
S = lambda x0, x1, y0, y1: (f"f[{x0},{y0}..{x1},{y1}] slide[{MAPX(x0):.1f}..{MAPX(x1):.1f} x {MAPY(y0):.1f}..{MAPY(y1):.1f}]")

X0, X1, Y0, Y1 = 712, 862, 349, 392  # interior, excluding the red border ring
sub = a[Y0:Y1 + 1, X0:X1 + 1]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]

masks = {
    "RED  (omega, 2k/d)": (r > 130) & (g < 90) & (b < 90),
    "BLUE (K sub, bar)": (b > 110) & (r < 110) & (b - r > 40),
    "BLACK(1, 10000, =)": (r < 110) & (g < 110) & (b < 110),
}
for name, m in masks.items():
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 3: continue
        comps.append((int(xs.min()) + X0, int(ys.min()) + Y0, int(xs.max()) + X0, int(ys.max()) + Y0, len(ys)))
    comps.sort(key=lambda c: (c[0]))
    print(f"--- {name}: {len(comps)} comps ---")
    for c in comps:
        print(f"  {S(c[0], c[2], c[1], c[3])} n={c[4]}")
