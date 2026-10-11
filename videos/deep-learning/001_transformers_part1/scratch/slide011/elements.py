#!/usr/bin/env python3
"""Precise element measurement on slide_011.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs_of(idx, gap=2, minlen=2):
    out = []
    s = p = None
    for i in idx:
        if s is None: s = p = i
        elif i <= p + gap: p = i
        else:
            out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return [(s, e) for (s, e) in out if e - s + 1 >= minlen]

def report(mask, name, rowthr=8):
    ys, xs = np.where(mask)
    if not len(xs):
        print(f"{name}: NONE"); return
    print(f"\n== {name}: n={len(xs)} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
    rc = np.bincount(ys, minlength=H)
    rows = np.where(rc >= rowthr)[0]
    for (s, e) in runs_of(rows, gap=3):
        band = mask[s:e+1, :]
        cc = np.bincount(np.where(band)[1], minlength=W)
        cols = np.where(cc >= 2)[0]
        cr = runs_of(cols, gap=6, minlen=3)
        print(f"   rows y[{s},{e}] (h={e-s+1}) col-runs: {cr[:14]}")

# yellow block
yellow = (r > 210) & (g > 210) & (b < 120)
report(yellow, "YELLOW block", rowthr=30)

# orange block
orange = (r > 230) & (g > 120) & (g < 205) & (b > 50) & (b < 155) & (r - g > 40) & (r - b > 70)
report(orange, "ORANGE block", rowthr=30)

# lavender tint (b - r >= 12, light)
lav = (b - r >= 12) & (b - g >= 10) & (r > 195) & (g > 195) & (b > 210)
report(lav, "LAVENDER tint", rowthr=6)

# beige tint
beige = (r - b >= 9) & (r - b <= 30) & (g - b >= 4) & (r > 225) & (g > 222)
report(beige, "BEIGE tint", rowthr=20)

# neutral gray BFBFBF
gray = (np.abs(r - g) < 10) & (np.abs(g - b) < 10) & (r > 160) & (r < 218)
report(gray, "GRAY BFBFBF", rowthr=25)

# strong red (incl dark red border)
red = (r > 120) & (r - g > 120) & (r - b > 100)
report(red, "RED strong", rowthr=4)

# blue
blue = (b - r > 60) & (b > 150) & (r < 140)
report(blue, "BLUE", rowthr=4)

# dark ink
dark = (r < 100) & (g < 100) & (b < 100)
report(dark, "DARK ink", rowthr=4)

# pink salmon
pink = (r > 225) & (g > 120) & (g < 200) & (b > 120) & (b < 200) & (r - g > 45) & (np.abs(g - b) < 40)
report(pink, "PINK salmon", rowthr=2)
