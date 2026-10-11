#!/usr/bin/env python3
"""Coarse color-class ASCII map of slide_037.jpg (96x54 blocks of 10x10px)."""
import numpy as np
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# palette discovered by scanning
PAL = {
    "W": (255, 255, 255),   # white canvas
    "P": (231, 233, 230),   # chrome panel E7E9E6
    "p": (247, 226, 205),   # peach canvas
    "t": (219, 203, 188),   # tan dot product
    "Y": (250, 243, 111),   # yellow (scaling + pills + W boxes?)
    "v": (247, 223, 249),   # light purple softmax
    "s": (235, 253, 253),   # pale cyan sigma box
    "g": (230, 253, 233),   # light green container
    "G": (146, 208, 80),    # med green W boxes
    "k": (0, 176, 80),      # saturated green
    "K": (255, 255, 0),     # saturated yellow
    "M": (255, 102, 204),   # pink
    "R": (255, 0, 0),       # red
    "B": (0, 0, 204),       # blue
    "D": (100, 40, 40),     # dark red/maroon text
    "b": (40, 40, 150),     # blue text
    "x": (0, 0, 0),         # black
    "y": (60, 58, 179),     # sigma blue
}

step = 10
out = []
for by in range(0, H, step):
    line = []
    for bx in range(0, W, step):
        block = a[by:by + step, bx:bx + step].reshape(-1, 3)
        med = np.median(block, axis=0)
        best = min(PAL.items(), key=lambda kv: np.abs(med - np.array(kv[1])).max())
        line.append(best[0])
    out.append("".join(line))
print("   " + "".join(str((i // 10) % 10) for i in range(0, W, step)))
for i, line in enumerate(out):
    print(f"{i * step:3d}" + line)
