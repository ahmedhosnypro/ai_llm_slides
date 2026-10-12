#!/usr/bin/env python3
"""measure11_ascii.py — ASCII ink maps for label zones (read extents directly)."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
S = r + g + b

navy = (b - r > 35) & (S < 500)
redl = (r - g > 35) & (r - b > 35) & (S < 560)
dark = S < 430

def art(mask, y0, y1, x0, x1, step=2, label=""):
    print(f"== {label} y{y0}-{y1} x{x0}-{x1} (cols mod {step}) ==")
    hdr = "     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1):
        row = ""
        for x in range(x0, x1, step):
            row += "#" if mask[y, x] else "."
        if row.strip("."):
            print(f"y{y:3d} {row}")

art(navy, 136, 198, 55, 170, 1, "LABEL BLOCK 1 (navy)")
art(redl, 214, 274, 55, 170, 1, "LABEL BLOCK 3 (red lines + navy paren)")
