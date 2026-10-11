#!/usr/bin/env python3
"""Fine 4px-cell maps of key bands + exact card top edges."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]

PAL = {
 'W': (255,255,255), 'G': (233,233,231), 'R': (192,0,0), 'D': (139,0,0), 'C': (204,0,0),
 'S': (240,128,128), 'L': (200,200,240), 'Y': (252,252,176), 'N': (204,255,204), 'P': (255,228,196),
 'B': (51,102,204), 'V': (238,130,238), 'T': (222,184,135), 'K': (40,40,40), 'M': (255,105,180),
 'F': (248,184,216), 'U': (0,51,204), 'E': (0,170,0), 'O': (255,165,0), 'A': (64,64,64), 'g': (255,215,0),
}
keys = list(PAL.keys())
cols = np.array([PAL[k] for k in keys])

def band(y0, y1, x0, x1, cell=4):
    print(f"== band y{y0}..{y1} x{x0}..{x1} cell={cell} ==")
    hdr = "     "
    for gx in range((x1-x0)//cell):
        col = x0 + gx*cell
        hdr += str(col//100%10)
    print(hdr)
    for gy in range(y0, y1, cell):
        row = ""
        for gx in range((x1-x0)//cell):
            block = im[gy:gy+cell, x0+gx*cell:x0+gx*cell+cell].reshape(-1,3)
            med = np.median(block, axis=0)
            d = np.abs(cols - med).sum(axis=1)
            i = int(d.argmin())
            row += keys[i] if d[i] < 110 else '?'
        print(f"{gy:4d} {row}")

import sys
which = sys.argv[1] if len(sys.argv)>1 else 'top'
if which == 'top':
    band(180, 275, 40, 960, 4)
elif which == 'pipe':
    band(40, 175, 40, 960, 4)
elif which == 'front':
    band(275, 540, 40, 960, 5)
