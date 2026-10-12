#!/usr/bin/env python3
"""m12.py — W^q branch rows, sticker rotation, green connector trace, Y-group red shape."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def strip(y, x0, x1, min_run=2):
    row = a[y, x0:x1]
    peach = (np.abs(row[:, 0] - 240) < 14) & (np.abs(row[:, 1] - 224) < 14) & (np.abs(row[:, 2] - 200) < 16)
    out = []; s = None
    for i in range(len(peach)):
        if not peach[i] and s is None: s = i
        elif peach[i] and s is not None:
            if i - s >= min_run:
                m = row[s:i].mean(axis=0).astype(int)
                out.append((x0 + s, x0 + i - 1, f"({m[0]},{m[1]},{m[2]})"))
            s = None
    print(f"y={y}:", " | ".join(f"[{c[0]}-{c[1]}]{c[2]}" for c in out))

print("=== W^q branch x[270,330] y[404,455] ===")
for y in range(404, 456, 4):
    strip(y, 270, 330)

# sticker angle: topmost yellow per column
yellow = (R > 200) & (G > 200) & (B < 120)
print("=== sticker top edge (col -> first yellow y) ===")
tops = []
for x in range(700, 885, 20):
    ys = np.where(yellow[400:540, x])[0]
    if len(ys): tops.append((x, 400 + ys.min()))
print(tops)
if len(tops) > 1:
    import math
    dx = tops[-1][0] - tops[0][0]; dy = tops[-1][1] - tops[0][1]
    print("slope deg:", math.degrees(math.atan2(dy, dx)))

# green connector trace (light green dashed)
lg = (G - R > 8) & (G - B > 15) & (G > 185) & (R > 130) & (R < 215)
print("=== light-green connector sample points ===")
pts = []
for y in range(240, 540, 12):
    xs = np.where(lg[y, 110:960])[0]
    if len(xs):
        # group runs
        runs = []; s = xs[0]; p = xs[0]
        for x in xs[1:]:
            if x - p > 4:
                runs.append((110 + s, 110 + p)); s = x
            p = x
        runs.append((110 + s, 110 + p))
        pts.append((y, runs))
for y, rr in pts: print("  y=", y, rr)

# Y1 red cluster shape: print ascii of red mask x[482,500] y[168,196]
red = (R > 140) & (R - G > 70) & (R - B > 70)
print("=== Y1 red cluster bitmap (x482-500, y168-196) ===")
for y in range(168, 197):
    print(f"{y:3d} " + "".join("#" if red[y, x] else "." for x in range(482, 501)))
