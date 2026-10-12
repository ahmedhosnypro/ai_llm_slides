#!/usr/bin/env python3
"""Slide 043 raw-pixel scans: stack top bands, right-of-front slivers, arrows, labels."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def hexpx(y, x):
    r, g, b = a[y, x]
    return f"({x},{y})#{r:02X}{g:02X}{b:02X}"

def rowhex(y, xs):
    return " ".join(hexpx(y, x) for x in xs)

def colhex(x, ys):
    return " ".join(hexpx(y, x) for y in ys)

print("=== LEFT STACK top bands: col scans (raw) ===")
for x in [130, 170, 210, 250, 290]:
    print(f"col x={x} y148..190:", colhex(x, range(148, 191, 2)))
print()
print("=== LEFT STACK right-of-front at y=300 (raw, x205..280) ===")
print(rowhex(300, range(203, 281, 3)))
print()
print("=== RIGHT STACK top bands: col scans (raw) ===")
for x in [680, 720, 760, 800, 840, 865]:
    print(f"col x={x} y85..170:", colhex(x, range(85, 171, 3)))
print()
print("=== RIGHT STACK right-of-front at y=250 (raw, x795..880) ===")
print(rowhex(250, range(795, 881, 3)))
print()
print("=== RIGHT STACK front bottom + h-arrow region: col x=690,720,760 y300..350 ===")
for x in [690, 720, 760]:
    print(f"col x={x} y300..350:", colhex(x, range(300, 351, 2)))
print()
print("=== diag arrow region: row y=280,300,320 x770..900 ===")
for y in [280, 300, 320]:
    print(f"row y={y}:", rowhex(y, range(770, 901, 5)))
print()
print("=== vertical arrow: row scans x620..690 at y=200,250,300 ===")
for y in [200, 250, 300]:
    print(f"row y={y}:", rowhex(y, range(620, 691, 2)))
print()
print("=== vertical arrow col profile: x645 y150..345 ===")
print(colhex(645, range(150, 346, 4)))
print()
print("=== h-arrow: col x=660..790 at y=330..345 ===")
for x in [660, 700, 740, 770]:
    print(f"col x={x} y326..348:", colhex(x, range(326, 349, 2)))
