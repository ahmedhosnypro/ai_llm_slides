from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def modal(region, label, exclude_light=True):
    px = region.reshape(-1,3)
    if exclude_light:
        keep = px.sum(axis=1) < 640   # drop near-white
        px = px[keep]
    if len(px)==0: print(label,'EMPTY'); return
    q = Counter(map(tuple,(px//8*8)))
    tot = len(px)
    print(label, 'n=',tot, 'modal:', [(c,round(100*n/tot,1)) for c,n in q.most_common(5)])

R = a[:,:,0]; G = a[:,:,1]; B = a[:,:,2]
redm  = (R-G>50)&(R-B>50)&(R>120)
bluem = (B-R>40)&(B-G>30)&(B>110)

modal(a[55:82, 50:840][redm[55:82, 50:840]], 'title1-red')
modal(a[210:222, 390:580][redm[210:222, 390:580]], 'sigmoid-note-red')
modal(a[387:432, 455:500][redm[387:432, 455:500]], 'Let-red')
modal(a[460:490, 455:510][redm[460:490, 455:510]], 'then-red')
modal(a[128:168, 315:352][redm[128:168, 315:352]], 'arrow1-red')
modal(a[86:112, 70:886][bluem[86:112, 70:886]], 'title2-blue')
modal(a[253:285, 340:570][bluem[253:285, 340:570]], 'only-note-blue')
modal(a[116:122, 200:700][bluem[116:122, 200:700]], 'container-top-border')
modal(a[200:400, 71:77][bluem[200:400, 71:77]], 'container-left-border')
modal(a[200:400, 883:890][bluem[200:400, 883:890]], 'container-right-border')
modal(a[140:200, 90:300], 'tan-fill-modal')
modal(a[315:350, 95:175], 'yellow-fill-modal')
modal(a[132:158, 115:295][ (a[132:158, 115:295].sum(axis=2)<300) ], 'eq-ink')
modal(a[522:537, 200:800], 'footer-modal')

# red arrow precise bbox in tan1 (red mask, rows 125..175, x 300..380)
sub = redm[125:175, 300:380]
ys,xs = np.where(sub)
print('arrow1 bbox rows', 125+ys.min(), 125+ys.max(), 'x', 300+xs.min(), 300+xs.max(), 'n', len(ys))
# per-row extent to see the arrow shape
for y in range(125+ys.min(), 125+ys.max()+1):
    xr = np.where(redm[y, 300:380])[0]
    if len(xr): print('  y',y,'x',300+xr.min(),300+xr.max(),'n',len(xr))

# sigmoid note rows precise
sub = redm[195:250, 390:580]
ys,xs = np.where(sub)
print('sigmoid note rows', 195+ys.min(), 195+ys.max(), 'x', 390+xs.min(), 390+xs.max())
# error note rows precise
sub = bluem[248:295, 340:570]
ys,xs = np.where(sub)
print('error note rows', 248+ys.min(), 248+ys.max(), 'x', 340+xs.min(), 340+xs.max())
# underline: dark rows 279..292 in x470..570
blk2 = (a.sum(axis=2)<420)
for y in range(276, 294):
    xr = np.where(blk2[y, 340:570])[0]
    if len(xr): print('  note-low y',y,'x',340+xr.min(),340+xr.max(),'n',len(xr))

# title glyph bands using color masks
def band_of(mask, y0,y1,x0,x1):
    m = mask[y0:y1, x0:x1]
    rows = np.where(m.sum(axis=1)>0)[0]; cols = np.where(m.sum(axis=0)>0)[0]
    return (y0+rows.min(), y0+rows.max(), x0+cols.min(), x0+cols.max()) if len(rows) else None
print('title1 full band:', band_of(redm, 45,85, 40,900))
print('title1 U:', band_of(redm, 45,85, 55,76))
print('title1 first word extent (Update):', band_of(redm, 45,85, 55,160))
print('title2 full band:', band_of(bluem, 80,116, 60,900))
print('title2 G:', band_of(bluem, 80,116, 72,98))
# title2 low rows (descenders?)
for y in range(100,120):
    xr = np.where(bluem[y, 60:900])[0]
    if len(xr)>3: print('  t2 y',y,'x',60+xr.min(),60+xr.max(),'n',len(xr))
# footer rows check
blkf = (a.sum(axis=2)<200)
for y in range(515,540):
    xr = np.where(blkf[y])[0]
    print('  footer y',y,'x', (xr.min(),xr.max(),'n',len(xr)) if len(xr) else None)
