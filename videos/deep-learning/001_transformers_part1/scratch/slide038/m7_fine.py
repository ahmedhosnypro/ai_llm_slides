#!/usr/bin/env python3
"""m7: 1px fine scans - box edges, arrowheads, labels, fills."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
im = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
ink = (R < 120) & (G < 120) & (B < 120)

def dump(y0, y1, x0, x1, label, step=1):
    print(f"--- {label} y[{y0}..{y1}] x[{x0}..{x1}] ---")
    for y in range(y0, y1):
        xs = np.where(ink[y, x0:x1])[0] + x0
        if len(xs):
            runs = []
            s = xs[0]; p = xs[0]
            for x in xs[1:]:
                if x == p + 1:
                    p = x
                else:
                    runs.append((s, p)); s = x; p = x
            runs.append((s, p))
            print(f"  y{y}: " + " ".join(f"{a}-{b}" if b > a else f"{a}" for a, b in runs))

# 1. below-box-E zone: labels + arrow tails
dump(270, 312, 795, 915, "below E")

# 2. above-A arrow
dump(116, 140, 856, 880, "above A")

# 3. box D fill + border samples
print("box D fill samples:", [tuple(im[y, x]) for x, y in [(835, 230), (845, 236), (855, 229), (830, 240)]])
print("box C fill samples:", [tuple(im[y, x]) for x, y in [(808, 200), (812, 208), (866, 202)]])
print("box B fill sample:", tuple(im[170, 810]), tuple(im[180, 860]))
print("box A border sample:", tuple(im[137, 860]), tuple(im[138, 870]), tuple(im[155, 860]))
print("box A side border:", tuple(im[145, 831]), tuple(im[145, 901]))
print("panel border samples:", tuple(im[200, 798]), tuple(im[200, 913]), tuple(im[116, 860]), tuple(im[311, 860]))
print("panel border vertical profile x795..802 @y250:", [tuple(im[250, x]) for x in range(795, 803)])
print("panel border vertical profile y308..315 @x860:", [tuple(im[y, 860]) for y in range(308, 316)])
