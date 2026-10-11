#!/usr/bin/env python3
"""Coarse color ASCII maps of slide_045.jpg delta zones (960x540). Cell=3px."""
import numpy as np
from PIL import Image
import sys

IM = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_045.jpg').convert('RGB')).astype(int)

def cls(px):
    r,g,b = px
    lum = (r+g+b)/3
    if lum < 90: return 'K'                      # dark ink
    if r>200 and g>170 and b<120: return 'Y'     # yellow
    if r>150 and g<100 and b<100: return 'R'     # red
    if r>180 and 90<=g<160 and b<140: return 'o' # orange/brown
    if b>130 and b-r>40 and b-g>25: return 'B'   # blue
    if b<100 and g>110 and g-r>30: return 'g'    # green
    if r>200 and 130<g<200 and b>170: return 'P' # pink/lavender
    if r>170 and g<140 and b>170: return 'M'     # magenta/purple
    if lum>242: return 'W'                       # white
    if lum>218: return 'w'                       # light gray/panel
    if 160<lum<=218: return ':'                  # mid gray
    return '+'                                   # mid-dark

def amap(y0,y1,x0,x1,cell=3,title=''):
    print(f"== {title} y{y0}..{y1} x{x0}..{x1} cell={cell} ==")
    hdr1="     "; hdr2="     "
    for gx in range((x1-x0)//cell):
        col=x0+gx*cell
        hdr1 += str(col//100%10); hdr2 += str(col//10%10)
    print(hdr1); print(hdr2)
    for gy in range(y0,y1,cell):
        row=""
        for gx in range((x1-x0)//cell):
            block = IM[gy:gy+cell, x0+gx*cell:x0+gx*cell+cell].reshape(-1,3)
            med = np.median(block,axis=0)
            row += cls(med)
        print(f"{gy:4d} {row}")

which = sys.argv[1]
if which=='pipe':   amap(38,135,370,580,3,"PIPELINE ZONE (vecbox/label/arrow/ltbox)")
elif which=='bar':  amap(118,165,150,720,4,"BAR ZONE")
elif which=='eqbox':amap(100,185,700,945,3,"TOP-RIGHT EQ BOX")
elif which=='botright': amap(340,540,690,960,4,"BOTTOM-RIGHT")
elif which=='title': amap(44,112,480,940,4,"TITLE/SUBTITLE")
elif which=='wcols': amap(230,540,540,820,4,"W COLUMNS / ARROWS")
