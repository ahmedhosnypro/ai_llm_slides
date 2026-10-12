#!/usr/bin/env python3
"""measure8.py — definitive per-cell fill classification via corner patches."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
im = Image.open(f"{BASE}/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def classify(px):
    r, g, b = px
    if b > 170 and b - r > 80: return "C"
    if g > 140 and g - b > 60 and r < 120: return "G"
    if r > 200 and g > 200 and b < 140: return "Y"
    return "?"

def cell_fills(x0, y0, n, m, cw, ch, label):
    print(f"{label}:")
    for r in range(m):
        row = ""
        for c in range(n):
            votes = []
            for fy in (0.18, 0.82):
                for fx in (0.18, 0.5, 0.82):
                    cx = int(x0 + c * cw + cw * fx)
                    cy = int(y0 + r * ch + ch * fy)
                    patch = a[cy - 1:cy + 2, cx - 1:cx + 2].reshape(-1, 3)
                    med = tuple(np.median(patch, axis=0).astype(int))
                    votes.append(classify(med))
            # majority vote among non-? votes
            v = [x for x in votes if x != "?"]
            row += max(set(v), key=v.count) if v else "?"
        print(f"  r{r+1}: {row}")

cell_fills(101, 173, 7, 7, 277 / 7, 210 / 7, "7x7 (x101 y173 cw39.57 ch30)")
cell_fills(440, 247, 3, 3, 87 / 3, 66 / 3, "3x3 (x440 y247 cw29 ch22)")
cell_fills(622, 203, 5, 5, 198 / 5, 151 / 5, "5x5 (x622 y203 cw39.6 ch30.2)")
