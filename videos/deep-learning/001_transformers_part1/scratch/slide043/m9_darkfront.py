#!/usr/bin/env python3
"""Dark-ink text maps of front card internals (2px cells)."""
import numpy as np
from PIL import Image
import sys
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
def darkmap(y0,y1,x0,x1,cell=2,thresh=140):
    print(f"== dark y{y0}..{y1} x{x0}..{x1} cell={cell} ==")
    h1="     "; h2="     "
    for gx in range((x1-x0)//cell):
        col=x0+gx*cell; h1+=str(col//100%10); h2+=str(col//10%10)
    print(h1); print(h2)
    for gy in range(y0,y1,cell):
        row=""
        for gx in range((x1-x0)//cell):
            blk = im[gy:gy+cell, x0+gx*cell:x0+gx*cell+cell].reshape(-1,3)
            lum = blk.mean()
            row += 'X' if lum<thresh else ('+' if lum<200 else '.')
        print(f"{gy:4d} {row}")
which = sys.argv[1]
if which=='left': darkmap(300,420,45,350,2)
elif which=='leftlow': darkmap(420,540,45,350,2)
elif which=='mid': darkmap(300,420,350,630,2)
elif which=='midlow': darkmap(420,540,350,630,2)
elif which=='right': darkmap(250,540,620,960,2)
elif which=='legend': darkmap(415,540,690,960,2)
