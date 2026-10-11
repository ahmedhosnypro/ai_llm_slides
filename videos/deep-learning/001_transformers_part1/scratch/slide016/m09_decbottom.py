#!/usr/bin/env python3
"""Fine scanlines through the ambiguous decoder-bottom + lower-container regions."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)

def runs_at(y, x0, x1, minrun=2):
    row = IM[y, x0:x1]
    q = (row // 10) * 10
    out = []
    s = 0
    for i in range(1, len(q)):
        if not np.array_equal(q[i], q[i-1]):
            if i - s >= minrun:
                out.append((x0+s, x0+i-1, tuple(int(v) for v in q[i-1])))
            s = i
    out.append((x0+s, x0+len(q)-1, tuple(int(v) for v in q[len(q)-1])))
    return out

def show(title, items):
    print(f"\n-- {title} --")
    for a, b, c in items:
        print(f"   {a:3d}-{b:3d} ({b-a+1:3d}) rgb{c}")

for y in [328, 336, 350, 360, 375, 388, 400, 406, 412, 420, 430, 438, 446, 456, 466, 474, 482, 490, 498, 506, 514, 520]:
    show(f"row y={y} dec x737-895", runs_at(y, 737, 895))
for x in [755, 770, 785, 800, 815, 828]:
    show(f"col x={x} dec y400-525", runs_at(x, 400, 525, 2))
