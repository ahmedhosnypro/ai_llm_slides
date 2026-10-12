from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

def peach(img,y0,y1,x0,x1):
    reg=img[y0:y1+1,x0:x1+1]
    mask=(reg[:,:,0]>225)&(reg[:,:,1]>200)&(reg[:,:,1]<235)&(reg[:,:,2]>170)&(reg[:,:,2]<215)
    ys,xs=np.where(mask)
    return (x0+xs.min(),y0+ys.min(),x0+xs.max(),y0+ys.max()) if len(ys) else None

print('peach ellipse bbox f16:',peach(f16,120,210,60,230))
print('peach ellipse bbox f09:',peach(f09,120,210,60,230))

# text ink bands inside ellipse (x90..200, y140..195)
def inkrows(img,y0,y1,x0,x1,th=100):
    reg=img[y0:y1+1,x0:x1+1]
    m=reg.max(axis=2)<th
    rows=m.sum(axis=1)
    bands=[];inr=False
    for i,c in enumerate(rows):
        if c>0 and not inr: s=i;inr=True
        if c==0 and inr: bands.append((y0+s,y0+i-1));inr=False
    if inr: bands.append((y0+s,y1))
    return bands
print('f16 ellipse text bands:',inkrows(f16,140,200,90,200))
print('f09 ellipse text bands:',inkrows(f09,140,200,90,200))
print('f16 ellipse text cols:',)
def inkcols(img,y0,y1,x0,x1,th=100):
    reg=img[y0:y1+1,x0:x1+1]
    m=reg.max(axis=2)<th
    cols=m.sum(axis=0)
    xs=np.where(cols>0)[0]
    return (x0+xs.min(),x0+xs.max()) if len(xs) else None
for b in inkrows(f16,140,200,90,200):
    print('  f16 band',b,'cols',inkcols(f16,b[0],b[1],85,210))
for b in inkrows(f09,140,200,90,200):
    print('  f09 band',b,'cols',inkcols(f09,b[0],b[1],85,210))

# curve1 region: red pixels below ellipse (x80..220, y190..215)
def red(img,y0,y1,x0,x1):
    reg=img[y0:y1+1,x0:x1+1]
    m=(reg[:,:,0]>150)&(reg[:,:,1]<90)&(reg[:,:,2]<90)
    ys,xs=np.where(m)
    return ((x0+xs.min(),y0+ys.min(),x0+xs.max(),y0+ys.max()), int(m.sum())) if len(ys) else (None,0)
print('f16 red ink y195..215 x70..230:',red(f16,195,215,70,230))
print('f09 red ink y195..215 x70..230:',red(f09,195,215,70,230))
