#!/usr/bin/env python3
"""selfcheck attempt 1 (v2 — check windows fixed: border/label exclusion, triangle
bbox centers, chrome-by-design exclusion) — closed-loop PIL ink check of render_1.png
(150dpi) against frame-measured targets. TOL = 4 render px (~1.92 slide pt)."""
import sys, math
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

R = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide029/render_1.png").convert("RGB")).astype(int)
H, W = R.shape[:2]
print(f"render {W}x{H}")
fails = []
def check(nm, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + nm + (" " + detail if detail else ""))
    if not ok: fails.append(nm)

def fx2rx(fx): return (fx-18.63)/0.96123*150/72
def fy2ry(fy): return fy*2.18028

def bbox(mask):
    ys,xs = np.nonzero(mask)
    if len(xs)==0: return None
    return (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),int(len(xs)))

# ---- title line 1: window excludes panel border strokes (render x<=93 / >=1913)
red = (R[:,:,0]>150)&(R[:,:,1]<85)&(R[:,:,2]<95)
sub = np.zeros_like(red)
sub[int(fy2ry(59)):int(fy2ry(81))+1, 96:740] = red[int(fy2ry(59)):int(fy2ry(81))+1, 96:740]
b = bbox(sub)
tx0,tx1,ty0,ty1 = fx2rx(68),fx2rx(310),fy2ry(59),fy2ry(81)
ok = b and abs(b[0]-tx0)<=4 and abs(b[2]-tx1)<=4 and abs(b[1]-ty0)<=4 and abs(b[3]-ty1)<=4
check("title1 ink bbox", bool(ok), f"render {b} target ({tx0:.0f},{ty0:.0f},{tx1:.0f},{ty1:.0f})")

# ---- callout outer border cores
redb = (R[:,:,0]>110)&((R[:,:,0]-R[:,:,1])>60)&(R[:,:,2]<110)
zone = np.zeros_like(redb); zone[int(fy2ry(385)):int(fy2ry(514)), int(fx2rx(45)):int(fx2rx(405))] = True
redz = redb & zone
rowc = redz.sum(axis=1); colc = redz.sum(axis=0)
hrows = list(np.nonzero(rowc>200)[0]); vcols = list(np.nonzero(colc>80)[0])
tT, tB = fy2ry(391.5), fy2ry(510)
tL, tI, tR = fx2rx(58), fx2rx(65), fx2rx(364)
def closest(v, lst): return min(lst, key=lambda z: abs(z-v)) if lst else None
top = closest(tT,hrows); bot = closest(tB,hrows)
check("callout top border", top is not None and abs(top-tT)<=4, f"{top} vs {tT:.0f}")
check("callout bottom border", bot is not None and abs(bot-tB)<=4, f"{bot} vs {tB:.0f}")
vl=[x for x in vcols if x<tI-6]; vi=[x for x in vcols if abs(x-tI)<=6]; vr=[x for x in vcols if x>tI+6]
# spurious = red strokes BETWEEN the chrome panel border (~85-91) and the callout stroke
spur = [x for x in vcols if (max(vl)+5 if vl else 89) <= x <= tI-3]
check("no spurious stroke between panel border and callout", not spur, f"{spur}")
check("callout left stroke", bool(vi), f"{vi} vs {tI:.0f}")
check("callout right stroke", bool(vr) and abs(min(vr,key=lambda z:abs(z-tR))-tR)<=4, f"{vr} vs {tR:.0f}")

