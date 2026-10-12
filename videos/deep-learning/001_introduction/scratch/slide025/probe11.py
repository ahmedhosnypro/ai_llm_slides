#!/usr/bin/env python3
"""probe11 — per-glyph ink layout of the three equation boxes (frame px)."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
dark = a.sum(axis=2) < 430

def glyph_cols(x0, x1, y0, y1, tag):
    print(f"== {tag} (x{x0}..{x1}, y{y0}..{y1}) ==")
    sub = dark[y0:y1, x0:x1]
    colink = sub.any(axis=0)
    runs = []
    s = None
    for i, v in enumerate(colink):
        if v and s is None: s = i
        if not v and s is not None:
            runs.append((x0+s, x0+i-1)); s = None
    if s is not None: runs.append((x0+s, x0+len(colink)-1))
    # merge runs separated by <=1 px (glyph interiors)
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 1:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    for (c0, c1) in merged:
        seg = sub[:, c0-x0:c1-x0+1]
        ys = np.where(seg.any(axis=1))[0]
        print(f"  glyph x {c0}..{c1} (w {c1-c0+1}), y {y0+ys.min()}..{y0+ys.max()} (h {ys.max()-ys.min()+1})")

glyph_cols(85, 240, 465, 497, "eq1 ink (box1 interior)")
glyph_cols(293, 490, 459, 499, "eq2 ink (box2 interior)")
glyph_cols(542, 710, 456, 500, "eq3 ink (box3 interior)")
