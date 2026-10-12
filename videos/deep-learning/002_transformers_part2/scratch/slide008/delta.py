#!/usr/bin/env python3
"""Delta analysis: 002:8 remapped to slide coords vs 001:33 frame (parent) and 002:13 (sibling).

Transform (deck fit, same as slide_013.js): slide_x = (fx-17.628)/0.961232, slide_y = fy/0.955556.
Frame content rect: x 17.6..940.4, y 0..516  -> resize to 960x540.
"""
from PIL import Image, ImageChops
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
F8 = f"{ROOT}/002_transformers_part2/unique_slides/slide_008.jpg"
F33 = f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg"
F13 = f"{ROOT}/002_transformers_part2/unique_slides/slide_013.jpg"

AX, SX, SY = 17.628, 0.961232, 0.955556
x0 = AX              # slide_x=0 -> frame x
x1 = AX + SX * 960   # slide_x=960
y1 = SY * 540        # slide_y=540
print(f"content rect: ({x0:.1f},0)-({x1:.1f},{y1:.1f})")

f8 = Image.open(F8).convert("RGB").crop((int(round(x0)), 0, int(round(x1)), int(round(y1)))).resize((960, 540), Image.LANCZOS)
f8.save(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png")
f33 = Image.open(F33).convert("RGB")
f13 = Image.open(F13).convert("RGB")

d33 = np.asarray(ImageChops.difference(f8, f33).convert("L")).astype(int)
d13 = np.asarray(ImageChops.difference(f8, f13).convert("L")).astype(int)

def grid(diff, tag):
    print(f"--- {tag}: mean {diff.mean():.1f}, p99 {np.percentile(diff,99):.0f} ---")
    cells = []
    for cy in range(0, 540, 45):      # 12 rows
        row = []
        for cx in range(0, 960, 40):  # 24 cols
            c = diff[cy:cy+45, cx:cx+40]
            row.append(int(c.mean()))
        cells.append(row)
    for i, row in enumerate(cells):
        print(f"y{i*45:3d}: " + "".join(f"{v:4d}" for v in row))
    return cells

g33 = grid(d33, "8 vs 001:33 (parent)")
g13 = grid(d13, "8 vs 002:13 (sibling)")

# significant-diff bbox for parent
mask = d33 > 60
ys, xs = np.where(mask)
print("8-vs-33 diff>60 count:", mask.sum(), "bbox:", (xs.min(), ys.min(), xs.max(), ys.max()) if mask.sum() else None)
