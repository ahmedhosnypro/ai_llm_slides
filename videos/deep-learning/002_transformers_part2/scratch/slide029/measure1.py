#!/usr/bin/env python3
"""measure1 — slide_029 vs parent slide_028: chrome landmarks (mapping check),
frame-diff census, chips, arrowheads, '+w' labels, callout box, title bands.
Frame px 960x540; slide pt via fx = 18.63 + 0.96123*sx ; fy = 0.95556*sy."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
CXf, CYf = 578.0, 284.0  # frame-px circle center (from 027/028 campaigns)

def near(img, rgb, tol):
    return (np.abs(img[:,:,0].astype(int)-rgb[0])<=tol)&(np.abs(img[:,:,1].astype(int)-rgb[1])<=tol)&(np.abs(img[:,:,2].astype(int)-rgb[2])<=tol)

def chrome(img):
    H, W = img.shape[:2]
    red = (img[:,:,0].astype(int)>150)&(img[:,:,1].astype(int)<70)&(img[:,:,2].astype(int)<70)
    cc, rc = red.sum(axis=0), red.sum(axis=1)
    bcols = [x for x in range(W) if cc[x] > H*0.7]
    brows = [y for y in range(H) if rc[y] > W*0.7]
    dark = (img[:,:,0]<40)&(img[:,:,1]<40)&(img[:,:,2]<40)
    bar = [y for y in range(H) if dark[y].sum() > W*0.8]
    return {"border_cols": bcols[:4]+bcols[-4:] if len(bcols)>8 else bcols,
            "border_rows": brows[:4]+brows[-4:] if len(brows)>8 else brows,
            "black_bar_rows": [min(bar), max(bar)] if bar else None}

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
        out.append({"ang":round(ang,1),"frame":[round(cx,1),round(cy,1)],
                    "slide":[round((cx-18.63)/0.96123,2),round(cy/0.95556,2)],
                    "wh":[int(w),int(h)]})
    out.sort(key=lambda c:c["ang"])
    return out

def heads_of(img):
    ah = near(img,(224,96,16),40)
    lab,n = ndi.label(ah)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.nonzero(lab==i)
        if len(xs)<25: continue
        cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
        out.append({"frame":[round(cx,1),round(cy,1)],
                    "slide":[round((cx-18.63)/0.96123,2),round(cy/0.95556,2)],
                    "wh":[int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)],"n":int(len(xs))})
    out.sort(key=lambda c:(c["frame"][1],c["frame"][0]))
    return out

def labels_of(img, L=None, R=None, T=None):
    lbl = (img[:,:,0].astype(int)>170)&(img[:,:,1].astype(int)<60)&(img[:,:,2].astype(int)<60)
    lbl[:, :60]=False; lbl[:150,:360]=False
    if L is not None:
        lbl[:, max(0,L-3):L+4]=False; lbl[:, R-3:R+4]=False
    if T is not None: lbl[T-3:T+4,:]=False
    lab,n = ndi.label(lbl)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.nonzero(lab==i)
        if len(xs)<30: continue
        cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
        out.append({"frame":[round(cx,1),round(cy,1)],
                    "slide":[round((cx-18.63)/0.96123,2),round(cy/0.95556,2)],
                    "x0y0":[int(xs.min()),int(ys.min())],"x1y1":[int(xs.max()),int(ys.max())],"n":int(len(xs))})
    out.sort(key=lambda c:(c["frame"][1],c["frame"][0]))
    return out

A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB"))
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB"))

def bands(counts, thr, gap=8):
    idx = np.nonzero(counts>thr)[0]; res=[]
    if len(idx):
        s=p=idx[0]
        for v in idx[1:]:
            if v-p>gap: res.append([int(s),int(p)]); s=v
            p=v
        res.append([int(s),int(p)])
    return res

d = (np.abs(A.astype(int)-B.astype(int)).sum(axis=2)>90)
diff = {"npx":int(d.sum()),"col_bands":bands(d.sum(axis=0),6),"row_bands":bands(d.sum(axis=1),6)}

ch28, ch29 = chips_of(A), chips_of(B)
hd28, hd29 = heads_of(A), heads_of(B)
lb28, lb29 = labels_of(A), labels_of(B)
out = {"chrome28": chrome(A), "chrome29": chrome(B),
       "diff28v29": diff,
       "chips28": ch28, "chips29": ch29,
       "heads28": hd28, "heads29": hd29,
       "labels28": lb28, "labels29": lb29}
print(json.dumps(out, indent=1))
