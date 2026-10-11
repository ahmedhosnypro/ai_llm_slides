#!/usr/bin/env python3
"""Forensics pass 4: cluster red/dark-red/green/blue/dark-blue elements with bboxes."""
import numpy as np
from PIL import Image
from scipy import ndimage

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

def clusters(mask, name, min_area=12):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_area:
            continue
        out.append([int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)])
    out.sort(key=lambda r: (r[2] // 12, r[0]))
    print(f"== {name}: {len(out)} clusters")
    for x0, x1, y0, y1, area in out:
        w_, h_ = x1 - x0 + 1, y1 - y0 + 1
        shape = "line-h" if h_ <= 6 and w_ > 3 * h_ else ("line-v" if w_ <= 6 and h_ > 3 * w_ else ("text" if area < 400 and max(w_, h_) < 60 else "blob"))
        print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={w_} h={h_} area={area} {shape}")

# strong red (arrows CC0000 + block arrow)
red = (R > 150) & (G < 90) & (B < 90)
clusters(red, "RED strong", 14)

# dark red (labels 8B0000-ish)
dred = (R > 100) & (R < 190) & (G < 70) & (B < 70) & ~red
clusters(dred, "DARK-RED labels", 10)

# green border/text (00A651 / 008000)
green = (G > 110) & (R < 140) & (B < 140) & (G - R > 40) & (G - B > 20)
clusters(green, "GREEN", 10)

# blue text 0000CC
blue = (B > 120) & (R < 90) & (G < 90)
clusters(blue, "BLUE text", 10)

# dark blue 003366
dblue = (R < 80) & (G < 90) & (B > 80) & (B < 160) & (B - G > 30)
clusters(dblue, "DARK-BLUE", 8)

# magenta FF00FF
mag = (R > 170) & (B > 170) & (G < 110)
clusters(mag, "MAGENTA", 8)

# black text (title)
black = (R < 90) & (G < 90) & (B < 90)
clusters(black, "BLACK", 25)
