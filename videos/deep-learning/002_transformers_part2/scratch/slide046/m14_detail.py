from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def sx(fx): return (fx-17.582)/0.962329
def sy(fy): return fy/0.955556
def runs1(arr, thresh, minlen=2):
    out=[]; s=None
    for i in range(len(arr)):
        if arr[i]>thresh and s is None: s=i
        elif arr[i]<=thresh and s is not None:
            if i-s>=minlen: out.append((s,i-1))
            s=None
    if s is not None: out.append((s,len(arr)-1))
    return out

# 1. LN bars: neutral gray per-row count in x 250..380 AND x 620..750 (avoid center text)
print('== LN bars ==')
for name, ylo, yhi in [('top',95,140),('bottom',305,350)]:
    for xlo,xhi,tag in [(250,380,'L'),(620,750,'R')]:
        seg = a[ylo:yhi, xlo:xhi]
        g = (np.abs(seg[:,:,0]-seg[:,:,1])<=10)&(np.abs(seg[:,:,1]-seg[:,:,2])<=10)&(seg[:,:,0]>=168)&(seg[:,:,0]<=238)
        rr = runs1(g.sum(axis=1), 60)
        print(f'  {name} {tag}: rows {[(r[0]+ylo, r[1]+ylo) for r in rr]}')
# bar x extent at its center row
for name, ymid in [('top',115),('bottom',326)]:
    row = a[ymid]
    g = (np.abs(row[:,0]-row[:,1])<=10)&(np.abs(row[:,1]-row[:,2])<=10)&(row[:,0]>=168)&(row[:,0]<=238)
    rr = runs1(g, 30, minlen=8)
    print(f'  {name} bar x-runs @y={ymid}: {[(r[0],r[1]) for r in rr if 100<r[0]<910]} -> slide {[(round(sx(r[0]),1), round(sx(r[1]),1)) for r in rr if 100<r[0]<910]}')

# 2. containers: green dash border rows+cols
print('== containers ==')
for name, ylo, yhi in [('top',88,175),('bottom',295,388)]:
    seg = a[ylo:yhi, 140:900]
    gr = (seg[:,:,1]>115)&(seg[:,:,0]<120)&(seg[:,:,2]<120)
    rows = runs1(gr.sum(axis=1), 25)
    cols = runs1(gr.sum(axis=0), 6)
    print(f'  {name}: dash rows {[(r[0]+ylo,r[1]+ylo) for r in rows]}, dash col-runs {[(c[0]+140,c[1]+140) for c in cols][:12]}')

# 3. plus discs per column (top unit y 138..160, bottom 348..372)
print('== plus discs ==')
for name, ylo, yhi in [('top',138,160),('bottom',348,372)]:
    for i, fcx in enumerate([205.1,277.7,350.8,424.5,498.6,570.1,760.3,834.4]):
        seg = a[ylo:yhi, int(fcx-14):int(fcx+15)]
        dr = (seg[:,:,0]>110)&(seg[:,:,1]<70)&(seg[:,:,2]<70)
        ys,xs = np.where(dr)
        if len(ys)>6:
            print(f'  {name} col{i+1}: y {ys.min()+ylo}..{ys.max()+ylo} (d={ys.max()-ys.min()+1}px={round((ys.max()-ys.min()+1)/0.955556,1)}pt) cy_slide={round(sy((ys.min()+ys.max())/2+ylo),1)} fill={tuple(a[(ys.min()+ys.max())//2+ylo, int(fcx)+4])}')

# 4. thin arrows: colors in gaps
print('== thin arrows in gaps (count per gap band, x 195..860) ==')
gaps = [('red top: finalrow<-bar', 82, 102), ('green top: plus->bar', 128, 141), ('navy top: row->plus', 157, 172),
        ('red bottom: postLN<-bar', 296, 313), ('green bottom: plus->bar', 339, 352), ('navy bottom: row->plus', 367, 383)]
