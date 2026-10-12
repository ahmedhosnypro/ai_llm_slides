#!/usr/bin/env python3
"""Slide 030: per-token ink colors + highlight/glyph boundary profiles."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (R + G + B) / 3
redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)
blam = (R < 110) & (G < 110) & (B < 110)

def tokencolor(x0, y0, x1, y1, label):
    nr = int(redm[y0:y1, x0:x1].sum()); nb = int(blum[y0:y1, x0:x1].sum())
    nk = int(blam[y0:y1, x0:x1].sum())
    kind = "RED" if nr > nb and nr > nk else ("BLUE" if nb > nk else "BLACK")
    print(f"{label}: red={nr} blue={nb} black={nk} -> {kind}")

print("== DERIV L1 token colors ==")
tokencolor(103, 249, 192, 267, "L1 sin(w(t+d))")
tokencolor(200, 249, 209, 267, "L1 = 1")
tokencolor(217, 249, 314, 267, "L1 sin(wt +wd)")
tokencolor(350, 249, 358, 267, "L1 = 2")
tokencolor(366, 249, 420, 267, "L1 sin(wt)")
tokencolor(429, 249, 494, 267, "L1 cos(wd)")
tokencolor(503, 249, 510, 267, "L1 +")
tokencolor(519, 249, 579, 267, "L1 cos(wt)")
tokencolor(587, 249, 647, 267, "L1 sin(wd)")
print("== DERIV L2 token colors ==")
tokencolor(104, 295, 199, 312, "L2 cos(w(t+d))")
tokencolor(207, 295, 215, 312, "L2 = 1")
tokencolor(223, 295, 326, 312, "L2 cos(wt +wd)")
tokencolor(350, 295, 358, 312, "L2 = 2")
tokencolor(366, 295, 426, 312, "L2 cos(wt)")
tokencolor(434, 295, 499, 312, "L2 cos(wd)")
tokencolor(508, 295, 511, 312, "L2 -")
tokencolor(520, 295, 574, 312, "L2 sin(wt)")
tokencolor(582, 295, 649, 312, "L2 sin(wd)")
print("== MATRIX cells ==")
tokencolor(125, 359, 232, 376, "lv r1 Sin(w(t+d))")
tokencolor(127, 398, 231, 415, "lv r2 cos(w(t+d))")
tokencolor(303, 353, 370, 376, "mx r1c1 cos(wd)")
tokencolor(388, 353, 448, 376, "mx r1c2 sin(wd)")
tokencolor(305, 401, 366, 421, "mx r2c1 sin(wd)")
tokencolor(384, 401, 449, 421, "mx r2c2 cos(wd)")
tokencolor(503, 364, 566, 381, "rv r1 sin(wt)")
tokencolor(503, 410, 562, 427, "rv r2 cos(wt)")

def profile(x0, x1, y0, y1, label):
    dark = (lum[y0:y1, x0:x1] < 140).sum(axis=0)
    print(f"{label}:")
    runs = []
    for i, v in enumerate(dark):
        if v > 0:
            runs.append(f"{i+x0}:{v}")
    print("  " + " ".join(runs))

print("== L1 highlight/glyph boundary (x140..215, y249..267) ==")
profile(140, 215, 249, 267, "L1 dark-ink cols")
ym = (R > 170) & (G > 150) & (R - B > 70)
prof = ym[245:270, 140:215].sum(axis=0)
yspan = [f"{i+140}" for i, v in enumerate(prof) if v > 5]
print("  yellow cols(>5):", yspan[0], "..", yspan[-1])
print("== v2 r1 boundary (x290..360, y152..174) ==")
profile(290, 360, 152, 174, "v2r1 dark cols")
prof = ym[150:178, 290:360].sum(axis=0)
ys = [i + 290 for i, v in enumerate(prof) if v > 5]
print("  yellow cols(>5):", ys[0], "..", ys[-1] if ys else None)
print("== mx lv r1 boundary (x170..240, y359..376) ==")
profile(170, 240, 359, 376, "lvl r1 dark cols")
prof = ym[352:380, 170:240].sum(axis=0)
ys = [i + 170 for i, v in enumerate(prof) if v > 5]
print("  yellow cols(>5):", ys[0], "..", ys[-1] if ys else None)
