#!/usr/bin/env python3
"""Scanline runs + mode samples for slide_016.jpg (960x540)."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
H, W = IM.shape[:2]

def runs_at(y, x0=0, x1=W, minrun=3):
    row = IM[y, x0:x1]
    q = (row // 12) * 12
    out = []
    s = 0
    for i in range(1, len(q)):
        if not np.array_equal(q[i], q[i-1]):
            if i - s >= minrun:
                out.append((x0+s, x0+i-1, tuple(int(v) for v in q[i-1])))
            s = i
    if len(q) - s >= minrun:
        out.append((x0+s, x0+len(q)-1, tuple(int(v) for v in q[len(q)-1])))
    return out

def cruns_at(x, y0=0, y1=H, minrun=3):
    col = IM[y0:y1, x]
    q = (col // 12) * 12
    out = []
    s = 0
    for i in range(1, len(q)):
        if not np.array_equal(q[i], q[i-1]):
            if i - s >= minrun:
                out.append((y0+s, y0+i-1, tuple(int(v) for v in q[i-1])))
            s = i
    if len(q) - s >= minrun:
        out.append((y0+s, y0+len(q)-1, tuple(int(v) for v in q[len(q)-1])))
    return out

def show(title, items):
    print(f"\n-- {title} --")
    for a, b, c in items:
        print(f"   {a:3d}-{b:3d} ({b-a+1:3d}) rgb{c}")

# row scans: callout zone (x<580) and diagram zone
for y in [60, 118, 160, 227, 320, 380, 425, 460, 495, 515]:
    show(f"row y={y} (full)", runs_at(y, 40, 920))
for y in [110, 270, 300, 330, 390, 410, 440, 480, 505]:
    show(f"row y={y} (diagram 560-920)", runs_at(y, 560, 920))
for x in [600, 650, 680, 700, 725, 745, 780, 800, 830, 860, 880]:
    show(f"col x={x} (diagram)", cruns_at(x, 100, 540))
