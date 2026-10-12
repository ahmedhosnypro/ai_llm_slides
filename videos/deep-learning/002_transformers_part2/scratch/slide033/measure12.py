#!/usr/bin/env python3
"""slide033 measure-12: example box row profile + L3/L4 hue probes + '=100' hue."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556

print("=== EXAMPLE box: dark-ink row profile (x 783..880, y 108..295) ===")
sub = a[108:296, 783:881]
dark = (sub.mean(axis=2) < 190)
rows = dark.sum(axis=1)
y = 0
while y < len(rows):
    if rows[y] > 1:
        y2 = y
        while y2 < len(rows) - 1 and (rows[y2 + 1] > 1 or (y2 + 2 < len(rows) and rows[y2 + 2] > 1 and y2 + 1 - y < 3)):
            y2 += 1
        xs = np.where(dark[y:y2 + 1].any(axis=0))[0]
        seg = sub[y:y2 + 1]
        m = seg.mean(axis=2) < 170
        px = seg[m]
        med = tuple(int(v) for v in np.median(px, axis=0)) if len(px) else None
        print(f"  f y {y+108}..{y2+108} x {xs.min()+783}..{xs.max()+783}  slide y {MAPY(y+108):.1f}..{MAPY(y2+108):.1f} x {MAPX(xs.min()+783):.1f}..{MAPX(xs.max()+783):.1f} inkmed={med}")
        y = y2 + 1
    else:
        y += 1

print("=== DEFS L3 runs: glyph-core hues along the line (y 181..193) ===")
for x0, x1, lab in [(437, 540, "Number of Vector Pairs"), (545, 610, "K=d/2 zone"), (620, 700, "[0,1,2 list a"), (700, 755, "list b")]:
    seg = a[181:194, x0:x1]
    m = seg.mean(axis=2) < 160
    px = seg[m]
    if len(px):
        med = tuple(int(v) for v in np.median(px, axis=0))
        print(f"  {lab:28s} n={len(px):4d} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")
    else:
        print(f"  {lab:28s} no ink")

print("=== DEFS L4 runs (y 218..232) ===")
for x0, x1, lab in [(437, 540, "Elements Index i"), (545, 690, "[0,1,2,... d-1]")]:
    seg = a[218:233, x0:x1]
    m = seg.mean(axis=2) < 160
    px = seg[m]
    if len(px):
        med = tuple(int(v) for v in np.median(px, axis=0))
        print(f"  {lab:28s} n={len(px):4d} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")
    else:
        print(f"  {lab:28s} no ink")

print("=== EXAMPLE '=100' hue (y 144..154, x 795..850) ===")
seg = a[144:155, 795:851]
m = seg.mean(axis=2) < 175
px = seg[m]
if len(px):
    med = tuple(int(v) for v in np.median(px, axis=0))
    print(f"  n={len(px)} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")

print("=== EXAMPLE 'd' hue (y 144..154, x 783..796) ===")
seg = a[144:155, 783:796]
m = seg.mean(axis=2) < 175
px = seg[m]
if len(px):
    med = tuple(int(v) for v in np.median(px, axis=0))
    print(f"  n={len(px)} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")

print("=== EXAMPLE K / i hues ===")
for y0, y1, x0, x1, lab in [(217, 231, 783, 794, "K glyph"), (217, 231, 794, 850, "=[0..49]"),
                             (243, 258, 788, 798, "i glyph"), (243, 258, 798, 875, "=[0..99]"),
                             (270, 285, 783, 860, "Sin line"), (296, 300, 783, 860, "below?")]:
    seg = a[y0:y1, x0:x1]
    m = seg.mean(axis=2) < 170
    px = seg[m]
    if len(px):
        med = tuple(int(v) for v in np.median(px, axis=0))
        print(f"  {lab:12s} n={len(px):4d} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")
    else:
        print(f"  {lab:12s} no ink")

print("=== DEFS L1/L2 hues ===")
for y0, y1, x0, x1, lab in [(117, 127, 437, 500, "L1 Word"), (117, 127, 500, 620, "L1 Embedding Dim"),
                             (117, 127, 620, 668, "L1 d"), (117, 127, 672, 755, "L1 [Even Num]"),
                             (144, 154, 437, 500, "L2 Position"), (144, 154, 500, 625, "L2 Enc Dim"),
                             (144, 154, 628, 670, "L2 d")]:
    seg = a[y0:y1, x0:x1]
    m = seg.mean(axis=2) < 170
    px = seg[m]
    if len(px):
        med = tuple(int(v) for v in np.median(px, axis=0))
        print(f"  {lab:18s} n={len(px):4d} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")
    else:
        print(f"  {lab:18s} no ink")

print("=== DEFS L5/L6 hues ===")
for y0, y1, x0, x1, lab in [(245, 256, 437, 490, "L5 Even"), (245, 256, 490, 560, "L5 Index i is"),
                             (245, 256, 560, 615, "L5 Sine Term"), (245, 256, 615, 672, "L5 comma"),
                             (245, 256, 672, 705, "L5 i=2*k"), (271, 283, 437, 480, "L6 Odd"),
                             (271, 283, 480, 555, "L6 Index i is"), (271, 283, 555, 615, "L6 Cosine Term"),
                             (271, 283, 660, 722, "L6 i=2*k+1")]:
    seg = a[y0:y1, x0:x1]
    m = seg.mean(axis=2) < 170
    px = seg[m]
    if len(px):
        med = tuple(int(v) for v in np.median(px, axis=0))
        print(f"  {lab:18s} n={len(px):4d} med=({med[0]},{med[1]},{med[2]}) #{med[0]:02x}{med[1]:02x}{med[2]:02x}")
    else:
        print(f"  {lab:18s} no ink")
