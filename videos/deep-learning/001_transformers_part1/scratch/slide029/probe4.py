#!/usr/bin/env python3
"""c2 text band pixel map with dark+mag predicate."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)

def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r > 130 and r - g > 60 and r - b > 60: return "R"
    if 120 < r < 215 and g < 140 and b > 130 and b - g > 35: return "M"
    if r + g + b < 330: return "k"
    return "."

print("== c2 x648..848 y140..186, ink only (step1) ==")
print("      " + "".join(str((648 + i) // 10 % 10) for i in range(0, 200)))
for y in range(140, 187):
    row = "".join(cls(A[y, 648 + i]) for i in range(0, 200))
    if row.strip("."):
        print(f"y{y:3d} {row}")
