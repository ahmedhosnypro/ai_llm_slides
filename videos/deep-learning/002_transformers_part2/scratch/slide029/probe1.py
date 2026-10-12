#!/usr/bin/env python3
import numpy as np
from PIL import Image
BASE="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
A=np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
B=np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
# slide->frame: fx=18.63+0.96123*sx, fy=0.95556*sy
def f(sx,sy): return (18.63+0.96123*sx, 0.95556*sy)
# label k=4 slide (407.6,122.8); head k=4 (385.7,185.1); chip k=6 (180deg) polar: cx=581-182.5=398.5? chipsMeasured...
def show(img,name,x,y,r=6):
    x,y=int(round(x)),int(round(y))
    reg=img[y-r:y+r+1, x-r:x+r+1].reshape(-1,3)
    # most saturated red pixel
    i=np.argmax(reg[:,0]-(reg[:,1]+reg[:,2])/2)
    print(f"{name} @({x},{y}) maxred={reg[i].tolist()} center={img[y,x].tolist()}")
sx,sy=f(407.6,122.8); show(A,"28 label k4 ink",sx,sy)
sx,sy=f(385.7,185.1); show(A,"28 head k4",sx,sy)
# left border col ~58, top row ~43
col=A[:,58]; i=np.argmax(col[:,0]-(col[:,1]+col[:,2])/2); print("28 col58 maxred px",col[i].tolist(),"row",i)
row=A[43]; i=np.argmax(row[:,0]-(row[:,1]+row[:,2])/2); print("28 row43 maxred px",row[i].tolist(),"col",i)
col=B[:,58]; i=np.argmax(col[:,0]-(col[:,1]+col[:,2])/2); print("29 col58 maxred px",col[i].tolist(),"row",i)
row=B[43]; i=np.argmax(row[:,0]-(row[:,1]+row[:,2])/2); print("29 row43 maxred px",row[i].tolist(),"col",i)
# count red-ish per column in border region for both frames
for name,img in (("28",A),("29",B)):
    red=(img[:,:,0]>140)&(img[:,:,1]<95)&(img[:,:,2]<95)
    cc=red.sum(axis=0); rc=red.sum(axis=1)
    bc=[x for x in range(960) if cc[x]>300]
    br=[y for y in range(540) if rc[y]>500]
    print(name,"cols>300:",bc[:6]+bc[-6:] if len(bc)>12 else bc," rows>500:",br[:6]+br[-6:] if len(br)>12 else br)
# sample '+w' label colors on 29: where? try near polar auto positions for k=8..10 later.
# For now sample known 28 label k=7 (372.7,489.2):
sx,sy=f(372.7,489.2); show(A,"28 label k7",sx,sy)
