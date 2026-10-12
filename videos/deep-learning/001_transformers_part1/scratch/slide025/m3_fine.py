#!/usr/bin/env python3
"""Fine region maps: classify pixels against a named palette and print run maps.
Usage: python3 m3_fine.py <img> <region>  ; region in {left, center, right}
"""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
H, W = im.shape[:2]
region = sys.argv[2]

PAL = {
    "W": (255, 255, 255),   # white
    "g": (233, 233, 231),   # panel gray
    "T": (224, 170, 117),   # left panel tan
    "i": (235, 182, 128),   # left inner tan (lighter)
    "B": (232, 213, 181),   # beige box
    "G": (0, 166, 81),      # green
    "d": (60, 130, 60),     # dark green
    "R": (192, 0, 0),       # red
    "D": (148, 5, 28),      # dark red bubble
    "b": (30, 60, 160),     # blue
    "P": (112, 48, 160),    # purple
    "L": (195, 166, 216),   # lavender
    "l": (209, 128, 195),   # decoder purple-pink
    "Y": (255, 255, 0),     # yellow
    "K": (166, 166, 166),   # gray
    "S": (214, 214, 214),   # light gray shadow
    "E": (254, 237, 221),   # peach container
    "C": (198, 156, 109),   # tan box
    "c": (200, 126, 87),    # salmon box
    "M": (158, 74, 74),     # maroon
    "N": (205, 255, 222),   # decoder container lt-green
    "F": (154, 169, 128),   # olive-ish (decoder FF?)
    "A": (149, 200, 167),   # teal-green (decoder Linear?)
    "k": (40, 40, 40),      # near-black
    "x": (128, 128, 128),   # mid gray text
}

def classify(p):
    best, bd = "?", 1e9
    for ch, (pr, pg, pb) in PAL.items():
        d = (p[0]-pr)**2 + (p[1]-pg)**2 + (p[2]-pb)**2
        if d < bd:
            bd, best = d, ch
    if bd > 3600:
        return "?"
    return best

def runs_row(y, x0, x1):
    out, cur, start = [], None, x0
    row = [classify(im[y, x]) for x in range(x0, x1)]
    for i, c in enumerate(row + ["END"]):
        if c != cur:
            if cur is not None and i - start >= 1:
                out.append(f"{x0+start}-{x0+i-1}{cur}")
            cur, start = c, i
    return " ".join(out)

def runs_col(x, y0, y1):
    out, cur, start = [], None, y0
    col = [classify(im[y, x]) for y in range(y0, y1)]
    for i, c in enumerate(col + ["END"]):
        if c != cur:
            if cur is not None and i - start >= 1:
                out.append(f"{y0+start}-{y0+i-1}{cur}")
            cur, start = c, i
    return " ".join(out)

REG = {
    "left": (40, 215, 200, 530),
    "center": (290, 515, 200, 525),
    "right": (565, 900, 95, 530),
}
x0, x1, y0, y1 = REG[region]
step = 4
print(f"### region {region} rows y={y0}..{y1} step {step}")
for y in range(y0, y1, step):
    print(f"y={y:3d}: {runs_row(y, x0, x1)}")
print(f"### region {region} cols x={x0}..{x1} step {step}")
for x in range(x0, x1, step):
    print(f"x={x:3d}: {runs_col(x, y0, y1)}")
