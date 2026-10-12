from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
a38 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg').convert('RGB')).astype(int)
def sx(fx): return (fx-17.582)/0.962329
def sy(fy): return fy/0.955556
# precise row bands via col1 gray-cell window x 216..228 (right of label, inside bar, no arrows)
print('== precise row bands (x 216..228 nonwhite runs) ==')
seg = a[:, 216:229]
nw = (seg.max(axis=2) < 243).sum(axis=1)
rr=[]; inb=False
for y in range(40, 516):
    if nw[y]>=8 and not inb: inb=True; y0=y
    elif nw[y]<8 and inb:
        if y-y0>=8: rr.append((y0,y-1))
        inb=False
for y0,y1 in rr:
    print(f'  band y {y0}..{y1} -> slide {sy(y0):.1f}..{sy(y1+1):.1f} (h={sy(y1+1)-sy(y0):.1f})')
# panel top border row
print('== panel top border ==')
for y in range(46, 56):
    nvy = sum(1 for x in range(100,880,7) if a[y,x][2]>90 and a[y,x][0]<90 and a[y,x][1]<90)
    print(f'  y={y}: navy-ish sampled={nvy}')
# containers: side borders x=141-142 and x=885-886 y-extents
print('== container side borders ==')
for x0,x1,tag in [(140,144,'left'),(884,888,'right')]:
    seg = a[:, x0:x1]
    grn = ((seg[:,:,1]>110)&(seg[:,:,0]<115)&(seg[:,:,2]<115)).sum(axis=1)
    ys = [y for y in range(40,516) if grn[y]>0]
    print(f'  {tag} green ys: {spans(ys,4) if (spans:=lambda l,g: None) else None}' if False else f'  {tag}: ', end='')
    # group
    out=[]; s=None; p=None
    for y in ys:
        if s is None: s=y; p=y
        elif y-p<=4: p=y
        else: out.append((s,p)); s=y; p=y
    if s is not None: out.append((s,p))
    print([(u,v) for u,v in out if v-u>10])
# X row green dots
print('== X row green dots ==')
grn = (a[:,:,1]>120)&(a[:,:,0]<120)&(a[:,:,2]<130)
xs = [x for x in range(600,740) if grn[486:505, x].sum()>0]
out=[]; s=None; p=None
for x in xs:
    if s is None: s=x; p=x
    elif x-p<=3: p=x
    else: out.append((s,p)); s=x; p=x
if s is not None: out.append((s,p))
print('  green dot clusters:', out, '-> slide centers', [round(sx((u+v)/2),1) for u,v in out])
ys = [y for y in range(484,506) if grn[y, 600:740].sum()>0]
print('  green dot rows:', ys)
# MHA bar right edge + white text extent
print('== MHA bar ==')
row = a[445]
nvy = [x for x in range(100,915) if row[x][2]>90 and row[x][0]<80 and row[x][1]<80]
print(f'  navy @445: {nvy[0]}..{nvy[-1]} -> slide {sx(nvy[0]):.1f}..{sx(nvy[-1]):.1f}')
seg = a[424:464, 170:880]
wh = (seg[:,:,0]>190)&(seg[:,:,1]>190)&(seg[:,:,2]>190)
cols = np.where(wh.sum(axis=0)>0)[0]
rows = [y+424 for y in range(seg.shape[0]) if wh[y].sum()>0]
print(f'  white text cols {cols.min()+170}..{cols.max()+170} rows {rows[0]}..{rows[-1]} -> slide x {sx(cols.min()+170):.1f}..{sx(cols.max()+170):.1f} y {sy(rows[0]):.1f}..{sy(rows[-1]):.1f}')
# callout box: nonwhite runs in x 55..178 (excluding panel border col 58)
print('== callout box edges ==')
seg = a[:, 62:168]
nw = (seg.max(axis=2) < 240).sum(axis=1)
rr2=[]; inb=False
for y in range(38, 120):
    if nw[y]>=60 and not inb: inb=True; y0=y
    elif nw[y]<60 and inb: rr2.append((y0,y-1)); inb=False
if inb: rr2.append((y0,119))
print('  dense pink rows (n>60):', rr2)
for y in (44, 46, 48, 108, 110, 112):
    xs = np.where((a[y,55:180].max(axis=1)<240))[0]+55
    print(f'  y={y}: nonwhite span {xs.min() if len(xs) else None}..{xs.max() if len(xs) else None}')
# 038 block-arrow ink calibration (midY arrow at col1: box slide 399.7..419.7 -> frame 382.0..401.1)
print('== 038 block arrow ink calibration ==')
bl38 = (a38[:,:,2]>a38[:,:,0]+25)&(a38[:,:,2]>110)
ys, xs = np.where(bl38[380:404, 196:216])
print(f'  038 arrow ink: y {ys.min()+380}..{ys.max()+380} (box frame 382..401) x {xs.min()+196}..{xs.max()+196}')
# top container: bottom dash row check rows 158..180
print('== top container bottom dash ==')
grn = (a[:,:,1]>110)&(a[:,:,0]<115)&(a[:,:,2]<115)
for y in range(158, 180):
    n = grn[y, 150:890].sum()
    if n>15: print(f'  y={y}: green n={n}')
