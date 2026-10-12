#!/usr/bin/env python3
"""measure5 — calibration + cleanup:
(1) measure4 head mask on 028 k=0..7 vs certified centers (mask bias),
(2) labels wide-window on 028 k=4..7 vs labelsMeasuredDelta + on 029 k8/k9 with row cap,
(3) clean callout per-line bboxes (strict row windows),
(4) moved-k7 vs 028-k7 label ink bbox comparison."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
CXs, CYs = 581.0, 297.2
def to_slide(fx, fy): return ((fx-18.63)/0.96123, fy/0.95556)
def polar_f(deg, r_slide):
    return (18.63+0.96123*(CXs+r_slide*np.cos(np.radians(deg))), 0.95556*(CYs-r_slide*np.sin(np.radians(deg))))

CERT_HEADS = {0:(776.4,188.4),1:(692.6,100.5),2:(585.6,71.2),3:(473.3,101.5),
              4:(385.7,185.1),5:(357.0,292.0),6:(385.5,405.2),7:(470.3,493.2)}
print("== head mask calibration on 028 ==")
for k in range(8):
    fx,fy = polar_f((k+1)*30, 224.5)
    x0,x1,y0,y1 = int(fx)-22, int(fx)+23, int(fy)-22, int(fy)+23
    sub = A[y0:y1,x0:x1]
    m = (sub[:,:,0]>160)&((sub[:,:,0]-sub[:,:,1])>80)&((sub[:,:,1]-sub[:,:,2])>40)
    if m.sum():
        ys,xs = np.where(m)
        cx,cy = x0+xs.mean(), y0+ys.mean()
        s = to_slide(cx,cy); c = CERT_HEADS[k]
        print(f" head{k}: mask_centroid ({s[0]:.1f},{s[1]:.1f}) certified ({c[0]},{c[1]}) bias=({s[0]-c[0]:+.1f},{s[1]-c[1]:+.1f}) n={int(m.sum())}")
    else: print(f" head{k}: none")

# fuller mask for whole-head centroid (calibrate on 028 too)
print("== head FULL mask (r>165, r-g>50, g<170, b<110) calibration on 028 ==")
for k in range(8):
    fx,fy = polar_f((k+1)*30, 224.5)
    x0,x1,y0,y1 = int(fx)-20, int(fx)+21, int(fy)-20, int(fy)+21
    sub = A[y0:y1,x0:x1]
    m = (sub[:,:,0]>165)&((sub[:,:,0]-sub[:,:,1])>50)&(sub[:,:,1]<170)&(sub[:,:,2]<110)
    if m.sum():
        ys,xs = np.where(m)
        cx,cy = x0+xs.mean(), y0+ys.mean()
        s = to_slide(cx,cy); c = CERT_HEADS[k]
        print(f" head{k}: full_centroid ({s[0]:.1f},{s[1]:.1f}) bias=({s[0]-c[0]:+.1f},{s[1]-c[1]:+.1f}) wh [{xs.max()-xs.min()+1},{ys.max()-ys.min()+1}] n={int(m.sum())}")

CERT_LBL = {4:(407.6,122.8),5:(328.1,230.0),6:(329.1,356.5),7:(372.7,489.2)}
print("== label wide-window calibration on 028 (row cap 513) ==")
rl = (A[:,:,0]>150)&((A[:,:,0]-A[:,:,1])>55)&(A[:,:,1]<185)&((A[:,:,2]-A[:,:,1])>-15)
rl[513:,:]=False
for k in range(4,8):
    sx,sy = CERT_LBL[k]
    fx,fy = 18.63+0.96123*sx, 0.95556*sy
    x0,x1,y0,y1 = int(fx)-42, int(fx)+43, int(fy)-26, int(fy)+27
    sub = rl[y0:y1,x0:x1]
    ys,xs = np.where(sub)
    cx,cy = x0+xs.mean(), y0+ys.mean()
    s = to_slide(cx,cy)
    print(f" label{k}: centroid ({s[0]:.1f},{s[1]:.1f}) certified ({sx},{sy}) bias=({s[0]-sx:+.1f},{s[1]-sy:+.1f}) wh [{xs.max()-xs.min()+1},{ys.max()-ys.min()+1}] n={len(ys)}")

print("== 029 labels k8/k9 re-measure (row cap 513) + k7m/k10 ==")
r2,g2,b2 = B[:,:,0],B[:,:,1],B[:,:,2]
rl2 = (r2>150)&((r2-g2)>55)&(g2<185)&((b2-g2)>-15)
rl2[513:,:]=False; rl2[:150,:360]=False; rl2[350:,:400]=False
for nm,(sx,sy) in (("k7m",(414.2,479.6)),("k8",(529.3,523.9)),("k9",(641.1,526.3)),("k10",(749.4,489.2))):
    fx,fy = 18.63+0.96123*sx, 0.95556*sy
    x0,x1,y0,y1 = int(fx)-40, int(fx)+41, int(fy)-24, int(fy)+25
    sub = rl2[y0:y1,x0:x1]
    ys,xs = np.where(sub)
    if len(ys)==0: print(f" {nm}: NONE"); continue
    cx,cy = x0+xs.mean(), y0+ys.mean()
    s = to_slide(cx,cy)
    print(f" {nm}: centroid slide ({s[0]:.1f},{s[1]:.1f}) inkbbox_frame [{x0+xs.min()},{y0+ys.min()},{x0+xs.max()},{y0+ys.max()}] wh [{xs.max()-xs.min()+1},{ys.max()-ys.min()+1}] n={len(ys)}")

print("== callout clean per-line bboxes (029) ==")
inw = np.zeros(B.shape[:2],bool); inw[394:509,67:362]=True
blue = ((b2-r2)>60)&(b2>120)&inw
yel  = (r2>200)&(g2>190)&(b2<130)&inw
redt = (r2>135)&((r2-g2)>40)&(g2<140)&(b2<150)&inw
def band(m, ylo, yhi, nm):
    mm = np.zeros_like(m); mm[ylo:yhi] = m[ylo:yhi]
    ys,xs = np.nonzero(mm)
    if len(xs)==0: print(f" {nm}: EMPTY"); return
    print(f" {nm}: frame x [{xs.min()},{xs.max()}] y [{ys.min()},{ys.max()}] slide x [{to_slide(xs.min(),0)[0]:.1f},{to_slide(xs.max(),0)[0]:.1f}] slide y [{ys.min()/0.95556:.1f},{ys.max()/0.95556:.1f}] n={len(xs)}")
band(blue, 394, 417, "blueL1")
band(blue, 417, 440, "blueL2")
band(redt, 448, 475, "redL3")
band(yel, 394, 418, "yellow")
# words in L1 (blue cols histogram)
mm = np.zeros_like(blue); mm[394:417] = blue[394:417]
cols = mm.sum(axis=0); idx = np.nonzero(cols>0)[0]
gaps=[]; s=p=idx[0]
for v in idx[1:]:
    if v-p>4: gaps.append((int(s),int(p))); s=v
    p=v
gaps.append((int(s),int(p)))
print(" blueL1 word col-ranges:", gaps)
mm = np.zeros_like(blue); mm[417:440] = blue[417:440]
cols = mm.sum(axis=0); idx = np.nonzero(cols>0)[0]
gaps=[]; s=p=idx[0]
for v in idx[1:]:
    if v-p>4: gaps.append((int(s),int(p))); s=v
    p=v
gaps.append((int(s),int(p)))
print(" blueL2 word col-ranges:", gaps)
mm = np.zeros_like(redt); mm[448:475] = redt[448:475]
cols = mm.sum(axis=0); idx = np.nonzero(cols>0)[0]
gaps=[]; s=p=idx[0]
for v in idx[1:]:
    if v-p>4: gaps.append((int(s),int(p))); s=v
    p=v
gaps.append((int(s),int(p)))
print(" redL3 word col-ranges:", gaps)
