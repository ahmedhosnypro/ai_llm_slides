# m6.py — exact bounds: eq panel border, equals, arrow, band, circles, navy head
import numpy as np
from PIL import Image
from scipy import ndimage
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
mx = a.max(axis=2); mn = a.min(axis=2); sat = mx-mn

def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs)==0: return None
    return (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),len(xs))

# eq panel border: red-ish ink in x50..475 y60..285 excluding matrix/pill/outcell boxes
redish = (R>170)&(sat>40)&(R-G>40)&(R-B>30)
eqzone = np.zeros(a.shape[:2],bool); eqzone[60:286,50:476]=True
m = redish & eqzone
print("EQ border+red ink bbox:", bbox(m))
# border rows/cols: count per row/col to find the rect edges
rows = m.sum(axis=1); cols = m.sum(axis=0)
print(" rows with >100 red px:", [ (y,int(rows[y])) for y in range(60,286) if rows[y]>100 ])
print(" cols with >50 red px:", [ (x,int(cols[x])) for x in range(50,476) if cols[x]>50 ])
# equals: redish in x372..410 y150..215
m2 = redish & np.pad(np.ones((66,39),bool),((150,540-215-1),(372,960-410-1)),constant_values=False) if False else (redish & (np.arange(960)[None,:]>=372)&(np.arange(960)[None,:]<=410)&(np.arange(540)[:,None]>=150)&(np.arange(540)[:,None]<=215))
print("EQUALS bbox:", bbox(m2))
# 1xd: redish x180..210 y140..160
m3 = redish & (np.arange(960)[None,:]>=180)&(np.arange(960)[None,:]<=212)&(np.arange(540)[:,None]>=138)&(np.arange(540)[:,None]<=160)
print("1xd bbox:", bbox(m3))
# X_2 label: redish x110..145 y150..190
m4 = redish & (np.arange(960)[None,:]>=105)&(np.arange(960)[None,:]<=145)&(np.arange(540)[:,None]>=150)&(np.arange(540)[:,None]<=190)
print("X2 label bbox:", bbox(m4))
# WQ label: redish x170..215 y200..240
m5 = redish & (np.arange(960)[None,:]>=170)&(np.arange(960)[None,:]<=215)&(np.arange(540)[:,None]>=198)&(np.arange(540)[:,None]<=242)
print("WQ label bbox:", bbox(m5))
# dxd labels
m6 = redish & (np.arange(960)[None,:]>=335)&(np.arange(960)[None,:]<=370)&(np.arange(540)[:,None]>=232)&(np.arange(540)[:,None]<=258)
print("dxd(matrix) bbox:", bbox(m6))
m7 = redish & (np.arange(960)[None,:]>=405)&(np.arange(960)[None,:]<=445)&(np.arange(540)[:,None]>=232)&(np.arange(540)[:,None]<=258)
print("under-output bbox:", bbox(m7))
# ARROW: redish outline in x470..920 y95..245 (excluding title x560..845 y115..175)
m8 = redish & (np.arange(960)[None,:]>=468)&(np.arange(960)[None,:]<=922)&(np.arange(540)[:,None]>=95)&(np.arange(540)[:,None]<=246)
m8 &= ~((np.arange(960)[None,:]>=555)&(np.arange(960)[None,:]<=850)&(np.arange(540)[:,None]>=115)&(np.arange(540)[:,None]<=175))
print("ARROW red bbox:", bbox(m8))
lab,n = ndimage.label(m8)
cc = sorted([(int(np.where(lab==i)[1].min()),int(np.where(lab==i)[0].min()),int(np.where(lab==i)[1].max()),int(np.where(lab==i)[0].max()),int((lab==i).sum())) for i in range(1,n+1)], key=lambda c:-c[4])
print("  arrow comps:", cc[:6])
# BAND: fill mask sat<14, 200<mx<240, in x480..910 y250..510; exclude white
bandf = (sat<14)&(mx>196)&(mx<242)
bandf[:300,:]=False; bandf[470:,:]=False; bandf[:,:495]=False; bandf[:,895:]=False
bb = bbox(bandf)
print("BAND bbox:", bb)
sub_ = a[bb[1]+8:bb[3]-8, bb[0]+8:bb[2]-8].reshape(-1,3)
print("  band fill median:", "#%02X%02X%02X"%tuple(np.median(sub_,axis=0).astype(int)))
# OUTPUT circles: blue ring mask
blue = (B>120)&(B-R>40)&(B-G>25)
oc = np.zeros(a.shape[:2],bool); oc[250:300,480:910]=True
moc = blue&oc
lab2,n2 = ndimage.label(moc)
cents=[]
for i in range(1,n2+1):
    ys,xs=np.where(lab2==i)
    if len(xs)<25: continue
    cents.append((float(xs.mean()),float(ys.mean()),len(xs),int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max())))
print("OUTPUT circle ring comps (cx,cy,px,...):", [(round(c[0],1),round(c[1],1),c[2]) for c in sorted(cents)])
# INPUT circles: red ring mask in y435..495
red2 = (R>150)&(sat>35)&(R-G>40)
ic = np.zeros(a.shape[:2],bool); ic[430:500,480:910]=True
mic = red2&ic
lab3,n3 = ndimage.label(mic)
cents3=[]
for i in range(1,n3+1):
    ys,xs=np.where(lab3==i)
    if len(xs)<20: continue
    cents3.append((round(float(xs.mean()),1),round(float(ys.mean()),1),len(xs)))
print("INPUT circle ring comps:", sorted(cents3))
# input circle fill: sample inside
for (x,y) in [(540,464),(647,464),(757,464),(861,464)]:
    print(f"  input fill ({x},{y}) #%02X%02X%02X" % tuple(a[y,x]))
# NAVY arrowhead: dark blue ink x640..760 y310..410
navy = (mx<130)&(B>R+20)
nn = np.zeros(a.shape[:2],bool); nn[300:420,620:780]=True
m9 = navy&nn
print("NAVY head bbox:", bbox(m9))
# output circle fill sample
for (x,y) in [(540,276),(648,276),(760,276),(863,276)]:
    print(f"  output fill ({x},{y}) #%02X%02X%02X" % tuple(a[y,x]))
