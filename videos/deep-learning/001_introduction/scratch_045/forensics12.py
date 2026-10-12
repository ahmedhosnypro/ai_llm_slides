#!/usr/bin/env python3
"""forensics12.py — ASCII ink maps of the equation regions (2px downsample).
Banked to qa/slide045/forensics12_out.txt"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (r + g + b) / 3
reddish = (r - g > 30) & (r - b > 20)
ink = (lum < 205) & (~reddish)
redm = (r - g > 30) & (r - b > 20) & (r > 100)

def ascii_map(x0, x1, y0, y1, label, ds=2):
    print(f"\n== {label} x{x0}..{x1} y{y0}..{y1} (ds={ds}; #=ink, R=red, .=bg) ==")
    hdr = "     " + "".join(str((x0 + c * ds) // 100 % 10) if (x0 + c * ds) % 20 < ds else " " for c in range((x1 - x0) // ds + 1))
    print(hdr)
    for yy in range(y0, y1, ds):
        row = ""
        for xx in range(x0, x1, ds):
            cell_ink = ink[yy:yy + ds, xx:xx + ds].sum()
            cell_red = redm[yy:yy + ds, xx:xx + ds].sum()
            if cell_red >= 2 and cell_red >= cell_ink: row += "R"
            elif cell_ink >= 2: row += "#"
            elif cell_ink >= 1: row += "+"
            else: row += "."
        print(f"y{yy:<4}{row}")

ascii_map(465, 700, 296, 375, "EQ(a)")
ascii_map(510, 660, 388, 418, "EQ(b)")
ascii_map(420, 695, 418, 497, "EQ(c)")
