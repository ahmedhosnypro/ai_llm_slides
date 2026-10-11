#!/usr/bin/env python3
"""Quantize the original frame to find the TRUE palette, and sample key points."""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
q = IM.quantize(colors=24, method=Image.MEDIANCUT).convert("RGB")
A = np.asarray(q).astype(int)
H, W, _ = A.shape
pal, counts = np.unique(A.reshape(-1, 3), axis=0, return_counts=True)
order = np.argsort(-counts)
print("== quantized palette (count, hex, bbox) ==")
for i in order[:24]:
    c = pal[i]
    m = (A == c).all(axis=2)
    ys, xs = np.where(m)
    if counts[i] < 200:
        continue
    print(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X} n={counts[i]:7d} x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")

print("\n== point samples ==")
pts = {
    "panel_gray_top": (500, 30), "peach_canvas_mid": (700, 200),
    "peach_left_of_stack": (60, 300),
    "title_text_core": (300, 65), "title_line2_area": (400, 95),
    "highlight": (600, 65),
}
A0 = np.asarray(IM).astype(int)
for k, (x, y) in pts.items():
    print(k, (x, y), tuple(A0[y, x]))
