#!/usr/bin/env python3
"""measure7: find D9D9D9-ish square outlines + label text bands numerically"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
S = a.sum(axis=2)

neutral = (np.abs(a[:, :, 0] - a[:, :, 2]) < 30)
lg = (S > 580) & (S < 740) & neutral

def rowprof(x0, x1, y0, y1, name, minc=30):
    print(f"-- {name}: rows with lightgray cnt>={minc} (x{x0}..{x1})")
    for y in range(y0, y1):
        c = int(lg[y, x0:x1].sum())
        if c >= minc:
            xs = np.where(lg[y, x0:x1])[0]
            print(f"   y={y} cnt={c} x{x0+xs.min()}..{x0+xs.max()}")

rowprof(160, 258, 145, 462, "L-INPUT")
rowprof(268, 362, 145, 462, "L-PROJ")
rowprof(375, 470, 145, 462, "L-OUT")
rowprof(501, 570, 145, 462, "R-INPUT")
rowprof(581, 657, 145, 462, "R-PROJ")
rowprof(668, 765, 145, 462, "R-OUT")

txt = (S > 300) & (S < 560)
def textprof(x0, x1, y0, y1, name, minc=6):
    print(f"-- {name}: text rows cnt>={minc}")
    run = None
    for y in range(y0, y1):
        c = int(txt[y, x0:x1].sum())
        if c >= minc:
            if run is None: run = [y, y]
            else: run[1] = y
        else:
            if run is not None:
                print(f"   y{run[0]}..{run[1]}")
                run = None
    if run is not None: print(f"   y{run[0]}..{run[1]}")

textprof(160, 258, 145, 462, "L-INPUT text")
textprof(375, 470, 145, 462, "L-OUT text")
textprof(501, 570, 145, 462, "R-INPUT text")
textprof(668, 765, 145, 462, "R-OUT text")
textprof(581, 657, 145, 462, "R-PROJ text")
textprof(268, 362, 145, 462, "L-PROJ text")
