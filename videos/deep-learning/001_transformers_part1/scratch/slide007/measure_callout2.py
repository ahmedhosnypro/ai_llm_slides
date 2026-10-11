#!/usr/bin/env python3
"""Callout pass 2: pure fill, box outline, per-line bands, underlines, connector trace."""
from PIL import Image
import numpy as np
from collections import Counter

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

# --- pure fill color: text-free strip y172..184 x60..440 ---
strip = b[172:184, 60:440].reshape(-1, 3)
cnt = Counter(map(tuple, strip))
print("top fill colors in text-free strip:", cnt.most_common(6))

# --- box outline via bluish mask (fill OR blue border), per-row extents ---
win = b[150:300, 30:510]
r, g, bl = win[:, :, 0], win[:, :, 1], win[:, :, 2]
mask = (bl > r + 18) & (bl > 150)  # any blue-ish
print("\nper-row extent of blue-ish mask (row: xmin..xmax, count) every 2 rows:")
for i in range(0, mask.shape[0], 2):
    xs = np.nonzero(mask[i])[0]
    if len(xs):
        print(f"  y={150+i:3d}: {30+xs.min():3d}..{30+xs.max():3d} n={len(xs)}")
