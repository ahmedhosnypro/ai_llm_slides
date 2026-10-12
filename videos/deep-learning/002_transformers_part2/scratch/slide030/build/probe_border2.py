#!/usr/bin/env python3
"""Slide 030: raw pixel probe along candidate border lines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def rowdump(y, x0, x1, step):
    px = [f"{x}:{R[y,x]},{G[y,x]},{B[y,x]}" for x in range(x0, x1, step)]
    print(f"row {y}: " + "  ".join(px))

def coldump(x, y0, y1, step):
    px = [f"{y}:{R[y,x]},{G[y,x]},{B[y,x]}" for y in range(y0, y1, step)]
    print(f"col {x}: " + "  ".join(px))

print("--- vertical scan col 500, rows 36..64 (top border?):")
coldump(500, 36, 64, 1)
print("--- vertical scan col 500, rows 510..522 (bottom border):")
coldump(500, 510, 522, 1)
print("--- horizontal scan row 300, cols 50..70 (left border?):")
rowdump(300, 50, 70, 1)
print("--- horizontal scan row 300, cols 894..912 (right border?):")
rowdump(300, 894, 912, 1)
print("--- horizontal scan row 100, cols 50..70:")
rowdump(100, 50, 70, 1)
print("--- horizontal scan row 450, cols 894..912:")
rowdump(450, 894, 912, 1)
