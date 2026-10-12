#!/usr/bin/env python3
"""Closed-loop check (attempt 3, corrected extents): ONLY the two notation spans changed.

Compares qa/slide041/render_3.png (post-fix) against render_1.png (certified, pre-fix).
Measured drawn extents (render, frame-scale px):
  L1 '(x,y)'       glyphs x172.8..212.6, y387.4..411.8   (I stem 165.1..170.9 stays red)
  L2 '(-a:a , -b:b)' glyphs x172.8..271.2, y409.9..428.2 (h 157.0..166.1, '(odd
     dimension)' 277.9.. stay red)
PASS requires: every diff pixel inside the two span allow-boxes; all guards zero-diff;
spans render modal (0,0,0) with zero red; I/h/(odd) still red; span glyph columns
unchanged (<=1 frame px deviation).
"""
from collections import Counter
from PIL import Image
import numpy as np

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide041"
VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
old = np.asarray(Image.open(f"{QA}/render_1.png").convert("RGB")).astype(int)
new = np.asarray(Image.open(f"{QA}/render_3.png").convert("RGB")).astype(int)
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_041.jpg").convert("RGB")).astype(int)
S = new.shape[0] / 540.0
fails = []

def fb(x0, x1, y0, y1):
    return (int(x0 * S), int(x1 * S) + 1, int(y0 * S), int(y1 * S) + 1)

ALLOW = {
    "L1 (x,y) span": fb(171.5, 214, 385, 413),
    "L2 (-a:a , -b:b) span": fb(171.5, 273, 408, 430),
}
GUARDS = {
    "Image: prefix": fb(88, 164, 383, 411),
    "I stem": fb(163, 172, 383, 411),
    "Filter: prefix": fb(88, 156, 408, 434),
    "h": fb(155, 172, 408, 434),
    "(odd dimension)": fb(274, 410, 408, 434),
    "a=1,b=1 block": fb(230, 290, 325, 365),
    "equation region": fb(450, 850, 355, 425),
    "instruction box": fb(70, 885, 440, 518),
    "filter grid (true area)": fb(135, 230, 312, 385),
    "title": fb(280, 680, 70, 115),
    "L1 span rows above": fb(171, 214, 380, 385),
    "L2 span rows below": fb(171, 273, 430, 436),
}

diff = (old != new).any(axis=2)
ys, xs = np.nonzero(diff)
print(f"diff pixels total = {len(ys)}")

inside = np.zeros_like(diff)
for (x0, x1, y0, y1) in ALLOW.values():
    inside[y0:y1, x0:x1] = True
stray = int((diff & ~inside).sum())
print(f"diff inside span allow-boxes = {int((diff & inside).sum())}   outside = {stray}")
if stray:
    sy, sx = np.nonzero(diff & ~inside)
    fails.append(f"STRAY DIFF: {stray} px bbox x[{sx.min()}..{sx.max()}] y[{sy.min()}..{sy.max()}]")

for name, (x0, x1, y0, y1) in GUARDS.items():
    n = int(diff[y0:y1, x0:x1].sum())
    if n:
        fails.append(f"guard {name}: {n} diff px")
print("guards:", ", ".join(f"{k}={int(diff[v[2]:v[3], v[0]:v[1]].sum())}" for k, v in GUARDS.items()))

# spans black, zero red
for name, fbk in {"L1 (x,y)": (177, 213, 386, 411), "L2 (-a:a , -b:b)": (173, 272, 409, 429)}.items():
    x0, x1, y0, y1 = fb(*fbk)
    reg = new[y0:y1, x0:x1]
    red = (reg[:, :, 0] >= 120) & (reg[:, :, 1] <= 90) & (reg[:, :, 2] <= 90)
    dark = (reg.max(axis=2) < 100)
    modal = Counter(map(tuple, reg[dark | red])).most_common(1)[0]
    print(f"post-fix {name:20s} dark={int(dark.sum())} red={int(red.sum())} modal={modal[0]} n={modal[1]}")
    if red.sum() or not dark.sum() or tuple(modal[0]) != (0, 0, 0):
        fails.append(f"{name} not black")

# I / h / (odd dimension) still red
for name, fbk in {"I stem": (164, 172, 385, 408), "h": (156, 167, 411, 428),
                  "(odd dimension)": (277, 340, 412, 431)}.items():
    x0, x1, y0, y1 = fb(*fbk)
    reg = new[y0:y1, x0:x1]
    red = (reg[:, :, 0] >= 120) & (reg[:, :, 1] <= 90) & (reg[:, :, 2] <= 90)
    print(f"post-fix red {name:18s} red px={int(red.sum())}")
    if not red.sum():
        fails.append(f"{name} lost red")

# span glyph columns unchanged (<=1 frame px deviation, per-glyph-run comparison)
for name, fbk in {"L1 (x,y)": (171, 214, 385, 413), "L2 (-a:a , -b:b)": (171, 273, 408, 430)}.items():
    boxes = []
    for im, tag in ((old, "old"), (new, "new")):
        x0, x1, y0, y1 = fb(*fbk)
        reg = im[y0:y1, x0:x1]
        ink = (reg.max(axis=2) < 150) | ((reg[:, :, 0] >= 120) & (reg[:, :, 1] <= 90) & (reg[:, :, 2] <= 90))
        cols = np.nonzero(ink.any(axis=0))[0]
        rows = np.nonzero(ink.any(axis=1))[0]
        boxes.append((cols.min(), cols.max(), rows.min(), rows.max()))
    dev = max(abs(a - b) for a, b in zip(boxes[0], boxes[1]))
    print(f"{name} ink bbox old(in-box px)={boxes[0]} new={boxes[1]} max dev={dev} px ({dev / S:.2f} frame px)")
    if dev / S > 1.0:
        fails.append(f"{name} glyphs moved >1 frame px (dev {dev / S:.2f})")

print()
if fails:
    print("FAIL:")
    for f in fails:
        print(" -", f)
    raise SystemExit(1)
print("CLOSED-LOOP PASS: diff confined to the two spans; spans black modal (0,0,0); "
      "all other ink byte-identical; span glyph positions unchanged.")
