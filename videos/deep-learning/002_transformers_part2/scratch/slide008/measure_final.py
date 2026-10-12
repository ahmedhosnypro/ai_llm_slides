#!/usr/bin/env python3
"""Final micro-pass: W_q magenta border bounds + interior fill census,
W_k/W_v box edges per band (clean), Y-strip subscript census, node stubs."""
import numpy as np
from PIL import Image
from collections import Counter

F8 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
im = np.asarray(Image.open(F8).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

AX, SX, SY = 17.628, 0.961232, 0.955556
def sx(fx): return (fx - AX) / SX
def sy(fy): return fy / SY

# 1) magenta dashed border under blend: blend of FF00FF ~ (181,52,233); accept wide
mag = (r > 130) & (r < 230) & (g < 120) & (b > 170)
ys, xs = np.where(mag[380:500, 250:360])
print("magenta-border pixels (query region):")
if len(xs):
    pts = sorted(zip(ys, xs))
    print("  bbox x", 250 + xs.min(), "..", 250 + xs.max(), " y", 380 + ys.min(), "..", 380 + ys.max(), "n=", len(xs))
    rows = {}
    for y, x in pts:
        rows.setdefault(380 + y, []).append(250 + x)
    for y in sorted(rows):
        xr = rows[y]
        print(f"  y {y}: x {min(xr)}..{max(xr)} n={len(xr)}")

# 2) W_q interior fill census: inside box, avoiding text/border (pick sub-windows)
print("\nW_q interior census (windows):")
for (x0, x1, y0, y1) in [(285, 300, 420, 440), (310, 322, 415, 440), (288, 300, 442, 452)]:
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    print(f"  win x{x0}..{x1} y{y0}..{y1}:", Counter(map(tuple, px)).most_common(3))

# 3) Y-strip subscript census: region x 582..600, y 128..146 (sub candidate), 1px classes
print("\nY-strip right zone 1px grid (x 580..612, y 126..148): '#'=dark ink g=green .=bg ?=other")
for y in range(126, 149):
    s = ""
    for x in range(580, 613):
        R, G, B = im[y, x]
        if R < 140 and G < 170 and B < 140: c = "#"
        elif G > 150 and G - R > 25 and G - B > 25: c = "g"
        elif R > 215 and G > 200 and B > 185: c = "."
        else: c = "?"
        s += c
    print(f"{y:3d} {s}")

# 4) W_k / W_v box edges per band: longest nonbg run near expected columns
def box_edges(x_lo, x_hi, y_a, y_z, name):
    reg = im[y_a:y_z, x_lo:x_hi]
    R, G, B = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
    nonbg = ~(((R > 225) & (G > 195) & (B > 165)) | ((R > 235) & (G > 235) & (B > 235)))
    colc = nonbg.sum(axis=0)
    thr = max(3, (y_z - y_a) // 3)
    idx = np.where(colc >= thr)[0]
    if len(idx):
        # contiguous runs
        runs, s, p = [], None, None
        for i in idx:
            if s is None: s = p = i
            elif i == p + 1: p = i
            else: runs.append((s, p)); s = p = i
        runs.append((s, p))
        runs = [(a, z) for a, z in runs if z - a >= 12]
        if runs:
            a, z = max(runs, key=lambda t: t[1] - t[0])
            print(f"{name} y{y_a}..{y_z}: box x {x_lo+a}..{x_lo+z} (w {z-a+1}) | slide x {sx(x_lo+a):.1f}..{sx(x_lo+z):.1f}")

print("\nW_k box edges per band:")
for (a, z) in [(224, 252), (263, 292), (303, 331), (345, 373)]:
    box_edges(150, 225, a, z, f"  W_k band y{a}..{z}")
print("W_v box edges per band:")
for (a, z) in [(224, 252), (263, 292), (303, 331), (345, 373)]:
    box_edges(680, 745, a, z, f"  W_v band y{a}..{z}")

# 5) node left/right stubs at 1px (rows at node centers)
print("\nnode rows 1px (x 480..530): R=red .=peach ?=other")
for cy in (228, 277, 316, 358):
    s = ""
    for x in range(480, 531):
        R, G, B = im[cy, x]
        if R > 140 and R - G > 40 and R - B > 40: c = "R"
        elif R > 225 and G > 195 and B > 165: c = "."
        else: c = "?"
        s += c
    print(f"y={cy}: {s}")
print("legend x480..530")
print("\nnode rows 1px right side (x 630..665):")
for cy in (228, 277, 316, 358):
    s = ""
    for x in range(630, 666):
        R, G, B = im[cy, x]
        if R > 140 and R - G > 40 and R - B > 40: c = "R"
        elif R > 225 and G > 195 and B > 165: c = "."
        else: c = "?"
        s += c
    print(f"y={cy}: {s}")
