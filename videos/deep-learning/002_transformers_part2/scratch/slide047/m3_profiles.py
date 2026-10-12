#!/usr/bin/env python3
"""m3_profiles.py — vertical/horizontal color-class profiles of slide_047.jpg."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg'
im = Image.open(F).convert('RGB')
A = np.asarray(im).astype(int)
H, W = A.shape[:2]

def cls(px):
    r, g, b = px
    if r > 248 and g > 248 and b > 248: return 'white'
    if r < 40 and g < 40 and b < 40: return 'black'
    if r > 150 and g < 90 and b < 90: return 'RED'
    if r > 200 and 120 < g < 210 and b < 140: return 'orange'
    if 200 < r < 250 and 150 < g < 200 and 90 < b < 150: return 'tan'
    if r < 160 and g < 80 and 70 < b < 140: return 'plum'
    if 90 < r < 140 and g < 70 and 130 < b < 190: return 'purple'
    if r > 225 and g > 205 and b > 225: return 'lav'
    if r > 235 and g > 235 and 200 < b < 245: return 'paleY'
    if r < 120 and g > 120 and b < 120: return 'green'
    if r > 180 and g < 110 and b < 110: return 'red2'
    return f'({r},{g},{b})'

print('=== VERTICAL profile x=480 (every 2px) ===')
prev = None
for y in range(0, H, 2):
    c = cls(A[y, 480])
    if c != prev:
        print(f'y={y}: {c}  {tuple(A[y,480])}')
        prev = c

print()
print('=== VERTICAL profile x=300 (every 2px, y=40..540) ===')
prev = None
for y in range(40, H, 2):
    c = cls(A[y, 300])
    if c != prev:
        print(f'y={y}: {c}  {tuple(A[y,300])}')
        prev = c

print()
print('=== HORIZONTAL profile y=64 (top row) every 2px, x=40..920 — class transitions only ===')
prev = None
for x in range(40, 925, 2):
    c = cls(A[64, x])
    if c != prev:
        print(f'x={x}: {c}  {tuple(A[64,x])}')
        prev = c
