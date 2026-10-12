from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# 1) ellipsis columns: dark-red px per column in y 318..352
drk = (R>110)&(R<210)&(G<80)&(B<90)
cnt = drk[318:352, 150:880].sum(axis=0)
cols = [150+i for i in range(730) if cnt[i] >= 12]
print('ellipsis dark cols y318..352:', cols)
# vertical continuity at first few
for x in cols[:1] + cols[-1:]:
    print(f'  vertical x={x}:', [(y, tuple(int(v) for v in a[y,x])) for y in range(316, 356, 2)])

# 2) bar text: pale px on bar rows
pale = (R>150)&(G>90)&(B>90)
for band,nm in (((281,295),'bar1'),((302,316),'bar2'),((353,368),'bar3')):
    sub = np.zeros_like(pale); sub[band[0]:band[1], 165:850] = pale[band[0]:band[1], 165:850]
    ys,xs = np.where(sub)
    if len(xs): print(nm, 'pale-text bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))

# 3) output row navy labels: clusters y 228..258 x 165..620
nav = (R<110)&(G<110)&(B>60)&(B<200)&(B-R>30)
sub = np.zeros_like(nav); sub[228:258, 165:620] = nav[228:258, 165:620]
lab,n = ndimage.label(sub)
res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<8: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort()
print('output row navy clusters:', len(res))
for c in res: print('   x %d..%d y %d..%d n%d cx %.1f' % (c[0],c[1],c[2],c[3],c[4],(c[0]+c[1])/2))

# 4) GAP box: dark border rows/cols
dk = (R<130)&(G<130)&(B<130)
cnt = dk[:, 165:880].sum(axis=1)
print('GAP dark rows 175..215:', {y:int(cnt[y]) for y in range(175,216) if cnt[y]>80})
cntc = dk[185:205, :].sum(axis=0)
print('GAP dark cols:', [x for x in range(960) if cntc[x]>12])
# GAP text bbox
ys,xs = np.where(dk[186:205, 170:880])
print('GAP text bbox x %d..%d y %d..%d' % (xs.min()+170, xs.max()+170, ys.min()+186, ys.max()+186))

# 5) softmax band: tan bar bbox tight
tan = (abs(R-238)<12)&(abs(G-199)<12)&(abs(B-162)<14)
ys,xs = np.where(tan[80:125, :])
print('tan bar bbox x %d..%d y %d..%d' % (xs.min(), xs.max(), ys.min()+80, ys.max()+80))
# Softmax Layer text: orange text on tan at left — find dark-orange clusters x 175..420 y 92..112
org = (R>180)&(R<245)&(G>90)&(G<170)&(B<110)
ys,xs = np.where(org[85:118, 170:430])
if len(xs): print('SoftmaxLayer text bbox x %d..%d y %d..%d n%d' % (xs.min()+170,xs.max()+170,ys.min()+85,ys.max()+85,len(xs)))
# circles: navy ring + fill? sample circle1 center and ring
print('circle1 samples:', [(dx, tuple(int(v) for v in a[102, 439+dx])) for dx in (-19,-17,-14,-10,0,10,14,17,19)])
print('circle1 vertical:', [(dy, tuple(int(v) for v in a[102+dy, 439])) for dy in (-19,-17,-14,-10,0,10,14,17,19)])
# red base node: red px below circle y 115..128 x 420..460
red = (R>140)&(G<110)&(B<110)&(R-G>50)
ys,xs = np.where(red[113:130, 415:465])
if len(xs): print('red base node c1 bbox x %d..%d y %d..%d n%d' % (xs.min()+415,xs.max()+415,ys.min()+113,ys.max()+113,len(xs)))

# 6) fan lines: dark-red thin lines between y 116..147, count rows
drk2 = (R>120)&(R<220)&(G<90)&(B<95)
cnt = drk2[:, 300:750].sum(axis=1)
print('fan-line rows 114..150:', {y:int(cnt[y]) for y in range(114,151) if cnt[y]>10})

# 7) C labels + Output Classes + tiny up arrows: blue text y 15..60
blu = (B>120)&(B-R>60)&(G<160)
ys,xs = np.where(blu[10:62, 200:750])
print('top blue ink bbox x %d..%d y %d..%d n%d' % (xs.min()+200,xs.max()+200,ys.min()+10,ys.max()+10,len(xs)))
sub = np.zeros_like(blu); sub[10:62, 200:750] = blu[10:62, 200:750]
lab,n = ndimage.label(sub)
res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<10: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort()
for c in res: print('   topblue x %d..%d y %d..%d n%d' % c)
