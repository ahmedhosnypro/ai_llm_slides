#!/usr/bin/env python3
"""m10: final precise inset measurements.
- exact edges of boxes A-E (border-row spans + side borders)
- core fill medians
- faint Q/K/V labels (relaxed threshold) in y286..305
- gap arrow columns (fine)
"""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
im = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
ink = (R < 130) & (G < 130) & (B < 130)

def runs_in_row(y, x0=795, x1=915, minw=1):
    xs = np.where(ink[y, x0:x1])[0] + x0
    if not len(xs):
        return []
    out = []
    s = p = xs[0]
    for x in xs[1:]:
        if x == p + 1:
            p = x
        else:
            out.append((s, p)); s = p = x
    out.append((s, p))
    return [r for r in out if r[1] - r[0] >= minw - 1]

print("== box border rows (wide runs) ==")
for y in list(range(134, 160)) + list(range(164, 190)) + list(range(194, 218)) + list(range(223, 247)) + list(range(252, 278)):
    rr = [r for r in runs_in_row(y) if r[1] - r[0] > 30]
    if rr:
        print(f"  y{y}: {rr}")

print("== box side borders (row through mid-box, text-free rows) ==")
for y, name in [(141, "A"), (171, "B"), (199, "C-top"), (229, "D"), (259, "E")]:
    print(f"  {name} y{y}:", runs_in_row(y))

print("== fills (median of 8x8 patch) ==")
for name, cx, cy in [("A", 845, 145), ("B", 815, 175), ("C", 870, 210), ("D", 828, 238), ("E", 822, 262)]:
    patch = im[cy - 4:cy + 4, cx - 4:cx + 4].reshape(-1, 3)
    print(f"  {name} ({cx},{cy}):", tuple(np.median(patch, axis=0).astype(int)))

print("== faint labels y286..306 (thr<170) ==")
ink2 = (R < 170) & (G < 170) & (B < 170)
for y in range(286, 307):
    xs = np.where(ink2[y, 800:911])[0] + 800
    if len(xs):
        out = []
        s = p = xs[0]
        for x in xs[1:]:
            if x == p + 1:
                p = x
            else:
                out.append((s, p)); s = p = x
        out.append((s, p))
        print(f"  y{y}: {out}")

print("== gap arrow columns (thr<130, x830..855) ==")
for y in range(157, 274):
    rr = runs_in_row(y, 830, 856)
    rr2 = runs_in_row(y, 880, 900)
    if rr or rr2:
        print(f"  y{y}: mid={rr} right={rr2}")
