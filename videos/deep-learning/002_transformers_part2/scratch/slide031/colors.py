#!/usr/bin/env python3
"""Calibrate: dominant colors + point samples."""
import numpy as np
from PIL import Image
from collections import Counter

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img)
H, W, _ = a.shape

q = (a // 16 * 16)
flat = q.reshape(-1, 3)
cnt = Counter(map(tuple, flat))
print("top 30 quantized colors:")
for c, n in cnt.most_common(30):
    print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  {n}")

pts = {
    "canvas-topleft": (10, 10), "panel-mid": (480, 300), "footer": (480, 530),
    "badge": (875, 71), "left-panel": (100, 150), "mid-panel": (400, 100),
    "banner": (400, 232), "deriv-panel": (450, 300), "callout": (640, 490),
}
print("\npoint samples (x,y -> RGB):")
for name, (x, y) in pts.items():
    print(f"  {name}: ({x},{y}) = #{a[y,x,0]:02X}{a[y,x,1]:02X}{a[y,x,2]:02X}")
