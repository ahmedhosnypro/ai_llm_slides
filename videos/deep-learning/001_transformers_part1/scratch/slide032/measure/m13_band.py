# m13_band.py — all colored text comps in band; navy head; border color medians
import numpy as np
from PIL import Image
from scipy import ndimage
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
mx=a.max(axis=2); sat=mx-a.min(axis=2)

zone=np.zeros(a.shape[:2],bool); zone[302:432,488:895]=True
masks = {
 "red":   (R>130)&(sat>30)&(R-G>35)&(R-B>25),
 "blue":  (B>110)&(B-R>30)&(B-G>20),
 "green": (G>90)&(G-R>20)&(G-B>20),
}
for name,mm in masks.items():
    m = mm&zone
    lab,n = ndimage.label(m)
    comps=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(xs)<8: continue
        comps.append((int(xs.mean()),int(ys.mean()),int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),len(xs)))
    comps.sort()
    print(f"--- BAND {name} comps (cx,cy bbox px):")
    for c in comps:
        print(f"   ({c[0]},{c[1]}) x{c[2]}..{c[4]} y{c[3]}..{c[5]} px={c[6]}")

# navy/dark head crop map
print("=== NAVY head zone x655..745 y315..395 cell=2 (#=dark, B=blue, R=red, G=green, -=gray, .=white)")
def cls(p):
    r,g,b=int(p[0]),int(p[1]),int(p[2])
    mxx=max(p)
    if mxx<115: return "#"
    if b-r>25 and b-g>10: return "B"
    if r-g>25 and r-b>15: return "R"
    if g-r>15 and g-b>15: return "G"
    if mxx-max(p[0],p[1],p[2])==0 and mxx<235: return "-"
    if mxx>=246 and mxx-min(p)<=10: return "."
    return "?"
for y in range(315,396,2):
    line="".join(cls(np.median(a[y:y+2,x:x+2].reshape(-1,3),axis=0)) for x in range(655,746,2))
    print(f"{y:3d} {line}")

# border color medians (darkest 30% of border-zone pixels)
def darkmed(x0,y0,x1,y1,pick=None):
    reg = a[y0:y1+1, x0:x1+1].reshape(-1,3)
    lum = reg.sum(axis=1)
    idx = np.argsort(lum)[:max(8,int(len(lum)*0.15))]
    return "#%02X%02X%02X"%tuple(np.median(reg[idx],axis=0).astype(int))
print("EQ panel border (left edge x56..60,y100..250):", darkmed(54,100,62,250))
print("EQ panel border (top y68..73,x150..350):", darkmed(150,66,350,74))
print("NET panel border (top y246..251,x600..800):", darkmed(600,244,800,252))
print("NET panel border (left x477..482,y300..450):", darkmed(475,300,484,450))
print("Output ring (circle2 top y257..262,x630..660):", darkmed(630,255,662,263))
print("Input ring (circle1 bottom y483..488,x530..555):", darkmed(528,481,556,489))
print("Matrix outer border (top y84..88,x240..330):", darkmed(240,83,330,89))
print("Title ink:", darkmed(582,123,823,139))
print("Subtitle ink:", darkmed(562,148,843,171))
print("Arrow outline (left edge x484..488,y150..205):", darkmed(482,150,490,205))
print("Equals ink:", darkmed(386,164,400,184))
print("Badge yellow:", "#%02X%02X%02X"%tuple(np.median(a[62:80,884:902].reshape(-1,3),axis=0).astype(int)))
print("Badge ring:", darkmed(874,60,914,86))
