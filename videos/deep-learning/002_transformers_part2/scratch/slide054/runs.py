#!/usr/bin/env python3
"""Print exact class runs per row for a region."""
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

def runs_row(y, x0, x1, minlen=2):
    out = []
    cur = None; start = x0
    for x in range(x0, x1):
        c = classify(y, x)
        if c != cur:
            if cur is not None and x - start >= minlen:
                out.append((start, x-1, cur))
            cur = c; start = x
    if cur is not None and x1 - start >= minlen:
        out.append((start, x1-1, cur))
    return [o for o in out if o[2] != "."] or out

which = sys.argv[1]
if which == "leftrow":
    # horizontal scan through the left container strip 1 + red diagonal
    for y in [228, 230, 233, 236, 240, 244, 246, 252]:
        print(y, runs_row(y, 62, 270))
elif which == "leftcol":
    # vertical scan at x=100 and x=120 (inside container) and x=165 (between container and W_k)
    for x in [80, 100, 110, 130, 150, 165]:
        col = [(y, classify(y, x)) for y in range(210, 395)]
        # compress
        out = []; cur=None; start=210
        for y, c in col:
            if c != cur:
                if cur is not None: out.append((start, y-1, cur))
                cur = c; start = y
        out.append((start, 394, cur))
        print(f"x={x}", out)
