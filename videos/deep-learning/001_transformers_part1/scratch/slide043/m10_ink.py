#!/usr/bin/env python3
"""Strict dark-ink (lum<100) maps + colored-chip maps for front card."""
import numpy as np
from PIL import Image
import sys
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3.0

def inkmap(y0,y1,x0,x1,cell=2):
    print(f"== ink(lum<100) y{y0}..{y1} x{x0}..{x1} cell={cell} ==")
    h1="     "; h2="     "
    for gx in range((x1-x0)//cell):
        col=x0+gx*cell; h1+=str(col//100%10); h2+=str(col//10%10)
    print(h1); print(h2)
    for gy in range(y0,y1,cell):
        row=""
        for gx in range((x1-x0)//cell):
            blk = lum[gy:gy+cell, x0+gx*cell:x0+gx*cell+cell]
            m = blk.min()
            row += 'X' if m<70 else ('+' if m<100 else ('o' if m<135 else '.'))
        print(f"{gy:4d} {row}")

which = sys.argv[1]
if which=='left': inkmap(295,540,45,360,2)
elif which=='mid': inkmap(295,540,350,640,2)
elif which=='right': inkmap(250,540,630,960,2)
elif which=='legend': inkmap(410,540,690,960,2)
