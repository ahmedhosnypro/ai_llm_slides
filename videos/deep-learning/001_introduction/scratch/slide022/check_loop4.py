#!/usr/bin/env python3
"""Precise re-measure with border bands zeroed. Reports per-element union bboxes."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide022/render_1.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_022.jpg"
S = 2000/960.0

orig = np.asarray(Image.open(O).convert('RGB')).astype(int)
rend = np.asarray(Image.open(R).convert('RGB')).astype(int)

def mask_strict(a):
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return ((r<150)&(g<150)) | ((r>120)&(r-g>45)&(r-b>35)) | ((b>90)&(b-r>30)) | ((g>150)&(g-r>40)&(b>150)&(b-r>40))
def mask_light(a):
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return ((r<205)&(g<205)&(b<215)) | ((r>120)&(r-g>35)&(r-b>25)) | ((b>95)&(b-r>25)) | ((g>150)&(g-r>30)&(b>150)&(b-r>30))

omi = mask_light(orig)   # light mask catches washed strokes
rmi = mask_strict(rend)

def zero_rect_bands(mask, rects, pad=2.5):
    m = mask.copy()
    for (x0,y0,x1,y1) in rects:
        m[max(0,int((y0-pad)*S)):int((y1+pad)*S), max(0,int((x0-pad)*S)):int((x0+pad)*S)] = False
        m[max(0,int((y0-pad)*S)):int((y1+pad)*S), int((x1-pad)*S):int((x1+pad)*S)] = False
        m[max(0,int((y0-pad)*S)):int((y0+pad)*S), max(0,int((x0-pad)*S)):int((x1+pad)*S)] = False
        m[int((y1-pad)*S):int((y1+pad)*S), max(0,int((x0-pad)*S)):int((x1+pad)*S)] = False
    return m

BOXES = [(82.5,88.5,418.5,246.5),(528.5,88.5,792.5,245.5),(81.5,255.5,766.5,342.5),
         (228.5,350.5,612.5,508),(626.5,395.5,818.5,444.5)]
omi = zero_rect_bands(omi, BOXES)
rmi = zero_rect_bands(rmi, BOXES)
# zero the sigma oval ring in render (ellipse path 411,406,33,26) and orig ring
def zero_ellipse_ring(mask, cx,cy,rx,ry,pad=2.0):
    m = mask.copy()
    ys,xs = np.mgrid[0:mask.shape[0],0:mask.shape[1]]
    fx, fy = xs/S, ys/S
    d = np.sqrt(((fx-cx)/rx)**2 + ((fy-cy)/ry)**2)
    m[(d>0.75)&(d<1.5)] = False
    return m
rmi = zero_ellipse_ring(rmi, 427.5, 419, 16.5, 13)

def union(mask, x0,y0,x1,y1):
    sub = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys,xs = np.nonzero(sub)
    if len(xs)==0: return None
    return (x0+xs.min()/S, y0+ys.min()/S, x0+xs.max()/S, y0+ys.max()/S)

def rowprofile(mask, x0,y0,x1,y1):
    sub = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    rows = np.nonzero(sub.any(axis=1))[0]
    if len(rows)==0: return None
    # find gaps > 3px -> bands
    bands=[]; s=rows[0]; p=rows[0]
    for r in rows[1:]:
        if r-p>3: bands.append((y0+s/S, y0+p/S)); s=r
        p=r
    bands.append((y0+s/S, y0+p/S))
    return bands

CHECKS = [
 # name, window, mask
 ("title",      (200,50,760,93),   rmi),
 ("title-orig", (200,50,760,93),   omi),
 ("label1",     (292,155,415,180), rmi),
 ("label2",     (662,155,770,180), rmi),
 ("eq2 b",      (599,102,616,124), rmi),
 ("v2 one",     (255,103,269,123), rmi),
 ("eq2 W",      (556,155,577,177), rmi),
 ("case1 word", (610,264,672,286), rmi),
 ("case2 word", (610,286,678,308), rmi),
 ("case3 word", (610,308,748,330), rmi),
 ("OP",         (578,410,616,433), rmi),
 ("callout both",(640,404,808,445),rmi),
 ("callout-orig",(640,404,808,445),omi),
 ("sigma",      (414,407,436,433), rmi),
 ("sigma-orig", (414,407,436,433), omi),
 ("blackbar",   (30,512,930,541),  rmi),
 ("blackbar-org",(30,512,930,541), omi),
 ("in x1 zone", (242,350,270,372), rmi),
 ("eq1 X clean",(84,154,102,177),  rmi),
 ("eq1 =1 clean",(100,158,116,173),rmi),
 ("eq1 =2 clean",(231,158,250,173),rmi),
 ("eq3 =1 clean",(134,288,151,301),rmi),
 ("eq3 WT clean",(154,279,185,305),rmi),
 ("eq3 b1 clean",(424,283,460,305),rmi),
 ("eq3 d( clean",(85,283,106,305), rmi),
 ("v1 parenL c",(112,116,121,232), rmi),
 ("v2 parenL c",(245,101,253,239), rmi),
 ("wt w1 clean",(286,352,310,372), rmi),
 ("wt w2 clean",(286,372,310,390), rmi),
 ("eq2 = clean",(575,158,593,173), rmi),
 ("case1 >0 c", (551,264,578,286), rmi),
 ("case2 <0 c", (551,286,578,308), rmi),
 ("case3 =0 c", (551,308,578,330), rmi),
]
for name, (x0,y0,x1,y1), m in CHECKS:
    u = union(m, x0,y0,x1,y1)
    if u is None: print(f"{name:14s} NONE"); continue
    w = u[2]-u[0]; h = u[3]-u[1]
    print(f"{name:14s} bbox=({u[0]:6.1f},{u[1]:6.1f})-({u[2]:6.1f},{u[3]:6.1f})  w={w:5.1f} h={h:5.1f}")

print("\ncallout row bands (render):", rowprofile(rmi, 640,404,808,445))
print("callout row bands (orig):  ", rowprofile(omi, 640,404,808,445))
print("\ntitle row bands (render):", rowprofile(rmi, 200,50,760,93))
print("title row bands (orig):  ", rowprofile(omi, 200,50,760,93))
