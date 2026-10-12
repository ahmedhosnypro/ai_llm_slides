#!/usr/bin/env python3
"""measure3 — fine delta campaign on slide_029 vs slide_028:
(a) pale-arc stroke census by angle, (b) new heads, (c) new '+w' labels,
(d) chips 9/10/11 fine centers, (e) callout box precise geometry,
(f) title-1 band, (g) label-k7 coverage check. Frame px; slide via fx=18.63+0.96123*sx, fy=0.95556*sy."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
CXf, CYf = 578.0, 284.0
def toslide(cx, cy): return [round((cx-18.63)/0.96123,2), round(cy/0.95556,2)]

A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)

def palemask(img):
    return (np.abs(img[:,:,0]-240)<=30)&(np.abs(img[:,:,1]-201)<=45)&(np.abs(img[:,:,2]-176)<=50)
def orangemask(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    return (r>170)&((r-g)>60)&(g>55)&(g<150)&(b<80)
def redmask(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    return (r>135)&((r-g)>50)&(g<100)&(b<120)

# ---- (a) NEW arc strokes: pale on 29 not on 28 (dilated), by angle bin
pA, pB = palemask(A), palemask(B)
newpale = pB & ~ndi.binary_dilation(pA, iterations=3)
Y, X = np.mgrid[0:540,0:960]
dx, dy = X-CXf, CYf-Y
rr = np.hypot(dx,dy); ang = np.degrees(np.arctan2(dy,dx))%360
sel = newpale & (rr>195) & (rr<245)
hist = {}
for th in range(0,360,5):
    m = sel & (ang>=th)&(ang<th+5)
    c = int(m.sum())
    if c>8: hist[th]=c
print("NEW_ARC_ANGLE_BINS(5deg):", json.dumps(hist))
ys,xs = np.nonzero(sel)
if len(xs): print("NEW_PALE_bbox",[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],"n",int(len(xs)))

# ---- (b) NEW heads (orange on 29 not on 28)
oA, oB = orangemask(A), orangemask(B)
newo = oB & ~ndi.binary_dilation(oA, iterations=3)
lab,n = ndi.label(ndi.binary_closing(newo, np.ones((2,2))))
heads=[]
for i in range(1,n+1):
    yy,xx = np.nonzero(lab==i)
    if len(xx)<20: continue
    cx,cy=(xx.min()+xx.max())/2,(yy.min()+yy.max())/2
    heads.append({"frame":[round(cx,1),round(cy,1)],"slide":toslide(cx,cy),
                  "bbox":[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],"n":int(len(xx))})
heads.sort(key=lambda h:(h["frame"][1],h["frame"][0]))
print("NEW_HEADS:", json.dumps(heads))
# also ALL heads on 29 (for arc-11 check on the right)
lab,n = ndi.label(ndi.binary_closing(oB, np.ones((2,2))))
allh=[]
for i in range(1,n+1):
    yy,xx = np.nonzero(lab==i)
    if len(xx)<18: continue
    cx,cy=(xx.min()+xx.max())/2,(yy.min()+yy.max())/2
    allh.append({"frame":[round(cx,1),round(cy,1)],"slide":toslide(cx,cy),"n":int(len(xx))})
allh.sort(key=lambda h:(h["frame"][1],h["frame"][0]))
print("ALL_HEADS29:", json.dumps(allh))

# ---- (c) NEW labels (red on 29 not on 28), excluding callout zone x<395,y>385
rA, rB = redmask(A), redmask(B)
newr = rB & ~ndi.binary_dilation(rA, iterations=3)
newr[385:,:400]=False; newr[:150,:360]=False; newr[510:,:]=False
lab,n = ndi.label(ndi.binary_closing(newr, np.ones((2,2))))
lbls=[]
for i in range(1,n+1):
    yy,xx = np.nonzero(lab==i)
    if len(xx)<30: continue
    cx,cy=(xx.min()+xx.max())/2,(yy.min()+yy.max())/2
    lbls.append({"frame":[round(cx,1),round(cy,1)],"slide":toslide(cx,cy),
                 "bbox":[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],"n":int(len(xx))})
lbls.sort(key=lambda l:(l["frame"][1],l["frame"][0]))
print("NEW_LABELS:", json.dumps(lbls))
# existing labels on 29 for k=0..7 (sanity: unchanged vs 28 measured)
print("LABELS28_ref_slidept: k4(407.6,122.8) k5(328.1,230.0) k6(329.1,356.5) k7(372.7,489.2)")

# ---- (d) chips 9/10/11 fine: window around polar prediction, union fill+border+text
def chip_fine(img, cxf, cyf, tag):
    x0,x1 = int(cxf-45), int(cxf+45); y0,y1 = int(cyf-50), int(cyf+50)
    reg = img[y0:y1, x0:x1]
    r,g,b = reg[:,:,0],reg[:,:,1],reg[:,:,2]
    fill = (np.abs(r-204)<=30)&(np.abs(g-255)<=25)&(np.abs(b-204)<=30)
    grn  = ((g-r)>40)&(g>110)&(b<120)  # border 009933 + text 009900
    u = ndi.binary_closing(fill|grn, np.ones((3,3)))
    lab,n = ndi.label(u)
    best=None;bestn=0
    for i in range(1,n+1):
        yy,xx = np.nonzero(lab==i)
        if len(xx)>bestn: bestn,best=len(xx),(int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max()))
    if not best: print("CHIP",tag,"NONE"); return
    bx0,by0,bx1,by1 = best
    fcx,fcy = x0+(bx0+bx1)/2, y0+(by0+by1)/2
    print("CHIP",tag,"bbox_frame",[x0+bx0,y0+by0,x0+bx1,y0+by1],"center_frame",[round(fcx,1),round(fcy,1)],
          "center_slide",toslide(fcx,fcy),"wh",[bx1-bx0+1,by1-by0+1],"n",bestn)

import math
def polarf(deg, r):  # slide pt polar -> frame px
    sx = 581.0 + r*math.cos(math.radians(deg)); sy = 297.2 - r*math.sin(math.radians(deg))
    return (18.63+0.96123*sx, 0.95556*sy)
for k,deg in ((9,270),(10,300),(11,330)):
    fx,fy = polarf(deg,182.5)
    chip_fine(B, fx, fy, f"k={k} pred_frame=({fx:.1f},{fy:.1f})")
# also verify an INHERITED chip (k=8, 240deg) unchanged:
fx,fy = polarf(240,182.5); chip_fine(B, fx, fy, "k=8(inherited)"); chip_fine(A, fx, fy, "k=8(on28)")

# ---- (e) callout precise geometry on 29
r,g,b = B[:,:,0],B[:,:,1],B[:,:,2]
zone = np.zeros(B.shape[:2],bool); zone[375:519,40:410]=True
redb = (r>110)&((r-g)>35)&(g<120)&zone
rowc = redb.sum(axis=1); colc = redb.sum(axis=0)
hrows = [y for y in range(375,519) if rowc[y]>200]   # long horizontal border strokes
vcols = [x for x in range(40,410) if colc[x]>80]     # long vertical border strokes
print("CALLOUT h-border rows:", hrows, " v-border cols:", vcols)
white = (r>240)&(g>240)&(b>230)&zone
lab,n = ndi.label(white)
best=None;bestn=0
for i in range(1,n+1):
    yy,xx = np.nonzero(lab==i)
    if len(xx)>bestn: bestn,best=len(xx),(int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max()))
print("CALLOUT white-fill bbox:", best, "npx", bestn)
# text bands (blue/yellow/red) within white fill
inw = np.zeros(B.shape[:2],bool)
inw[best[1]+2:best[3]-1, best[0]+2:best[2]-1]=True
blue = ((b-r)>60)&(b>120)&inw
yel  = (r>200)&(g>190)&(b<130)&inw
redt = (r>135)&((r-g)>50)&(g<100)&inw
for nm,m in (("blue",blue),("yellow",yel),("red",redt)):
    yy,xx = np.nonzero(m)
    if len(xx)==0: print("CALLOUT",nm,"EMPTY"); continue
    rows=np.nonzero(m.sum(axis=1)>0)[0]; cols=np.nonzero(m.sum(axis=0)>0)[0]
    # group rows into lines
    lines=[]; s=p=rows[0]
    for v in rows[1:]:
        if v-p>3: lines.append([int(s),int(p)]); s=v
        p=v
    lines.append([int(s),int(p)])
    print("CALLOUT",nm,"rows",lines,"cols",[int(cols.min()),int(cols.max())],"npx",int(len(xx)))
# (g) is 28's label-k7 spot covered on 29?
fy7,fx7 = polarf(0,0), None
lx,ly = 18.63+0.96123*372.7, 0.95556*489.2
print("28_label_k7_frame",(round(lx,1),round(ly,1)),"29_pixel_there",B[int(round(ly)),int(round(lx))].tolist(),
      "28_pixel_there",A[int(round(ly)),int(round(lx))].tolist())

# ---- (f) title line-1 band on 29 vs 28
ti = (r>150)&(g<85)&(b<95); tiA = (A[:,:,0]>150)&(A[:,:,1]<85)&(A[:,:,2]<95)
for nm,m in (("29",ti),("28",tiA)):
    sub = m[50:95,55:340]
    yy,xx = np.nonzero(sub)
    print("TITLE1",nm,"frame bbox x",55+int(xx.min()),55+int(xx.max()),"y",50+int(yy.min()),50+int(yy.max()),
          "slide x",[round((55+int(xx.min())-18.63)/0.96123,1),round((55+int(xx.max())-18.63)/0.96123,1)],
          "slide y",[round((50+int(yy.min()))/0.95556,1),round((50+int(yy.max()))/0.95556,1)])
