from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def vdump(x, y0, y1, label):
    print(f'--- vertical x={x} {label}')
    prev=None
    for y in range(y0, y1):
        px = tuple(int(v) for v in a[y, x])
        if prev is None or max(abs(px[i]-prev[i]) for i in range(3))>25:
            print(y, px); prev=px

vdump(200, 210, 265, 'output row box1')     # Y1 box region
vdump(300, 268, 280, 'arrow2 zone')
vdump(508, 200, 268, 'arrow3/box5 zone')

# output container dashed border: blue-ish rows/cols
blueish = (B>120)&(B-R>35)&(G<170)
cnt = blueish[:, 150:920].sum(axis=1)
print('output container blue rows 210..270:', {y:int(cnt[y]) for y in range(210,271) if cnt[y]>100})
cntc = blueish[218:265, :].sum(axis=0)
cols=[x for x in range(960) if cntc[x]>25]
print('output container blue cols:', cols)

# encoder: bar x extents at bar rows
dcore = (R>120)&(R<210)&(G<70)&(B<80)
for band,nm in (((279,297),'bar1'),((300,319),'bar2'),((351,370),'bar3')):
    ys,xs = np.where(dcore[band[0]:band[1], :])
    print(nm, 'x', xs.min(), xs.max(), 'y', ys.min()+band[0], ys.max()+band[0])
# ellipsis dots: white-ish clusters in y 320..350 OUTSIDE title x-range (title 393..608)
wht = (R>200)&(G>150)&(B>150)
sub = np.zeros_like(wht); sub[318:352, 150:392] = wht[318:352, 150:392]
lab,n = ndimage.label(sub); res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<5: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort()
print('white clusters LEFT of title (x150..392, y318..352):', len(res))
for c in res: print('   x %d..%d y %d..%d n%d' % c)
sub = np.zeros_like(wht); sub[318:352, 610:880] = wht[318:352, 610:880]
lab,n = ndimage.label(sub); res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<5: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort()
print('white clusters RIGHT of title (x610..880, y318..352):', len(res))
for c in res: print('   x %d..%d y %d..%d n%d' % c)
# Transformer Block text: white clusters ON the bars
for band,nm in (((279,297),'bar1'),((300,319),'bar2'),((351,370),'bar3')):
    sub = np.zeros_like(wht); sub[band[0]:band[1], 150:880] = wht[band[0]:band[1], 150:880]
    ys,xs = np.where(sub)
    if len(xs): print(nm, 'white text bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min()+band[0],ys.max()+band[0],len(xs)))
