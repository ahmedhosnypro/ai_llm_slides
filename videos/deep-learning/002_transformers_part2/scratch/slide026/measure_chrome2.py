#!/usr/bin/env python3
"""Measure slide_026.jpg chrome landmarks precisely, in expected neighborhoods."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# red-ish (dark red border C00000): r high, g/b low
red = (r > 120) & (g < 100) & (b < 100)

def vscan(x0, x1, y0, y1, label):
    """find vertical red line: for each col, max consecutive-ish run"""
    best = []
    for x in range(x0, x1):
        cnt = red[y0:y1, x].sum()
        best.append((x, int(cnt)))
    best.sort(key=lambda t: -t[1])
    print(label, best[:6])
    return best[0]

def hscan(y0, y1, x0, x1, label):
    best = []
    for y in range(y0, y1):
        cnt = red[x0:x1, y].sum()
        best.append((y, int(cnt)))
    best.sort(key=lambda t: -t[1])
    print(label, best[:6])
    return best[0]

# expected (from slide_002 mapping): left ~59, right ~902, top ~43, bottom ~516
L = vscan(45, 75, 100, 450, "left border col:")
R = vscan(885, 915, 100, 450, "right border col:")
T = hscan(30, 60, 150, 800, "top border row:")
B = hscan(500, 530, 150, 800, "bottom border row:")

# badge: yellow circle near (875,70); fill FDFD96 (253,253,150)
sub_y0, sub_y1, sub_x0, sub_x1 = 40, 105, 840, 910
yellow = (r > 210) & (g > 210) & (b > 110) & (b < 200)
ys, xs = np.nonzero(yellow[sub_y0:sub_y1, sub_x0:sub_x1])
if len(xs):
    xs = xs + sub_x0; ys = ys + sub_y0
    print(f"badge yellow bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} center ({(xs.min()+xs.max())/2},{(ys.min()+ys.max())/2}) n={len(xs)}")
else:
    print("no badge yellow found in neighborhood")

# ring: purple 6A5ACD ~ (106,90,205)
purple = (b > 150) & (r > 60) & (r < 160) & (g < 130)
ys2, xs2 = np.nonzero(purple[sub_y0:sub_y1, sub_x0:sub_x1])
if len(xs2):
    xs2 = xs2 + sub_x0; ys2 = ys2 + sub_y0
    print(f"badge ring bbox: x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} center ({(xs2.min()+xs2.max())/2},{(ys2.max()+ys2.min())/2}) n={len(xs2)}")
