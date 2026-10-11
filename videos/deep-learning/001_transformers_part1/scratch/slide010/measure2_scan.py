#!/usr/bin/env python3
"""Pass 2 (slide010): decoder + encoder structure via scanline color runs.

For key rows, print color runs (start-end:hex) so bar/cell geometry can be
pinned exactly; also vertical profiles at key columns.
"""
from PIL import Image
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_010.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = a.shape[:2]

def runs_on_row(y, x0=0, x1=W, min_run=4, thr=60):
    row = a[y, x0:x1]
    out, prev, start = [], None, x0
    for i in range(row.shape[0]):
        c = tuple(row[i])
        if prev is None:
            prev, start = c, x0 + i
        elif abs(c[0]-prev[0]) + abs(c[1]-prev[1]) + abs(c[2]-prev[2]) > thr:
            if (x0 + i) - start >= min_run:
                out.append((start, x0 + i - 1, "#%02x%02x%02x" % prev))
            prev, start = c, x0 + i
    if (x1 - 1) - start >= min_run:
        out.append((start, x1 - 1, "#%02x%02x%02x" % prev))
    return out

def runs_on_col(x, y0=0, y1=H, min_run=4, thr=60):
    col = a[y0:y1, x]
    out, prev, start = [], None, y0
    for i in range(col.shape[0]):
        c = tuple(col[i])
        if prev is None:
            prev, start = c, y0 + i
        elif abs(c[0]-prev[0]) + abs(c[1]-prev[1]) + abs(c[2]-prev[2]) > thr:
            if (y0 + i) - start >= min_run:
                out.append((start, y0 + i - 1, "#%02x%02x%02x" % prev))
            prev, start = c, y0 + i
    if (y1 - 1) - start >= min_run:
        out.append((start, y1 - 1, "#%02x%02x%02x" % prev))
    return out

print("== DECODER horizontal scanlines ==")
for y in (120, 145, 170, 195, 205, 216, 235, 250, 260, 270, 278, 285):
    print(f" y={y}: " + " | ".join(f"{s}-{e}:{c}" for s, e, c in runs_on_row(y, 470, 920, 3)))

print("\n== ENCODER horizontal scanlines ==")
for y in (315, 325, 340, 350, 365, 380, 395, 410, 420, 435, 445, 460, 475, 490):
    print(f" y={y}: " + " | ".join(f"{s}-{e}:{c}" for s, e, c in runs_on_row(y, 40, 500, 3)))

print("\n== vertical profiles at decoder column centers (probe 554/685/815 like parent) ==")
for x in (554, 685, 815):
    print(f" x={x}: " + " | ".join(f"{s}-{e}:{c}" for s, e, c in runs_on_col(x, 110, 300, 3)))

print("\n== vertical profiles at encoder column centers (probe 161/291/422 like parent) ==")
for x in (161, 291, 422):
    print(f" x={x}: " + " | ".join(f"{s}-{e}:{c}" for s, e, c in runs_on_col(x, 300, 510, 3)))
