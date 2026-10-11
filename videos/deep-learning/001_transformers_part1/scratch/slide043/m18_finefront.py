#!/usr/bin/env python3
"""Fine color map of front-card left internals."""
import numpy as np
from PIL import Image
import sys
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
PAL = {
 'S': (241,139,150),  # salmon card
 'W': (255,255,255), 'G': (233,233,231),
 'e': (133,197,145),  # dashed green border
 'p': (247,183,199),  # pale pink cell
 'P': (255,105,180),  # hot pink
 'B': (51,102,204),   # royal blue
 'T': (222,184,135),  # tan
 'V': (238,130,238),  # violet
 'K': (40,40,40), 'R': (204,0,0), 'D': (139,0,0),
 'C': (250,220,175),  # chip pale fill
 'F': (248,184,216),
 'U': (0,51,204),
}
keys=list(PAL.keys()); cols=np.array([PAL[k] for k in keys])
def band(y0,y1,x0,x1,cell=2):
    print(f"== y{y0}..{y1} x{x0}..{x1} cell={cell} ==")
    h1="     "; h2="     "
    for gx in range((x1-x0)//cell):
        c=x0+gx*cell; h1+=str(c//100%10); h2+=str(c//10%10)
    print(h1); print(h2)
    for gy in range(y0,y1,cell):
        row=""
        for gx in range((x1-x0)//cell):
            blk = im[gy:gy+cell, x0+gx*cell:x0+gx*cell+cell].reshape(-1,3)
            med = np.median(blk,axis=0)
            d = np.abs(cols-med).sum(axis=1)
            i=int(d.argmin())
            row += keys[i] if d[i]<105 else '?'
        print(f"{gy:4d} {row}")
which=sys.argv[1]
if which=='chips': band(318,445,100,250,2)
elif which=='blue': band(318,445,240,360,2)
elif which=='mid': band(318,530,350,640,2)
