#!/usr/bin/env python3
"""measure5: numeric stroke scans per container + color samples"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

dark = a.sum(axis=2) < 330          # text/arrow ink
grayish = (np.abs(a[:, :, 0] - a[:, :, 1]) < 18) & (np.abs(a[:, :, 1] - a[:, :, 2]) < 18) & \
          (a.sum(axis=2) > 480) & (a.sum(axis=2) < 690)   # mid-gray (D9D9D9 outline etc)

def hstrokes(x0, x1, y0, y1, minw, name):
    print(f"-- {name}: horizontal strokes rows (dark cnt>={minw} in x{x0}..{x1})")
    for y in range(y0, y1):
        c = int(dark[y, x0:x1].sum())
        if c >= minw:
            xs = np.where(dark[y, x0:x1])[0]
            print(f"   y={y} cnt={c} x{x0+xs.min()}..{x0+xs.max()}")

def vstrokes(x0, x1, y0, y1, minh, name):
    print(f"-- {name}: vertical strokes cols (dark cnt>={minh} in y{y0}..{y1})")
    for x in range(x0, x1):
        c = int(dark[y0:y1, x].sum())
        if c >= minh:
            ys = np.where(dark[y0:y1, x])[0]
            print(f"   x={x} cnt={c} y{y0+ys.min()}..{y0+ys.max()}")

# container interiors: find square edges (long-ish horizontal dark runs)
hstrokes(162, 256, 145, 462, 40, "L-INPUT interior")
hstrokes(268, 362, 145, 462, 40, "L-PROJ interior")
hstrokes(376, 470, 145, 462, 40, "L-OUT interior")
hstrokes(502, 570, 145, 462, 40, "R-INPUT interior")
hstrokes(581, 655, 145, 462, 40, "R-PROJ interior")
hstrokes(669, 763, 145, 462, 40, "R-OUT interior")

# gray outline rows (D9D9D9-ish horizontal edges) inside L-INPUT
print("-- L-INPUT gray rows (grayish cnt>=50)")
for y in range(145, 465):
    c = int(grayish[y, 162:256].sum())
    if c >= 50:
        print(f"   y={y} cnt={c}")
