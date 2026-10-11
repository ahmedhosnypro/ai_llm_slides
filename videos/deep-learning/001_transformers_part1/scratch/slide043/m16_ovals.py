#!/usr/bin/env python3
"""White ovals + h1 tag + output vectors in staircase band."""
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
lum = (r+g+b)/3.0
white = lum > 235
sub = white[183:300, 45:915]
lab, n = ndimage.label(sub)
res=[]
for i in range(1, n+1):
    ys, xs = np.where(lab==i)
    if len(ys) < 40: continue
    x0,x1,y0,y1 = 45+xs.min(), 45+xs.max(), 183+ys.min(), 183+ys.max()
    w=x1-x0; h=y1-y0
    if w>8 and h>5 and w<120 and h<40:
        res.append((y0,x0,x1,y1,len(ys)))
print("== white ovals/boxes y183-300 ==")
for t in sorted(res):
    print(f"  y {t[0]}..{t[3]}  x {t[1]}..{t[2]}  n={t[4]}")
# h1 tag: dark comps y 274..300
dark = lum < 75
sub2 = dark[270:305, 500:680]
lab2, n2 = ndimage.label(sub2)
print("== dark comps y270-305 x500-680 (h1 tag) ==")
for i in range(1, n2+1):
    ys, xs = np.where(lab2==i)
    if len(ys) < 60: continue
    print(f"  x {500+xs.min()}..{500+xs.max()}  y {270+ys.min()}..{270+ys.max()}  n={len(ys)}")
# output vectors: dark segmented boxes near top edges of cards (between ovals)
# scan for dark rows in y 190..275 per card region
darkm = lum < 90
print("== dark runs per row y188-278 x230-700 (vectors) ==")
for y in range(188, 278, 2):
    xs = np.where(darkm[y, 200:620])[0]
    if len(xs) > 15:
        runs=[]; s=xs[0]; p=xs[0]
        for x in xs[1:]:
            if x==p+1: p=x
            else:
                if p-s>=6: runs.append((200+s,200+p))
                s=p=x
        if p-s>=6: runs.append((200+s,200+p))
        if runs: print(f"  y={y}: {runs}")
