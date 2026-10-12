#!/usr/bin/env python3
"""Measure slide_040.jpg (960x540, 1px=1pt=1/72in) — chrome + content geometry."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_040.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Panel gray extent (sample text-free bands)
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
band = gray[80:520, :]
cols = np.where(band.sum(axis=0) > (520 - 80) * 0.5)[0]
print(f"panel gray cols: {cols.min()}..{cols.max()}")
bandc = gray[:, 60:160]
rows = np.where(bandc.sum(axis=1) > 80)[0]
print(f"panel gray rows (left band): {rows.min()}..{rows.max()}")

# Red pixels (border + title)
red = (r > 130) & (g < 90) & (b < 90)
# Border strokes: columns where red spans many rows
col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
print("red-heavy cols (border verticals):", [c for c in np.where(col_red > 200)[0]])
print("red-heavy rows (border horizontals):", [x for x in np.where(row_red > 400)[0]])

# Title red text: red pixels inside panel, away from border
inner = red[60:520, 50:910]
ys, xs = np.where(inner)
if len(ys):
    print(f"inner red text bbox: x {xs.min()+50}..{xs.max()+50}, y {ys.min()+60}..{ys.max()+60}  (h={ys.max()-ys.min()+1}px)")
    # row profile of the red text to see line bands
    rr = inner.sum(axis=1)
    bands = []
    s = None
    for i, v in enumerate(rr):
        if v > 2 and s is None:
            s = i
        elif v <= 2 and s is not None:
            bands.append((s + 60, i - 1 + 60)); s = None
    if s is not None:
        bands.append((s + 60, len(rr) - 1 + 60))
    print("inner red row bands:", bands)

# Blue text
blue = (b > 110) & (r < 110) & (g < 110)
innerb = blue[60:540, 50:910]
ys, xs = np.where(innerb)
if len(ys):
    print(f"inner blue text bbox: x {xs.min()+50}..{xs.max()+50}, y {ys.min()+60}..{ys.max()+60}")
    rr = innerb.sum(axis=1)
    bands = []
    s = None
    for i, v in enumerate(rr):
        if v > 2 and s is None:
            s = i
        elif v <= 2 and s is not None:
            bands.append((s + 60, i - 1 + 60)); s = None
    if s is not None:
        bands.append((s + 60, len(rr) - 1 + 60))
    print("inner blue row bands:", bands)
    # per-band x extent
    for (y0, y1) in bands:
        sub = innerb[y0 - 60:y1 - 60 + 1, :]
        ys2, xs2 = np.where(sub)
        print(f"  blue band y {y0}-{y1} (h={y1-y0+1}): x {xs2.min()+50}..{xs2.max()+50}")

# Badge: yellow disc top-right
yel = (r > 200) & (g > 200) & (b < 190)
ys, xs = np.where(yel)
if len(ys):
    print(f"badge yellow bbox: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}  center=({(xs.min()+xs.max())/2:.1f},{(ys.min()+ys.max())/2:.1f}) d~{xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}")

# Badge numeral (dark pixels inside badge bbox)
if len(ys):
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    dark = (r < 120) & (g < 120) & (b < 120)
    sub = dark[y0:y1 + 1, x0:x1 + 1]
    ys2, xs2 = np.where(sub)
    if len(ys2):
        print(f"badge numeral bbox: x {xs2.min()+x0}..{xs2.max()+x0}, y {ys2.min()+y0}..{ys2.max()+y0} (h={ys2.max()-ys2.min()+1})")

# Purple ring
pur = (b > 150) & (r > 70) & (r < 180) & (g < 130)
ys, xs = np.where(pur)
if len(ys):
    print(f"purple ring bbox: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")

# Sample colors
print("panel gray sample (300,300):", im[300, 300])
print("white margin sample (10,300):", im[10, 300])
print("red border sample (row 300, col", cols.min(), "):", im[300, cols.min()])
print("title red sample at red text center:", None)
