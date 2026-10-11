#!/usr/bin/env python3
"""Mode-sample regions + border scans for slide_016.jpg diagram."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)

def mode_sample(name, x0, y0, x1, y1, inset=0):
    reg = IM[y0+inset:y1+1-inset, x0+inset:x1+1-inset].reshape(-1, 3)
    c = Counter(map(tuple, reg))
    top = c.most_common(8)
    s = ", ".join(f"({a},{b},{d})x{n}" for (a, b, d), n in top)
    print(f"{name} x{x0}-{x1} y{y0}-{y1}: {s}")

REGIONS = [
    ("R1 enc embed",    640, 440, 730, 490),
    ("R2 enc PE node",  590, 408, 690, 445),
    ("R3 dec top",      737, 100, 890, 145),
    ("R4 softmax/lin",  737, 145, 890, 200),
    ("R5 dec upper",    737, 200, 890, 330),
    ("R6 dec lower",    737, 320, 890, 412),
    ("R7 dec embed",    737, 412, 890, 525),
    ("R8 highlight",    680, 245, 760, 330),
    ("R9 enc top",      577, 105, 735, 148),
    ("R10 encNx",       594, 325, 628, 358),
    ("R11 decNx",       840, 295, 875, 325),
]
for r in REGIONS:
    mode_sample(*r)

# horizontal dark-stroke scan: rows with many dark px in a column window
def hstrokes(name, x0, x1, y0, y1, minfrac=0.55, maxv=110):
    print(f"\n-- horizontal strokes {name} (x{x0}-{x1}) --")
    for y in range(y0, y1):
        seg = IM[y, x0:x1]
        dark = ((seg.max(axis=1) < maxv)).mean()
        if dark > minfrac:
            print(f"   y={y} darkfrac={dark:.2f}")

def vstrokes(name, y0, y1, x0, x1, minfrac=0.55, maxv=110):
    print(f"\n-- vertical strokes {name} (y{y0}-{y1}) --")
    for x in range(x0, x1):
        seg = IM[y0:y1, x]
        dark = ((seg.max(axis=1) < maxv)).mean()
        if dark > minfrac:
            print(f"   x={x} darkfrac={dark:.2f}")

hstrokes("enc container", 636, 722, 260, 415)
hstrokes("dec stack", 752, 838, 195, 330, minfrac=0.45)
hstrokes("dec lower", 752, 838, 320, 415, minfrac=0.45)
vstrokes("enc container", 270, 405, 625, 735)
vstrokes("dec upper", 205, 318, 738, 895)
vstrokes("dec lower", 325, 405, 738, 895)
