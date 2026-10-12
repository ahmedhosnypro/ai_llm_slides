#!/usr/bin/env python3
"""m07_fine.py — fine grid dumps (4px cells) of both panels with ink markers.
Uppercase = cell median matches palette; lowercase = same class but cell contains
dark ink (min luminance < 90) — lets us see text/arrows inside light fills.
"""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

PAL = {
    ".": (233, 233, 231), ".": (233, 233, 231),
    "W": (255, 255, 255),
    "P": (252, 233, 217),
    "G": (17, 255, 116),
    "O": (243, 168, 92),
    "L": (207, 255, 226),
    "B": (68, 114, 196),
    "E": (127, 127, 127),
    "e": (242, 242, 242),
    "K": (252, 194, 203),
    "M": (210, 128, 196),
    "C": (102, 204, 204),
    "Y": (255, 255, 0),
    "N": (162, 110, 62),
    "R": (255, 0, 0),
    "T": (180, 20, 20),
    "v": (149, 159, 72),
    "b": (60, 170, 80),
    "D": (40, 40, 40),
}
names = list(PAL.keys())
cols = np.array([PAL[k] for k in names])

def dump(x0, x1, y0, y1, cell=4, tag=""):
    print(f"== {tag} frame x {x0}..{x1} y {y0}..{y1} cell={cell} ==")
    hdr = "     " + "".join(str((x0 + gx * cell) // 100 % 10) for gx in range((x1 - x0) // cell))
    hdr2 = "     " + "".join(str((x0 + gx * cell) // 10 % 10) for gx in range((x1 - x0) // cell))
    print(hdr); print(hdr2)
    for gy in range((y1 - y0) // cell):
        y = y0 + gy * cell
        row = ""
        for gx in range((x1 - x0) // cell):
            c = im[y:y + cell, x0 + gx * cell:x0 + gx * cell + cell].reshape(-1, 3)
            m = np.median(c, axis=0)
            lum = c.min(axis=1)
            d = np.abs(cols - m).sum(axis=1)
            k = int(np.argmin(d))
            ch = names[k]
            if ch.isupper() and lum.min() < 90 and ch not in "DN":
                ch = ch.lower()
            row += ch
        print("%4d %s" % (y, row))

import sys
which = sys.argv[1] if len(sys.argv) > 1 else "both"
if which in ("enc", "both"):
    dump(130, 466, 100, 505, 4, "ENCODER PANEL")
if which in ("dec", "both"):
    dump(566, 902, 100, 505, 4, "DECODER PANEL")
