# m14_cores.py — fill cores, band bbox, chip geometry, text cores
import numpy as np
from PIL import Image
from scipy import ndimage
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
def med(x0,y0,x1,y1):
    m = np.median(a[y0:y1+1,x0:x1+1].reshape(-1,3),axis=0).astype(int)
    return "#%02X%02X%02X"%tuple(m)
def darkmed(x0,y0,x1,y1,frac=0.12):
    reg = a[y0:y1+1, x0:x1+1].reshape(-1,3)
    lum = reg.sum(axis=1); idx=np.argsort(lum)[:max(6,int(len(lum)*frac))]
    return "#%02X%02X%02X"%tuple(np.median(reg[idx],axis=0).astype(int))
print("matrix cell fill core (x230..250,y88..98):", med(230,88,250,98), med(270,90,290,98), med(340,214,360,222))
print("matrix cell border vert (x257..260,y90..100):", darkmed(256,90,261,100))
print("matrix chip fill (x246..251,y106..114):", med(244,105,252,115), med(282,105,290,115))
print("matrix chip border:", darkmed(228,101,256,104), darkmed(228,117,256,120))
print("matrix text cores: r1", darkmed(228,104,246,117), "r2", darkmed(228,142,246,155), "r3", darkmed(228,185,246,199), "r4", darkmed(228,226,246,240))
print("outcell fill (x420..446,y95..102):", med(420,95,446,102), med(420,180,446,187))
print("outcell border:", darkmed(409,100,414,200), darkmed(448,100,453,200))
print("outcell text core (x416..439,y105..118):", darkmed(416,104,440,119,0.2))
print("output ring:", darkmed(534,256,556,262), darkmed(534,292,556,298))
print("output fill:", med(546,283,558,291), med(654,283,666,291))
print("input ring:", darkmed(528,480,556,487), darkmed(518,458,524,472))
print("input fill:", med(528,452,536,460), med(636,452,644,460), med(746,452,754,460))
print("band fill:", med(560,410,600,420), med(700,405,740,415), med(560,360,580,368))
print("title core:", darkmed(582,123,823,139,0.1))
print("subtitle core:", darkmed(562,148,843,171,0.1))
print("WQ band label core:", darkmed(499,368,533,397,0.15))
print("red label core:", darkmed(513,313,538,329,0.15), darkmed(570,325,596,342,0.15))
print("blue label core:", darkmed(627,313,651,331,0.15), darkmed(668,333,693,348,0.15))
print("green label core:", darkmed(759,325,785,341,0.15), darkmed(848,383,874,399,0.15))
print("X2 label core:", darkmed(117,157,141,183,0.15))
print("1xd core:", darkmed(185,138,204,155,0.15))
print("eq panel fill:", med(70,250,90,262), med(400,80,440,90))
print("arrow fill:", med(500,155,540,170), med(530,210,545,220))
# band bbox: gray runs at several rows
mx=a.max(axis=2); sat=a.max(axis=2)-a.min(axis=2)
band=(sat<15)&(mx>200)&(mx<247)
for y in [308,315,330,360,390,415,424,427]:
    xs=np.where(band[y,480:910])[0]
    if len(xs): print(f"band row y{y}: x{xs.min()+480}..{xs.max()+480} count={len(xs)}")
# chip bboxes row1: yellow mask
yel=(a[:,:,0]>242)&(a[:,:,1]>238)&(a[:,:,2]>140)&(a[:,:,2]<230)&((a[:,:,0]-a[:,:,2])>=18)
z=np.zeros(a.shape[:2],bool); z[95:260,218:378]=True
m=yel&z
lab,n=ndimage.label(m)
chips=[]
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(xs)<60: continue
    chips.append((int(xs.mean()),int(ys.mean()),int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),len(xs)))
chips.sort(key=lambda c:(c[1],c[0]))
print("CHIPS (cx,cy,bbox,px):")
for c in chips: print(f"   ({c[0]},{c[1]}) x{c[2]}..{c[4]} y{c[3]}..{c[5]} px={c[6]}")
