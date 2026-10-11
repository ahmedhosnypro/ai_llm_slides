#!/usr/bin/env python3
"""m17: fix measurements for judge attempt-1 issues on slide_016.jpg (960x540, 1px=1pt).
A) dec-top zone x725-925 y95-205: rows of ink (any pixel far from panel fill / frame)
   -> where do 'Decoder' label, 'Output Probabilities', red arrow actually sit?
B) enc container zone x560-740 y250-420: per-row runs of non-panel ink to resolve
   one-container vs two-sub-blocks (rounded outlines).
C) Nx loop arrows: left Nx x575-640 y315-375, right Nx x835-895 y285-345 -> ink runs.
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def runs_row(y, x0, x1, bg):
    """print runs of pixels differing from bg by >40 in any channel"""
    xs = []
    row = im[y, x0:x1]
    d = np.abs(row - np.array(bg)).max(axis=1)
    idx = np.where(d > 40)[0] + x0
    if len(idx) == 0:
        return f"  y={y}: (clean)"
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i == p + 1:
            p = i
        else:
            out.append((s, p)); s = p = i
    out.append((s, p))
    parts = []
    for (a, bb) in out:
        mid = (a + bb) // 2
        rgb = tuple(im[y, mid])
        parts.append(f"{a}-{bb} rgb{rgb}")
    return f"  y={y}: " + "  ".join(parts)

print("== A) dec-top zone rows y95-205 x725-925 (bg=dec panel 206,254,225) ==")
for y in range(95, 206, 2):
    print(runs_row(y, 725, 925, (206, 254, 225)))

print()
print("== B) enc container zone rows y255-415 x585-740 (bg=enc panel 253,237,221) ==")
for y in range(255, 416, 2):
    print(runs_row(y, 585, 740, (253, 237, 221)))

print()
print("== C1) left Nx zone rows y315-375 x575-645 (bg=enc panel 253,237,221) ==")
for y in range(315, 376, 2):
    print(runs_row(y, 575, 645, (253, 237, 221)))

print()
print("== C2) right Nx zone rows y285-350 x835-900 (bg=dec panel 206,254,225) ==")
for y in range(285, 351, 2):
    print(runs_row(y, 835, 900, (206, 254, 225)))
