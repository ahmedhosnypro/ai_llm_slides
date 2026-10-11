#!/usr/bin/env python3
"""Slide 030: core color sampling + pill connected components + crops."""
import numpy as np
from PIL import Image

im0 = Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")
im = np.asarray(im0).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def darkest_in(x0, y0, x1, y1, n=6):
    sub = im[y0:y1, x0:x1]
    lum = sub.sum(axis=2)
    idx = np.argsort(lum, axis=None)[:n]
    px = [tuple(sub[i // (x1 - x0), i % (x1 - x0)]) for i in idx]
    return px

def most_saturated(x0, y0, x1, y1, chan="B", n=6):
    sub = im[y0:y1, x0:x1]
    if chan == "B": score = sub[:, :, 2] - sub[:, :, 0]
    elif chan == "R": score = sub[:, :, 0] - sub[:, :, 1]
    else: score = sub[:, :, 1] - sub[:, :, 0]
    idx = np.argsort(score, axis=None)[-n:]
    return [tuple(sub[i // (x1 - x0), i % (x1 - x0)]) for i in idx]

print("vecbox border blue core:", most_saturated(89, 130, 92, 160))
print("vecbox v1 cell ink (x262..312 y65..90):", darkest_in(262, 65, 312, 90))
print("vecbox v1 bracket stem (x242..245 y80..120):", most_saturated(242, 80, 246, 120, "R"))
print("vecbox v2 cell ink (x262..300 y160..185):", darkest_in(262, 160, 300, 185))
print("remember blue text core (x511..590 y112..122):", most_saturated(511, 112, 590, 122))
print("remember fill:", im[135, 700], im[140, 550])
print("remember underline rows y122..130 x511..591 blue counts:", [(y, int(((B[y, 511:591] > 100) & (B[y, 511:591] - R[y, 511:591] > 40)).sum())) for y in range(121, 131)])
print("deriv black ink core:", darkest_in(217, 250, 316, 266))
print("deriv red ink core (x368..424):", most_saturated(368, 251, 424, 265, "R"))
print("deriv yellow pill core:", im[258, 470], im[255, 160])
print("deriv green pill core:", im[258, 460], im[300, 610])
print("matrix left-bracket blue core (x279..282 y390..410):", most_saturated(279, 390, 283, 410))
print("matrix right-bracket blue core (x465..468):", most_saturated(465, 390, 469, 410))
print("matrix left-vec bracket (x119..123 y390):", darkest_in(119, 390, 124, 410))
print("right-vec bracket red core (x484..488):", most_saturated(484, 390, 489, 410, "R"))
print("right-vec cell ink (x503..560 y365..390):", most_saturated(503, 365, 560, 390, "R")[:4], darkest_in(503, 365, 560, 390)[:4])
print("brace red core (x272..475 y447..467):", most_saturated(300, 450, 450, 465, "R")[:4])
print("blue label core (x259..478 y481..494):", most_saturated(259, 481, 478, 494)[:4])
print("note box border right col scan x855..875 y400:")
for x in range(855, 876):
    print(f"  x={x} {tuple(im[400, x])}")
print("note box border top row scan y336..352 x750:")
for y in range(336, 353):
    print(f"  y={y} {tuple(im[y, 750])}")
print("note fill:", im[380, 700], im[455, 700])
print("note green text core (x634..856 y392..404):", most_saturated(634, 392, 856, 404))
print("note red header core:", most_saturated(634, 361, 844, 375, "R")[:4])
print("badge numeral ink:", darkest_in(868, 62, 884, 78, 3))
print("panel bg (between boxes):", im[240, 700], im[320, 750], im[60, 500])

# yellow pills connected components over derivation band
from scipy import ndimage
YEL = (R > 200) & (G > 180) & (B < 130)
GRN = (G > 140) & (G - R > 25) & (G - B > 30)
for name, mask, y0, y1 in (("derivL1", YEL, 244, 272), ("derivL2", YEL, 290, 318),
                            ("vecbox2", YEL, 148, 232), ("matrixband", YEL, 348, 435),
                            ("derivL1g", GRN, 244, 272), ("derivL2g", GRN, 290, 318),
                            ("matrixband-g", GRN, 348, 435)):
    lab, n = ndimage.label(mask[y0:y1, 90:660])
    print(f"-- {name} components:")
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) > 40:
            print(f"   x{90+xs.min()}..{90+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(ys)}")

# matrix cells: per-cell ink+pill map — split band at row gap
print("-- matrix cell rows: ink row profile x300..460 y352..432")
ink = (im.sum(axis=2) < 600)
prof = ink[350:435, 300:460].sum(axis=1)
print([(350 + i, int(v)) for i, v in enumerate(prof)])
