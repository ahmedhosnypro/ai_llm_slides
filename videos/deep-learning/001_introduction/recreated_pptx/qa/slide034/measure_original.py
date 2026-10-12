#!/usr/bin/env python3
"""Measure slide_034.jpg (960x540, 1px = 1pt) — 'What would a k-D filter looks like?'.

Regions (from spec): red content frame; red bold title; handwritten header
'e.g. Sobel 2-D filter'; left Grumpy-Cat meme w/ red matrix; RGB channel stack
(3 tinted copies); red '3-D Filter' label; isometric 3x3x3 cube + 'Third D'
yellow annotation; letterbox bar at bottom (artifact, not recreated).
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

print("== global background samples ==")
for (x, y, tag) in [(10, 10, "outer-left-top"), (950, 20, "outer-right-top"),
                    (30, 300, "outer-left-mid"), (940, 300, "outer-right-mid"),
                    (480, 30, "above-panel?"), (480, 60, "panel top strip"),
                    (50, 500, "panel bottom-left"), (480, 250, "center")]:
    print(f"  ({x},{y}) {tag}: {tuple(im[y, x])}")

print("== letterbox (black rows) ==")
dark = (r < 60) & (g < 60) & (b < 60)
rowdark = dark.sum(axis=1)
for y in range(H - 1, 400, -1):
    if rowdark[y] > 800:
        print(f"  row {y}: {rowdark[y]} dark px")
last = max(y for y in range(H) if rowdark[y] > 800)
first = min(y for y in range(H) if rowdark[y] > 800)
print(f"  letterbox rows {first}..{last}")

print("== red pixels profile (C00000-ish) ==")
red = (r > 120) & (g < 110) & (b < 110)
colred = red.sum(axis=0)
rowred = red.sum(axis=1)
print("  cols with >200 red px:", [int(c) for c in np.where(colred > 200)[0]])
print("  rows with >200 red px:", [int(y) for y in np.where(rowred > 200)[0]])
print("  cols with >100 red px:", [int(c) for c in np.where(colred > 100)[0]])
print("  rows with >100 red px:", [int(y) for y in np.where(rowred > 100)[0]])


def bbox(mask, x0, y0, x1, y1, tag):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"  {tag}: EMPTY in window x{x0}..{x1} y{y0}..{y1}")
        return None
    bx0, bx1 = x0 + xs.min(), x0 + xs.max()
    by0, by1 = y0 + ys.min(), y0 + ys.max()
    print(f"  {tag}: x {bx0}..{bx1} (w {bx1-bx0+1}), y {by0}..{by1} (h {by1-by0+1}), n={len(xs)}")
    return (bx0, by0, bx1, by1)


print("== non-white content in window inside presumed frame ==")
# find frame first from red profile above; provisional content mask:
nonwhite = (r < 225) | (g < 225) | (b < 225)

print("== title (red text) ==")
title = bbox(red & (rowred[:, None].T * 0 + 1).astype(bool), 100, 55, 880, 110, "red ink y55..110") if False else None
bbox(red, 100, 55, 880, 115, "title red ink window")

print("== header 'e.g. Sobel 2-D filter' (dark ink upper-left) ==")
darkink = (r < 120) & (g < 120) & (b < 120)
bbox(darkink, 60, 160, 360, 220, "header dark ink window")

print("== left meme photo (non-white block left side) ==")
# meme is a photo: pixels differ from white substantially; find bbox in window
photo = (abs(r - g) > 12) | (abs(g - b) > 12) | (r < 200)
bbox(photo, 60, 195, 360, 460, "left meme-ish window (photo/colored)")

print("== RGB stack (strong tints center-right) ==")
strong = ((r - g > 60) & (r - b > 60)) | ((g - r > 50) & (g - b > 50)) | ((b - r > 60) & (b - g > 60))
bbox(strong, 380, 180, 800, 470, "strong tint window x380..800")

print("== red text '3-D Filter' (right, above cube) ==")
bbox(red, 760, 180, 920, 240, "3-D Filter window")

print("== cube region (gray faces + black lines far right) ==")
grayish = (abs(r - g) < 14) & (abs(g - b) < 14) & (r > 150) & (r < 240)
bbox(grayish, 700, 250, 920, 470, "cube gray faces window")

print("== Third D yellow ==")
yel = (r > 200) & (g > 180) & (b < 140)
bbox(yel, 640, 340, 830, 480, "yellow label window")

print("== red matrix on meme (left panel red ink below title) ==")
bbox(red, 60, 200, 360, 470, "left red ink window")

print("== color samples ==")
for (x, y, tag) in [(90, 300, "meme left"), (200, 300, "meme center"), (300, 350, "meme right-low"),
                    (500, 260, "rgb stack"), (860, 300, "cube right face"), (820, 280, "cube top"),
                    (480, 120, "inside frame under title"), (480, 470, "inside frame bottom")]:
    print(f"  ({x},{y}) {tag}: {tuple(im[y, x])}")
