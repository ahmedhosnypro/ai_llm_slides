#!/usr/bin/env python3
"""ASCII-render a region so the worker can 'read' the layout.
Each cell = avg of STEPxSTEP block; mapped to a letter by nearest palette color.
Usage: python3 m7_ascii.py <img> <x0> <x1> <y0> <y1> <step>"""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
x0, x1, y0, y1, step = (int(v) for v in sys.argv[2:7])

PAL = {
    ".": (255, 255, 255), "g": (233, 233, 231),
    "T": (222, 170, 116),   # left panel tan
    "i": (235, 182, 128),   # left inner tan
    "B": (210, 150, 100),   # tan-brown box family
    "R": (190, 30, 20),     # red
    "D": (150, 10, 30),     # dark red
    "G": (20, 150, 70),     # green
    "d": (55, 105, 75),     # dark green
    "Y": (250, 250, 60),    # yellow
    "L": (200, 130, 200),   # lavender/pink-purple
    "P": (120, 60, 170),    # purple
    "b": (60, 70, 200),     # blue
    "n": (95, 160, 170),    # steel teal
    "N": (210, 250, 225),   # pale green container
    "E": (252, 235, 218),   # peach
    "K": (160, 160, 160),   # gray
    "x": (110, 115, 105),   # dark gray-olive
    "k": (35, 35, 35),      # near black
    "o": (175, 185, 125),   # olive
    "m": (160, 90, 90),     # maroon
    "w": (150, 200, 170),   # pale green box (softmax/linear)
}

def cell_color(cx, cy):
    blk = im[cy:cy + step, cx:cx + step].reshape(-1, 3)
    return blk.mean(axis=0)

out = []
hdr = "    " + "".join(str((x0 + i * step) // 100 % 10) for i in range((x1 - x0) // step))
hdr2 = "    " + "".join(str((x0 + i * step) // 10 % 10) for i in range((x1 - x0) // step))
out.append(hdr)
out.append(hdr2)
for cy in range(y0, y1, step):
    row = []
    for cx in range(x0, x1, step):
        c = cell_color(cx, cy)
        best, bd = "?", 1e9
        for ch, p in PAL.items():
            d = sum((int(c[i]) - p[i]) ** 2 for i in range(3))
            if d < bd:
                bd, best = d, ch
        row.append(best)
    out.append(f"{cy:3d} " + "".join(row))
print("\n".join(out))
