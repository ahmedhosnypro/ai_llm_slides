# m11_net.py — network panel: band bbox, circles, lines, arcs, colors
import numpy as np
from PIL import Image
from scipy import ndimage
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
mx=a.max(axis=2); sat=mx-a.min(axis=2)

# BAND: gray fill inside white panel. interior gray mask
band = (sat<15)&(mx>200)&(mx<246)
zone = np.zeros(a.shape[:2],bool); zone[250:505,482:905]=True
bm = band&zone
# largest comp
lab,n = ndimage.label(bm)
sizes = ndimage.sum(bm,lab,range(1,n+1))
i = int(np.argmax(sizes))+1
ys,xs = np.where(lab==i)
print(f"BAND comp bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} px={int(sizes[i-1])}")
# fill median of band interior
core = a[ys.min()+10:ys.max()-10, xs.min()+10:xs.max()-10].reshape(-1,3)
corem = core[(core.max(axis=1)<250)]
print("band fill median:", "#%02X%02X%02X"%tuple(np.median(corem,axis=0).astype(int)))
# row profile of band comp at its middle
ymid=(ys.min()+ys.max())//2
row = lab[ymid]
xs_in = np.where(row==i)[0]
print(f"band row y={ymid} x{xs_in.min()}..{xs_in.max()}")
xmid=(xs.min()+xs.max())//2
col = lab[:,xmid]
ys_in = np.where(col==i)[0]
print(f"band col x={xmid} y{ys_in.min()}..{ys_in.max()}")

# OUTPUT circles: sample ring color + fill
print("output ring sample:", "#%02X%02X%02X"%tuple(a[259,540]), "#%02X%02X%02X"%tuple(a[277,522]))
print("output fill samples:", " ".join("#%02X%02X%02X"%tuple(a[y,x]) for (x,y) in [(548,288),(656,288),(768,288),(871,288)]))
# INPUT circles: ring + fill
print("input ring samples:", " ".join("#%02X%02X%02X"%tuple(a[y,x]) for (x,y) in [(540,486),(648,486),(758,486),(862,486),(519,464),(759,446)]))
print("input fill samples:", " ".join("#%02X%02X%02X"%tuple(a[y,x]) for (x,y) in [(528,455),(636,455),(746,455),(850,455),(528,472),(636,472)]))
# circle bboxes: blue ring comps in output row; red ring comps in input row (min_px small)
blue=(B>110)&(B-R>30)&(B-G>20)
zone2=np.zeros(a.shape[:2],bool); zone2[250:305,495:900]=True
m=blue&zone2
lab,n=ndimage.label(m)
print("OUTPUT ring comps:")
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(xs)<15: continue
    print(f"  x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} px={len(xs)}")
red=(R>140)&(sat>30)&(R-G>35)&(R-B>35)
zone3=np.zeros(a.shape[:2],bool); zone3[438:498,495:900]=True
m=red&zone3
lab,n=ndimage.label(m)
print("INPUT ring comps:")
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(xs)<15: continue
    print(f"  x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} px={len(xs)}")
# ARCS under output circles
zone4=np.zeros(a.shape[:2],bool); zone4[290:312,495:900]=True
mr=(red|((B>110)&(B-R>30))|((G>100)&(G-R>20)&(G-B>20)))&zone4
lab,n=ndimage.label(mr)
print("ARC comps under outputs:")
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(xs)<10: continue
    med = "#%02X%02X%02X"%tuple(np.median(a[ys,xs].reshape(-1,3),axis=0).astype(int))
    print(f"  x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} px={len(xs)} {med}")
# LINES in upper fan (y250..300) and lower fan (y430..445): colored thin lines
for (y0,y1,name) in [(250,302,"UPPER fan"),(428,448,"LOWER fan")]:
    z=np.zeros(a.shape[:2],bool); z[y0:y1,482:905]=True
    ml=((R>140)&(sat>30)&(R-G>30))|((B>110)&(B-R>25)&(B-G>15))|((G>100)&(G-R>15)&(G-B>15))
    m=ml&z
    lab,n=ndimage.label(m)
    print(f"{name} colored comps:")
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(xs)<12: continue
        med = "#%02X%02X%02X"%tuple(np.median(a[ys,xs].reshape(-1,3),axis=0).astype(int))
        print(f"  x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} px={len(xs)} {med}")
