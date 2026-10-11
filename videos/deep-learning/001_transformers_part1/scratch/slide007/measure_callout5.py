#!/usr/bin/env python3
"""Connector top-end scan + line3 underline runs + line4 right-edge check."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

print("connector top zone: any px sum<660 in x455..470, y166..200:")
for yy in range(166, 201):
    seg = b[yy, 455:471]
    dk = np.nonzero(seg.sum(axis=1) < 660)[0]
    if len(dk):
        cols = {tuple(seg[i]) for i in dk}
        print(f"  y={yy}: x {(455+dk).tolist()} cols{list(cols)[:3]}")

print("\nbox top-right corner colors x450..470 y166..175:")
for yy in range(166, 176, 2):
    print(f"  y={yy}:", [tuple(b[yy, x]) for x in range(450, 471, 4)])

print("\nline3 underline row 234,235,236 run structure (x50..445, thr<560):")
for yy in (234, 235, 236):
    seg = b[yy, 50:445]
    dk = seg.sum(axis=1) < 560
    runs = []
    start = None
    for i, v in enumerate(dk):
        if v and start is None: start = i
        if not v and start is not None:
            runs.append((50 + start, 50 + i - 1)); start = None
    if start is not None: runs.append((50 + start, 444))
    print(f"  y={yy}: runs={runs}")

print("\nline4 rows 243..253 runs (x50..445, thr<560):")
for yy in range(243, 254):
    seg = b[yy, 50:445]
    dk = seg.sum(axis=1) < 560
    xs = np.nonzero(dk)[0]
    if len(xs):
        runs = []
        start = prev = xs[0]
        for i in xs[1:]:
            if i - prev > 6:
                runs.append((50 + start, 50 + prev)); start = i
            prev = i
        runs.append((50 + start, 50 + prev))
        print(f"  y={yy}: {runs}")

print("\nline1/2/3/4 union bboxes (thr<560):")
def ubbox(y0, y1, x0=50, x1=445, thr=560):
    win = b[y0:y1, x0:x1]
    dk = win.sum(axis=2) < thr
    ys, xs = np.nonzero(dk)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()) if len(ys) else None
print("  L1 y183..202:", ubbox(183, 202))
print("  L2 y203..220:", ubbox(203, 220))
print("  L3 y221..239:", ubbox(221, 239))
print("  L4 y240..254:", ubbox(240, 254))
