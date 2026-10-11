#!/usr/bin/env python3
"""Red/green ink density maps: 4px blocks, showing arrow topology."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

strong_red = (R - G > 70) & (R - B > 70) & (R > 140)
faint_red = (R - G > 25) & (R - B > 25) & (R > 150) & ~strong_red
green = (G - R > 40) & (G - B > 20) & (G > 110) & (R < 190)
darkred = (R - G > 45) & (R - B > 45) & (R > 110) & (R < 200) & (G < 100)

def density_map(mask, y0, y1, x0, x1, blk=4):
    sub = mask[y0:y1, x0:x1]
    h, w = sub.shape
    H2, W2 = h // blk, w // blk
    print(f"    x={x0}", "".join(str((x0 + i * blk) // 10 % 10) for i in range(W2)))
    for by in range(H2):
        row = ""
        for bx in range(W2):
            c = sub[by * blk:(by + 1) * blk, bx * blk:(bx + 1) * blk].sum()
            row += " " if c == 0 else ("." if c <= 2 else ("+" if c <= 6 else ("#" if c <= 12 else "@")))
        print(f"{y0 + by * blk:4d} {row}")

which = sys.argv[1]
y0, y1, x0, x1 = map(int, sys.argv[2:6])
m = {"red": strong_red, "faint": faint_red, "green": green, "darkred": darkred}[which]
density_map(m, y0, y1, x0, x1, int(sys.argv[6]) if len(sys.argv) > 6 else 4)
