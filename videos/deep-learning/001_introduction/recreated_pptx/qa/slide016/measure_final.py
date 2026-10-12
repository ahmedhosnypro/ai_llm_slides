from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

def darkbbox(img,y0,y1,x0,x1,label,th=140):
    reg=img[y0:y1+1,x0:x1+1]
    m=reg.max(axis=2)<th
    ys,xs=np.where(m)
    print(label,(x0+int(xs.min()),y0+int(ys.min()),x0+int(xs.max()),y0+int(ys.max())),'n',len(ys))
darkbbox(f09,200,280,735,875,'f09 box5 dark bbox')
darkbbox(f16,200,280,735,875,'f16 box5 dark bbox')

# f16 box5 top border row 208/209 sample
print('f16 box5 top rows 207..211 at x760,790,820,850:')
for y in range(207,212):
    print(' y',y,[tuple(f16[y,x]) for x in (760,790,820,850)])
# f09 box5 top border rows for comparison
print('f09 box5 top rows 207..211:')
for y in range(207,212):
    print(' y',y,[tuple(f09[y,x]) for x in (760,790,820,850)])

# f09 label_cleaned ink bands (x242..328, y292..333)
def inkbands(img,y0,y1,x0,x1,label,th=110):
    reg=img[y0:y1+1,x0:x1+1]
    m=reg.max(axis=2)<th
    rows=m.sum(axis=1)
    bands=[];inr=False
    for i,c in enumerate(rows):
        if c>1 and not inr: s=i;inr=True
        if c<=1 and inr: bands.append((y0+s,y0+i-1));inr=False
    if inr: bands.append((y0+s,y1))
    out=[]
    for b in bands:
        mm=img[b[0]:b[1]+1,x0:x1+1].max(axis=2)<th
        cc=mm.sum(axis=0); xs=np.where(cc>0)[0]
        out.append((b,(x0+int(xs.min()),x0+int(xs.max()))))
    print(label,out)
inkbands(f09,292,333,243,328,'f09 label_cleaned ink')
inkbands(f16,292,333,86,277,'f16 calloutA ink')

# box5 border color: median of darkest 25% ring pixels
reg=f16[207:267,746:865]
ring=np.ones(reg.shape[:2],bool)
ring[4:-4,4:-4]=False
px=reg[ring]
lum=px.max(axis=1)
idx=np.argsort(lum)[:max(20,int(len(px)*0.2))]
sel=px[idx]
med=np.median(sel,axis=0)
print('f16 box5 border darkest-20% median:',med, 'n=',len(sel))
# also 2pt border? count dark pixels per border side row y208
row=f16[208,747:864]
print('row208 dark count:',int((row.max(axis=1)<140).sum()),'of',len(row))
col=f16[210:263,862]
print('col862 dark count:',int((col.max(axis=1)<140).sum()),'of',len(col))
col=f16[210:263,748]
print('col748 dark count:',int((col.max(axis=1)<140).sum()),'of',len(col))
