#!/usr/bin/env python3
"""1px-resolution ASCII of a small region."""
from PIL import Image
import numpy as np
import sys

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)

def classify(y, x):
    r, g, b = A[y, x]
    if r < 110 and g < 110 and b < 110: return "K"
    if r - g >= 70 and r - b >= 60 and r >= 150: return "R"
    if b - r >= 60 and b >= 130: return "B"
    if r >= 190 and b >= 190 and g <= 175 and r - g >= 40: return "M"
    if r >= 235 and g >= 235 and b <= 215 and r - b >= 35: return "Y"
    if g - r >= 14 and g - b >= 14 and g >= 228: return "G"
    if abs(r-245)<=10 and abs(g-209)<=12 and abs(b-246)<=10: return "P"
    if abs(r-216)<=15 and abs(g-200)<=15 and abs(b-185)<=15: return "T"
    if abs(r-247)<=8 and abs(g-212)<=10 and abs(b-215)<=10: return "S"
    if r >= 238 and g >= 238 and b >= 238: return "W"
    if abs(r-231)<=6 and abs(g-231)<=6 and abs(b-231)<=6: return "E"
    return "."

x0, x1, y0, y1 = map(int, sys.argv[1:5])
print("     " + "".join(str(x // 10 % 10) for x in range(x0, x1)))
print("     " + "".join(str(x % 10) for x in range(x0, x1)))
for y in range(y0, y1):
    print(f"{y:4d} " + "".join(classify(y, x) for x in range(x0, x1)))
