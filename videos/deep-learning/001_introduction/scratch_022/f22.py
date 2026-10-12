from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3
# circle1 fill samples away from glyph
for p in [(425,433),(440,410),(430,431),(447,421),(418,421)]:
    x,y=p; print(f'circle1 ({x},{y}):', tuple(im[y,x]))
# circle1 bbox: non-bg in x408..455 y398..445
mask = (np.abs(im[:,:,0]-252)>18)|(np.abs(im[:,:,1]-252)>18)|(np.abs(im[:,:,2]-252)>18)
sub = mask[398:446, 405:458]
ys,xs = np.where(sub)
print('circle1-ish bbox: x', 405+xs.min(),'..',405+xs.max(),' y',398+ys.min(),'..',398+ys.max())
sub = mask[398:446, 462:516]
ys,xs = np.where(sub)
print('circle2-ish bbox: x', 462+xs.min(),'..',462+xs.max(),' y',398+ys.min(),'..',398+ys.max())
# callout edge runs
print('callout top edge y398-402 at x700:', [tuple(im[y,700]) for y in range(396,404)])
print('callout left edge x626-632 at y420:', [tuple(im[420,x]) for x in range(624,632)])
# decision eq: scan x405..470 y288..300 clusters
row = []
for x in range(400,470):
    colmin = lum[286:302, x].min()
    row.append((x, round(colmin)))
print('decision eq min-lum per col x400..469:', row)
# cases: glyph clusters per line
for (y0,y1,lab) in [(266,284,'case1'),(288,306,'case2'),(310,328,'case3')]:
    cols=[]
    for x in range(548,748):
        if lum[y0:y1, x].min() < 190: cols.append(x)
    # group
    out=[]
    for x in cols:
        if out and x-out[-1][-1]<=3: out[-1].append(x)
        else: out.append([x])
    print(lab, 'col clusters:', [(o[0],o[-1]) for o in out])
# step glyph stroke colors
print('step top bar (500,413):', tuple(im[413,500]), ' vert (488,422):', tuple(im[422,488]), ' bot bar (485,429):', tuple(im[429,485]))
# title: cap height via column profile of a stem, e.g. 'V' at x228-250
sub = (lum[46:95, 228:720] < 150)
rows = np.where(sub.any(axis=1))[0]
print('title ink rows y:', 46+rows.min(), '..', 46+rows.max())
cols = np.where(sub.any(axis=0))[0]
print('title ink cols x:', 228+cols.min(), '..', 228+cols.max())
# per-letter gaps: column occupancy
occ = sub.sum(axis=0)
gaps=[]; s=None
for i,v in enumerate(occ):
    if v==0 and s is None: s=i
    elif v>0 and s is not None:
        if i-s>=4: gaps.append((228+s, 228+i-1))
        s=None
print('title word gaps (>=4px):', gaps)
