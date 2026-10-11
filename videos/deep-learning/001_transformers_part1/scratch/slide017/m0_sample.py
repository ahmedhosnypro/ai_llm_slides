#!/usr/bin/env python3
"""Sample dominant colors in regions of slide_017.jpg."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im)

def sample(name, x0, y0, x1, y1):
    r = A[y0:y1, x0:x1].reshape(-1, 3)
    q = (r // 16 * 16)
    c = Counter(map(tuple, q))
    top = c.most_common(6)
    tot = len(r)
    print(f"{name} [{x0},{y0}..{x1},{y1}] ({tot}px):")
    for col, n in top:
        sel = np.all(np.abs(r - np.array(col)) <= 8, axis=1)
        if np.any(sel):
            avg = tuple(int(v) for v in r[sel].mean(axis=0))
        else:
            avg = col
        print(f"    q{col} avg{avg} x{n} ({100*n/tot:.1f}%)")

for name, box in [
    ("left col y120-160", (60, 120, 560, 160)),
    ("left col y150-175", (60, 150, 560, 175)),
    ("left col y220-260", (60, 220, 500, 260)),
    ("left col y250-270", (60, 250, 500, 270)),
    ("left col y340-390", (60, 340, 560, 390)),
    ("left col y470-520", (60, 470, 560, 520)),
    ("title area", (150, 30, 800, 90)),
]:
    sample(name, *box)
