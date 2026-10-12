#!/usr/bin/env python3
"""Row-run scan: for sampled rows, print runs of non-background pixels with avg color."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def is_bg(c):
    # panel gray E9E9E7-ish, white, canvas
    r, g, b = c
    if r > 246 and g > 246 and b > 246: return True
    if abs(r-233) < 13 and abs(g-233) < 13 and abs(b-231) < 15: return True
    return False

def runs_at(y, minlen=3):
    out = []
    x = 40
    while x < 910:
        c = px[x, y]
        if not is_bg(c):
            x0 = x
            cols = []
            while x < 910 and not is_bg(px[x, y]):
                cols.append(px[x, y])
                x += 1
            if len(cols) >= minlen:
                n = len(cols)
                avg = tuple(sum(cc[i] for cc in cols)//n for i in range(3))
                out.append((x0, x-1, avg))
        else:
            x += 1
    return out

for y in range(45, 517, 6):
    rr = runs_at(y)
    if rr:
        s = ' '.join(f"[{a}-{b}]{c}" for a, b, c in rr)
        print(f"y={y:3d}: {s}")
