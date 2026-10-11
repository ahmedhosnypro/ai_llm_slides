#!/usr/bin/env python3
"""Slide 030: pale-pill text colors, border cores, bracket stems, underline, pill fills."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def core_stats(name, x0, y0, x1, y1):
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    lum = sub.sum(axis=1)
    dark = sub[np.argsort(lum)[:12]]
    bright = sub[np.argsort(lum)[-12:]]
    print(f"{name}: darkest12 {dark.tolist()[:6]} brightest12 {bright.tolist()[:6]}")

# matrix col2 cells
core_stats("matrix r1c2 sin(wd) region", 425, 356, 462, 378)
core_stats("matrix r2c2 cos(wd) region", 420, 398, 462, 422)
# deriv tails
core_stats("L1 final sin(wd)", 596, 249, 644, 268)
core_stats("L2 cos(wd)", 450, 295, 516, 314)
# pill fills (median)
def med(name, x0, y0, x1, y1):
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    print(f"{name} median {np.median(sub, axis=0)}")
med("vivid yellow pill (L1 t+d)", 150, 250, 186, 264)
med("pale pill L1 tail", 600, 252, 640, 264)
med("pale pill L2 cos(wd)", 455, 298, 512, 310)
med("green pill L1 cos(wd)", 436, 252, 488, 264)
med("green pill matrix r1c1", 310, 358, 370, 372)
med("yellow pill matrix r1c2", 430, 358, 460, 372)
med("yellow pill matrix r2c2", 425, 402, 458, 416)
med("remember fill", 600, 130, 840, 180)
med("note fill", 640, 380, 860, 460)
med("vecbox fill", 100, 60, 230, 85)

# border stroke cores: histogram darkest along strokes
def stroke_core(name, pts):
    vals = [tuple(im[y, x]) for (x, y) in pts]
    vals.sort(key=lambda v: sum(v))
    print(f"{name} darkest strokes: {vals[:4]}")
stroke_core("vecbox left border", [(x, 150) for x in range(88, 93)])
stroke_core("remember top border", [(700, y) for y in range(102, 107)])
stroke_core("remember left border", [(x, 140) for x in range(500, 505)])
stroke_core("deriv top border", [(400, y) for y in range(240, 245)])
stroke_core("matrix top border", [(400, y) for y in range(332, 337)])
stroke_core("note top border", [(750, y) for y in range(350, 355)])
stroke_core("note left border", [(x, 420) for x in range(622, 628)])

# underline scan rows 122..136, x505..600, loose navy mask
navy = (B - R > 25) & (B > 90)
print("underline scan:", [(y, int(navy[y, 505:600].sum())) for y in range(120, 138)])

# bracket stems: for each bracket, columns of vertical runs
def vruns(name, x0, x1, y0, y1, mask):
    print(f"-- {name}")
    for x in range(x0, x1):
        col = mask[y0:y1, x]
        if col.sum() > 25:
            ys = np.where(col)[0]
            print(f"   x={x} n={int(col.sum())} y{y0+ys[0]}..{y0+ys[-1]}")

RED = (R > 120) & (R - G > 55) & (R - B > 40)
BLACK = (np.maximum(np.maximum(R, G), B) < 110)
NAVY = (B - R > 40) & (B - G > 30) & (B > 90)
vruns("vecbox v1 left bracket (red)", 238, 258, 55, 140, RED)
vruns("vecbox v1 right bracket (red)", 320, 345, 55, 140, RED)
vruns("vecbox v2 left bracket (black)", 238, 258, 148, 235, BLACK)
vruns("vecbox v2 right bracket (black)", 348, 370, 148, 235, BLACK)
vruns("matrix left-vec left bracket (black)", 115, 135, 348, 435, BLACK)
vruns("matrix left-vec right bracket (black)", 225, 245, 348, 435, BLACK)
vruns("matrix left bracket (navy)", 275, 298, 348, 435, NAVY)
vruns("matrix right bracket (navy)", 462, 480, 348, 435, NAVY)
vruns("right-vec left bracket (red)", 480, 500, 348, 435, RED)
vruns("right-vec right bracket (red)", 560, 580, 348, 435, RED)

# bracket tick extents (horizontal runs at top/bottom rows)
def hrun(name, y, x0, x1, mask):
    row = mask[y, x0:x1]
    xs = np.where(row)[0]
    if len(xs): print(f"{name} y={y}: x{x0+xs[0]}..{x0+xs[-1]}")
    else: print(f"{name} y={y}: none")
print("== tick rows (top and bottom of each bracket) ==")
hrun("v1 Lbrk top", 60, 238, 258, RED); hrun("v1 Lbrk bottom", 134, 238, 258, RED)
hrun("v1 Rbrk top", 60, 320, 345, RED); hrun("v1 Rbrk bottom", 134, 320, 345, RED)
hrun("v2 Lbrk top", 154, 238, 258, BLACK); hrun("v2 Lbrk bottom", 227, 238, 258, BLACK)
hrun("v2 Rbrk top", 154, 348, 370, BLACK); hrun("v2 Rbrk bottom", 227, 348, 370, BLACK)
hrun("mLv Lbrk top", 355, 115, 135, BLACK); hrun("mLv Lbrk bottom", 428, 115, 135, BLACK)
hrun("mLv Rbrk top", 355, 225, 245, BLACK); hrun("mLv Rbrk bottom", 428, 225, 245, BLACK)
hrun("mtx Lbrk top", 355, 275, 298, NAVY); hrun("mtx Lbrk bottom", 428, 275, 298, NAVY)
hrun("mtx Rbrk top", 355, 462, 480, NAVY); hrun("mtx Rbrk bottom", 428, 462, 480, NAVY)
hrun("rvec Lbrk top", 355, 480, 500, RED); hrun("rvec Lbrk bottom", 428, 480, 500, RED)
hrun("rvec Rbrk top", 355, 560, 580, RED); hrun("rvec Rbrk bottom", 428, 560, 580, RED)
