#!/usr/bin/env python3
"""Diff slide_024.jpg vs slide_023.jpg in slide coordinates (each via its own mapping).

Mapping fit (slide_002 precedent): landmarks frame (L,R,T,B) <-> slide (42,919,45,540).
"""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"

def load(n):
    return np.asarray(Image.open(f"{V}/unique_slides/slide_{n:03d}.jpg").convert("RGB")).astype(int)

def landmarks(img):
    H, W, _ = img.shape
    # border ink: reddish-dark pixel
    def is_border(px):
        r, g, b = px
        return (r < 200 and r > g + 40 and r > b + 40) or (r < 150 and g < 80 and b < 80)
    y = 250
    L = next((x for x in range(W) if is_border(img[y, x])), None)
    R = next((x for x in range(W - 1, -1, -1) if is_border(img[y, x])), None)
    x = 480
    T = next((yy for yy in range(H) if is_border(img[yy, x])), None)
    B = next((yy for yy in range(H - 1, -1, -1) if is_border(img[yy, x])), None)
    return L, R, T, B

def fit(L, R, T, B):
    sx = (R - L) / (919.0 - 42.0)
    a = L - sx * 42.0
    sy = (B - T) / (540.0 - 45.0)
    b = T - sy * 45.0
    return a, sx, b, sy

f23, f24 = load(23), load(24)
L23, R23, T23, B23 = landmarks(f23)
L24, R24, T24, B24 = landmarks(f24)
print("frame23 landmarks L,R,T,B =", L23, R23, T23, B23)
print("frame24 landmarks L,R,T,B =", L24, R24, T24, B24)
a23, sx23, b23, sy23 = fit(L23, R23, T23, B23)
a24, sx24, b24, sy24 = fit(L24, R24, T24, B24)
print(f"map23: fx={a23:.3f}+{sx23:.6f}sx  fy={b23:.3f}+{sy23:.6f}sy")
print(f"map24: fx={a24:.3f}+{sx24:.6f}sx  fy={b24:.3f}+{sy24:.6f}sy")

# Resample frame23 into frame24's pixel grid via slide coords:
# for each frame24 pixel (fx24, fy24): slide = ((fx24-a24)/sx24, (fy24-b24)/sy24)
# then frame23 pixel = (a23 + sx23*sx, b23 + sy23*sy)
ys, xs = np.mgrid[0:540, 0:960]
sx_coord = (xs - a24) / sx24
sy_coord = (ys - b24) / sy24
fx23 = a23 + sx23 * sx_coord
fy23 = b23 + sy23 * sy_coord
fx23c = np.clip(np.round(fx23).astype(int), 0, 959)
fy23c = np.clip(np.round(fy23).astype(int), 0, 539)
w23 = f23[fy23c, fx23c]

diff = np.abs(f24 - w23).sum(axis=2)
print("diff stats: mean %.2f  p99 %d  max %d" % (diff.mean(), np.percentile(diff, 99), diff.max()))
big = diff > 90
print("big-diff pixel count:", int(big.sum()))
# connected row/col profile: print dense regions
rows = big.sum(axis=1)
print("rows with >40 big-diff px:")
in_run = False
for yy in range(540):
    if rows[yy] > 40 and not in_run:
        start = yy; in_run = True
    elif rows[yy] <= 40 and in_run:
        print(f"  y {start}..{yy-1}  (peak {rows[start:yy].max()})")
        in_run = False
if in_run:
    print(f"  y {start}..539")

Image.fromarray((np.clip(diff, 0, 255)).astype(np.uint8)).save(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide024/diff23_24.png")
Image.fromarray(big.astype(np.uint8) * 255).save(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide024/diff23_24_mask.png")
print("saved diff heatmaps")
