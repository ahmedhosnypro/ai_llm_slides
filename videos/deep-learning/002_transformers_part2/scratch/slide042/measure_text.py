#!/usr/bin/env python3
"""Definitive pass: per-row ink classification in label boxes (true coords),
faint border scan, exact cube scanlines, right-block layer geometry, arrows."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 240 and G > 240 and B > 235: return "."
    if R > 140 and G < 120 and B < 120 and R - G > 50 and R - B > 50: return "R"   # red
    if B > 120 and B - R > 30 and B - G > 20: return "B"                            # blue
    if G > 120 and G - R > 40 and G - B > 60: return "G"                            # bright green
    if G > 90 and G - R > 20 and G - B > 40: return "d"                             # mid/dark green
    if R > 120 and B > 120 and G < 110: return "M"                                  # magenta
    if R > 170 and G > 150 and B < 130: return "Y"                                  # yellow
    if R > 170 and 80 < G < 170 and B < 100: return "O"                             # orange
    if R < 100 and G < 100 and B < 100: return "K"                                  # dark
    return "?"

def classify_region(x0, x1, y0, y1, name):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1} — per-row color runs (min 2px)")
    for y in range(y0, y1):
        codes = [cls(a[y, x]) for x in range(x0, x1)]
        runs, cur, st = [], None, 0
        for i, c in enumerate(codes + [None]):
            if c != cur:
                if cur is not None and i - st >= 2 and cur not in ".":
                    runs.append((cur, x0 + st, x0 + i - 1))
                cur, st = c, i
        if runs:
            print(f"  y{y}: " + " ".join(f"{c}[{s}-{e}]" for c, s, e in runs))

# 1) label boxes: full text + border region
classify_region(88, 320, 188, 240, "LEFT BOX")
print()
classify_region(330, 600, 188, 240, "MIDDLE BOX")
print()
classify_region(625, 895, 160, 235, "RIGHT BOX")
