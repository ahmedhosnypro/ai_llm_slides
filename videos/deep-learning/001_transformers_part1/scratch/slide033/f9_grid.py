#!/usr/bin/env python3
"""Numeric color grid dumps for precise fill sampling."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)

def grid(y0, y1, x0, x1, sy=2, sx=2):
    print(f"== grid y[{y0}..{y1}] x[{x0}..{x1}] step {sy}x{sx}; each cell '#RRGGBB'")
    hdr = "      " + "".join(f"{x:<7d}" for x in range(x0, x1, sx))
    print(hdr)
    for y in range(y0, y1, sy):
        row = f"{y:4d}  " + " ".join(f"{a[y,x,0]:02x}{a[y,x,1]:02x}{a[y,x,2]:02x}" for x in range(x0, x1, sx))
        print(row)

which = sys.argv[1]
if which == "leftrow1":
    grid(236, 258, 60, 142, 2, 2)
elif which == "rightrow1":
    grid(236, 258, 764, 846, 2, 2)
elif which == "wkbox":
    grid(226, 292, 148, 202, 3, 3)
elif which == "dotprod":
    grid(194, 250, 252, 348, 3, 3)
elif which == "softmax":
    grid(194, 230, 455, 494, 3, 3)
elif which == "sigma":
    grid(190, 222, 510, 662, 3, 3)
elif which == "vrow1":
    grid(228, 246, 636, 700, 2, 2)
elif which == "y2box":
    grid(116, 172, 540, 620, 2, 2)
elif which == "pill1":
    grid(158, 190, 270, 345, 2, 2)
elif which == "panelborder":
    grid(104, 114, 380, 420, 1, 2)
