#!/usr/bin/env python3
"""Classification-grid census of 002:slide_008.jpg delta zones.

Prints 3px-cell classification grids so structure is readable without eyes.
"""
import numpy as np
from PIL import Image

F8 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
im = np.asarray(Image.open(F8).convert("RGB")).astype(int)

# sample the actual palette from known regions first
def sample(x, y): return tuple(im[y, x])

def classify(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R < 70 and G < 70 and B < 70: return "#"          # dark text/ink
    if R > 150 and R - G > 60 and R - B > 60: return "R"  # red
    if R > 200 and G > 200 and B < 180: return "Y"        # yellow
    if G > 140 and G - R > 25 and G - B > 15: return "G"  # saturated green
    if G > 200 and R > 150 and B > 150 and G - R > 20: return "g"  # pale green (E7FFE9/mint)
    if B > 200 and G > 190 and R < 215 and B - R > 20: return "b"  # pale blue (B8D8F0)
    if B > 130 and B - R > 25 and B - G > 10 and R < 190: return "B"  # mid blue
    if R > 170 and B > 170 and G < R - 12 and G < B - 12: return "P"  # purple/lavender
    if R > 200 and G > 120 and G < 190 and B > 140: return "m"  # pink/magenta
    if R > 225 and G > 195 and B > 170: return "."         # peach/white bg
    if abs(R - G) < 18 and abs(G - B) < 18 and R < 200: return "-"  # gray
    return "?"

def grid(x0, x1, y0, y1, step, title):
    print(f"\n== {title} (x {x0}..{x1}, y {y0}..{y1}, step {step}) ==")
    for y in range(y0, y1, step):
        row = "".join(classify(im[y, x]) for x in range(x0, x1, step))
        print(f"{y:3d} {row}")
    hdr = "    " + "".join(str((x // 10) % 10) for x in range(x0, x1, step))
    print(hdr)

grid(130, 250, 210, 420, 4, "W_k left column")
grid(650, 760, 210, 420, 4, "W_v right column")
