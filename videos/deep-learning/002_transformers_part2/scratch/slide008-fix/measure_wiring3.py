#!/usr/bin/env python3
"""Pass 3 — fine 1px ASCII maps to settle: softmax right-edge structures,
feed lanes, arrowhead shapes (read-only)."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)

def amap(x0, x1, y0, y1, step=1):
    """ASCII map; '#'=strong red, '+'=mid red, '.'=faint red, ' '=bg."""
    hdr = "    " + "".join(str((x0 + i) % 10) for i in range(0, x1 - x0 + 1, step))
    print(hdr)
    for y in range(y0, y1 + 1, step):
        line = []
        for x in range(x0, x1 + 1, step):
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
        print(f"{y:3d} " + "".join(line))

print("=== MAP 1: softmax right edge + feed starts, x 486..520, y 224..326 ===")
amap(486, 520, 224, 326)

print("\n=== MAP 2: stem arrowheads under Sigma, x 524..624 (step 2), y 208..226 ===")
amap(524, 624, 208, 226, step=2)
