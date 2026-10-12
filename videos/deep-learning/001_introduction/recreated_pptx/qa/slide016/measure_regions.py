from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

def modal(img,y0,y1,x0,x1,q=8):
    reg=img[y0:y1+1,x0:x1+1]
    cnt=Counter(map(tuple,(reg//q*q).reshape(-1,3)))
    return cnt.most_common(3)

def bbox_ink(img,y0,y1,x0,x1,thresh=120):
    # dark-ish ink bbox
    reg=img[y0:y1+1,x0:x1+1]
    mask=reg.max(axis=2)<thresh
    ys,xs=np.where(mask)
    if len(ys)==0: return None
    return (x0+xs.min(),y0+ys.min(),x0+xs.max(),y0+ys.max())

print('== rows 129..196 (parent Training Data ellipse region) ==')
for name,img in (('f16',f16),('f09',f09)):
    print(name,'modal 130..195 x85..205:',modal(img,130,195,85,205))
print()
print('== chain band rows 205..265: sample fills at box centers (y=236) ==')
# parent box centers x: pre 198, extr 350, sel 500, class 655, post 805
for name,img in (('f16',f16),('f09',f09)):
    print(name,[ (x, tuple(img[236,x])) for x in (198,300,350,450,500,600,655,760,805,860)])
print()
print('== last chain box: cols scan row 236 for fill transitions (f16) ==')
row=f16[236]
prev=None
for x in range(700,930):
    c=tuple(row[x]//16*16)
    if c!=prev:
        print(x,c)
        prev=c
