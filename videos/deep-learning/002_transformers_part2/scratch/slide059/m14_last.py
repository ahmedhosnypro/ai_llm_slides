from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# 1) C labels: blue in y 25..62 x 400..650
blu = (B>110)&(B-R>40)&(G<180)
sub = np.zeros_like(blu); sub[25:63, 400:660] = blu[25:63, 400:660]
lab,n = ndimage.label(sub); res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<6: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort(); print('C-label candidates y25..62:', res[:12])

# 2) circles: navy ring bbox per circle window
nav = (R<90)&(G<90)&(B>85)
for nm,(x0,x1) in (('c1',(415,465)),('c2',(490,540)),('c3',(560,612))):
    sub = np.zeros_like(nav); sub[80:132, x0:x1] = nav[80:132, x0:x1]
    ys,xs = np.where(sub)
    print(nm, 'navy bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))
# yellow inside circles
yel = (R>200)&(G>160)&(B<150)
for nm,(x0,x1) in (('c1',(415,465)),('c2',(490,540)),('c3',(560,612))):
    sub = np.zeros_like(yel); sub[90:122, x0:x1] = yel[90:122, x0:x1]
    ys,xs = np.where(sub)
    if len(xs): print(nm, 'yellow-in-circle x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))
# circle fill color sample (inside ring, away from text): c1 (445,107), (435,105)
print('c1 fill samples:', [tuple(int(v) for v in a[y,x]) for x,y in ((445,107),(435,106),(447,105))])

# 3) output row: dark-red glyphs y 230..254 (Y labels?)
dred = (R>110)&(R<200)&(G<90)&(B<95)&(R-G>45)
sub = np.zeros_like(dred); sub[230:255, 165:900] = dred[230:255, 165:900]
lab,n = ndimage.label(sub); res=[]
for i in range(1,n+1):
    ys,xs = np.where(lab==i)
    if len(xs)<6: continue
    res.append((int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),len(xs)))
res.sort(); print('output row dark-red clusters:', len(res))
for c in res: print('   x %d..%d y %d..%d n%d cx %.1f' % (c[0],c[1],c[2],c[3],c[4],(c[0]+c[1])/2))

# output box1 2D grid x 178..236 y 226..258
print('output box1 grid (n=navy,d=darkred,y=yellow,g=green,p=pink,l=lblue,W=white):')
for y in range(226, 259, 1):
    row=''
    for x in range(178, 237):
        r,g,b = a[y,x]
        if r<90 and g<90 and b>85: row+='n'
        elif r>110 and r<200 and g<90 and b<95 and r-g>45: row+='d'
        elif r>230 and g>230 and b<190: row+='y'
        elif g>170 and g-r>15 and g-b>15: row+='g'
        elif r>230 and 150<g<215 and 150<b<220 and r-g>25: row+='p'
        elif 195<r<235 and 215<g<245 and b>235: row+='l'
        elif r>240 and g>240 and b>235: row+='W'
        else: row+='.'
    print(y, row)

# 4) fan lines low threshold
fan = (R>165)&(R-G>12)&(R-B>12)&(G<225)
cnt = fan[:, 340:700].sum(axis=1)
print('fan rows 126..152 (>3):', {y:int(cnt[y]) for y in range(126,153) if cnt[y]>3})

# 5) arrows: lavender fill mask per band
lav = (B>235)&(B-R>12)&(R>190)
for nm,(y0,y1) in (('arrow4',(166,179)),('arrow3',(208,222)),('arrow2',(264,277)),('arrow1',(373,387))):
    sub = np.zeros_like(lav); sub[y0:y1, 470:560] = lav[y0:y1, 470:560]
    ys,xs = np.where(sub)
    if len(xs): print(nm, 'fill bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))
    sub2 = np.zeros_like(lav); sub2[y0:y1, 470:560] = (R[y0:y1,470:560]<100)&(B[y0:y1,470:560]>90)
    ys,xs = np.where(sub2)
    if len(xs): print(nm, '  outline bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))

# 6) input container edges at y=455
print('left y455:', [(x, tuple(int(v) for v in a[455,x])) for x in range(54,80,2)])
print('right y455:', [(x, tuple(int(v) for v in a[455,x])) for x in range(886,906,2)])

# 7) green/orange border extents (x-limited)
grn = (G>120)&(G-R>18)&(G-B>8)
ys,xs = np.where(grn[411:416, 240:920]); print('green top border x (x>240):', xs.min()+240, xs.max()+240)
ys,xs = np.where(grn[440:446, 240:920]); print('green bottom border x:', xs.min()+240, xs.max()+240)
org = (R>195)&(G>140)&(G<215)&(B<200)&(R-B>35)
ys,xs = np.where(org[468:474, 100:880]); print('orange top border x:', xs.min()+100, xs.max()+100)
ys,xs = np.where(org[502:508, 100:880]); print('orange bottom border x:', xs.min()+100, xs.max()+100)

# 8) pooled cell core colors (3x3 median at cell centers)
cells = [395, 407, 419, 431, 443, 455, 467, 479, 491, 503, 515, 527, 539, 551, 563, 575, 587, 599, 611, 623]
meds = []
for cx in cells:
    block = a[153:161, cx-2:cx+3].reshape(-1,3)
    meds.append(tuple(int(v) for v in np.median(block, axis=0)))
print('pooled cell medians:', list(zip(cells, meds)))
