from PIL import Image
import numpy as np
QA='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa'
S=2001/960.0
r=np.asarray(Image.open(QA+'/slide016/render_1.png').convert('RGB')).astype(int)
p=np.asarray(Image.open(QA+'/slide009/render_1.png').convert('RGB')).astype(int)
o=np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_016.jpg').convert('RGB')).astype(int)

def prof(img,y0,y1,x0,x1,label,th=110):
    reg=img[int(y0*S):int((y1+1)*S), int(x0*S):int((x1+1)*S)]
    m=reg.max(axis=2)<th
    rows=m.sum(axis=1)
    print(f'--- {label} ink rows (render rows {int(y0*S)}..{int((y1+1)*S)}) ---')
    inr=False
    for i,c in enumerate(rows):
        if c>0 and not inr: s=i;inr=True
        if c==0 and inr: print(f'   band {y0+s/S:.1f}..{y0+(i-1)/S:.1f} (frame px)');inr=False
    if inr: print(f'   band {y0+s/S:.1f}..{y1} (frame px, open)')
prof(p,292,333,243,328,'PARENT render label_cleaned')
prof(r,292,333,86,277,'MY render callout A')
prof(o,292,333,86,277,'ORIGINAL f16 callout A')
prof(p,292,333,538,625,'PARENT render label_features')
prof(r,282,342,436,573,'MY render callout C')
prof(o,282,342,436,573,'ORIGINAL f16 callout C')

# box5 border rows in my render at x805
print('--- box5 top border rows (render) x=805 frame ---')
for ry in range(int(205*S),int(214*S)):
    print(f'  render row {ry} (frame {ry/S:.1f}):', tuple(r[ry,int(805*S)]))

# stray diff locations
mask=np.ones((1125,2001),bool)
mask[int(43*S):int(110*S),:]=False
mask[int(43*S):int(540*S),int(870*S):int(915*S)]=False
dr=(np.abs(r-p).max(axis=2)>48)&mask
dz=np.zeros((1125,2001),bool)
for (y0,y1,x0,x1) in [(125,250,70,250),(205,270,125,255),(230,244,232,296),(204,270,744,868),(278,400,80,580),(265,355,705,900)]:
    dz[int(y0*S):int((y1+1)*S),int(x0*S):int((x1+1)*S)]=True
stray=dr&~dz
ys,xs=np.where(stray)
print('stray px:',len(ys))
if len(ys):
    # cluster by coarse grid
    from collections import Counter
    cnt=Counter(( (y//50*50, x//50*50) for y,x in zip(ys,xs)))
    for (gy,gx),n in sorted(cnt.items(),key=lambda kv:-kv[1])[:15]:
        print(f'  stray cluster render({gx}..{gx+50},{gy}..{gy+50}) frame({gx/S:.0f}..{(gx+50)/S:.0f},{gy/S:.0f}..{(gy+50)/S:.0f}) n={n}')
