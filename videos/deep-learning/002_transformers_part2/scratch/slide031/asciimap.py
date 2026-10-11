#!/usr/bin/env python3
"""ASCII map of slide_031.jpg: classify each 8px cell by dominant color family."""
import numpy as np
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(y, x):
    r, g, b = a[y, x]
    if r < 80 and g < 80 and b < 80: return "K"          # black ink/bar
    if r > 160 and g < 110 and b < 110: return "R"       # red ink
    if b > 140 and r < 120 and g < 120: return "B"       # blue ink
    if b > 140 and r < 140 and g >= 140: return "b"      # light blue / periwinkle
    if r > 200 and g > 200 and b < 150: return "Y"       # yellow
    if g > 200 and r < 210 and b < 200 and g - b > 25: return "g"  # green/mint/lime
    if g > 190 and b > 190 and r < 210: return "c"       # cyan
    if r > 225 and g > 225 and b > 225: return "."       # white
    return " "

CELL = 12
rows = H // CELL
cols = W // CELL
print("    " + "".join(str((c * CELL) // 100 % 10) for c in range(cols)))
for ri in range(rows):
    y = ri * CELL + CELL // 2
    line = []
    for ci in range(cols):
        x = ci * CELL + CELL // 2
        # majority vote in 4x4 block
        from collections import Counter
        blk = [cls(y + dy, x + dx) for dy in (-3, 0, 3) for dx in (-3, 0, 3)]
        line.append(Counter(blk).most_common(1)[0][0])
    print(f"{y:3d} " + "".join(line))
