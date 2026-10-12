from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
red = (r>110)&(g<105)&(b<105)&((r-g)>50)

def modal(x0,y0,x1,y1,label,q=6):
    reg = a[y0:y1,x0:x1].reshape(-1,3)
    qq=(reg//q*q); cnt=Counter(map(tuple,qq)); (c,n)=cnt.most_common(1)[0]
    print(f"{label:30s} modal#{c[0]+3:02X}{c[1]+3:02X}{c[2]+3:02X} n={n}/{len(reg)}")

def vscan(x, y0, y1, label):
    print(f"-- vscan x={x} {label}")
    prev=None
    for y in range(y0,y1):
        px=a[y,x]; c=f"{px[0]:02X}{px[1]:02X}{px[2]:02X}"
        if c!=prev: print(f"   y={y} #{c}"); prev=c
def bboxm(mask,label,ox=0,oy=0):
    ys,xs = np.where(mask)
    if len(ys)==0: print(label,"EMPTY"); return
    print(f"{label:28s} x[{xs.min()+ox}..{xs.max()+ox+1}) y[{ys.min()+oy}..{ys.max()+oy+1}) n={len(ys)}")

vscan(365, 202, 214, "FE top border")
vscan(470, 202, 214, "FS top border")
vscan(365, 258, 270, "FE bottom border")
# classification white text looser
wt = (r>190)&(g>170)&(b>170)
sub = wt[225:250, 538:628]
ys,xs = np.where(sub)
print("Classif white text: x", xs.min()+538, xs.max()+538, "y", ys.min()+225, ys.max()+225)
# starburst yellow
yel = (r>235)&(g>225)&(b>150)&(b<225)
sub = yel[370:445, 700:890]
ys,xs = np.where(sub)
print("starburst yellow: x", xs.min()+700, xs.max()+700, "y", ys.min()+370, ys.max()+370, "n", len(ys))
modal(775,402,835,418,"starburst yellow core")
sred = red[370:445, 700:895]
ys,xs = np.where(sred)
print("starburst red outline: x", xs.min()+700, xs.max()+700, "y", ys.min()+370, ys.max()+370)
# starburst text: red strictly inside yellow hull x740..850 y392..428
sub = red[392:430, 740:855]
ys,xs = np.where(sub)
print("starburst text: x", xs.min()+740, xs.max()+740, "y", ys.min()+392, ys.max()+392)
rows = sub.sum(axis=1)
bands=[]; inb=False
for i,c in enumerate(rows):
    if c>0 and not inb: inb=True; s=i
    if c==0 and inb: inb=False; bands.append((s+392,i+392))
if inb: bands.append((s+392,430))
print("starburst text bands:", bands)
# black bar
black = (r<70)&(g<70)&(b<70)
sub = black[500:540, :]
ys,xs = np.where(sub)
print("blackbar: x", xs.min(), xs.max()+1, "y", ys.min()+500, ys.max()+501)
rows = sub.sum(axis=1)
print("blackbar rows:", [(i+500,int(rows[i])) for i in range(len(rows)) if rows[i]>50])
# error text core color
modal(759,200,788,270,"error text core")
# error text vertical bands
sub = red[175:296, 759:768]
rows = sub.sum(axis=1)
bands=[]; inb=False
for i,c in enumerate(rows):
    if c>0 and not inb: inb=True; s=i
    if c==0 and inb: inb=False; bands.append((s+175,i+175))
if inb: bands.append((s+175,296))
print("err lineA bands:", bands)
sub = red[175:296, 775:787]
rows = sub.sum(axis=1)
bands=[]; inb=False
for i,c in enumerate(rows):
    if c>0 and not inb: inb=True; s=i
    if c==0 and inb: inb=False; bands.append((s+175,i+175))
if inb: bands.append((s+175,296))
print("err lineB bands:", bands)
# green stem top: does green touch error box bottom y298?
grn = (g-r>25)&(g-b>15)&(g>70)&(g<210)
sub = grn[296:312, 750:790]
ys,xs = np.where(sub)
print("green stem: x", xs.min()+750, xs.max()+750, "y", ys.min()+296, ys.max()+296)
# green box border core modal
modal(262,355,264,360,"greenbox left border")
# title: per-word red runs at y78 to see spacing
m = np.where(red[78,100:900])[0]+100
groups = np.split(m, np.where(np.diff(m)>6)[0]+1)
print("title y=78 word runs:", [f"{gp.min()}-{gp.max()}" for gp in groups])
