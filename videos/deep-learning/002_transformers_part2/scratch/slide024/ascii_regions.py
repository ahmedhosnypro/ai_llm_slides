#!/usr/bin/env python3
"""ASCII-dump blue/red masks for ambiguous regions of the rules box."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)

def dump(y0, y1, x0, x1, tag):
    print(f"--- {tag} (frame y {y0}..{y1}, x {x0}..{x1}) ---")
    reg = img[y0:y1, x0:x1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (b > 100) & (b > r + 30)
    red = (r > 110) & (r > b + 40) & (g < r - 30)
    for yy in range(reg.shape[0]):
        line = ""
        for xx in range(reg.shape[0] and reg.shape[1]):
            if red[yy, xx]: line += "R"
            elif blue[yy, xx]: line += "#"
            else: line += "."
        print(f"{y0+yy:3d} {line}")

dump(362, 386, 262, 312, "L1 'same' zone (mystery run row 371)")
dump(408, 432, 678, 728, "L3 mystery run rows 414-418")
dump(452, 476, 580, 712, "L5 underline zone A")
dump(452, 476, 820, 885, "L5 underline zone B (Embedding?)")
