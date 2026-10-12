#!/usr/bin/env python3
"""m17_cells.py — exact cell structure: 1px color transitions inside each row band,
vertical extent per column, and far-right region detail."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg"
A = np.asarray(Image.open(F).convert("RGB")).astype(int)
SX, OX, SY = 0.962329, 17.582, 0.955556
sx = lambda x: (x - OX) / SX
sy = lambda y: y / SY
hx = lambda c: "#%02X%02X%02X" % tuple(int(round(v)) for v in c)

def trans(yy, x0, x1, q=18):
    line = A[yy]
    out, prev, runstart = [], None, x0
    for x in range(x0, x1):
        c = tuple((line[x] // q) * q)
        if prev is None:
            prev, runstart = c, x
        elif c != prev:
            if x - runstart >= 3:
                out.append(f"{sx(runstart):.0f}-{sx(x):.0f}:{hx(np.median(line[runstart:x],axis=0))}")
            prev, runstart = c, x
    out.append(f"{sx(runstart):.0f}-{sx(x1):.0f}:{hx(np.median(line[runstart:x1],axis=0))}")
    return out

ROWS = {"output": (59, 74), "A": (172, 190), "B": (281, 298), "C": (383, 400), "X": (494, 509)}
for name, (y0, y1) in ROWS.items():
    ymid = (y0 + y1) // 2
    print(f"== {name} band {y0}..{y1} (slide {sy(y0):.1f}..{sy(y1):.1f}) ==")
    print(f"  y={y0+2}:", " ".join(trans(y0 + 2, 178, 910)))
    print(f"  y={y1-2}:", " ".join(trans(y1 - 2, 178, 910)))

print("== vertical extent at col centers (cell outlines) ==")
for name, cx in [("col1", 205), ("col8", 833)]:
    for name2, (y0, y1) in ROWS.items():
        col = A[y0 - 6:y1 + 6, cx]
        dk = [y0 - 6 + i for i, c in enumerate(col) if c.sum() < 500]
        if dk:
            print(f" {name} {name2}: dark rows {dk[0]}..{dk[-1]} -> slide {sy(dk[0]):.1f}..{sy(dk[-1]):.1f}")

print("== far right of output row (frame x 855..915, y 55..80) ==")
for yy in (62, 67, 71):
    print(f" y={yy}:", [(x, hx(A[yy, x])) for x in range(858, 912, 3)])
