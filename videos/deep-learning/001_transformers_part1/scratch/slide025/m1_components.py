#!/usr/bin/env python3
"""Targeted component maps for slide_025.jpg (960x540). For each color mask,
find connected components and print bboxes (min area threshold)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

MASKS = {
    "tan_panel (D2A679)": (abs(r - 210) < 25) & (abs(g - 166) < 25) & (abs(b - 121) < 30),
    "green (00A651)": (abs(r - 0) < 90) & (abs(g - 150) < 60) & (abs(b - 80) < 60) & (g > r + 60) & (g > b + 30),
    "lavender (C3A6D8)": (abs(r - 195) < 35) & (abs(g - 166) < 35) & (abs(b - 216) < 35) & (b > g),
    "peach (FBE5D6)": (abs(r - 251) < 12) & (abs(g - 229) < 15) & (abs(b - 214) < 15),
    "ltgreen (C5E0B4)": (abs(r - 197) < 25) & (abs(g - 224) < 20) & (abs(b - 180) < 25) & (g > r + 10),
    "yellow (FFFF00)": (r > 220) & (g > 220) & (b < 120),
    "darkred (9E1B1B)": (abs(r - 158) < 45) & (g < 70) & (b < 70) & (r > 110),
    "gray (A6A6A6)": (abs(r - 166) < 20) & (abs(g - 166) < 20) & (abs(b - 166) < 20),
    "tanbox (C69C6D)": (abs(r - 198) < 25) & (abs(g - 156) < 25) & (abs(b - 109) < 25),
    "maroon (9E4A4A)": (abs(r - 158) < 30) & (abs(g - 74) < 30) & (abs(b - 74) < 30) & (g > b - 10),
    "blue (1F4E9C)": (r < 90) & (g < 110) & (b > 110) & (b > r + 40),
    "purple (7030A0)": (r > 80) & (r < 160) & (g < 80) & (b > 120) & (b < 200),
    "red (C00000)": (r > 150) & (g < 80) & (b < 80),
}

for name, mask in MASKS.items():
    lab, n = ndimage.label(mask)
    print(f"== {name} ==")
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 25:
            continue
        comps.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
    comps.sort(reverse=True)
    for area, x0, x1, y0, y1 in comps[:18]:
        print(f"  bbox x{x0}-{x1} y{y0}-{y1} (w{x1-x0+1} h{y1-y0+1}) area={area}")
