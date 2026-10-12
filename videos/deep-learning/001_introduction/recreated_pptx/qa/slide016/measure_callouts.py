from PIL import Image
import numpy as np
from collections import Counter
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)

mask=(np.abs(f16[:,:,0]-f16[:,:,1])<10)&(np.abs(f16[:,:,1]-f16[:,:,2])<10)&(f16[:,:,0]>195)&(f16[:,:,0]<246)
band=mask[270:400,:]
cols=band.sum(axis=0)
runs=[];inr=False
for x,c in enumerate(cols):
    if c>8 and not inr: x0=x;inr=True
    if c<=8 and inr: runs.append((x0,x-1));inr=False
if inr: runs.append((x0,959))
for (x0,x1) in runs:
    if x1-x0<30: continue
    sub=mask[270:400,x0:x1+1]
    rows=sub.sum(axis=1)
    rr=[i for i,c in enumerate(rows) if c>10]
    if not rr: continue
    y0,y1=270+rr[0],270+rr[-1]
    sub2=f16[y0:y1+1,x0:x1+1]
    cnt=Counter(map(tuple,sub2.reshape(-1,3)))
    print(f'CALLOUT x{x0}..{x1} y{y0}..{y1}  modal:',cnt.most_common(3))
    ring=(np.abs(sub2[:,:,0]-sub2[:,:,1])<12)&(np.abs(sub2[:,:,1]-sub2[:,:,2])<12)&(sub2[:,:,0]>140)&(sub2[:,:,0]<205)
    print('    gray-ring(140..205) px:',int(ring.sum()))
    ink=sub2.max(axis=2)<110
    ir=ink.sum(axis=1)
    bands=[];inr=False
    for i,c in enumerate(ir):
        if c>1 and not inr: s=i;inr=True
        if c<=1 and inr: bands.append((y0+s,y0+i-1));inr=False
    if inr: bands.append((y0+s,y1))
    for b in bands:
        mm=f16[b[0]:b[1]+1,x0:x1+1].max(axis=2)<110
        cc=mm.sum(axis=0); xs2=np.where(cc>0)[0]
        print('    text band',b,'cols',x0+int(xs2.min()),'..',x0+int(xs2.max()))
