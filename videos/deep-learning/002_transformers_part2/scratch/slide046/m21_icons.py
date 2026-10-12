from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
a45 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
def sx(fx): return (fx-17.582)/0.962329
def sy(fy): return fy/0.955556
def spans(xs, gap=4):
    if not len(xs): return []
    out=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>gap: out.append((s,p)); s=x
        p=x
    out.append((s,p)); return out

# 1. RELU tags: red-ish ink anywhere in FFN box y 225..268
print('== RELU tags (red ink y 222..268) ==')
red = (a[:,:,0]>120)&(a[:,:,1]<100)&(a[:,:,2]<100)
band = red[222:269, 165:895]
rr = [y+222 for y in range(band.shape[0]) if band[y].sum()>3]
print('  red rows:', spans(rr, 2))
for y in (rr[:1] + rr[-1:]):
    xs = np.where(red[y, 165:895])[0] + 165
    print(f'  y={y}: red x-spans {spans(list(xs))[:12]}')
# compare 045 RELU rows
red45 = (a45[:,:,0]>120)&(a45[:,:,1]<100)&(a45[:,:,2]<100)
band45 = red45[225:250, 165:895]
rr45 = [y+225 for y in range(band45.shape[0]) if band45[y].sum()>3]
print('  045 RELU red rows:', spans(rr45,2), '(045 tile relu capTop 238.6 -> frame 228.0)')

# 2. magenta shapes: per-column cluster extents
print('== magenta clusters ==')
mag = (a[:,:,0]>140)&(a[:,:,2]>140)&(a[:,:,1]<130)
for cx in (205, 277, 760, 834):
    ys, xs = np.where(mag[230:264, cx-40:cx+40])
    if len(ys):
        print(f'  col@{cx}: magenta y {ys.min()+230}..{ys.max()+230}; x-spans {spans(sorted(set(xs+cx-40)))[:10]}')

# 3. tile interior census col1 (x 172..248, y 231..262)
print('== tile interior col1 histogram ==')
crop = a[231:262, 172:248].reshape(-1,3)
from collections import Counter
cnt = Counter((tuple((p//24*24).tolist())) for p in crop)
for c, n in cnt.most_common(8): print('   ', c, n)
# 045 tile for comparison
crop45 = a45[224:255, 172:248].reshape(-1,3)
cnt45 = Counter((tuple((p//24*24).tolist())) for p in crop45)
print('  045 tile col1 histogram:', cnt45.most_common(5))

# 4. bar texts
print('== top bar text: dark ink rows/cols in x 330..700, y 104..127 ==')
seg = a[104:128, 330:700]
dk = (seg.max(axis=2)<150)
rows = [y+104 for y in range(seg.shape[0]) if dk[y].sum()>3]
cols = np.where(dk.sum(axis=0)>0)[0]
print(f'  rows {spans(rows,2)} cols {cols.min()+330}..{cols.max()+330} -> slide {sx(cols.min()+330):.1f}..{sx(cols.max()+330):.1f}')
redc = np.where(((seg[:,:,0]>120)&(seg[:,:,1]<90)&(seg[:,:,2]<90)).sum(axis=0)>0)[0]
print(f'  red-part cols {redc.min()+330}..{redc.max()+330} -> slide {sx(redc.min()+330):.1f}..{sx(redc.max()+330):.1f}')
print('== bottom bar text ==')
seg = a[315:338, 330:700]
dk = (seg.max(axis=2)<150)
rows = [y+315 for y in range(seg.shape[0]) if dk[y].sum()>3]
cols = np.where(dk.sum(axis=0)>0)[0]
print(f'  rows {spans(rows,2)} cols {cols.min()+330}..{cols.max()+330} -> slide {sx(cols.min()+330):.1f}..{sx(cols.max()+330):.1f}')

# 5. MHA bar x extent at y=440
row = a[440]
nvy = [x for x in range(100, 910) if row[x][2]>90 and row[x][0]<80 and row[x][1]<80]
sp = spans(nvy, 6)
print('== MHA bar x-spans @y=440:', sp[:4], '-> slide', [(round(sx(s1),1), round(sx(e1),1)) for s1,e1 in sp[:4]])

# 6. callout: pink fill rows + red text/border
print('== callout ==')
pk = (np.abs(a - np.array([0xFF,0xCC,0xCC])).max(axis=2) <= 20)
for y in range(40, 118, 2):
    xs = np.where(pk[y, 40:220])[0]
    if len(xs)>10: print(f'  y={y}: pink x {xs.min()+40}..{xs.max()+40} n={len(xs)}')
rd = (a[:,:,0]>130)&(a[:,:,1]<85)&(a[:,:,2]<85)
for y in range(56, 108):
    xs = np.where(rd[y, 40:220])[0]
    if len(xs)>2: print(f'  red y={y}: x-spans {spans(list(xs+40),3)[:8]}')

# 7. FFN-gap arrow ink (col1): blue-ish (incl light) extents
print('== FFN-gap arrows col1 ==')
bluish = (a[:,:,2]>a[:,:,0]+25)&(a[:,:,2]>110)
for gname, y0, y1 in [('FFN->postFFN', 188, 208), ('postLN->FFN', 262, 280)]:
    ys, xs = np.where(bluish[y0:y1, 196:216])
    if len(ys): print(f'  {gname}: ink y {ys.min()+y0}..{ys.max()+y0} x {xs.min()+196}..{xs.max()+196} -> slide y {sy(ys.min()+y0):.1f}..{sy(ys.max()+y0):.1f}')
for gname, y0, y1 in [('MHA->outatt', 398, 419), ('X->MHA', 468, 487)]:
    ys, xs = np.where(bluish[y0:y1, 196:216])
    if len(ys): print(f'  {gname}: ink y {ys.min()+y0}..{ys.max()+y0} x {xs.min()+196}..{xs.max()+196} -> slide y {sy(ys.min()+y0):.1f}..{sy(ys.max()+y0):.1f}')

# 8. ellipsis dots per row (x 620..715)
print('== ellipsis dots ==')
for rname, y0, y1 in [('final',64,82),('postFFN',172,190),('postLN',277,296),('outatt',383,401),('X',486,504)]:
    seg = a[y0:y1, 615:720]
    dk = (seg.max(axis=2)<170)
    cols = np.where(dk.sum(axis=0)>0)[0]
    print(f'  {rname}: dot x-spans {spans(list(cols+615),3)}')
