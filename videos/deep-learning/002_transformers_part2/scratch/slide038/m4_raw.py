#!/usr/bin/env python3
"""Slide 038 — raw RGB probes: chrome right border, defbox top, diagram panel top."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

print("== raw RGB rows 95..120 at x=400 (defbox top border?) ==")
for y in range(95, 121):
    print(" ", y, tuple(img[y, 400]), "  x=105:", tuple(img[y, 105]))

print("== raw RGB cols 895..912 at y=300 (chrome right border?) ==")
for x in range(895, 913):
    print(" ", x, tuple(img[300, x]), " y=100:", tuple(img[100, x]))

print("== raw RGB rows 236..262 at x=400 (diagram panel top?) ==")
for y in range(236, 263):
    print(" ", y, tuple(img[y, 400]))

print("== diagram panel left/right/bottom edges: raw at y=300, x 60..70 and x 888..896 ==")
for x in list(range(60, 71)) + list(range(888, 897)):
    print(" ", x, tuple(img[300, x]))
