#!/usr/bin/env python3
# m15_edges.py — resolve the four contested highlight edges with on-segment probes.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
warp = np.asarray(Image.open(S + "/frame_warped_contentfit.png").convert("RGB"), dtype=np.float64)
O = np.array([240, 122, 2.]); A = 0.50

def probe(tag, xs, ys):
    print(tag)
    for ry in ys:
        row = []
        for rx in xs:
            cb = render[ry, rx]; cf = warp[ry, rx]
            dv = O - cb; den = (dv * dv).sum()
            t = ((cf - cb) * dv).sum() / den
            off = np.linalg.norm((cf - cb) - t * dv)
            ok = "Y" if (abs(t - A) < 0.17 and off < 32 and t * np.sqrt(den) > 45) else ("h" if (0.15 < t < 0.85 and off < 32) else ".")
            row.append(f"{rx}:{t:+.2f}{ok}")
        print(f"  y{ry}({ry*0.48:.0f}pt): " + "  ".join(row))

# H1 right edge (render x, y in H1 band)
probe("H1 right edge zone (x 1495..1548):", range(1495, 1549, 4), [755, 775, 795, 815, 830])
# H2 left edge zone
probe("H2 left edge zone (x 1528..1590):", range(1528, 1591, 4), [585, 605, 625, 645, 660])
# H2 right edge zone
probe("H2 right edge zone (x 1836..1878):", range(1836, 1879, 3), [585, 605, 625, 645, 660])
# H1 left edge zone
probe("H1 left edge zone (x 1198..1236):", range(1198, 1237, 3), [755, 775, 795, 815, 830])
# H1 top/bottom sanity at x 1260
probe("H1 top/bottom (x1260):", [1260], range(730, 860, 8))
# H2 top/bottom sanity at x 1800
probe("H2 top/bottom (x1800):", [1800], range(560, 690, 8))
