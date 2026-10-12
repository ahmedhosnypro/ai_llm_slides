import numpy as np
from PIL import Image
ren=np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/render_1.png').convert('RGB')).astype(int)
S=ren.shape[1]/960.0
dk=(ren.sum(axis=2)<560)
# expected bars: c103@152.5 (x363..433), c303@270.5 (x145..159), c402/404/405@333.5, c503/c603@410
for name,(x0,x1),yb in [('c103',(363,433),152.5),('c303',(145,159),270.5),('c402',(265,326),333.5),
                        ('c404',(409,490),333.5),('c405',(512,593),333.5),('c503',(260,341),410.0),('c603',(712,792),410.0)]:
    x0i,x1i=int((x0-3)*S),int((x1+3)*S); y0i,y1i=int((yb-25)*S),int((yb+25)*S)
    sub=dk[y0i:y1i, x0i:x1i]
    best=(0,0)
    for i,row in enumerate(sub):
        idx=np.where(row)[0]
        if len(idx)==0: continue
        s=p=idx[0]; mx=0
        for k in idx[1:]:
            if k>p+1: mx=max(mx,p-s+1); s=k
            p=k
        mx=max(mx,p-s+1)
        if mx>best[1]: best=(i,mx)
    got_y=(y0i+best[0])/S
    print(f'{name}: rendered bar y={got_y:.1f} frame (len {best[1]} render px) expected {yb}  d={got_y-yb:+.1f}')
