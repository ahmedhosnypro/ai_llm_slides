from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def sx(fx): return (fx-17.582)/0.962329
def sy(fy): return fy/0.955556
print('== caption pink band + navy edges ==')
for y in range(504, 517):
    pk = [x for x in range(200, 700) if abs(a[y,x][0]-255)<40 and abs(a[y,x][1]-185)<55 and abs(a[y,x][2]-195)<55]
    dk = [x for x in range(200, 700) if a[y,x][0]<175 and a[y,x][1]<110 and a[y,x][2]<130]
    print(f'  y={y}: pink n={len(pk)} span={(min(pk),max(pk)) if pk else None} | dark n={len(dk)} span={(min(dk),max(dk)) if dk else None}')
print('  navy edge cols at y=510:', [x for x in range(200,700) if a[510,x][2]>100 and a[510,x][0]<80 and a[510,x][1]<80])
print()
print('== MHA bar text (white ink inside bar y 425..465) ==')
seg = a[420:470, 160:900]
wh = (seg[:,:,0]>200)&(seg[:,:,1]>200)&(seg[:,:,2]>200)
rows = [y+420 for y in range(seg.shape[0]) if wh[y].sum()>10]
cols = np.where(wh.sum(axis=0)>2)[0]
print(f'  white text rows {rows[0]}..{rows[-1]} cols {cols.min()+160}..{cols.max()+160} -> slide x {sx(cols.min()+160):.1f}..{sx(cols.max()+160):.1f} y {sy(rows[0]):.1f}..{sy(rows[-1]):.1f}')
print()
print('== FFN box title (blue ink y 212..232) ==')
seg = a[210:234, 200:880]
bl = (seg[:,:,2]>110)&(seg[:,:,0]<90)&(seg[:,:,1]<90)
rows = [y+210 for y in range(seg.shape[0]) if bl[y].sum()>5]
cols = np.where(bl.sum(axis=0)>1)[0]
print(f'  blue text rows {rows[0]}..{rows[-1]} cols {cols.min()+200}..{cols.max()+200} -> slide x {sx(cols.min()+200):.1f}..{sx(cols.max()+200):.1f} y {sy(rows[0]):.1f}..{sy(rows[-1]):.1f}')
print()
print('== FFN icons: census in box y 232..262 ==')
seg = a[230:264, 165:895]
for cname, test in [('green dots', lambda s:(s[:,:,1]>110)&(s[:,:,0]<110)&(s[:,:,2]<110)),
                    ('magenta', lambda s:(s[:,:,0]>150)&(s[:,:,2]>150)&(s[:,:,1]<120)&(abs(s[:,:,0]-s[:,:,2])<80)),
                    ('tile cream FFE699', lambda s:(np.abs(s-np.array([0xFF,0xE6,0x99])).max(axis=2)<=22)),
                    ('tile border dred', lambda s:(s[:,:,0]>120)&(s[:,:,1]<80)&(s[:,:,2]<80)),
                    ('RELU red', lambda s:(s[:,:,0]>150)&(s[:,:,1]<90)&(s[:,:,2]<90))]:
    m = test(seg)
    rr = [y+230 for y in range(seg.shape[0]) if m[y].sum()>8]
    cc = np.where(m.sum(axis=0)>2)[0]
    print(f'  {cname}: rows {rr[:3]}..{rr[-3:] if rr else []} n={int(m.sum())} cols {(cc.min()+165, cc.max()+165) if len(cc) else None}')
print('  green dot x-clusters @row-band 236..240:', end=' ')
grn = (a[235:241,:,1]>110)&(a[235:241,:,0]<110)&(a[235:241,:,2]<110)
cols = np.where(grn.sum(axis=0)>0)[0]
groups=[]
for c in cols:
    if groups and c-groups[-1][-1]<=2: groups[-1].append(c)
    else: groups.append([c])
print([(g[0],g[-1]) for g in groups])
print()
print('== LN bar text ink (dark px inside top bar y 106..130) ==')
seg = a[105:131, 300:800]
dk = (seg.max(axis=2)<150)
rows = [y+105 for y in range(seg.shape[0]) if dk[y].sum()>5]
cols = np.where(dk.sum(axis=0)>1)[0]
print(f'  dark text rows {rows[0]}..{rows[-1]} cols {cols.min()+300}..{cols.max()+300} -> slide x {sx(cols.min()+300):.1f}..{sx(cols.max()+300):.1f}')
# red 'Layer' vs black 'Normalization' split: red pixels
red = (seg[:,:,0]>130)&(seg[:,:,1]<80)&(seg[:,:,2]<80)
rc = np.where(red.sum(axis=0)>0)[0]
print(f'  red-part cols {rc.min()+300}..{rc.max()+300} -> slide {sx(rc.min()+300):.1f}..{sx(rc.max()+300):.1f}')
print()
print('== annotations exact (x 60..170) ==')
for cname, test in [('blue', lambda s:(s[:,:,2]>110)&(s[:,:,0]<80)&(s[:,:,1]<80)),
                    ('orange', lambda s:(np.abs(s[:,:,0]-0xE8)<55)&(np.abs(s[:,:,1]-0xA0)<55)&(s[:,:,2]<100)),
                    ('red', lambda s:(s[:,:,0]>130)&(s[:,:,1]<80)&(s[:,:,2]<80))]:
    m = test(a[190:510, 60:170])
    for y in range(m.shape[0]):
        pass
    rr=[]
    inb=False
    for y in range(m.shape[0]):
        c = m[y].sum()
        if c>=2 and not inb: inb=True; y0=y
        elif c<2 and inb: inb=False; rr.append((y0+190, y-1+190))
    for r in rr:
        xs = np.where(m[r[0]-190:r[1]-190+1].sum(axis=0)>0)[0]
        print(f'  {cname} band y {r[0]}..{r[1]} x {xs.min()+60}..{xs.max()+60} -> slide y {sy(r[0]):.1f}..{sy(r[1]):.1f} x {sx(xs.min()+60):.1f}..{sx(xs.max()+60):.1f}')
