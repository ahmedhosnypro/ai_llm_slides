#!/usr/bin/env python3
"""m06_probe.py — median color at probe points + fine grid dumps of both panels."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

def med(x0, x1, y0, y1):
    return tuple(int(v) for v in np.median(im[y0:y1, x0:x1].reshape(-1, 3), axis=0))

probes = [
    ("encoder peach fill", 170, 200, 130, 160),
    ("green overlay (enc)", 350, 420, 200, 260),
    ("green overlay lower", 350, 420, 400, 450),
    ("encoder stack cont fill", 240, 270, 270, 278),
    ("decoder orange fill", 600, 650, 200, 230),
    ("decoder ccffcc fill", 850, 890, 200, 260),
    ("decoder container fill", 790, 820, 305, 315),
    ("decoder purple box", 780, 805, 345, 365),
    ("decoder brown mid", 755, 785, 276, 292),
    ("decoder brown bottom", 745, 810, 435, 450),
    ("encoder brown bottom", 225, 265, 440, 448),
    ("yellow enc mid", 250, 285, 248, 253),
    ("yellow dec top", 760, 790, 112, 120),
    ("yellow dec bottom", 760, 790, 477, 485),
    ("panel gap between (bg)", 480, 540, 200, 300),
    ("title ink", 230, 236, 65, 75),
    ("white callout", 590, 640, 150, 160),
    ("encoder top edge above panel", 200, 260, 95, 100),
    ("panel left edge col", 136, 140, 200, 300),
    ("between peach and green", 300, 310, 200, 300),
    ("between orange and ccffcc", 730, 740, 200, 230),
]
for name, x0, x1, y0, y1 in probes:
    print(f"{name:32s} ({x0}..{x1},{y0}..{y1}) = {med(x0,x1,y0,y1)}")
