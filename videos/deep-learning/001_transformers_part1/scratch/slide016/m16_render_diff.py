#!/usr/bin/env python3
"""Coarse alignment check: render_1.png (2000x1125) downscaled to 960x540 vs original."""
import numpy as np
from PIL import Image

R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide016/render_1.png").convert("RGB")
A = np.asarray(R.resize((960, 540), Image.LANCZOS)).astype(int)
B = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
d = np.abs(A - B).max(axis=2)

print("overall diff>40: %.2f%%" % ((d > 40).mean() * 100))
print("\n-- diff>40 by 30px row bands --")
for y0 in range(0, 540, 30):
    band = d[y0:y0+30, :]
    pct = (band > 40).mean() * 100
    bar = "#" * int(pct / 2)
    print(f"  y{y0:3d}-{y0+29:3d}: {pct:5.1f}% {bar}")
print("\n-- diff>40 by 40px col bands --")
for x0 in range(0, 960, 40):
    band = d[:, x0:x0+40]
    pct = (band > 40).mean() * 100
    bar = "#" * int(pct / 2)
    print(f"  x{x0:3d}-{x0+39:3d}: {pct:5.1f}% {bar}")
