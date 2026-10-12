#!/usr/bin/env python3
"""Slide 038 forensics pass 3: dark-red mask (top rule, borders), title metrics, right border."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# dark crimson mask (JPEG-darkened C00000, e.g. (105,45,53))
dred = (r > 70) & (r < 175) & (g < 90) & (b < 100) & ((r - g) > 25) & ((r - b) > 15)

print("--- dark-red rows with >300 px ---")
for y in range(H):
    c = dred[y].sum()
    if c > 300:
        xs = np.nonzero(dred[y])[0]
        print(f"y={y} n={c} x {xs.min()}..{xs.max()}")

print("--- dark-red cols with >200 px ---")
for x in range(W):
    c = dred[:, x].sum()
    if c > 200:
        ys = np.nonzero(dred[:, x])[0]
        print(f"x={x} n={c} y {ys.min()}..{ys.max()}")

print("--- right border hunt x795..890, y251..510: red OR dred count per col ---")
for x in range(795, 891):
    m1 = ((r > 120) & (g < 110) & (b < 110))[251:511, x].sum()
    m2 = dred[251:511, x].sum()
    if m1 + m2 > 20:
        print(f"x={x} bright={m1} dark={m2}")

print("--- samples ---")
for (x, y, label) in [(58, 300, "left bar x58"), (183, 380, "x183 line"), (480, 43, "top rule"),
                      (480, 251, "box top border"), (480, 510, "box bottom border"),
                      (90, 175, "formula box left border"), (878, 175, "formula box right border")]:
    print(f"{label} ({x},{y}):", a[y, x], " 3x3 modal:", np.median(a[y-1:y+2, x-1:x+2].reshape(-1, 3), axis=0))

print("--- title precise: ink y60..105 x100..900 ---")
ink = ((r < 190) & (g < 150) & (b < 150))[60:106, 100:900]
ys = np.where(ink.sum(axis=1) > 0)[0] + 60
xs = np.where(ink.sum(axis=0) > 0)[0] + 100
print(f"bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
# per-column runs to find word gaps
colink = ink.sum(axis=0)
gaps = []
prev = None
for i, v in enumerate(colink):
    if v == 0:
        if prev is None: prev = i
    else:
        if prev is not None and i - prev > 12: gaps.append((prev + 100, i - 1 + 100))
        prev = None
print("word gaps >12px:", gaps)
# cap height of first glyph (F): column at xs.min()+2
x0 = xs.min()
stem = np.where(ink[:, x0 - 100 + 3])[0] + 60
print(f"F stem col x{x0+3}: y {stem.min()}..{stem.max()}")
