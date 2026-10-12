#!/usr/bin/env python3
"""m16.py — sticker unrotated crop + V-line presence scan + bottom-cell fill hexes."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
org = np.asarray(Image.open(BASE + "unique_slides/slide_039.jpg").convert("RGB")).astype(int)
out = []

# sticker unrotated crop (x3)
cy, cx = 477, 790
patch = org[420:535, 680:905]
im = Image.fromarray(patch.astype(np.uint8)).rotate(-18.43, resample=Image.BICUBIC, center=(cx - 680, cy - 420), fillcolor=(255, 255, 255))
u = np.asarray(im).astype(int)
ym = (u[..., 0] > 200) & (u[..., 1] > 200) & (u[..., 2] < 140)
ys, xs = np.where(ym)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
crop = im.crop((max(0, x0 - 8), max(0, y0 - 8), x1 + 9, y1 + 9))
crop = crop.resize((crop.width * 3, crop.height * 3), Image.LANCZOS)
crop.save(BASE + "scratch/slide039/probe_sticker_unrot.png")
out.append(f"probe_sticker_unrot.png: frame-x[{x0+680},{x1+680}] y[{y0+420},{y1+420}] x3 -> {crop.size}")

# V-line presence between the otimes nodes and the W^V boxes (row centers)
def redm(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 120) & (R - G > 55) & (R - B > 55)
for yy in [299, 327, 355, 384]:
    seg = org[yy - 2:yy + 3, 470:615]
    m = redm(seg)
    cols = np.where(m.sum(axis=0) > 0)[0]
    if len(cols):
        runs = []
        s = cols[0]; p = cols[0]
        for c in cols[1:]:
            if c - p > 3: runs.append((s + 470, p + 470)); s = c
            p = c
        runs.append((s + 470, p + 470))
        out.append(f"y{yy} red runs x470-615: {runs} px={m.sum()}")
    else:
        out.append(f"y{yy} red runs x470-615: NONE px=0")

# bottom cells fill hexes (clean spots)
for nm, xa, xb in [("cell1", 266, 326), ("cell2", 328, 374), ("cell3", 376, 422), ("cell4", 424, 470)]:
    cell = org[456:483, xa + 2:xb - 2]
    s = cell.sum(axis=2)
    bright = cell[s > 640]
    out.append(f"bot {nm} bright fill avg: {bright.mean(axis=0).round(0) if len(bright) else None} ({len(bright)}px)")

# bottom cell1: is there a subscript after the big glyph? red map fine
cell = org[458:480, 266:326]
m = redm(cell)
for y in range(m.shape[0]):
    xs = np.where(m[y])[0]
    if len(xs): out.append(f"  c1 y{458+y}: " + ",".join(f"{x+266}" for x in xs))

print("\n".join(out))
