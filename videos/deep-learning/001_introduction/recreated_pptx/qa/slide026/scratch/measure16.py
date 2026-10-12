from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
dk = (a.sum(axis=2)<560)
# horizontal-bar detector: rows where a contiguous dark run >= 30px exists
def bars(y0,y1,x0,x1,label):
    print(label)
    for y in range(y0,y1):
        row = dk[y,x0:x1]
        idx = np.where(row)[0]
        if len(idx)<25: continue
        # longest contiguous run
        runs=[]; s=p=idx[0]
        for i in idx[1:]:
            if i>p+1: runs.append((s,p)); s=i
            p=i
        runs.append((s,p))
        long=[(x0+s,x0+e) for s,e in runs if e-s>=25]
        if long: print('  y',y,long)
bars(305,370,100,600,'eq4 bars:')
bars(124,180,355,500,'eq1b bars:')
# eq1b '=' search: two short bars stacked around x440..470
print('eq1b zone rows 138..162, x430..480:')
for y in range(138,163):
    row=dk[y,430:481]
    idx=np.where(row)[0]
    print(' ',y, [(430+s,430+e) for s,e in [(idx[0],idx[-1])]] if len(idx) else '.', len(idx))
