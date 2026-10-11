#!/usr/bin/env python3
"""Measure slide-029 delta elements: exact bboxes, fills, text colors."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)

def hexc(t):
    return "%02X%02X%02X" % tuple(int(round(v)) for v in t)

def avg(x0, y0, x1, y1):
    return hexc(A[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0))

def bbox(x0, y0, x1, y1, pred):
    reg = A[y0:y1, x0:x1]
    m = pred(reg)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max()))

print("== callout band y141..187 ==")
print(" scanline y=165 colors:")
prev = None
for x in range(250, 900, 1):
    c = hexc(A[165, x])
    if c != prev:
        print(f"   x{x}: {c}")
        prev = c
print(" vertical scan x=350:")
prev = None
for y in range(130, 230, 1):
    c = hexc(A[y, 350])
    if c != prev:
        print(f"   y{y}: {c}")
        prev = c