for gname, y0, y1 in gaps:
    seg = a[y0:y1, 190:860]
    red = ((seg[:,:,0]>130)&(seg[:,:,1]<80)&(seg[:,:,2]<80)).sum()
    grn = ((seg[:,:,1]>110)&(seg[:,:,0]<110)&(seg[:,:,2]<110)).sum()
    nvy = ((seg[:,:,2]>90)&(seg[:,:,0]<80)&(seg[:,:,1]<80)).sum()
    print(f'  {gname}: red={red} green={grn} navy={nvy}')

# 5. block arrows in 4 gaps (wide ink?)
print('== block arrows ==')
for gname, y0, y1 in [('X->MHA', 469, 486), ('MHA->outatt', 401, 418), ('postLN->FFN', 265, 277), ('FFN->postFFN', 189, 205)]:
    seg = a[y0:y1, 190:860]
    blue = ((seg[:,:,2]>110)&(seg[:,:,0]<110)&(seg[:,:,1]<110))
    colcounts = blue.sum(axis=0)
    wide = runs1(colcounts, 3, minlen=5)
    print(f'  {gname}: blue-ink col-runs n={len(wide)} widths={[b-a1+1 for a1,b in wide][:12]}')

# 6. orange curves: per-column presence
print('== orange curves ==')
for uname, y0, y1 in [('top-unit', 150, 300), ('bottom-unit', 360, 510)]:
    seg = a[y0:y1]
    oran = (np.abs(seg[:,:,0]-0xE8)<60)&(np.abs(seg[:,:,1]-0xA0)<60)&(seg[:,:,2]<110)
    colcounts = oran.sum(axis=0)
    rr = runs1(colcounts, 4, minlen=3)
    print(f'  {uname}: orange col-runs {[(r[0],r[1]) for r in rr][:20]}')

# 7. callout bbox (top-left)
print('== callout ==')
seg = a[40:115, 55:175]
pk = (np.abs(seg - np.array([0xFF,0xCC,0xCC])).max(axis=2) <= 25)
ys,xs = np.where(pk)
print(f'  pink bbox frame x {xs.min()+55}..{xs.max()+55} y {ys.min()+40}..{ys.max()+40} -> slide x {round(sx(xs.min()+55),1)}..{round(sx(xs.max()+55),1)} y {round(sy(ys.min()+40),1)}..{round(sy(ys.max()+40),1)}')
rd = (seg[:,:,0]>130)&(seg[:,:,1]<80)&(seg[:,:,2]<80)
rr = runs1(rd.sum(axis=1), 3)
print(f'  red ink rows (text/border): {[(r[0]+40,r[1]+40) for r in rr]}')

# 8. annotations left column (x 60..168): colored ink bands
print('== annotations ==')
seg = a[190:510, 60:168]
for cname, test in [('blue', lambda s:(s[:,:,2]>110)&(s[:,:,0]<80)&(s[:,:,1]<80)),
                    ('orange', lambda s:(np.abs(s[:,:,0]-0xE8)<55)&(np.abs(s[:,:,1]-0xA0)<55)&(s[:,:,2]<100)),
                    ('red', lambda s:(s[:,:,0]>130)&(s[:,:,1]<80)&(s[:,:,2]<80))]:
    rr = runs1(test(seg).sum(axis=1), 2, minlen=3)
    print(f'  {cname} ink rows: {[(r[0]+190, r[1]+190) for r in rr]} -> slide {[(round(sy(r[0]+190),1), round(sy(r[1]+190),1)) for r in rr]}')

# 9. caption region (below X row): y 503..516
print('== caption ==')
seg = a[503:516, 200:640]
# classify column colors
for y in range(503, 516):
    row = a[y]
    pk = sum(1 for x in range(200,640) if abs(row[x][0]-0xFF)<30 and abs(row[x][1]-0xB6)<45 and abs(row[x][2]-0xC1)<45)
    dk = sum(1 for x in range(200,640) if row[x][0]<160 and row[x][1]<100)
    yl = sum(1 for x in range(200,640) if row[x][0]>200 and row[x][1]>200 and row[x][2]<120)
    print(f'  y={y}: pink={pk} darktext={dk} yellow={yl}')
