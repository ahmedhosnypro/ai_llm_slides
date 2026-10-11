#!/usr/bin/env python3
"""Fine measurements: label box borders, text line ink by color, cube scanlines,
right-block layer geometry, arrows. All frame px; slide = (fx-18.63)/0.96123, fy/0.95556."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (r > 120) & (r - g > 45) & (r - b > 45)
blue = (b > 110) & (b - r > 40) & (b - g > 30)
green = (g > 110) & (g - r > 30) & (g - b > 50)
mag = (r > 90) & (b > 90) & (r - g > 60) & (b - g > 60)
yel = (r > 180) & (g > 180) & (b < 140)

def runs(mask1d, minlen=3):
    out, inr = [], False
    for i, v in enumerate(mask1d):
        if v and not inr: st, inr = i, True
        elif not v and inr:
            if i - st >= minlen: out.append((st, i - 1))
            inr = False
    if inr and len(mask1d) - st >= minlen: out.append((st, len(mask1d) - 1))
    return out

def S(x): return (x - 18.63) / 0.96123
def SY(y): return y / 0.95556

print("=== LABEL BOX BORDERS: red horizontal runs len>25, y 150..300 ===")
for y in range(150, 300):
    rr = runs(red[y, 60:890], 25)
    for s, e in rr:
        print(f"  y{y} x {s+60}..{e+60} len{e-s+1}  -> slide y {SY(y):.1f} x {S(s+60):.1f}..{S(e+60):.1f}")

print("=== red vertical runs len>12, x 60..890 in y 150..300 (sampled) ===")
for x in range(60, 890):
    rr = runs(red[150:300, x], 12)
    for s, e in rr:
        print(f"  x{x} y {s+150}..{e+150} len{e-s+1} -> slide x {S(x):.1f} y {SY(s+150):.1f}..{SY(e+150):.1f}")

print("=== TEXT LINES per box: ink bbox per color class, y-banded ===")
def band_ink(x0, x1, y0, y1, name):
    print(f"-- {name} region x{x0}..{x1} y{y0}..{y1}")
    for cname, m in [("red", red), ("blue", blue), ("green", green), ("mag", mag), ("yel", yel)]:
        sub = np.zeros_like(m)
        sub[y0:y1, x0:x1] = m[y0:y1, x0:x1]
        rows = sub.sum(axis=1)
        bands = []
        inb = False
        for i, v in enumerate(rows):
            if v > 0 and not inb: st, inb = i, True
            elif v == 0 and inb:
                bands.append((st, i - 1)); inb = False
        if inb: bands.append((st, len(rows) - 1))
        for s, e in bands:
            seg = sub[s:e + 1]
            xs = np.nonzero(seg.any(axis=0))[0]
            print(f"   {cname}: y {s+y0}..{e+y0} x {x0+xs.min()}..{x0+xs.max()} n={int(seg.sum())} -> slide y {SY(s+y0):.1f}..{SY(e+y0):.1f} x {S(x0+xs.min()):.1f}..{S(x0+xs.max()):.1f}")

band_ink(70, 310, 185, 245, "LEFT BOX")
band_ink(320, 600, 185, 245, "MIDDLE BOX")
band_ink(615, 890, 165, 280, "RIGHT BOX")

print("=== colored x-segments per text row band (which words are colored) ===")
def word_segs(x0, x1, y0, y1, mask, minlen=2):
    m = np.zeros_like(mask)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    cols = m.any(axis=0)
    return [(s + x0, e + x0) for s, e in runs(cols, minlen)]

for name, (x0, x1, y0, y1) in [("L1", (70, 310, 198, 214)), ("L2", (70, 310, 216, 236)),
                                ("M1", (320, 600, 198, 214)), ("M2", (320, 600, 216, 236)),
                                ("R1", (615, 890, 168, 186)), ("R2", (615, 890, 188, 208)),
                                ("R3", (615, 890, 210, 232))]:
    for cname, m in [("red", red), ("blue", blue), ("green", green), ("mag", mag)]:
        segs = word_segs(x0, x1, y0, y1, m)
        if segs: print(f"  {name} {cname}: {segs}")
