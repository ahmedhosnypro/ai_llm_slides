#!/usr/bin/env python3
"""Closed-loop self-check slide 011 attempt 1: 150dpi render vs original-frame measurements.
Scale: render px * 72/150 = frame px (960x540, 1px=1pt). Tolerance ~4 frame px (~8.3 render px)."""
from PIL import Image
import numpy as np, sys

RENDER='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide011/render_1.png'
im = np.asarray(Image.open(RENDER).convert('RGB')).astype(int)
H,W = im.shape[:2]
S = 72/150.0  # render px -> frame px factor (0.48); 1 frame px = 2.0833 render px
R = 150/72.0
def fr(v): return v*S      # render px -> frame px (measurements)
def toR(v): return v*R     # frame px -> render px (window bounds)
def fr_(v): return v*S     # render px -> frame px (measurements)
r,g,b = im[:,:,0],im[:,:,1],im[:,:,2]
fails=[]; notes=[]
def chk(name, got_frame, want, tol=4.0):
    d = abs(got_frame-want)
    (notes if d<=tol else fails).append(f"{name}: {got_frame:.1f} vs {want} (d={d:.1f})")

# masks in render space
dark=(r<130)&(g<130)&(b<130)
navy=(r<110)&(g<110)&(b>70)&(b<235)&((b-g)>25)
redink=(r>110)&(g<110)&(b<110)&((r-g)>60)
yellow=(r>200)&(g>200)&(b<190)
grayish=(abs(r-233)<16)&(abs(g-233)<16)&(abs(b-231)<18)
blackm=(r<80)&(g<80)&(b<80)

# 1. title box border centerlines (want x94..364 y61..119)
tb = navy[int(toR(50)):int(toR(126)), int(toR(85)):int(toR(380))]
ys,xs = np.where(tb)
if len(xs)==0: fails.append("title box: no navy border found")
else:
    chk("titlebox left",  fr_(int(toR(85))+xs.min()), 94); chk("titlebox right", fr_(int(toR(85))+xs.max()), 364)
    chk("titlebox top",   fr_(int(toR(50))+ys.min()), 61); chk("titlebox bottom",fr_(int(toR(50))+ys.max()), 119)
# fill color at box interior sample
fy,fx = int(toR(90)), int(toR(150))
notes.append(f"titlebox fill sample render{fx,fy}={tuple(im[fy,fx])} (want ~(224,255,255))")

# 2. content box border (want x95..881 y128..499)
cb = navy[int(toR(122)):int(toR(510)), int(toR(90)):int(toR(890))]
ys,xs = np.where(cb)
if len(xs)==0: fails.append("content box: no navy border found")
else:
    chk("contentbox left",  fr_(int(toR(90))+xs.min()), 95); chk("contentbox right", fr_(int(toR(90))+xs.max()), 881)
    chk("contentbox top",   fr_(int(toR(122))+ys.min()), 128); chk("contentbox bottom",fr_(int(toR(122))+ys.max()), 499)

# 3. title ink (want x123..335, cap-top 80, baseline ~97.5, center 229)
ti = dark[int(toR(62)):int(toR(118)), int(toR(96)):int(toR(362))]
ys,xs = np.where(ti)
if len(xs)==0: fails.append("title ink: none found")
else:
    x0,x1,y0,y1 = fr_(int(toR(96))+xs.min()), fr_(int(toR(96))+xs.max()), fr_(int(toR(62))+ys.min()), fr_(int(toR(62))+ys.max())
    chk("title ink left",x0,123); chk("title ink right",x1,335)
    chk("title cap top",y0,80);  chk("title ink bottom(baseline)",y1,97.5)
    notes.append(f"title ink center {(x0+x1)/2:.1f} (want ~229), width {x1-x0:.1f} (want 213)")

# 4. headline band (want cap-top 138, baseline 151.75; red 128..314; is 324..336; prob 338..527; underline rows 154-155)
band_y0,band_y1 = int(toR(130)), int(toR(165))
redb = redink[band_y0:band_y1, int(toR(100)):int(toR(560))]
ys,xs = np.where(redb)
if len(xs)==0: fails.append("headline red: none")
else:
    chk("headline red left",  fr_(int(toR(100))+xs.min()), 128)
    chk("headline red right", fr_(int(toR(100))+xs.max()), 314)
    chk("headline red top",   fr(band_y0+ys.min()), 138)
darkb = dark[band_y0:band_y1, int(toR(318)):int(toR(560))]
ys,xs = np.where(darkb)
if len(xs)==0: fails.append("headline black: none")
else:
    chk("headline black right", fr_(int(toR(318))+xs.max()), 527)
# underline: continuous run rows
ul=[]
for y in range(int(toR(148)), int(toR(162))):
    row = (r[y,int(toR(340)):int(toR(540))]<200)&(g[y,int(toR(340)):int(toR(540))]<200)&(b[y,int(toR(340)):int(toR(540))]<200)
    xs2=np.where(row)[0]
    if len(xs2)>60:
        best=cur=1
        for i in range(1,len(xs2)):
            cur = cur+1 if xs2[i]==xs2[i-1]+1 else 1
            best=max(best,cur)
        if best>60: ul.append((fr(y),best,fr_(int(toR(340))+xs2.min()),fr_(int(toR(340))+xs2.max())))
if not ul: fails.append("underline: no continuous run found")
else:
    notes.append(f"underline rows(frame): {[(round(u[0],1),int(u[1]),round(u[2],1),round(u[3],1)) for u in ul]} (want rows ~154-155, x345..527)")

