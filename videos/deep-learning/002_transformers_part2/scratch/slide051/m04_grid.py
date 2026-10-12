#!/usr/bin/env python3
"""m04_grid.py — dominant-color grid dump of the slide_051 frame body so the layout
is readable as text. 48x27 grid over frame px x 56..906, y 42..518.
"""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

# named palette for classification
PAL = {
    ".": (233, 233, 231),  # gray panel
    "W": (255, 255, 255),  # white
    "T": (192, 0, 0),      # title red C00000
    "R": (255, 0, 0),      # pure red accents
    "P": (251, 229, 214),  # peach FBE5D6
    "O": (237, 125, 49),   # orange ED7D31
    "G": (0, 225, 0),      # bright green 00E100
    "L": (204, 255, 204),  # light green CCFFCC
    "B": (68, 114, 196),   # blue 4472C4
    "E": (127, 127, 127),  # gray 7F7F7F
    "K": (255, 199, 206),  # pink FFC7CE
    "M": (201, 160, 220),  # purple C9A0DC
    "C": (102, 204, 204),  # teal 66CCCC
    "Y": (255, 255, 0),    # yellow
    "N": (160, 98, 45),    # brown A0622D
    "D": (0, 0, 0),        # black
    "w": (242, 242, 242),  # near-white container fill
}
names = list(PAL.keys())
cols = np.array([PAL[k] for k in names])

x0, x1, y0, y1 = 56, 906, 42, 518
GX, GY = 85, 48
cw = (x1 - x0) / GX
ch = (y1 - y0) / GY

body = im[y0:y1, x0:x1]
hh, ww, _ = body.shape
out = []
for gy in range(GY):
    row = ""
    for gx in range(GX):
        cell = body[int(gy * ch):int((gy + 1) * ch), int(gx * cw):int((gx + 1) * cw)]
        px = cell.reshape(-1, 3)
        med = np.median(px, axis=0)
        d = np.abs(cols - med).sum(axis=1)
        row += names[int(np.argmin(d))]
    out.append(row)
print("cols: frame x %d..%d, %.2f px/col; rows: frame y %d..%d, %.2f px/row" % (x0, x1, cw, y0, y1, ch))
for i, row in enumerate(out):
    fy = y0 + i * ch
    print("%3d %5.0f %s" % (i, fy, row))
