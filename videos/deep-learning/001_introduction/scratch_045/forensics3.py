#!/usr/bin/env python3
"""Forensics pass 3: precise bands — borders of def/Remember boxes, starburst bbox,
black bar, and text line bands inside every region."""
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

nonwhite = (R < 235) | (G < 235) | (B < 235)
dark = (R < 150) & (G < 150) & (B < 170)

def rowprofile(y0, y1, x0, x1, mask=nonwhite, label=""):
    print(f"-- rows {label} y{y0}..{y1} x{x0}..{x1} (count of mask px per row) --")
    for y in range(y0, y1):
        n = int(mask[y, x0:x1].sum())
        if n > 0:
            xs = np.where(mask[y, x0:x1])[0]
            print(f"  y={y} n={n} x{x0+xs[0]}..{x0+xs[-1]}")

def colprofile(x0, x1, y0, y1, mask=nonwhite, label=""):
    print(f"-- cols {label} x{x0}..{x1} y{y0}..{y1} --")
    for x in range(x0, x1):
        n = int(mask[y0:y1, x].sum())
        if n > 0:
            ys = np.where(mask[y0:y1, x])[0]
            print(f"  x={x} n={n} y{y0+ys[0]}..{y0+ys[-1]}")

# def box: top/bottom border rows around y114 and y~207; left/right borders
rowprofile(110, 122, 80, 860, nonwhite, "defbox-top")
rowprofile(200, 215, 80, 860, nonwhite, "defbox-bottom")
colprofile(66, 78, 110, 215, nonwhite, "defbox-left")
colprofile(884, 896, 110, 215, nonwhite, "defbox-right")

# Remember box: find rows with long pinkish runs y225..285
pink = (R - G > 12) & (R - B > 12) & (R > 170) & (R < 252)
rowprofile(225, 285, 80, 900, pink, "remember-pink-borders")

# black bottom bar
black = (R < 60) & (G < 60) & (B < 60)
rowprofile(505, 540, 30, 940, black, "blackbar")
colprofile(30, 70, 505, 540, black, "blackbar-left")
colprofile(890, 940, 505, 540, black, "blackbar-right")

# starburst: yellow region top right
yellow = (R > 200) & (G > 190) & (B < 170) & (R - B > 60)
ys, xs = np.where(yellow)
if len(ys):
    print(f"\nSTARBURST yellow bbox: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
# red of starburst outline (top right region only)
redtr = (R - G > 55) & (R - B > 55) & (R > 120)
sub = redtr[30:130, 760:940]
ys2, xs2 = np.where(sub)
if len(ys2):
    print(f"STARBURST red-outline bbox (in region x760..940,y30..130): x{760+xs2.min()}..{760+xs2.max()} y{30+ys2.min()}..{30+ys2.max()} n={len(ys2)}")
