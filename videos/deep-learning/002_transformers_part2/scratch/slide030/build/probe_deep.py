#!/usr/bin/env python3
"""Slide 030: deep probe - exact ink cores, all highlight blobs (loose), text line bboxes."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# LOOSE yellow: any warm yellow-ish (catches JPEG-darkened FFFF00)
yl = (R > 170) & (G > 150) & (R - B > 70) & (G - B > 50)
lab, n = ndi.label(yl)
print("=== ALL yellow-ish blobs >120px (loose) ===")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(xs) > 120:
        # core color = median of brightest 30%
        px = im[ys, xs]
        s = px.sum(axis=1); idx = np.argsort(-s)[:max(1, len(s)//3)]
        med = np.median(px[idx], axis=0).astype(int)
        print(f"  Y: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} px={len(xs)} core={tuple(med)}")

gr = (G > 120) & (G - R > 25) & (G - B > 25)
lab, n = ndi.label(gr)
print("=== ALL green-ish blobs >120px (loose) ===")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(xs) > 120:
        px = im[ys, xs]
        s = px.sum(axis=1); idx = np.argsort(-s)[:max(1, len(s)//3)]
        med = np.median(px[idx], axis=0).astype(int)
        print(f"  G: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} px={len(xs)} core={tuple(med)}")

def core(x0, y0, x1, y1, sel, label):
    reg = im[y0:y1, x0:x1]
    m = sel[y0:y1, x0:x1]
    if m.sum() == 0:
        print(f"{label}: none"); return
    px = reg[m]
    s = px.sum(axis=1)
    idx = np.argsort(s)[:max(1, len(s)//4)]  # darkest quartile = ink core
    print(f"{label}: n={m.sum()} core={tuple(np.median(px[idx],axis=0).astype(int))}")

redm = (R > 90) & (R - G > 50) & (R - B > 50)
blum = (B > 90) & (B - R > 30) & (B - G > 30)
blam = (R < 100) & (G < 100) & (B < 100)

print("=== INK CORES (darkest-quartile medians) ===")
core(95, 85, 250, 105, redm, "vecbox label1 red")
core(95, 180, 265, 205, redm, "vecbox label2 red")
core(230, 60, 370, 230, blam, "vecbox vector text black")
core(238, 62, 258, 225, redm, "vecbox v1 red bracket")
core(505, 105, 700, 195, blum, "remember text blue")
core(100, 245, 660, 270, blam, "deriv L1 black")
core(100, 290, 660, 315, blam, "deriv L2 black")
core(120, 355, 240, 425, blam, "matrix left vec text")
core(260, 350, 500, 430, blam, "matrix 2x2 text")
core(500, 350, 610, 430, blam, "matrix right vec text")
core(95, 440, 300, 465, redm, "caption1 red")
core(480, 440, 620, 465, redm, "caption2 red")
core(280, 455, 430, 490, redm, "brace red")
core(250, 478, 460, 500, blum, "Independent blue")
core(630, 385, 890, 410, redm, "note header red")
core(630, 405, 890, 490, blum, "note body blue")
core(640, 370, 680, 500, lambda *a: None, "skip")

# note box green border core
gren = (G > 100) & (G - R > 20) & (G - B > 20)
core(625, 380, 628, 460, gren, "note border green core")
# blue box border cores
core(87, 360, 90, 480, blum, "matrix box border blue core")
core(660, 250, 663, 320, blum, "deriv box border blue core")
core(90, 100, 93, 220, blum, "vecbox border blue core")

# fills: exact medians (pure fill pixels = mode)
def fillmode(x0, y0, x1, y1, label):
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    keys, counts = np.unique(reg, axis=0, return_counts=True)
    o = np.argsort(-counts)[:3]
    print(f"{label}: " + "  ".join(f"({keys[i][0]},{keys[i][1]},{keys[i][2]})x{counts[i]}" for i in o))
fillmode(600, 120, 820, 175, "remember fill mode")
fillmode(660, 400, 850, 460, "note fill mode")
fillmode(120, 120, 220, 170, "vecbox fill mode")
fillmode(120, 260, 400, 310, "deriv fill mode")
fillmode(120, 430, 250, 470, "matrix fill mode (lower left)")
