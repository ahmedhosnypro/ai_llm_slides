#!/usr/bin/env python3
"""Targeted color profiles for slide_055.jpg — resolve columns, pills, boxes, arrows."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
A = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = A.shape

def q(r, g, b):
    if r >= 240 and g >= 238 and b >= 232 and abs(r-g) < 14 and (r-b) < 18: return "WHITE"
    if r >= 240 and g >= 230 and 185 <= b <= 225: return "PEACH"
    if r >= 235 and g >= 235 and b <= 190 and r - b >= 60: return "YELLOW"
    if 200 <= r <= 250 and 200 <= g <= 250 and 150 <= b <= 210 and abs(int(r)-int(g)) < 25 and r-b >= 18: return "PALEYEL"
    if r < 150 and g < 150 and b < 150: return "DARK"
    if r - g >= 60 and r - b >= 50 and r >= 140: return "RED"
    if g - r >= 12 and g - b >= 12 and g >= 225: return "PALEGRN"
    if g - r >= 40 and g - b >= 40: return "GREEN"
    if b - r >= 40 and b >= 150: return "BLUE"
    if b - r >= 12 and b - g >= 8 and b >= 220 and r >= 170: return "LTBLUE"
    if r >= 190 and b >= 150 and r - g >= 30 and b - g >= 20: return "PINK/MAG"
    if r - g >= 25 and abs(int(r)-int(b)) < 40 and 150 <= r <= 230 and b <= r: return "TAN"
    return f"other({r},{g},{b})"

def hprofile(y, x0, x1, step=1):
    print(f"\n== h-profile y={y} x {x0}..{x1} ==")
    prev = None; run0 = x0
    for x in range(x0, x1, step):
        r, g, b = A[y, x]
        lab = q(int(r), int(g), int(b))
        if lab != prev:
            if prev is not None: print(f"   x {run0}..{x-1}: {prev}")
            prev = lab; run0 = x
    print(f"   x {run0}..{x1-1}: {prev}")

def vprofile(x, y0, y1):
    print(f"\n== v-profile x={x} y {y0}..{y1} ==")
    prev = None; run0 = y0
    for y in range(y0, y1):
        r, g, b = A[y, x]
        lab = q(int(r), int(g), int(b))
        if lab != prev:
            if prev is not None: print(f"   y {run0}..{y-1}: {prev}")
            prev = lab; run0 = y
    print(f"   y {run0}..{y1-1}: {prev}")

# mid-diagram horizontal cuts
hprofile(300, 60, 900)
hprofile(200, 280, 900)
hprofile(160, 280, 700)   # pills row?
hprofile(250, 280, 900)   # upper rows: dots / nodes
hprofile(350, 280, 900)
hprofile(470, 180, 900)   # Z row / legend
hprofile(430, 250, 700)   # W_q / caption row
# vertical cuts
vprofile(425, 110, 500)   # scaling column
vprofile(500, 110, 500)   # softmax column?
vprofile(545, 110, 500)
vprofile(600, 110, 500)   # sigma / O
vprofile(140, 100, 500)   # left container
vprofile(820, 100, 500)   # right container
vprofile(60, 130, 220)    # far-left edge: hatched callout + arrow
vprofile(905, 130, 220)   # far-right edge
vprofile(240, 100, 520)   # W_k / K strips / Z row
vprofile(360, 100, 520)   # dot product box
