from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R=a[:,:,0]; G=a[:,:,1]; B=a[:,:,2]
dk = (a.sum(axis=2)<340)   # dark ink: black text + red C00000 (sum 192) + navy 000080 (128)

def runs2d(y0,y1,x0,x1,gapx=10,minrow=0):
    m = dk[y0:y1, x0:x1]
    colproj = m.sum(axis=0)
    idx = np.where(colproj>minrow)[0]
    out=[]
    if len(idx):
        s=p=idx[0]
        for i in idx[1:]:
            if i>p+gapx:
                out.append((s,p)); s=i
            p=i
        out.append((s,p))
    res=[]
    for (c0,c1) in out:
        sub = m[:, c0:c1+1]
        rows = np.where(sub.sum(axis=1)>0)[0]
        res.append((x0+int(c0), x0+int(c1), y0+int(rows.min()), y0+int(rows.max()), int(sub.sum())))
    return res

print('== TAN1 line1 (rows 126..175) ==')
for r in runs2d(126,176,79,649): print('  x%d..%d y%d..%d n%d'%r)
print('== TAN1 line2 sigmoid (rows 195..250) ==')
for r in runs2d(195,250,79,649): print('  x%d..%d y%d..%d n%d'%r)
print('== TAN1 line3 error (rows 250..296) ==')
for r in runs2d(250,296,79,649): print('  x%d..%d y%d..%d n%d'%r)
print('== YELLOW chain (rows 300..372) ==')
for r in runs2d(300,372,79,763): print('  x%d..%d y%d..%d n%d'%r)
print('== TAN2 line1 (rows 380..440) ==')
for r in runs2d(380,440,79,843): print('  x%d..%d y%d..%d n%d'%r)
print('== TAN2 line2 (rows 455..495) ==')
for r in runs2d(455,495,79,843): print('  x%d..%d y%d..%d n%d'%r)
print('== title1 (rows 50..85) ==')
for r in runs2d(50,85,40,900,gapx=40): print('  x%d..%d y%d..%d n%d'%r)
print('== title2 (rows 85..116) ==')
for r in runs2d(85,116,40,900,gapx=40): print('  x%d..%d y%d..%d n%d'%r)
