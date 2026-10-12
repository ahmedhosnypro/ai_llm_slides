#!/usr/bin/env python3
"""measure2 — ground-truth delta census: connected components of the 28-vs-29 diff
mask (every delta element's frame bbox), + calibrated chips/heads/labels masks
(int-cast), + callout-box geometry on 29, + arc-11 presence check.
slide pt via fx = 18.63 + 0.96123*sx ; fy = 0.95556*sy (028 chrome-identical)."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
CXf, CYf = 578.0, 284.0

def toslide(cx, cy):
    return [round((cx-18.63)/0.96123, 2), round(cy/0.95556, 2)]

A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)

# ---- 1. diff blob decomposition -------------------------------------------
d = (np.abs(A-B).sum(axis=2) > 90)
d = ndi.binary_closing(d, structure=np.ones((3,3)))
lab, n = ndi.label(d)
blobs = []
for i in range(1, n+1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 25: continue
    blobs.append({"bbox":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
                  "n":int(len(xs)),
                  "c28": [int(v) for v in A[ys,xs].mean(axis=0)],
                  "c29": [int(v) for v in B[ys,xs].mean(axis=0)]})
blobs.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))
print("DIFFBLOBS", json.dumps(blobs))

# ---- 2. chips (greenish-union, int) ----------------------------------------
def chips_of(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    green = ((g-r)>22)&((g-b)>18)&(g>110)
    green = ndi.binary_closing(green, structure=np.ones((7,7)))
    lab,n = ndi.label(green)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.nonzero(lab==i)
        if len(xs)<600: continue
        w,h = xs.max()-xs.min()+1, ys.max()-ys.min()+1
        if not (40<=w<=95 and 15<=h<=62): continue
        cx,cy = (xs.min()+xs.max())/2,(ys.min()+ys.max())/2
        ang = float(np.degrees(np.arctan2(CYf-cy, cx-CXf))%360)
        out.append({"ang":round(ang,1),"frame":[round(cx,1),round(cy,1)],"slide":toslide(cx,cy),"wh":[int(w),int(h)]})
    out.sort(key=lambda c:c["ang"])
    return out
print("CHIPS28", json.dumps(chips_of(A)))
print("CHIPS29", json.dumps(chips_of(B)))

# ---- 3. arrowheads (orange, int) -------------------------------------------
def heads_of(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    ah = (np.abs(r-224)<=45)&(np.abs(g-96)<=45)&(np.abs(b-16)<=45)
    ah = ndi.binary_closing(ah, structure=np.ones((2,2)))
    lab,n = ndi.label(ah)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.nonzero(lab==i)
        if len(xs)<25: continue
        cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
        out.append({"frame":[round(cx,1),round(cy,1)],"slide":toslide(cx,cy),
                    "wh":[int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)],"n":int(len(xs))})
    out.sort(key=lambda c:(c["frame"][1],c["frame"][0]))
    return out
print("HEADS28", json.dumps(heads_of(A)))
print("HEADS29", json.dumps(heads_of(B)))

# ---- 4. '+w' labels (red ink, calibrated to JPEG: r-g>55, r>130, g<95, b<115)
def labels_of(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    lbl = (r>130)&((r-g)>55)&(g<95)&(b<115)
    lbl[:, :60]=False; lbl[:150,:360]=False; lbl[350:,:380]=False  # title + callout zones
    lab,n = ndi.label(lbl)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.nonzero(lab==i)
        if len(xs)<30: continue
        cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
        out.append({"frame":[round(cx,1),round(cy,1)],"slide":toslide(cx,cy),
                    "x0y0":[int(xs.min()),int(ys.min())],"x1y1":[int(xs.max()),int(ys.max())],"n":int(len(xs))})
    out.sort(key=lambda c:(c["frame"][1],c["frame"][0]))
    return out
print("LABELS28", json.dumps(labels_of(A)))
print("LABELS29", json.dumps(labels_of(B)))

# ---- 5. callout box on 29 (bottom-left): red border + white fill + text bands
r,g,b = B[:,:,0],B[:,:,1],B[:,:,2]
reg = np.zeros(B.shape[:2], bool); reg[340:519, 40:400] = True
redb = (r>110)&((r-g)>40)&(g<110)&reg
ys,xs = np.nonzero(redb)
print("CALLOUT_border_bbox", [int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())])
white = (r>235)&(g>235)&(b>225)&reg
lab,n = ndi.label(white)
best=None;bestn=0
for i in range(1,n+1):
    yy,xx = np.nonzero(lab==i)
    if len(xx)>bestn: bestn,best=len(xx),(int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max()))
print("CALLOUT_white_bbox", best, "npx", bestn)
# text bands inside the callout: non-white, non-red-border rows/cols
inner = np.zeros(B.shape[:2], bool); inner[345:515, 55:395]=True
inner &= ~((np.abs(r-255)<12)&(np.abs(g-255)<12)&(np.abs(b-255)<12))
blue = ((b-r)>60)&(b>120)&inner
yel  = (r>200)&(g>190)&(b<120)&inner
redt = (r>130)&((r-g)>55)&(g<95)&inner
for nm,m in (("blue",blue),("yellow",yel),("red",redt)):
    yy,xx = np.nonzero(m)
    if len(xx)==0: print("CALLOUT",nm,"EMPTY"); continue
    rows=np.nonzero(m.sum(axis=1)>1)[0]; cols=np.nonzero(m.sum(axis=0)>1)[0]
    print("CALLOUT",nm,"rows",int(rows.min()),int(rows.max()),"cols",int(cols.min()),int(cols.max()),"npx",int(len(xx)))

# ---- 6. arc-11 presence (pale salmon F0C9B0 between Word 11 (330deg) and Word 0)
# sector: radius ~215 frame px, angles -18..-1.5 deg (right side, slightly below horizontal)
pale = (np.abs(B[:,:,0]-240)<=25)&(np.abs(B[:,:,1]-201)<=35)&(np.abs(B[:,:,2]-176)<=40)
sect = np.zeros(B.shape[:2],bool)
for yy in range(250,340):
    for xx in range(760,880):
        pass
# vectorized: points at r in [205..225] frame px, angle in [-20..0] deg (screen: y down)
Y,X = np.mgrid[0:540,0:960]
dx, dy = X-CXf, CYf-Y   # math coords (y up)
rr = np.hypot(dx,dy)
ang = np.degrees(np.arctan2(dy,dx))
sect = (rr>200)&(rr<232)&(ang>-20)&(ang<2)
print("ARC11_region_29_pale_px", int((pale&sect).sum()), "ARC11_region_28_pale_px", int(((np.abs(A[:,:,0]-240)<=25)&(np.abs(A[:,:,1]-201)<=35)&(np.abs(A[:,:,2]-176)<=40)&sect).sum()))
# where exactly?
ys,xs = np.nonzero(pale&sect)
if len(xs): print("ARC11_29_bbox",[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],"n",int(len(xs)))

# ---- 7. title line-1 band + badge band (for confirmation only)
print("TITLE29_rows", [int(v) for v in np.nonzero((((r>150)&(g<85)&(b<95))[:150,60:360]).sum(axis=1)>2)[0][:5]])
