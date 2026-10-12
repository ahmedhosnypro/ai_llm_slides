#!/usr/bin/env python3
"""Pass 4 — 1px maps of the full ring band: stems, feeds, right-side wiring (read-only)."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)

def amap(x0, x1, y0, y1):
    print("     " + "".join(str((x0 + i) % 10) for i in range(0, x1 - x0 + 1)))
    for y in range(y0, y1 + 1):
        line = []
        for x in range(x0, x1 + 1):
            r, g, b = frame[y, x]
            rg, rb = r - g, r - b
            if rg >= 60 and rb >= 60 and r >= 150:
                line.append("#")
            elif rg >= 25 and rb >= 25 and r >= 150:
                line.append("+")
            elif r < 228 and rg >= 12 and rb >= 12:
                line.append(".")
            else:
                line.append(" ")
        print(f"{y:3d}  " + "".join(line))

print("=== MAP A: x 545..660, y 210..265 (ring1 right / stem2 / ring2 top / V4) ===")
amap(545, 660, 210, 265)