# 5. lead-in band (want ink x127..346, cap-top 185, baseline 198.8)
lb = dark[int(toR(178)):int(toR(208)), int(toR(120)):int(toR(400))]
ys,xs = np.where(lb)
if len(xs)==0: fails.append("lead-in: none")
else:
    chk("lead-in left", fr_(int(toR(120))+xs.min()), 127)
    chk("lead-in right",fr_(int(toR(120))+xs.max()), 346)
    chk("lead-in cap top", fr_(int(toR(178))+ys.min()), 185)

# 6. bullet bands (want cap tops 217/249/282/314/347/377/410/442; text-left ~147; rights 387/268/314/372/236/358/210/296)
want=[(217,147,387),(249,146,268),(282,148,314),(314,148,372),(347,148,236),(377,147,358),(410,147,210),(442,146,296)]
for i,(ct,tl,tr) in enumerate(want):
    bb = dark[int(toR(ct-6)):int(toR(ct+26)), int(toR(138)):int(toR(450))]
    ys,xs = np.where(bb)
    if len(xs)==0: fails.append(f"bullet{i+1}: no ink"); continue
    y0 = fr_(int(toR(ct-6))+ys.min()); x0 = fr_(int(toR(138))+xs.min()); x1 = fr_(int(toR(138))+xs.max())
    chk(f"bullet{i+1} cap top", y0, ct)
    chk(f"bullet{i+1} text left", x0, tl)
    chk(f"bullet{i+1} text right", x1, tr)

# 7. ellipsis dots (want 9 dots x148..204 y486..489 pitch 6.6)
eb = dark[int(toR(478)):int(toR(496)), int(toR(136)):int(toR(300))]
ys,xs = np.where(eb)
if len(xs)==0: fails.append("ellipsis: no ink")
else:
    x0,x1 = fr_(int(toR(136))+xs.min()), fr_(int(toR(136))+xs.max())
    y0,y1 = fr_(int(toR(478))+ys.min()), fr_(int(toR(478))+ys.max())
    cols = dark[int(toR(478)):int(toR(496)), int(toR(136)):int(toR(300))].sum(axis=0)
    runs=[];s=None
    for i,v in enumerate(cols):
        if v>0 and s is None: s=i
        if v==0 and s is not None: runs.append((s,i-1)); s=None
    if s is not None: runs.append((s,len(cols)-1))
    notes.append(f"ellipsis dots: {len(runs)} runs x[{x0:.1f}..{x1:.1f}] y[{y0:.1f}..{y1:.1f}] (want 9 dots x[148..204] y[486..489])")
    if len(runs)!=9: fails.append(f"ellipsis dot count {len(runs)} != 9")
    chk("ellipsis left", x0, 148); chk("ellipsis right", x1, 204)

# 8. bullet dots (want centers x129, y 224/256/288/320.5/352.5/385/417/449/481)
for i,cy in enumerate([224,256,288,320.5,352.5,385,417,449,481]):
    dd = dark[int(toR(cy-8)):int(toR(cy+8)), int(toR(120)):int(toR(136))]
    ys,xs = np.where(dd)
    if len(ys)==0: fails.append(f"dot{i+1}: none"); continue
    ycen = fr_(int(toR(cy-8))+(ys.min()+ys.max())/2); xcen = fr_(int(toR(120))+(xs.min()+xs.max())/2)
    chk(f"dot{i+1} y", ycen, cy); notes.append(f"dot{i+1} x {xcen:.1f} (want 129)")

# 9. left rule (want cols 57-58 core, y 43..517)
lr = (r>60)&(g<170)&(b<170)&((r-g)>40)
band = lr[int(toR(100)):int(toR(400)), int(toR(50)):int(toR(70))]
ys,xs = np.where(band)
if len(xs)==0: fails.append("left rule: no red found")
else:
    xcen = fr_(int(toR(50))+xs.mean())
    chk("left rule x center", xcen, 57.5)
    col = lr[int(toR(35)):int(toR(516)), int(toR(56)):int(toR(60))]
    ys2,_ = np.where(col)
    if len(ys2)==0: fails.append("left rule: vertical extent none")
    else: notes.append(f"left rule y extent {fr_(int(toR(35))+ys2.min()):.1f}..{fr_(int(toR(35))+ys2.max()):.1f} (want 43..517)")

# 10. black bar (want x38..921, top 518.5)
bar = blackm[int(toR(500)):, :]
ys,xs = np.where(bar)
if len(xs)==0: fails.append("black bar: none")
else:
    chk("bar left", fr(xs.min()), 38); chk("bar right", fr(xs.max()), 921)
    chk("bar top", fr_(int(toR(500))+ys.min()), 518.5, tol=3.0)

# 11. containment: content ink inside content box (x95..881 y128..499) + no stray ink between boxes/rules
inbox = dark[int(toR(130)):int(toR(498)), int(toR(96)):int(toR(880))]
notes.append(f"containment scan: content-box interior ink bbox checked separately above")
stray = dark[int(toR(121)):int(toR(127)), int(toR(100)):int(toR(875))]  # rows between titlebox bottom(119) and contentbox top(128)
if stray.sum()>0: fails.append(f"stray ink rows 121-127: {stray.sum()} px")

print("== NOTES ==");  [print("  "+n) for n in notes]
print("== FAILS ==");  [print("  "+f) for f in fails] or print("  NONE — ALL CHECKS PASS")
sys.exit(1 if fails else 0)
