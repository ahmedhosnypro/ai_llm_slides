#!/usr/bin/env python3
"""Slide 038 — m18: full ASCII grids of the top-row tail labels (col7, col8) and col1/col2
labels with WIDE windows, loose red-ink classification, to settle subscript widths/digits."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)

def grid(x0, x1, y0, y1, label):
    print(f"== {label} (x{x0}..{x1}, y{y0}..{y1}) ==")
    hdr1 = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1))
    hdr2 = "     " + "".join(str(x % 10) for x in range(x0, x1))
    print(hdr1); print(hdr2)
    for y in range(y0, y1):
        row = ""
        for x in range(x0, x1):
            r, g, b = img[y, x]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            redness = r - (g + b) / 2
            if redness > 60 and r > 110: row += "#" if redness > 110 else "+"
            elif lum < 120: row += "k"          # dark (borders)
            elif lum < 190: row += "-"          # mid
            else: row += "."
        print(f"y{y}: {row}")

grid(742, 800, 259, 279, "TOP col7 tail label Y_?")
grid(815, 862, 259, 279, "TOP col8 tail label Y_?")
grid(190, 232, 259, 279, "TOP col1 label")
grid(264, 300, 259, 279, "TOP col2 label")
