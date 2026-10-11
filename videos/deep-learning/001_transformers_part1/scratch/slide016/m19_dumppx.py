#!/usr/bin/env python3
"""m19: pixel dumps to resolve enc container structure on slide_016.jpg."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)

def dump_row(y, x0, x1, step=1):
    cells = []
    for x in range(x0, x1 + 1, step):
        p = im[y, x]
        cells.append(f"{x}:({p[0]},{p[1]},{p[2]})")
    print(f"y={y}: " + " ".join(cells))

print("== rows through the y286-291 double line, x626-732 ==")
for y in (284, 285, 286, 287, 288, 289, 290, 291, 292):
    dump_row(y, 626, 732, 6)

print()
print("== rows through y316-322, x626-732 ==")
for y in (314, 315, 316, 317, 318, 319, 320, 321, 322):
    dump_row(y, 626, 732, 6)

print()
print("== rows through y339-344 and y352-360, x626-732 ==")
for y in (339, 340, 341, 342, 343, 352, 353, 354, 355, 356, 357, 358, 359):
    dump_row(y, 626, 732, 6)

print()
print("== rows through y381-386, y401-411, x626-732 ==")
for y in (381, 382, 383, 384, 385, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411):
    dump_row(y, 626, 732, 6)

print()
print("== columns x627-634 and x725-733, rows y265-412 step 4 (right border continuity) ==")
for x in (627, 628, 629, 630, 631):
    vals = []
    for y in range(265, 413, 8):
        p = im[y, x]
        vals.append(f"y{y}:({p[0]},{p[1]},{p[2]})")
    print(f"x={x}: " + " ".join(vals))
for x in (725, 726, 727, 728, 729, 730, 731):
    vals = []
    for y in range(265, 413, 8):
        p = im[y, x]
        vals.append(f"y{y}:({p[0]},{p[1]},{p[2]})")
    print(f"x={x}: " + " ".join(vals))
