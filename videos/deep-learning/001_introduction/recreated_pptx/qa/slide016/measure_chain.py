from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)

# red line extent at y235..238 between x230..300 (arrow1) and other arrows
def red_span(img,y0,y1,x0,x1,label):
    reg=img[y0:y1+1,x0:x1+1]
    m=(reg[:,:,0]>140)&(reg[:,:,1]<95)&(reg[:,:,2]<95)
    cols=m.sum(axis=0)
    xs=np.where(cols>0)[0]
    print(label,'red cols:',x0+int(xs.min()),'..',x0+int(xs.max()) if len(xs) else None,'n=',len(xs))
red_span(f16,234,239,228,300,'f16 arrow1 zone')
red_span(f09,234,239,228,300,'f09 arrow1 zone')
red_span(f16,234,239,410,445,'f16 arrow2 zone')
red_span(f09,234,239,410,445,'f09 arrow2 zone')
red_span(f16,234,239,560,592,'f16 arrow3 zone')
red_span(f09,234,239,560,592,'f09 arrow3 zone')
red_span(f16,234,239,722,752,'f16 arrow4 zone')
red_span(f09,234,239,722,752,'f09 arrow4 zone')

# box text ink bands/cols for box1 in f16 (fill x131..234) vs f09 (x146..249)
def textbands(img,y0,y1,x0,x1,label):
    reg=img[y0:y1+1,x0:x1+1]
    m=reg.max(axis=2)<110
    rows=m.sum(axis=1)
    bands=[];inr=False
    for i,c in enumerate(rows):
        if c>1 and not inr: s=i;inr=True
        if c<=1 and inr: bands.append((y0+s,y0+i-1));inr=False
    if inr: bands.append((y0+s,y1))
    out=[]
    for b in bands:
        mm=img[b[0]:b[1]+1,x0:x1+1].max(axis=2)<110
        cc=mm.sum(axis=0); xs=np.where(cc>0)[0]
        out.append((b,(x0+int(xs.min()),x0+int(xs.max()))))
    print(label,out)
textbands(f16,215,262,132,234,'f16 box1 text')
textbands(f09,215,262,147,249,'f09 box1 text')
textbands(f16,215,262,294,407,'f16 box2 text')
textbands(f09,215,262,294,407,'f09 box2 text')
textbands(f16,215,262,592,720,'f16 box4 (Classification) text')
textbands(f09,215,262,592,720,'f09 box4 text')

# box1 border color modal in f16
from collections import Counter
reg=f16[208:267,128:238]
m=(reg.max(axis=2)<160)
px=reg[m]
cnt=Counter(map(tuple,px))
print('f16 box1 border-ish modal:',cnt.most_common(4))
# last box border modal
reg=f16[208:267,747:864]
m=(reg.max(axis=2)<140)
cnt=Counter(map(tuple,reg[m]))
print('f16 box5 border modal:',cnt.most_common(4))
# last box fill modal (core)
reg=f16[215:260,755:855]
cnt=Counter(map(tuple,reg.reshape(-1,3)))
print('f16 box5 fill modal:',cnt.most_common(4))
# training ellipse fill modal core
reg=f16[140:180,100:190]
cnt=Counter(map(tuple,reg.reshape(-1,3)))
print('f16 train ellipse fill modal:',cnt.most_common(3))
reg=f09[148:188,100:190]
cnt=Counter(map(tuple,reg.reshape(-1,3)))
print('f09 train ellipse fill modal:',cnt.most_common(3))
