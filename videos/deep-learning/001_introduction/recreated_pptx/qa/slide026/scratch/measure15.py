from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
dk = (a.sum(axis=2)<560)
def runs2d(y0,y1,x0,x1,gapx=5):
    m = dk[y0:y1, x0:x1]
    idx = np.where(m.sum(axis=0)>0)[0]
    out=[]
    if len(idx):
        s=p=idx[0]
        for i in idx[1:]:
            if i>p+gapx: out.append((s,p)); s=i
            p=i
        out.append((s,p))
    res=[]
    for (c0,c1) in out:
        sub = m[:, c0:c1+1]
        rows = np.where(sub.sum(axis=1)>0)[0]
        res.append((x0+int(c0), x0+int(c1), y0+int(rows.min()), y0+int(rows.max())))
    return res
print('eq1a:', [(r[0],r[1],r[2],r[3]) for r in runs2d(126,176,100,310)])
print('eq1b:', [(r[0],r[1],r[2],r[3]) for r in runs2d(124,180,355,495)])
print('eq2: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(192,248,95,370)])
print('eq3: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(246,300,98,312)])
print('eq4: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(303,368,100,600)])
print('eq5: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(382,444,98,400)])
print('eq6: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(382,444,598,800)])
print('eq7: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(455,495,120,335)])
print('eq8: ', [(r[0],r[1],r[2],r[3]) for r in runs2d(455,495,558,820)])
