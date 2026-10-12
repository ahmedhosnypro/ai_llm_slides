#!/usr/bin/env python3
"""Raw column scans through the right architecture to read box fills/borders."""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)

def scan_col(x, y0, y1, step=2):
    print(f"--- col x={x} ---")
    prev = None
    for y in range(y0, y1, step):
        p = im[y, x]
        cur = (p[0] // 24, p[1] // 24, p[2] // 24)
        if cur != prev:
            print(f"  y={y:3d} #{p[0]:02X}{p[1]:02X}{p[2]:02X} {tuple(int(v) for v in p)}")
            prev = cur

# decoder top: Output Probabilities / Softmax / Linear boxes
scan_col(785, 105, 200)
# decoder stack: gray/olive boxes + MHA
scan_col(770, 185, 335)
# decoder purple box + PE + embedding
scan_col(790, 325, 500)
# encoder stack
scan_col(686, 260, 520)
# encoder left part (Add&Norm labels region)
scan_col(620, 260, 520)
