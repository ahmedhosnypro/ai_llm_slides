from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def band(mask, axis, min_count):
    rows = np.where(mask.sum(axis=axis) > min_count)[0]
    out=[]
    if len(rows):
        s=rows[0]; p=rows[0]
        for r in rows[1:]:
            if r>p+2: out.append((int(s),int(p))); s=r
            p=r
        out.append((int(s),int(p)))
    return out

# Gray panel check: E9E9E7 ~ (233,233,231)
gray = (np.abs(a[:,:,0]-233)<10)&(np.abs(a[:,:,1]-233)<10)&(np.abs(a[:,:,2]-231)<10)
print('gray-panel px count:', gray.sum())
if gray.sum()>1000:
    ys,xs = np.where(gray)
    print('gray extent x', xs.min(), xs.max(), 'y', ys.min(), ys.max())

# Tan fill mask (D6CFC5 area): R 195..225, G 188..218, B 178..208
tan = (a[:,:,0]>190)&(a[:,:,0]<235)&(a[:,:,1]>180)&(a[:,:,1]<225)&(a[:,:,2]>170)&(a[:,:,2]<215)&(a[:,:,0]-a[:,:,2]>8)
print('tan count', tan.sum())
tb = band(tan,1,300)
print('tan row bands:', tb)
for (s,e) in tb:
    sub = tan[s:e+1]
    xs = np.where(sub.sum(axis=0)> (e-s)//2 )[0]
    print('  tan band rows',s,e,'x', xs.min(), xs.max())

# Yellow fill (FFFFCC): R>235 G>235 B 180..220
yel = (a[:,:,0]>232)&(a[:,:,1]>232)&(a[:,:,2]>170)&(a[:,:,2]<225)
print('yellow count', yel.sum())
yb = band(yel,1,200)
print('yellow row bands:', yb)
for (s,e) in yb:
    sub = yel[s:e+1]
    xs = np.where(sub.sum(axis=0)> (e-s)//2)[0]
    print('  yellow band rows',s,e,'x', xs.min(), xs.max())

# Black ink bands (footer bar + text)
blk = (a[:,:,0]<70)&(a[:,:,1]<70)&(a[:,:,2]<70)
bb = band(blk,1,150)
print('black row bands (>150):', bb)
for (s,e) in bb:
    sub = blk[s:e+1]
    xs = np.where(sub.sum(axis=0)> (e-s)//2)[0]
    if len(xs): print('  black band rows',s,e,'x', xs.min(), xs.max(), 'density', sub.sum())
