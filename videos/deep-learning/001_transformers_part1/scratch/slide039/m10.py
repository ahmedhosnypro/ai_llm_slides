#!/usr/bin/env python3
"""m10.py — color-annotated horizontal strips: for sample rows, print runs of
non-peach ink with mean RGB, so elements identify by color signature."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

def classify(mean):
    r, g, b = mean
    if r > 235 and g > 235 and b > 235: return "white"
    if abs(r-233) < 8 and abs(g-233) < 8: return "gray"
    if abs(r-240) < 14 and abs(g-224) < 14 and abs(b-200) < 16: return "peach"
    if abs(r-216) < 10 and abs(g-200) < 10 and abs(b-184) < 10: return "TAN(dot)"
    if abs(r-232) < 14 and abs(g-248) < 10 and abs(b-248) < 10 and b-r > 8: return "CYAN(sigma)"
    if g-r > 15 and g-b > 5: return "GREENISH"
    if r-g > 35 and r-b > 35 and r > 140: return "RED"
    if b-r > 40: return "BLUE"
    if r-g > 18 and r > 225 and b > g: return "PINK"
    if r > 200 and g > 150 and b < 190 and r-b > 30: return "tanish"
    return f"other({r},{g},{b})"

def strip(y, x0, x1, min_run=2):
    row = a[y, x0:x1]
    peach = (np.abs(row[:, 0] - 240) < 14) & (np.abs(row[:, 1] - 224) < 14) & (np.abs(row[:, 2] - 200) < 16)
    out = []
    s = None
    for i in range(len(peach)):
        if not peach[i] and s is None: s = i
        elif peach[i] and s is not None:
            if i - s >= min_run:
                seg = row[s:i]
                out.append((x0 + s, x0 + i - 1, tuple(seg.mean(axis=0).astype(int)), classify(seg.mean(axis=0))))
            s = None
    if s is not None:
        seg = row[s:]
        out.append((x0 + s, x0 + len(peach) - 1, tuple(seg.mean(axis=0).astype(int)), classify(seg.mean(axis=0))))
    print(f"y={y}:", " | ".join(f"[{c[0]}-{c[1]}]{c[3]}" for c in out))

# K-row band centers and key rows
for y in [270, 280, 292, 299, 306, 327, 355, 384, 412, 430, 465, 470, 475]:
    strip(y, 110, 700)
