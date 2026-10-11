#!/usr/bin/env python3
"""m18: fine border-line scan of enc container on slide_016.jpg.
For each row y255-415, list runs of DARK BROWN border pixels (the container stroke
color ~ (110-160, 60-115, 25-90)) within x610-745, to map horizontal borders and
rounded corners -> one container vs two sub-blocks.
Also: column scan at x=628..632 and x=724..730 to see vertical border continuity
(a gap in the left border between y~317-320 = two separate rounded blocks).
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

dark = (r >= 40) & (r <= 170) & (g >= 20) & (g <= 125) & (b <= 105) & (r > g) & (g >= b - 10)

def row_runs(y, x0, x1):
    idx = np.where(dark[y, x0:x1])[0] + x0
    if len(idx) == 0:
        return None
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i == p + 1:
            p = i
        else:
            out.append((s, p)); s = p = i
    out.append((s, p))
    return out

print("== rows with dark-brown border runs, y255-415, x610-745 ==")
for y in range(255, 416):
    rr = row_runs(y, 610, 745)
    if rr:
        print(f"y={y}: " + "  ".join(f"{a}-{bb}" for a, bb in rr))
