#!/usr/bin/env python3
"""Dark-ink text maps: X = dark pixel, . = light. Plus color runs."""
import numpy as np
from PIL import Image
import sys

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)

def darkmap(y0,y1,x0,x1,cell=2,thresh=140):
    print(f"== dark map y{y0}..{y1} x{x0}..{x1} cell={cell} ==")
    hdr1 = "     "; hdr2="     "
    for gx in range((x1-x0)//cell):
        col = x0+gx*cell
        hdr1 += str(col//100%10)
        hdr2 += str(col//10%10)
    print(hdr1); print(hdr2)
    for gy in range(y0,y1,cell):
        row=""
        for gx in range((x1-x0)//cell):
            block = im[gy:gy+cell, x0+gx*cell:x0+gx*cell+cell].reshape(-1,3)
            lum = block.mean()
            row += 'X' if lum<thresh else ('+' if lum<190 else '.')
        print(f"{gy:4d} {row}")

which = sys.argv[1]
if which=='title': darkmap(44,120,540,925,2)
elif which=='vec': darkmap(44,82,395,545,2)
elif which=='lt': darkmap(84,118,315,560,2)
elif which=='bar': darkmap(124,155,160,800,2, 170)
elif which=='mid': darkmap(185,275,420,600,2, 150)
