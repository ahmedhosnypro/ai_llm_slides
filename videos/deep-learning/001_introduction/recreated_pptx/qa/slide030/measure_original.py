#!/usr/bin/env python3
"""PIL ink forensics for slide 030 original (960x540, 1px = 1pt).
Measures: chrome region colors, red content frame, black bottom bar, title ink,
left panel + caption + photo + matrix, arrow, right panel + image, cursor artifact.
Pure numeric output (no image bytes to context)."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{name}: NO PIXELS")
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(f"{name}: bbox x[{x0}..{x1}] y[{y0}..{y1}]  px={int(mask.sum())}")
    return (x0, y0, x1, y1)

print("=== sample colors ===")
for (x, y, lbl) in [(20, 20, "top-left corner (outside panel?)"), (480, 20, "top-center"),
                    (480, 300, "center bg"), (20, 300, "left edge bg"), (940, 300, "right edge bg"),
                    (480, 535, "bottom strip"), (480, 520, "near-bottom"), (100, 250, "left panel?"),
                    (480, 80, "title band"), (700, 300, "right panel area")]:
    print(f"  ({x},{y}) {lbl}: #{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}")

# red-ish mask (C00000 family): strong R, low G/B
red = (R > 130) & (G < 90) & (B < 90)
print("\n=== red ink (C00000 family) ===")
bbox(red, "all red")

# scan red per row to find horizontal frame edges (long horizontal runs)
rowsum = red.sum(axis=1)
colsum = red.sum(axis=0)
print("rows with >400 red px (frame horizontals):", [int(y) for y in np.where(rowsum > 400)[0]])
print("cols with >200 red px (frame verticals):", [int(x) for x in np.where(colsum > 200)[0]])

# black mask
black = (R < 70) & (G < 70) & (B < 70)
print("\n=== black ink ===")
rows_black = black.sum(axis=1)
print("rows with >500 black px (bottom bar?):", [int(y) for y in np.where(rows_black > 500)[0]])
if len(np.where(rows_black > 500)[0]):
    y0 = int(np.where(rows_black > 500)[0].min()); y1 = int(np.where(rows_black > 500)[0].max())
    seg = black[y0:y1+1]
    xs = np.where(seg.any(axis=0))[0]
    print(f"  bar: y[{y0}..{y1}] x[{xs.min()}..{xs.max()}]")

# title region: red ink in y<120
title = red.copy(); title[120:, :] = False
print("\n=== title (red ink y<120) ===")
tb = bbox(title, "title ink")
if tb:
    x0, y0, x1, y1 = tb
    # column profile to see word gaps
    colp = title.sum(axis=0)
    nz = np.where(colp > 0)[0]
    gaps = []
    prev = nz[0]
    for x in nz[1:]:
        if x - prev > 8:
            gaps.append((int(prev), int(x)))
        prev = x
    print("  title word gaps (>8px):", gaps[:20])
    # row profile for line count
    rowp = title.sum(axis=1)
    nzr = np.where(rowp > 0)[0]
    segs = []
    start = nzr[0]; prev = nzr[0]
    for y in nzr[1:]:
        if y - prev > 3:
            segs.append((int(start), int(prev))); start = y
        prev = y
    segs.append((int(start), int(prev)))
    print("  title line row-segments:", segs)

# left panel: white box. Find near-white region in left half
white = (R > 235) & (G > 235) & (B > 235)
print("\n=== white regions ===")
wl = white.copy(); wl[:, 480:] = False; wl[120:, :] = wl[120:, :]  # left half
wr = white.copy(); wr[:, :480] = False
bbox(wl, "white left half")
bbox(wr, "white right half")

# left panel red border: red ink in region x<500, y>100 excluding matrix (matrix is x~150-400,y~300-440)
red_left = red.copy(); red_left[:, 500:] = False; red_left[:100, :] = False
print("\n=== red in left half (y>100) ===")
bbox(red_left, "red left")
# column/row profiles of red-left
rl_cols = red_left.sum(axis=0); rl_rows = red_left.sum(axis=1)
print("  red-left cols>50:", [int(x) for x in np.where(rl_cols > 50)[0]])
print("  red-left rows>50:", [int(y) for y in np.where(rl_rows > 50)[0]])

# photo region inside left panel: pixels that are neither near-white nor near-gray-bg nor red
photo = ~white & ~red & ~(((R - G).abs() if hasattr(R - G, 'abs') else abs(R - G)) < 25) if False else None
diff_rg = np.abs(R - G) + np.abs(G - B)
nonflat = diff_rg > 30  # colorful-ish (photo has cream cat, shadows)
print("\n=== photo-ish (non-flat color) left half ===")
pl = nonflat.copy(); pl[:, 500:] = False
bbox(pl, "photo-ish left")

# matrix red ink: red in left half, y 250..470
mtx = red.copy(); mtx[:, 500:] = False; mtx[:250, :] = False; mtx[480:, :] = False
print("\n=== matrix red ink (left, y250-480) ===")
bbox(mtx, "matrix ink")

# right panel red border: red in x>480
red_right = red.copy(); red_right[:, :480] = False; red_right[:100, :] = False
print("\n=== red in right half (y>100) ===")
bbox(red_right, "red right")
rr_cols = red_right.sum(axis=0); rr_rows = red_right.sum(axis=1)
print("  red-right cols>50:", [int(x) for x in np.where(rr_cols > 50)[0]])
print("  red-right rows>50:", [int(y) for y in np.where(rr_rows > 50)[0]])

# arrow: red in center gap x 440..540
arrow = red.copy(); arrow[:, :440] = False; arrow[:, 560:] = False
print("\n=== arrow (red x440-560) ===")
bbox(arrow, "arrow ink")

# dark (near-black) ink in right panel = the sobel image; find its bbox via low luminance
lum = 0.299 * R + 0.587 * G + 0.114 * B
dark = lum < 100
dr = dark.copy(); dr[:, :500] = False; dr[:120, :] = False; dr[500:, :] = False
print("\n=== dark image region (right half) ===")
bbox(dr, "dark right")

# caption ink: dark pixels in left panel above photo (y 150..260, x 60..470)
cap = dark.copy(); cap[:140, :] = False; cap[280:, :] = False; cap[:, :60] = False; cap[:, 470:] = False
print("\n=== caption ink (left panel, y140-280) ===")
bbox(cap, "caption ink")

# cursor artifact: look for saturated white arrow shape over matrix region — check for
# pixels with very high brightness within matrix bbox
print("\n=== bright pixels inside matrix bbox (cursor?) ===")
if mtx.sum():
    x0, y0, x1, y1 = np.where(mtx)[1].min(), np.where(mtx)[0].min(), np.where(mtx)[1].max(), np.where(mtx)[0].max()
    sub = lum[y0:y1+1, x0:x1+1]
    bright = sub > 235
    ys, xs = np.where(bright)
    if len(xs):
        print(f"  bright px={len(xs)} local bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] -> global x[{x0+xs.min()}..{x0+xs.max()}] y[{y0+ys.min()}..{y0+ys.max()}]")
    else:
        print("  none")

# watermark: bottom-left of right image — bright tiny ink near dark image bottom-left
print("\n=== bottom-left corner of right dark image ===")
if dr.sum():
    x0, y0, x1, y1 = np.where(dr)[1].min(), np.where(dr)[0].min(), np.where(dr)[1].max(), np.where(dr)[0].max()
    print(f"  dark image bbox: x[{x0}..{x1}] y[{y0}..{y1}]")
    sub = lum[y1-40:y1+1, x0:x0+140]
    br = sub > 120
    ys, xs = np.where(br)
    if len(xs):
        print(f"  lighter ink px={len(xs)} local x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
    else:
        print("  none (uniform dark)")

# meme captions in left photo: white text on photo (top of photo) — bright pixels inside photo bbox
print("\n=== left photo bbox refined ===")
# photo: non-white, non-red, non-gray-bg within left panel interior
panel_white = (R > 225) & (G > 225) & (B > 225)
inside = np.zeros_like(panel_white)
inside[140:470, 60:470] = True
photoish = (~panel_white) & (~red) & inside
ys, xs = np.where(photoish)
print(f"  non-white/red content in panel interior: x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
