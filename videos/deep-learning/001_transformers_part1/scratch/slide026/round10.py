#!/usr/bin/env python3
import numpy as np
from PIL import Image
IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
PEACH = np.array([247, 227, 206])

print("== strip top/bottom border rows x170..500 ==")
for y in list(range(462, 482)) + list(range(508, 524)):
    row = A[y, 170:500]
    ink = np.abs(row - PEACH).sum(axis=1) > 40
    xs = np.where(ink)[0]
    if len(xs):
        runs, s, prev = [], xs[0], xs[0]
        for v in xs[1:]:
            if v > prev + 3: runs.append((170 + s, 170 + prev)); s = v
            prev = v
        runs.append((170 + s, 170 + prev))
        print(f"  y{y}: n={len(xs)} {runs[:14]}")
    else:
        print(f"  y{y}: -")

print("\n== right curve sensitive scan x500..810, y400..500 ==")
sub = A[400:500, 500:810]
m = (np.abs(sub - PEACH).sum(axis=2) > 28) & (np.abs(sub - np.array([233,233,231])).sum(axis=2) > 28)
ys, xs = np.where(m)
print(f"  n={len(xs)}")
if len(xs):
    for by in range(0, 100, 10):
        sel = (ys >= by) & (ys < by + 10)
        if sel.sum() >= 2:
            print(f"    y{400+by}..{400+by+9}: x~{500+int(xs[sel].mean())} n={int(sel.sum())} x{500+xs[sel].min()}..{500+xs[sel].max()}")

print("\n== left curve sensitive x40..180, y406..470 ==")
sub = A[406:470, 40:180]
m = (np.abs(sub - PEACH).sum(axis=2) > 28)
ys, xs = np.where(m)
print(f"  n={len(xs)}")
if len(xs):
    for by in range(0, 64, 8):
        sel = (ys >= by) & (ys < by + 8)
        if sel.sum() >= 2:
            print(f"    y{406+by}..{406+by+7}: x~{40+int(xs[sel].mean())} n={int(sel.sum())} x{40+xs[sel].min()}..{40+xs[sel].max()}")

print("\n== strip left/right border cols x172..180 / x488..496 ==")
for x in (172, 174, 176, 178, 486, 490, 492, 494):
    col = A[472:518, x]
    ink = np.abs(col - PEACH).sum(axis=1) > 40
    print(f"  x{x}: ink_ys={ [472+i for i,v in enumerate(ink) if v][:20] }")
