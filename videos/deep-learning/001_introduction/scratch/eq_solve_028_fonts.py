#!/usr/bin/env python3
"""Metric-solve font sizes for slide 028 against the real Arial TTFs (fixed bbox)."""
from PIL import ImageFont, Image, ImageDraw

AB = "/usr/share/fonts/TTF/Arialbd.TTF"
AI = "/usr/share/fonts/TTF/Ariali.TTF"

def ink(path, size, s):
    f = ImageFont.truetype(path, size)
    img = Image.new("L", (2400, 400), 0)
    d = ImageDraw.Draw(img)
    d.text((60, 120), s, font=f, fill=255)
    bb = img.getbbox()  # ink bbox of non-zero (text)
    return bb  # l,t,r,b

def solve(path, label, s, target_w, sizes, target_h=None):
    best = None
    rows = []
    for size in sizes:
        bb = ink(path, size, s)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        rows.append((size, w, h, bb[0] - 60, bb[1] - 120))
        d = abs(w - target_w)
        if best is None or d < best[0]:
            best = (d, size, w, h)
    print(f"-- {label} {s!r} target_w={target_w}")
    for (size, w, h, l, t) in rows:
        mark = " <-- best" if size == best[1] else ""
        print(f"   {size:5.2f}pt: ink w={w:4d} h={h:3d} lsb={l:3d} top={t:3d}{mark}")
    if target_h:
        for (size, w, h, l, t) in rows:
            if abs(h - target_h) <= 2:
                print(f"   height-match {size}pt: h={h} vs {target_h}")
    return best

T = [x * 0.5 for x in range(76, 130)]
solve(AB, "t1", "Introduction to", 360, T, target_h=39)
solve(AB, "t2", "Convolutional Neural Network", 736, T, target_h=39)
solve(AB, "t3", "(CNN)", 142, T, target_h=49)
A = [x * 0.5 for x in range(18, 40)]
solve(AI, "a2", "UVA Deep Learning Course   EFSTRATIOS GAVVES", 334, A, target_h=15)
solve(AI, "a1", "Some of Slides are picked from", 170, A, target_h=15)

# a1 width up to the cursor zone: measure only x<=235 in the ORIGINAL -> compare with TTF prefix widths
print("\n-- a1 prefix width check (original text visible up to cursor at x~241) --")
import numpy as np
from PIL import Image as PImage
im = PImage.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_028.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
am = (R >= 45) & (R <= 200) & (np.abs(R.astype(int) - G) < 25) & (np.abs(G - B) < 25)
sub = am[465:483, 62:238]  # stop before cursor dense zone (x 241)
cp = sub.sum(axis=0)
xs = np.where(cp > 0)[0]
print(f"   a1 visible x {xs.min()+62}..{xs.max()+62} (may be clipped at 237)")
for size in (11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0):
    bb = ink(AI, size, "Some of Slides are picked ")
    print(f"   Italic {size}pt 'Some of Slides are picked ' w={bb[2]-bb[0]}")
