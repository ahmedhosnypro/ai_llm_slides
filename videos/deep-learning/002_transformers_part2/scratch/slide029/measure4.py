#!/usr/bin/env python3
"""measure4 — 029 fine pass, 028-comparable methods:
heads k=8..10 (measure4 method), labels (measure5 wide-window) at the 4 rough spots
+ old-k7 check, chips 9/10/11 (fixed fill mask), callout border probes, title ink sweep."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
CXf, CYf = 578.0, 284.0
CXs, CYs = 581.0, 297.2
def to_slide(fx, fy): return ((fx-18.63)/0.96123, fy/0.95556)
def polar_f(deg, r_slide):
    xs_ = CXs + r_slide*np.cos(np.radians(deg)); ys_ = CYs - r_slide*np.sin(np.radians(deg))
    return (18.63+0.96123*xs_, 0.95556*ys_)

# ---- heads k=8,9,10: measure4 mask, window around polar((k+1)*30, 224.5) ----
print("== heads 029 (measure4 mask) ==")
for k in (8,9,10):
    fx, fy = polar_f((k+1)*30, 224.5)
    x0,x1,y0,y1 = int(fx)-22, int(fx)+23, int(fy)-22, int(fy)+23
    sub = B[y0:y1, x0:x1]
    sr,sg,sb = sub[:,:,0],sub[:,:,1],sub[:,:,2]
    m = (sr>160)&((sr-sg)>80)&((sg-sb)>40)
    n = int(m.sum())
    if n:
        ys,xs = np.where(m)
        cx,cy = x0+xs.mean(), y0+ys.mean()
        sxx,syy = to_slide(cx,cy)
        pred = (CXs+224.5*np.cos(np.radians((k+1)*30)), CYs-224.5*np.sin(np.radians((k+1)*30)))
        print(f" head{k}: n={n} centroid slide ({sxx:.1f},{syy:.1f}) d_polar=({sxx-pred[0]:+.1f},{syy-pred[1]:+.1f}) bbox_frame [{x0+xs.min()},{y0+ys.min()},{x0+xs.max()},{y0+ys.max()}]")
    else:
        print(f" head{k}: NO ink near frame ({fx:.0f},{fy:.0f})")
# head 11 check (polar 360)
fx, fy = polar_f(360, 224.5)
sub = B[int(fy)-22:int(fy)+23, int(fx)-22:int(fx)+23]
m = (sub[:,:,0]>160)&((sub[:,:,0]-sub[:,:,1])>80)&((sub[:,:,1]-sub[:,:,2])>40)
print(" head11 window n=", int(m.sum()))

# ---- labels: measure5 wide-window at 4 rough spots + old k7 spot ----
r,g,b = B[:,:,0],B[:,:,1],B[:,:,2]
rl = (r>150)&((r-g)>55)&(g<185)&((b-g)>-15)
rough = {"k7_MOVED? (411.9,479.3)": (411.9,479.3), "k8 (529.3,523.9)": (529.3,523.9),
         "k9 (641.1,526.3)": (641.1,526.3), "k10 (748.2,488.5)": (748.2,488.5),
         "OLD k7 spot (372.7,489.2)": (372.7,489.2)}
print("== labels 029 (measure5 wide window +-42x+-26 frame) ==")
for nm,(sx,sy) in rough.items():
    fx, fy = 18.63+0.96123*sx, 0.95556*sy
    x0,x1,y0,y1 = int(fx)-42, int(fx)+43, int(fy)-26, int(fy)+27
    sub = rl[y0:y1, x0:x1]
    ys,xs = np.where(sub)
    n = len(ys)
    if n:
        cx,cy = x0+xs.mean(), y0+ys.mean()
        sxx,syy = to_slide(cx,cy)
        print(f" {nm}: n={n} slide ({sxx:.1f},{syy:.1f}) wh [{xs.max()-xs.min()+1},{ys.max()-ys.min()+1}] bbox_frame [{x0+xs.min()},{y0+ys.min()},{x0+xs.max()},{y0+ys.max()}]")
    else:
        print(f" {nm}: NO red ink")

# ---- chips 9/10/11 fine (fixed fill mask: g-r>25) ----
print("== chips 029 fine ==")
def chip_fine(img, deg, tag):
    fx,fy = polar_f(deg,182.5)
    x0,x1,y0,y1 = int(fx)-42, int(fx)+43, int(fy)-46, int(fy)+47
    reg = img[y0:y1, x0:x1]
    rr_,gg_,bb_ = reg[:,:,0],reg[:,:,1],reg[:,:,2]
    fill = ((gg_-rr_)>25)&(gg_>180)&((gg_-bb_)>15)          # CCFFCC fill
    grn  = ((gg_-rr_)>40)&(gg_>110)&(bb_<120)               # border+text
    u = ndi.binary_closing(fill|grn, np.ones((3,3)))
    lab,n = ndi.label(u)
    best=None;bestn=0
    for i in range(1,n+1):
        yy,xx = np.nonzero(lab==i)
        if len(xx)>bestn: bestn,best=len(xx),(int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max()))
    if not best: print(" CHIP",tag,"NONE"); return
    bx0,by0,bx1,by1 = best
    fcx,fcy = x0+(bx0+bx1)/2, y0+(by0+by1)/2
    sxx,syy = to_slide(fcx,fcy)
    print(f" CHIP {tag}: bbox_frame [{x0+bx0},{y0+by0},{x0+bx1},{y0+by1}] center_frame ({fcx:.1f},{fcy:.1f}) center_slide ({sxx:.1f},{syy:.1f}) wh_frame [{bx1-bx0+1},{by1-by0+1}] n={bestn}")
for k,deg in ((9,270),(10,300),(11,330)):
    chip_fine(B, deg, f"k={k}")
chip_fine(B, 240, "k=8 (029)")
chip_fine(A, 240, "k=8 (028)")

# ---- callout border probes ----
print("== callout border probes (029) ==")
for row in (389,390,391,392,393,509,510,511):
    seg = B[row,100:300]
    m = (seg[:,0]>110)&((seg[:,0]-seg[:,1])>35)
    print(f" row {row}: redcount={int(m.sum())} sample={seg[100].tolist()}")
for col in (56,57,58,59,60,63,64,65,66,67,362,363,364,365,366):
    seg = B[400:505,col]
    m = (seg[:,0]>110)&((seg[:,0]-seg[:,1])>35)
    print(f" col {col}: redcount={int(m.sum())} sample@450={B[450,col].tolist()}")

# ---- title ink sweep ----
print("== title line1 ink (threshold sweep) ==")
for nm,img in (("28",A),("29",B)):
    for thr in ((150,85,95),(140,100,110),(160,70,80)):
        m = (img[:,:,0]>thr[0])&(img[:,:,1]<thr[1])&(img[:,:,2]<thr[2])
        sub = m[55:95,55:340]
        ys,xs = np.nonzero(sub)
        sxx0,sxx1 = to_slide(55+xs.min(),0)[0], to_slide(55+xs.max(),0)[0]
        print(f" {nm} thr{thr}: frame x [{55+xs.min()},{55+xs.max()}] slide x [{sxx0:.1f},{sxx1:.1f}] n={int(len(xs))}")

# ---- callout text line fine bboxes (looser masks, per line) ----
print("== callout text fine ==")
inw = np.zeros(B.shape[:2],bool); inw[394:509,67:362]=True
blue = ((b-r)>60)&(b>120)&inw
yel  = (r>200)&(g>190)&(b<130)&inw
redt = (r>135)&((r-g)>40)&(g<140)&(b<150)&inw
for nm,m,rows in (("blueL1",blue,(396,417)),("blueL2",blue,(417,436)),("redL3",redt,(448,472)),("yellow",yel,(394,418))):
    mm = m.copy(); mm[:rows[0]]=False; mm[rows[1]]=False
    ys,xs = np.nonzero(mm)
    if len(xs)==0: print(f" {nm}: EMPTY"); continue
    print(f" {nm}: frame x [{xs.min()},{xs.max()}] y [{ys.min()},{ys.max()}] slide x [{to_slide(xs.min(),0)[0]:.1f},{to_slide(xs.max(),0)[0]:.1f}] slide y [{ys.min()/0.95556:.1f},{ys.max()/0.95556:.1f}] n={int(len(xs))}")
# red omega in line 1 (cols 210-232)?
mm = redt.copy(); mm[:396]=False; mm[417:]=False; mm[:, :210]=False; mm[:, 233:]=False
ys,xs = np.nonzero(mm)
print(" redL1-omega:", f"frame x [{xs.min()},{xs.max()}] y [{ys.min()},{ys.max()}] n={int(len(xs))}" if len(xs) else "EMPTY")
