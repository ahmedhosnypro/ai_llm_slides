#!/usr/bin/env python3
"""Fine ASCII map of a crop region, 4px blocks, extended palette."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

x0, y0, x1, y1, step = (int(v) for v in sys.argv[1:6])

PAL = {
    ".": (247, 226, 205),   # peach canvas
    "t": (219, 203, 188),   # tan dot product
    "T": (168, 133, 124),   # dark tan/salmon (arrow blur)
    "Y": (250, 243, 111),   # yellow scaling
    "y": (252, 254, 221),   # pale pill yellow
    "v": (247, 223, 249),   # purple softmax
    "s": (235, 253, 253),   # pale cyan sigma
    "g": (231, 254, 233),   # light green container
    "G": (146, 208, 80),    # med green
    "k": (0, 176, 80),      # sat green
    "K": (255, 255, 0),     # sat yellow
    "M": (255, 102, 204),   # pink
    "R": (255, 0, 0),       # red
    "r": (139, 0, 10),      # dark red text
    "B": (0, 0, 204),       # blue
    "b": (60, 58, 179),     # blue text
    "x": (0, 0, 0),         # black
    "d": (120, 100, 90),    # dark gray-brown
    "W": (255, 255, 255),   # white
    "P": (231, 233, 230),   # panel gray
}

for by in range(y0, y1, step):
    line = []
    for bx in range(x0, x1, step):
        block = a[by:by + step, bx:bx + step].reshape(-1, 3)
        med = np.median(block, axis=0)
        best = min(PAL.items(), key=lambda kv: np.abs(med - np.array(kv[1])).max())
        line.append(best[0])
    print(f"{by:3d} " + "".join(line))
