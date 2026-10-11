#!/usr/bin/env python3
"""Coarse ASCII color map of slide_043.jpg: 10px cells -> palette letters."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]

PAL = {
 'W': (255,255,255),  # white
 'G': (233,233,231),  # gray panel
 'R': (192,0,0),      # frame red
 'D': (139,0,0),      # dark red
 'C': (204,0,0),      # bright red CC
 'S': (240,128,128),  # salmon
 'L': (200,200,240),  # lavender
 'Y': (252,252,176),  # pale yellow
 'N': (204,255,204),  # pale green
 'P': (255,228,196),  # peach
 'B': (51,102,204),   # royal blue
 'V': (238,130,238),  # violet
 'T': (222,184,135),  # tan
 'K': (0,0,0),        # black
 'M': (255,105,180),  # hot pink
 'F': (248,184,216),  # light pink
 'U': (0,51,204),     # deep blue (0033CC)
 'E': (0,170,0),      # green 00AA00
 'O': (255,165,0),    # orange FFA500
 'A': (64,64,64),     # dark gray 404040
 'g': (255,215,0),    # gold FFD700
}

keys = list(PAL.keys())
cols = np.array([PAL[k] for k in keys])

cell = 10
gh, gw = H//cell, W//cell
for gy in range(gh):
    row = []
    for gx in range(gw):
        block = im[gy*cell:(gy+1)*cell, gx*cell:(gx+1)*cell].reshape(-1,3)
        med = np.median(block, axis=0)
        d = np.abs(cols - med).sum(axis=1)
        i = int(d.argmin())
        row.append(keys[i] if d[i] < 90 else '?')
    print(f"{gy*cell:3d} " + ''.join(row))
print("cols: " + ''.join([str((i*10)//100%10) for i in range(gw)]))
print("      " + ''.join([str((i*10)%100//10) for i in range(gw)]))
