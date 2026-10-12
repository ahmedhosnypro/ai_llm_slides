#!/usr/bin/env python3
"""Slide 038 forensics pass 6: fine ASCII of diagram region + circle zoom + = hunt."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def cls(p):
    rr, gg, bb = p
    if rr > 235 and gg > 235 and bb > 235: return '.'
    if abs(rr - 232) < 12 and abs(gg - 232) < 12 and abs(bb - 231) < 12: return ' '
    if rr < 110 and gg < 110 and bb < 110: return '#'
    if rr < 170 and gg < 150 and bb < 150 and (rr - bb) > 20 and (gg - bb) > 10 and rr < 200 and gg < 160: return 'd'  # dark ink gray
    if rr > 170 and gg < 100 and bb < 100: return 'R'
    if rr > 150 and gg > 95 and gg < 175 and bb < 100: return 'o'   # brown
    if rr > 150 and gg > 175 and bb < 120: return 'y'
    if gg > 120 and gg - rr > 30 and gg - bb > 15: return 'G'
    if bb > 130 and gg > 120 and rr < 140: return 'c'
    if rr > 80 and bb > 110 and gg < 100: return 'P'
    if bb > 190 and rr < 160 and gg > 130: return 'l'
    return '+'

print("=== diagram LEFT half: x186..500 y254..510, 3px cells (105 cols x 85 rows) ===")
for cy in range(254, 510, 3):
    row = ''
    for cx in range(186, 501, 3):
        cell = a[cy:cy+3, cx:cx+3].reshape(-1, 3)
        med = np.median(cell, axis=0)
        row += cls(med)
    print(f"{cy:3d} {row}")

print()
print("=== diagram RIGHT half: x500..810 y254..510 ===")
for cy in range(254, 510, 3):
    row = ''
    for cx in range(500, 811, 3):
        cell = a[cy:cy+3, cx:cx+3].reshape(-1, 3)
        med = np.median(cell, axis=0)
        row += cls(med)
    print(f"{cy:3d} {row}")
