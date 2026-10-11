#!/usr/bin/env python3
"""Measure pass 5: strict hue predicates for pink/tan boxes; raw profiles."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_012.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(float)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# pink: r and b both well above g
pink = (r - g > 45) & (b - g > 45) & (r > 200) & (b > 195)
# tan: r above g above b, not too dark, not red (red has low g AND low b)
tan = (r - b > 40) & (r > 225) & (g > 150) & (g < 240) & (b > 110) & (b < 220) & (g - b > 15)

def span(mask, x0, x1, y0, y1, axis, frac=0.30):
    reg = mask[y0:y1, x0:x1]
    f = reg.mean(axis=0 if axis == "x" else 1)
    idx = np.where(f > frac)[0]
    if len(idx) == 0:
        return None
    return (idx.min(), idx.max(), f.max())

print("== pink boxes (strict) ==")
for name, (x0, x1, y0, y1) in {
    "vaswani": (250, 345, 155, 205), "shazeer": (378, 468, 155, 205),
    "parmar": (487, 590, 155, 205), "uszkoreit": (602, 705, 155, 205),
    "jones": (245, 350, 216, 258), "kaiser": (563, 655, 216, 258),
}.items():
    rx = span(pink, x0, x1, y0, y1, "x")
    ry = span(pink, x0, x1, y0, y1, "y")
    print(f"  {name}: x[{x0+rx[0]},{x0+rx[1]}] (fmax {rx[2]:.2f})  y[{y0+ry[0]},{y0+ry[1]}] (fmax {ry[2]:.2f})")

print("== tan title (strict) ==")
rx = span(tan, 320, 612, 48, 92, "x")
ry = span(tan, 320, 612, 48, 92, "y")
print(f"  x[{320+rx[0]},{320+rx[1]}] (fmax {rx[2]:.2f})  y[{48+ry[0]},{48+ry[1]}] (fmax {ry[2]:.2f})")

print("== tan date band (strict) ==")
rx = span(tan, 86, 150, 170, 325, "x")
ry = span(tan, 86, 150, 170, 325, "y")
print(f"  x[{86+rx[0]},{86+rx[1]}] (fmax {rx[2]:.2f})  y[{170+ry[0]},{170+ry[1]}] (fmax {ry[2]:.2f})")
# vertical profile detail through the band at x 100..133
sub = tan[170:330, 100:133]
f = sub.mean(axis=1)
print("  band row fractions (y: frac) where >0.2:")
runs = []
for i, v in enumerate(f):
    if v > 0.2:
        runs.append((170 + i, round(float(v), 2)))
print("  ", runs[:8], "...", runs[-8:] if len(runs) > 8 else "")

print("== raw row medians through Vaswani box (x270..330) ==")
for y in range(158, 202, 2):
    seg = a[y, 270:330]
    print(f"  y={y}: {np.median(seg, axis=0).astype(int)}")

print("== raw row medians through date band (x102..130) ==")
for y in range(178, 320, 6):
    seg = a[y, 102:130]
    print(f"  y={y}: {np.median(seg, axis=0).astype(int)}")

print("== raw col medians through date band (y200..300) ==")
for x in range(90, 142, 2):
    seg = a[200:300, x]
    print(f"  x={x}: {np.median(seg, axis=0).astype(int)}")
