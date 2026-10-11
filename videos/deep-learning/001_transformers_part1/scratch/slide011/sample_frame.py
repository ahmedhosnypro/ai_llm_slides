#!/usr/bin/env python3
"""Sample the frame's palette: dominant colors + point samples at grid positions."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im)
H, W = a.shape[:2]

# quantize to /16 buckets and count dominant colors
q = (a // 16 * 16).reshape(-1, 3)
cnt = Counter(map(tuple, q))
print("top 25 quantized colors:")
for c, n in cnt.most_common(25):
    print(f"  {c}  n={n}")

print("\npoint samples (x,y) -> rgb:")
pts = [(480, 20), (480, 50), (480, 75), (480, 100), (480, 200), (480, 300), (480, 400), (480, 500), (480, 535),
       (200, 250), (200, 300), (200, 350), (700, 200), (700, 320), (700, 350),
       (650, 450), (650, 500), (850, 520), (100, 520), (46, 270), (914, 270), (46, 538), (914, 538),
       (893, 71), (905, 60), (880, 82), (150, 495), (250, 505), (500, 240)]
for (x, y) in pts:
    print(f"  ({x:3d},{y:3d}) -> {tuple(a[y, x])}")
