#!/usr/bin/env python3
"""Find dark tags + output vectors + ovals in staircase band via components."""
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
lum = (r+g+b)/3.0
# very dark components in the band
dark = lum < 75
sub = dark[183:280, 40:960]
lab, n = ndimage.label(sub)
print("== dark comps y183-280 ==")
res=[]
for i in range(1, n+1):
    ys, xs = np.where(lab==i)
    if len(ys) < 60: continue
    x0,x1,y0,y1 = 40+xs.min(), 40+xs.max(), 183+ys.min(), 183+ys.max()
    # average color
    col = a[y0:y1+1, x0:x1+1][lab[y0-183:y1-183+1, x0-40:x1-40+1]==i].mean(axis=0)
    res.append((x0,x1,y0,y1,len(ys),'#%02X%02X%02X'%tuple(col.astype(int))))
for t in sorted(res, key=lambda t:t[2]):
    print(f"  x {t[0]}..{t[1]}  y {t[2]}..{t[3]}  n={t[4]}  col={t[5]}")
# white ovals (lum>240 blobs) in band
white = lum > 242
sub2 = white[183:280, 40:960]
lab2, n2 = ndimage.label(sub2)
print("== white comps y183-280 (ovals) ==")
res2=[]
for i in range(1, n2+1):
    ys, xs = np.where(lab2==i)
    if len(ys) < 150: continue
    x0,x1,y0,y1 = 40+xs.min(), 40+xs.max(), 183+ys.min(), 183+ys.max()
    res2.append((x0,x1,y0,y1,len(ys)))
for t in sorted(res2, key=lambda t:t[2]):
    print(f"  x {t[0]}..{t[1]}  y {t[2]}..{t[3]}  n={t[4]}")
