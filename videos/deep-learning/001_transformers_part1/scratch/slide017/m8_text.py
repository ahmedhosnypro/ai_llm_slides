#!/usr/bin/env python3
"""Dark-ink text bands per region of slide_017.jpg — localize every label."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def ink(px, thr=150):
    r, g, b = px
    return r < thr and g < thr and b < thr

def bands(x0, x1, y0, y1, name, min_ink=2, thr=150):
    print(f"== {name} (x{x0}..{x1}, y{y0}..{y1}, ink thr {thr})")
    cur = None
    out = []
    for y in range(y0, y1+1):
        xs = [x for x in range(x0, x1+1) if ink(A[y, x], thr)]
        if len(xs) >= min_ink:
            if cur is None:
                cur = [y, y, xs[0], xs[-1], 1]
            else:
                cur[1] = y
                cur[2] = min(cur[2], xs[0])
                cur[3] = max(cur[3], xs[-1])
                cur[4] += len(xs)
        else:
            if cur is not None:
                out.append(tuple(cur))
                cur = None
    if cur is not None:
        out.append(tuple(cur))
    for y0b, y1b, xa, xb, n in out:
        print(f"   y{y0b:3d}..{y1b:3d} h={y1b-y0b+1:3d}  x{xa:3d}..{xb:3d}  inkpx={n}")

# encoder panel
bands(578, 738, 100, 535, "ENCODER panel text")
# decoder panel
bands(742, 898, 100, 535, "DECODER panel text")
# left: callout column dark text (for callout text bboxes)
bands(60, 560, 100, 535, "CALLOUT column text", thr=140)
# title band
bands(100, 860, 30, 100, "TITLE text", thr=160)
