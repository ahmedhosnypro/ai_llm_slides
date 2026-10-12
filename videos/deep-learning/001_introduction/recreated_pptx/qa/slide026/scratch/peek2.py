import numpy as np
from PIL import Image
ren=np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/render_1.png').convert('RGB')).astype(int)
S=ren.shape[1]/960.0
dk=(ren.sum(axis=2)<400)
def bands(y0f,y1f,x0f,x1f,axis,gap=6):
    sub=dk[int(y0f*S):int(y1f*S), int(x0f*S):int(x1f*S)]
    proj=sub.sum(axis=axis)
    idx=np.where(proj>0)[0]
    out=[]
    if len(idx):
        s=p=idx[0]
        for i in idx[1:]:
            if i>p+gap: out.append((s,p)); s=i
            p=i
        out.append((s,p))
    base = y0f if axis==1 else x0f
    return [(round(base+int(a/S),1), round(base+int(b/S),1)) for a,b in out]
print('tan1 row bands:', bands(127,298,80,647,1))
print('tan1 col bands:', bands(127,298,80,647,0,gap=14))
print('yellow row bands:', bands(307,368,83,761,1))
print('tan2 row bands:', bands(376,500,80,841,1))
print('tan2 col bands:', bands(376,500,80,841,0,gap=14))
# where ARE dark pixels overall? full-slide row bands
print('full-slide row bands:', bands(45,518,40,920,1,gap=10))
