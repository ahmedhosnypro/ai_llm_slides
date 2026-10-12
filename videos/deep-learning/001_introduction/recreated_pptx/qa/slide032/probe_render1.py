#!/usr/bin/env python3
"""Clean probe of qa/slide032/render_1.png (2001x1125 @150dpi; frame px = render/2.0833).
Tight per-element bands (no neighbor bleed) + hunt the brown ink right of the plane."""
import numpy as np
from PIL import Image

R = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide032/render_1.png"
).convert("RGB")).astype(int)
H, W = R.shape[:2]
S = 2001.0 / 960.0  # render px per frame px
r, g, b = R[:, :, 0], R[:, :, 1], R[:, :, 2]

red = (r > 130) & (g < 90) & (b < 90)
blue = (b > 110) & (b > r + 50) & (b > g + 40)
brown = (r > 130) & (r < 215) & (g > 55) & (g < 140) & (b < 70)
black = (r < 70) & (g < 70) & (b < 70)

def fx(v): return v / S  # render px -> frame px

def band_bbox(mask, y0f, y1f, x0f, x1f, label):
    y0, y1, x0, x1 = int(y0f * S), int(y1f * S), int(x0f * S), int(x1f * S)
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        print(f"{label}: EMPTY")
        return
    print(f"{label}: frame bbox x {fx(x0+xs.min()):.1f}..{fx(x0+xs.max()):.1f}  "
          f"y {fx(y0+ys.min()):.1f}..{fx(y0+ys.max()):.1f}  n={len(ys)}")

print("== title (band y 55..120 frame, x 60..880 EXCLUDES chrome border/badge) ==")
band_bbox(red, 55, 122, 60, 880, "title red ink")

print("\n== body lines (tight heavy bands, frame coords) ==")
for i, (y0, y1, x1w) in enumerate([(144, 172, 600), (170, 199, 600),
                                   (233, 261, 600), (258, 290, 600),
                                   (320, 350, 600), (346, 378, 600)]):
    band_bbox(blue, y0, y1, 60, x1w, f"L{i+1}")

print("\n== brown hunt: right of plane (x 775..812, y 310..500) ==")
y0, y1, x0, x1 = int(310 * S), int(500 * S), int(775 * S), int(812 * S)
sub = brown[y0:y1, x0:x1]
ys, xs = np.where(sub)
if len(ys):
    ys_f = [fx(y0 + v) for v in (ys.min(), ys.max())]
    xs_f = [fx(x0 + v) for v in (xs.min(), xs.max())]
    print(f"brown right of plane: x {xs_f[0]:.1f}..{xs_f[1]:.1f} y {ys_f[0]:.1f}..{ys_f[1]:.1f} n={len(ys)}")
    # sample the actual colors
    pts = list(zip(ys[:10], xs[:10]))
    for yy, xx in pts[:6]:
        print(f"  sample at frame ({fx(x0+xx):.1f},{fx(y0+yy):.1f}): RGB {tuple(R[y0+yy, x0+xx])}")
else:
    print("no brown right of plane")

print("\n== plane bbox tight (x 600..810, y 300..500) ==")
band_bbox(brown, 300, 500, 600, 810, "plane brown")

print("\n== red arrow region tight (x 740..800, y 360..460) ==")
band_bbox(red, 360, 460, 740, 800, "arrow red")

print("\n== word Filters red (x 770..850, y 436..462) ==")
band_bbox(red, 436, 462, 770, 850, "'Filters'")

print("\n== label 2-D Image (x 620..890, y 222..258) ==")
band_bbox(red, 222, 258, 620, 890, "label")

print("\n== black bar (y 505..540, x 20..940) ==")
band_bbox(black, 505, 540, 20, 940, "black bar")

print("\n== 'Grayscale' black (x 670..880, y 270..312) ==")
band_bbox(black, 270, 312, 670, 880, "'Grayscale'")

print("\n== per-line row profiles in render (blue, frame-y) for baseline check ==")
for i, (y0, y1) in enumerate([(144, 200), (233, 290), (320, 378)]):
    y0i, y1i = int(y0 * S), int(y1 * S)
    prof = blue[y0i:y1i, int(80 * S):int(600 * S)].sum(axis=1)
    rows = [(fx(y0 + j), int(v)) for j, v in enumerate(prof) if v > 0]
    # print first/last few
    print(f"L-group {i+1}: first rows {rows[:3]} ... last rows {rows[-3:]}")
