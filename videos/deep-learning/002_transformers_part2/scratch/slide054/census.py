#!/usr/bin/env python3
"""Global color census + precise means per cluster."""
from PIL import Image
import numpy as np
from collections import Counter
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape

q = 16
qd = (A // q) * q
flat = qd.reshape(-1, 3)
c = Counter(map(tuple, flat))
print("TOP 25 quantized colors (frame-wide):")
for col, n in c.most_common(25):
    # precise mean of pixels in this bucket
    m = np.all(np.abs(A - np.array(col)) <= q, axis=2)
    if m.sum() == 0: continue
    mean = A[m].mean(axis=0)
    print(f"  q={col} n={n} mean=({mean[0]:.0f},{mean[1]:.0f},{mean[2]:.0f}) -> #{int(mean[0]):02X}{int(mean[1]):02X}{int(mean[2]):02X}")
