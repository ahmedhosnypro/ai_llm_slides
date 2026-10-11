#!/usr/bin/env python3
"""Fine ASCII maps (2px/char) of key regions, on demand."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

PAL = [
    (" ", lambda r, g, b: False),
    ("W", lambda r, g, b: r > 238 and g > 238 and b > 238),                    # white
    ("p", lambda r, g, b: r > 235 and 215 < g < 242 and 190 < b < 222),        # peach
    ("g", lambda r, g, b: 222 < r < 246 and 222 < g < 246 and 218 < b < 246 and abs(r-g) < 10),  # gray chrome
    ("G", lambda r, g, b: g > 228 and r > 215 and b > 215 and g - r > 8 and g - b > 8),  # pale green fill
    ("n", lambda r, g, b: g > 120 and g - r > 45 and g - b > 30 and r < 180),  # green stroke
    ("Y", lambda r, g, b: r > 235 and g > 235 and b < 180),                    # yellow fill
    ("y", lambda r, g, b: r > 242 and g > 242 and 180 <= b < 228),             # pale yellow
    ("o", lambda r, g, b: r > 150 and 80 < g < 190 and b < 90 and r - g > 25), # orange
    ("T", lambda r, g, b: 195 < r < 235 and 180 < g < 220 and 165 < b < 205),  # taupe
    ("O", lambda r, g, b: r > 235 and 200 < g < 240 and b > 235 and r-g > 6 and b-g > 6),  # orchid/pink
    ("B", lambda r, g, b: b > 235 and r > 190 and g > 215 and b - g > 8),      # light blue
    ("b", lambda r, g, b: b > 110 and b - r > 60 and b - g > 40 and r < 120),  # blue
    ("d", lambda r, g, b: r < 100 and g < 100 and b > 110),                    # dark blue
    ("r", lambda r, g, b: r > 130 and r - g > 60 and r - b > 60 and g < 140),  # red
    ("R", lambda r, g, b: 100 < r < 210 and r - g > 55 and r - b > 55),        # muted red/dark-red text
    ("m", lambda r, g, b: r > 170 and b > 170 and g < 120),                    # magenta
    ("k", lambda r, g, b: r < 100 and g < 100 and b < 100),                    # black
    ("s", lambda r, g, b: 160 < r < 225 and 140 < g < 205 and b > 195 and b - g > 15),  # lavender
    ("q", lambda r, g, b: 215 < r < 250 and 205 < g < 245 and 110 < b < 175),  # khaki
    ("h", lambda r, g, b: r > 230 and 165 < g < 215 and 175 < b < 225 and r-g > 25),  # pink sq
    ("c", lambda r, g, b: 100 < r < 220 and 100 < g < 220 and 100 < b < 220),  # mid gray (fallback)
]

def classify_block(y0, y1, x0, x1):
    out = []
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            r, g, b = a[y, x]
            ch = " "
            for c, f in PAL[1:]:
                if f(r, g, b):
                    ch = c
                    break
            row.append(ch)
        out.append("".join(row))
    return out

def show(name, y0, y1, x0, x1, step=2):
    print(f"== {name} x[{x0}..{x1}] y[{y0}..{y1}] 2px/char, col ruler mod 10")
    hdr1 = "     " + "".join(str((x0 + i * step) // 10 % 10) for i in range(0, (x1 - x0) // step))
    print(hdr1)
    for i, row in enumerate(classify_block(y0, y1, x0, x1, )):
        if i % 2 == 0:
            print(f"{y0 + i:4d} {row[:]}")
        else:
            print(f"     {row[:]}")

if __name__ == "__main__":
    import json
    regions = json.loads(sys.argv[1])
    for nm, y0, y1, x0, x1 in regions:
        show(nm, y0, y1, x0, x1)
