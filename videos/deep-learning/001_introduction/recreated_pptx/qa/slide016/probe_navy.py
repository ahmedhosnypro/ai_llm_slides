from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
# navy-ish mask: blue dominant, dark
def navy(img,label,y0,y1,x0,x1):
    reg=img[y0:y1,x0:x1]
    m=(reg[:,:,2]-reg[:,:,0]>25)&(reg[:,:,2]<200)&(reg[:,:,0]<150)
    ys,xs=np.where(m)
    if len(ys)==0: print(label,'none'); return
    print(label,'navy bbox y',y0+ys.min(),'..',y0+ys.max(),' x',x0+xs.min(),'..',x0+xs.max(),' n=',len(ys))
    # column histogram
    cols={}
    for yy,xx in zip(ys,xs):
        cols[x0+xx]=cols.get(x0+xx,0)+1
    top=sorted(cols.items(),key=lambda kv:-kv[1])[:12]
    print('  top cols:',top)
navy(f16,'f16',100,300,60,740)
navy(f09,'f09',100,300,60,740)
# where does the f16 navy column at 129-130 start/end vertically?
col=f16[:,129]
m=(col[:,2]-col[:,0]>25)&(col[:,0]<150)
ys=np.where(m)[0]
print('f16 col129 navy rows:',ys.min() if len(ys) else None,'..',ys.max() if len(ys) else None, 'count',len(ys))
col=f16[:,130]
m=(col[:,2]-col[:,0]>25)&(col[:,0]<150)
ys=np.where(m)[0]
print('f16 col130 navy rows:',ys.min() if len(ys) else None,'..',ys.max() if len(ys) else None,'count',len(ys))
