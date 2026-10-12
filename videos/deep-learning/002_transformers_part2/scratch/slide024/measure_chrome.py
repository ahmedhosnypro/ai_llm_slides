#!/usr/bin/env python3
"""Slide 024 chrome landmarks + frame->slide mapping.

Fits the mapping from the four chrome border landmarks (panel left/right/top,
bottom-border) exactly like slide_002's precedent, then cross-checks the badge.
"""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = img.shape
print("frame size", W, H)

def is_red(px):
    r, g, b = px
    return r > 140 and g < 90 and b < 90

# Panel left/right edge: scan a horizontal line through mid-slide (y=250)
y = 250
row = img[y]
left = right = None
for x in range(W):
    if is_red(row[x]):
        left = x
        break
for x in range(W - 1, -1, -1):
    if is_red(row[x]):
        right = x
        break
print(f"y={y}: red left={left} right={right}")

# Panel top edge: scan a vertical line through mid-slide (x=480)
x = 480
col = img[:, x]
top = None
for yy in range(H):
    if is_red(col[yy]):
        top = yy
        break
print(f"x={x}: red top={top}")

# bottom red border (half-visible stroke): scan up from bottom at x=480
bot = None
for yy in range(H - 1, -1, -1):
    if is_red(col[yy]):
        bot = yy
        break
print(f"x={x}: red bottom={bot}")

# cross-check at other columns/rows
for y2 in (200, 300, 400):
    r2 = img[y2]
    l2 = next((x2 for x2 in range(W) if is_red(r2[x2])), None)
    rr2 = next((x2 for x2 in range(W - 1, -1, -1) if is_red(r2[x2])), None)
    print(f"y={y2}: left={l2} right={rr2}")
for x2 in (200, 700, 850):
    c2 = img[:, x2]
    t2 = next((yy2 for yy2 in range(H) if is_red(c2[yy2])), None)
    b2 = next((yy2 for yy2 in range(H - 1, -1, -1) if is_red(c2[yy2])), None)
    print(f"x={x2}: top={t2} bottom={b2}")

# badge: find yellow FDFD96-ish disc in top-right quadrant
ys, xs = np.mgrid[0:H, 0:W]
reg = (xs > 800) & (ys < 130)
r_, g_, b_ = img[..., 0], img[..., 1], img[..., 2]
yellow = reg & (r_ > 220) & (g_ > 220) & (b_ < 190) & (b_ > 120)
if yellow.any():
    bx0, bx1 = xs[yellow].min(), xs[yellow].max()
    by0, by1 = ys[yellow].min(), ys[yellow].max()
    print(f"badge yellow bbox x {bx0}..{bx1} y {by0}..{by1} center=({(bx0+bx1)/2},{(by0+by1)/2}) d=({bx1-bx0},{by1-by0})")

# Fit mapping like slide_002: landmarks frame (L,R,T,B) <-> slide chrome (42, 919, 45, 540)
# slide_x = (fx - a)/s ; from L,R:  s = (R_f - L_f)/(919-42)
Lf, Rf, Tf, Bf = left, right, top, bot
sx = (Rf - Lf) / (919.0 - 42.0)
a = Lf - sx * 42.0
sy = (Bf - Tf) / (540.0 - 45.0)
# slide_y = (fy - b)/sy  ->  b = fy - sy*slide_y ; use top: slide_y=45
b0 = Tf - sy * 45.0
print(f"\nFIT: slide_x = (fx - {a:.3f}) / {sx:.6f}")
print(f"     slide_y = (fy - {b0:.3f}) / {sy:.6f}")
print(f"inverse: fx = {a:.3f} + {sx:.6f} * slide_x ; fy = {b0:.3f} + {sy:.6f} * slide_y")
# badge cross-check: house badge center (893,71)
bx_f, by_f = a + sx * 893.0, b0 + sy * 71.0
print(f"house badge (893,71) maps to frame ({bx_f:.1f},{by_f:.1f}) — compare with measured yellow-bbox center")
