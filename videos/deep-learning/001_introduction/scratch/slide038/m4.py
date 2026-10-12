#!/usr/bin/env python3
"""Slide 038 forensics pass 4: panel borders, rule segments, box edges."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]

print("--- raw probes: vertical x880..915 at several y ---")
for y in [60, 100, 200, 300, 400, 460]:
    row = a[y, 880:916]
    s = ' '.join(f"{x+880}:({p[0]},{p[1]},{p[2]})" for x, p in enumerate(row) if p[0] < 210 and not (abs(p[0]-232)<12))
    print(f"y={y}: {s}")

print("--- horizontal probe y511..522 at x=480 (below box bottom) ---")
for y in range(509, 524):
    print(f"y={y}:", a[y, 480])

print("--- row 251 & 510: red counts in segments ---")
dred = (r > 70) & (r < 175) & (g < 90) & (b < 100) & ((r - g) > 25) & ((r - b) > 15)
for y in [43, 44, 251, 252, 510, 511]:
    xs = np.nonzero(dred[y])[0]
    if len(xs):
        seg1 = ((xs >= 59) & (xs <= 182)).sum()
        seg2 = ((xs >= 183) & (xs <= 810)).sum()
        seg3 = (xs > 810).sum()
        print(f"y={y}: total={len(xs)} x59-182:{seg1} x183-810:{seg2} x>810:{seg3} min={xs.min()} max={xs.max()}")

print("--- col 58 & 183 & 809: dred runs ---")
for x in [57, 58, 59, 183, 184, 808, 809, 810]:
    ys = np.nonzero(dred[:, x])[0]
    if len(ys):
        runs = []
        s = p = ys[0]
        for v in ys[1:]:
            if v <= p + 2: p = v
            else: runs.append((s, p)); s = p = v
        runs.append((s, p))
        print(f"x={x}: n={len(ys)} runs={runs}")

print("--- where does the top rule really end on the right? y42..45 x850..910 ---")
for x in range(850, 911):
    c = dred[42:46, x].sum()
    if c:
        print(f"x={x} n={c}", a[43, x])
