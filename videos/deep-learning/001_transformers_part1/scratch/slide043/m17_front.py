#!/usr/bin/env python3
"""Front card internals via color components."""
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
lum=(r+g+b)/3

def comps(mask, name, min_n=50, y0=270, y1=540, x0=45, x1=930):
    lab, n = ndimage.label(mask[y0:y1, x0:x1])
    out=[]
    for i in range(1, n+1):
        ys, xs = np.where(lab==i)
        if len(ys) < min_n: continue
        bx0,bx1,by0,by1 = x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max()
        col = a[by0:by1+1, bx0:bx1+1][lab[by0-y0:by1-y0+1, bx0-x0:bx1-x0+1]==i].mean(axis=0)
        out.append((by0,bx0,bx1,by1,len(ys),'#%02X%02X%02X'%tuple(col.astype(int))))
    out.sort()
    print(f"== {name} ==")
    for t in out: print(f"  y {t[0]}..{t[3]}  x {t[1]}..{t[2]}  n={t[4]} col={t[5]}")
    return out

# royal blue chips (3366CC) — big enough blocks
blue = (abs(r-51)<45)&(abs(g-102)<45)&(abs(b-204)<45)
comps(blue, 'royal blue chips', 120)
# violet pills
vio = (abs(r-238)<35)&(abs(g-130)<45)&(abs(b-238)<35)
comps(vio, 'violet pills', 100)
# tan box
tan = (abs(r-222)<30)&(abs(g-184)<30)&(abs(b-135)<35)
comps(tan, 'tan box', 200)
# hot pink / magenta (X2 chip FF69B4)
mag = (abs(r-255)<30)&(abs(g-105)<50)&(abs(b-180)<50)
comps(mag, 'magenta FF69B4', 80)
# green 00AA00 arrows/thick
grn = (abs(r-0)<60)&(abs(g-170)<55)&(abs(b-0)<60)&(g-r>60)&(g-b>60)
comps(grn, 'green 00AA00', 60)
# dashed green chip borders: thin green strokes — catch lighter green too
grn2 = (g>120)&(g-r>40)&(g-b>40)&(r<200)
comps(grn2, 'greenish strokes', 40)