# white fill: connected component containing the callout center
white = (R[:,:,0]>240)&(R[:,:,1]>240)&(R[:,:,2]>230)
lab,n = ndi.label(white)
cc = lab[int(fy2ry(470)), int(fx2rx(200))]
ys,xs = np.nonzero(lab==cc)
b = (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
tw = (fx2rx(67), fy2ry(394), fx2rx(361), fy2ry(508))
ok = abs(b[0]-tw[0])<=5 and abs(b[2]-tw[2])<=5 and abs(b[1]-tw[1])<=5 and abs(b[3]-tw[3])<=5
check("callout white fill", bool(ok), f"render {b} target {tuple(round(v) for v in tw)}")

# ---- callout text lines: x-window frame 80..350 (excludes borders + arc labels)
blue = ((R[:,:,2]-R[:,:,0])>60)&(R[:,:,2]>120)
redt = (R[:,:,0]>135)&((R[:,:,0]-R[:,:,1])>40)&(R[:,:,1]<140)&(R[:,:,2]<150)
yel  = (R[:,:,0]>200)&(R[:,:,1]>190)&(R[:,:,2]<130)
X0,X1 = int(fx2rx(80)), int(fx2rx(350))+1
def linebox(mask, fylo, fyhi, nm):
    m = np.zeros_like(mask); m[int(fy2ry(fylo)):int(fy2ry(fyhi))+1, X0:X1] = mask[int(fy2ry(fylo)):int(fy2ry(fyhi))+1, X0:X1]
    b = bbox(m)
    t = (fx2rx(80), fy2ry(fylo), fx2rx(350), fy2ry(fyhi))
    ok = b and b[1]>=t[1]-6 and b[3]<=t[3]+6 and b[0]>=t[0]-6 and b[2]<=t[2]+6
    check(nm, bool(ok), f"render {b} in band y({t[1]:.0f},{t[3]:.0f})")
# measured ink targets: L1 frame y 401..414 x 106..322; L2 419..431 x 80..348; L3 455..469 x 104..324
linebox(blue, 398, 417, "L1 ink band")
linebox(blue, 417, 434, "L2 ink band")
linebox(redt, 452, 472, "L3 ink band")
# precise width checks (closed loop ~4px)
def ink_w(mask, fylo, fyhi):
    m = np.zeros_like(mask); m[int(fy2ry(fylo)):int(fy2ry(fyhi))+1, X0:X1] = mask[int(fy2ry(fylo)):int(fy2ry(fyhi))+1, X0:X1]
    b = bbox(m); return (b[0],b[2]) if b else None
for nm, mask, fylo, fyhi, tx0f, tx1f in (("L1 width",blue,398,417,106,322),("L2 width",blue,417,434,80,348),("L3 width",redt,452,472,104,324)):
    w = ink_w(mask,fylo,fyhi)
    ok = w and abs(w[0]-fx2rx(tx0f))<=4 and abs(w[1]-fx2rx(tx1f))<=4
    check(nm, bool(ok), f"render x({w[0]},{w[1]}) target ({fx2rx(tx0f):.0f},{fx2rx(tx1f):.0f})")
linebox(yel, 396, 418, "yellow highlight")
m = np.zeros_like(redt); m[int(fy2ry(400)):int(fy2ry(415)), int(fx2rx(212)):int(fx2rx(232))] = redt[int(fy2ry(400)):int(fy2ry(415)), int(fx2rx(212)):int(fx2rx(232))]
check("red omega in L1", int(m.sum())>10, f"n={int(m.sum())}")

# ---- heads 8..10: BBOX centers (triangles' pixel centroid sits 1/3-h above center)
orange = (np.abs(R[:,:,0]-224)<=50)&(np.abs(R[:,:,1]-96)<=55)&(np.abs(R[:,:,2]-16)<=55)
for k,(sx,sy) in {8:(576.2,522.7),9:(689.1,493.4),10:(777.0,408.7)}.items():
    x0,y0 = int(to_rx(sx))-14 if False else int(sx*150/72)-14, int(sy*150/72)-14
    m = orange[y0:y0+28, x0:x0+28]
    bb = bbox(m)
    cx,cy = x0+(bb[0]+bb[2])/2, y0+(bb[1]+bb[3])/2
    check(f"head k={k} bbox-center", bb[4]>8 and abs(cx-sx*150/72)<=4 and abs(cy-sy*150/72)<=4,
          f"({cx:.0f},{cy:.0f}) vs ({sx*150/72:.0f},{sy*150/72:.0f}) n={bb[4]}")
x0,y0 = int(805.5*150/72)-14, int(297.2*150/72)-14
check("head k=11 absent", int(orange[y0:y0+28, x0:x0+28].sum())==0, f"n={int(orange[y0:y0+28, x0:x0+28].sum())}")

# ---- labels k7m,8,9,10 (red CC0000) bbox centers near measured centroids
lblred = (R[:,:,0]>150)&((R[:,:,0]-R[:,:,1])>80)&(R[:,:,1]<120)
for k,(sx,sy) in {7:(414.2,479.6),8:(530.3,523.7),9:(642.8,527.0),10:(749.4,489.2)}.items():
    x0,y0 = int(sx*150/72)-20, int(sy*150/72)-13
    m = lblred[y0:y0+26, x0:x0+40]
    bb = bbox(m)
    cx,cy = x0+(bb[0]+bb[2])/2, y0+(bb[1]+bb[3])/2
    check(f"label k={k} center", bb[4]>8 and abs(cx-sx*150/72)<=4 and abs(cy-sy*150/72)<=4,
          f"({cx:.0f},{cy:.0f}) vs ({sx*150/72:.0f},{sy*150/72:.0f}) n={bb[4]}")
x0,y0 = int(fx2rx(376.9))-16, int(fy2ry(467.5))-12
check("label k7 old spot absent", int(lblred[y0:y0+24, x0:x0+32].sum())==0, f"n={int(lblred[y0:y0+24, x0:x0+32].sum())}")

# ---- chips 9..11 fill present near polar predictions
fill = (np.abs(R[:,:,0]-204)<=35)&(np.abs(R[:,:,1]-255)<=30)&(np.abs(R[:,:,2]-204)<=35)
for k,deg in {9:270,10:300,11:330}.items():
    sx = 581+182.5*math.cos(math.radians(deg)); sy = 297.2-182.5*math.sin(math.radians(deg))
    x0,y0 = int(sx*150/72)-45, int(sy*150/72)-55
    m = fill[y0:y0+110, x0:x0+90]
    check(f"chip k={k} fill present", int(m.sum())>500, f"n={int(m.sum())}")

# ---- arcs 8..10 pale strokes present; arc 11 absent
pale = (np.abs(R[:,:,0]-240)<=28)&(np.abs(R[:,:,1]-201)<=38)&(np.abs(R[:,:,2]-176)<=45)
Yf,Xf = np.mgrid[0:H,0:W]
dx = (Xf/(150/72) - 581.0)*0.96123; dy = -(Yf/(150/72) - 297.2)*0.95556
rr = np.hypot(dx,dy); ang = np.degrees(np.arctan2(dy,dx))%360
for k,(alo,ahi) in {8:(250,270),9:(280,300),10:(310,330)}.items():
    m = pale&(rr>195)&(rr<245)&(ang>=alo)&(ang<=ahi)
    check(f"arc k={k} pale ink", int(m.sum())>40, f"n={int(m.sum())}")
m11 = pale&(rr>195)&(rr<245)&(ang>=340)&(ang<=359)
check("arc k=11 absent", int(m11.sum())<25, f"n={int(m11.sum())}")

# ---- containment: text ink inside callout interior (frame x 70..356)
for nm, mask in (("blue text within callout",blue),("red text within callout",redt)):
    m = np.zeros_like(mask); m[int(fy2ry(396)):int(fy2ry(512)), int(fx2rx(70)):int(fx2rx(356))] = \
        mask[int(fy2ry(396)):int(fy2ry(512)), int(fx2rx(70)):int(fx2rx(356))]
    b = bbox(m)
    ok = bool(b) and b[0]>=fx2rx(70)-2 and b[2]<=fx2rx(356)+2 and b[1]>=fy2ry(392) and b[3]<=fy2ry(512)
    check(nm, bool(ok), f"{b}")

# ---- house frame containment: no ink on the white canvas margin (x<84, x>1917, y<92);
# the panel's bottom stroke half-visible at the slide edge is chrome BY DESIGN.
ink = (np.abs(R-233).sum(axis=2)>150)
band = np.zeros_like(ink); band[:, :84]=True; band[:, 1918:]=True; band[:92,:]=True
check("house frame containment", int((ink&band).sum())<30, f"n={int((ink&band).sum())}")

print(f"\nSELFCHECK {'FAIL: '+', '.join(fails) if fails else 'ALL PASS'}")
sys.exit(1 if fails else 0)
