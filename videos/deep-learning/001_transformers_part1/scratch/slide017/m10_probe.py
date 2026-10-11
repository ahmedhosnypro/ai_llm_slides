#!/usr/bin/env python3
"""Sample the unclassified regions and remaining structure points."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def avg(x0, y0, x1, y1):
    r = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    return tuple(int(v) for v in r.mean(axis=0))

pts = [
    ("dec top ? region A", 770, 160, 790, 175),
    ("dec top ? region B", 790, 205, 810, 220),
    ("dec top ? region C", 800, 130, 820, 142),
    ("dec ltgreen stripe", 834, 250, 838, 350),
    ("dec Nx badge", 848, 303, 864, 319),
    ("dec right of stripe", 845, 250, 855, 350),
    ("dec yellow top band", 770, 113, 820, 127),
    ("dec R at y117", 745, 117, 753, 126),
    ("enc top empty", 600, 150, 700, 250),
    ("enc label 'Encoder'", 585, 117, 620, 127),
    ("enc PE label", 578, 210, 620, 250),
    ("enc PE label2", 580, 155, 640, 200),
    ("dec PE label right", 840, 430, 895, 470),
    ("dec PE label2", 840, 475, 895, 490),
    ("yellow cross band", 690, 252, 740, 320),
    ("cross paths", 680, 250, 676, 0) if False else ("cross paths row260", 678, 258, 745, 262),
    ("block arrow dec top", 785, 130, 800, 145),
    ("feedback arrow right", 895, 200, 905, 400),
    ("feedback arrow right2", 885, 450, 900, 500),
]
for name, x0, y0, x1, y1 in pts:
    print(f"{name:26s} [{x0},{y0}..{x1},{y1}] = {avg(x0,y0,x1,y1)}")

# scan column x=836 (the light-green stripe)
print("\ncol x=836:")
cur = None
for y in range(100, 540):
    px = tuple(int(v) for v in A[y, 836])
    if cur is None or np.abs(A[y, 836] - cur[2]).sum() > 40:
        if cur: print(f"   y{cur[0]:3d}..{y-1:3d} rgb{tuple(int(v) for v in cur[2])}")
        cur = [y, y, A[y, 836]]
    else:
        cur[1] = y
        cur[2] = (cur[2]*3 + A[y, 836]) // 4
if cur: print(f"   y{cur[0]:3d}..{cur[1]:3d} rgb{tuple(int(v) for v in cur[2])}")
