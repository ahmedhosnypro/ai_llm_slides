#!/usr/bin/env python3
"""Calibrate font sizes against measured frame ink using real Arial (metric-identical to render)."""
from PIL import Image, ImageDraw, ImageFont

ARIAL_B = "/usr/share/fonts/TTF/Arialbd.TTF"

def ink(fontsize, text):
    f = ImageFont.truetype(ARIAL_B, fontsize)
    # generous canvas
    img = Image.new("L", (fontsize * len(text) * 2, fontsize * 4), 255)
    d = ImageDraw.Draw(img)
    d.text((50, 50), text, font=f, fill=0)
    a = __import__("numpy").asarray(img)
    ys, xs = np.where(a < 200)
    return xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, xs.min() - 50, ys.min() - 50

import numpy as np

targets = [
    ("title", "Encoder \u2013 Decoder Transformer", 539, 27),
    ("redcap", "Orientation is not the Issue", 256, 15),
    ("blue", "Let us focus on the  Building  blocks", 424, 23),
]
for tag, text, tw, th in targets:
    print(f"--- {tag}: target w={tw} h={th}")
    for size in range(16, 44, 1):
        w, h, _, _ = ink(size, text)
        if abs(w - tw) <= 14 or abs(h - th) <= 2:
            print(f"  size {size}pt: ink {w}x{h} (dw={w-tw:+d}, dh={h-th:+d})")
