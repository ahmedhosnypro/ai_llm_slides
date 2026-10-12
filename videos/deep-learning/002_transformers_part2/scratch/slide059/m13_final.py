from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# C labels + arrows between border and tan bar: blue ink y 44..92
blu = (B>120)&(B-R>50)&(G<170)
sub = np.zeros_like(blu); sub[44:92, 250:750] = blu[44:92, 250:750]
lab,n = ndimage.label(sub)
res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<8: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort()
print('top blue clusters y44..92:', len(res))
for c in res: print('   x %d..%d y %d..%d n%d' % c)

# circle1 internals grid: x 420..462, y 82..122
print('circle1 grid (C=navy ring, l=lightblue, y=yellow, r=red, .=other):')
for y in range(82, 124, 2):
    row=''
    for x in range(418, 464):
        r,g,b = a[y,x]
        if b>90 and r<80 and g<80: row+='C'
        elif 120<r<190 and 150<g<205 and 180<b<230: row+='l'
        elif r>200 and g>170 and b<140: row+='y'
        elif r>150 and g<110 and b<110 and r-g>60: row+='r'
        else: row+='.'
    print(y, row)

# Y1 label color: fine strip y=240 x 178..232
print('Y1 strip y=240 x178..232:', [(x, tuple(int(v) for v in a[240,x])) for x in range(178, 233, 2)])

# fan lines rescan low threshold
drk2 = (R>120)&(R<225)&(G<100)&(B<105)
cnt = drk2[:, 300:750].sum(axis=1)
print('fan rows 115..170 (>3):', {y:int(cnt[y]) for y in range(115,171) if cnt[y]>3})

# pooled row: cell colors at y=156 (mid): classify x 385..635
print('pooled y=156:', end=' ')
seq=[]
for x in range(385, 636, 1):
    r,g,b = a[156,x]
    if r>200 and g>170 and b<150: seq.append('Y')
    elif g>170 and g-r>20 and g-b>20: seq.append('G')
    elif r>200 and 120<g<190 and 110<b<190: seq.append('P')
    elif r<190 and g<190: seq.append('#')
    else: seq.append('.')
print(''.join(seq))

# 4 arrows exact bboxes: non-gray clusters in gap bands
gray = (abs(R-231)<14)&(abs(G-233)<14)&(abs(B-229)<14)
for nm,(y0,y1) in (('arrow4',(166,179)),('arrow3',(208,221)),('arrow2',(264,276)),('arrow1',(374,387))):
    sub = np.zeros_like(gray); sub[y0:y1, 460:560] = ~gray[y0:y1, 460:560]
    ys,xs = np.where(sub)
    if len(xs): print(nm, 'ink bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))

# output container left/right dashed border cols (low threshold)
bluish = (B>110)&(B-R>30)
cntc = bluish[230:254, :].sum(axis=0)
print('output container border cols (>4):', [x for x in range(150,930) if cntc[x]>4])

# input container edges at y=400: x 52..78 and 890..910
print('input cont left y400:', [(x, tuple(int(v) for v in a[400,x])) for x in range(52,79,2)])
print('input cont right y400:', [(x, tuple(int(v) for v in a[400,x])) for x in range(890,911,2)])
# word row green border x extent (y=413 row): green-ish cols
grn = (G>120)&(G-R>20)&(G-B>10)
ys,xs = np.where(grn[411:416, :])
print('green top border row x extent:', xs.min(), xs.max())
ys,xs = np.where(grn[440:446, :])
print('green bottom border row x extent:', xs.min(), xs.max())
# orange border rows x extent
org = (R>190)&(G>130)&(G<210)&(B<190)&(R-B>40)
ys,xs = np.where(org[468:474, :])
print('orange top border x extent:', xs.min(), xs.max())
ys,xs = np.where(org[502:508, :])
print('orange bottom border x extent:', xs.min(), xs.max())
