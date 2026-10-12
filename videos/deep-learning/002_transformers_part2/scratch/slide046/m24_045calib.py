from PIL import Image
import numpy as np
a45 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def sy(fy): return fy/0.955556
def bartest(a, ylo, yhi, tag):
    seg = a[ylo:yhi, 220:380]
    g = (np.abs(seg[:,:,0]-seg[:,:,1])<=10)&(np.abs(seg[:,:,1]-seg[:,:,2])<=10)&(seg[:,:,0]>=168)&(seg[:,:,0]<=238)
    rows = np.where(g.sum(axis=1) > 100)[0]
    print(f'{tag}: gray rows {rows.min()+ylo}..{rows.max()+ylo} -> slide {sy(rows.min()+ylo):.1f}..{sy(rows.max()+ylo):.1f}')
# 045 certified bar: slide 322.3..350.6 -> frame 308.0..335.1
bartest(a45, 295, 350, '045 bar (cert build 322.3..350.6 slide = 308.0..335.1 frame)')
# 045 unit container dashes (green rows) around 310.9..389.4 -> frame 297.1..372.2
grn = (a45[:,:,1]>110)&(a45[:,:,0]<115)&(a45[:,:,2]<115)
for y in range(290, 380):
    n = grn[y, 150:890].sum()
    if n > 60: print(f'  045 dash row y={y} n={n} (container 297..372 frame)')
# 045 plus discs
seg = a45[345:375, 185:226]
dr = (seg[:,:,0]>110)&(seg[:,:,1]<70)&(seg[:,:,2]<70)
ys,xs = np.where(dr)
print(f'045 plus col1: y {ys.min()+345}..{ys.max()+345} (cert cy 369.9 slide = 353.5 frame, d 15.6pt=14.9px)')
# 045 rows via lav bands for like-for-like
def lavband(a, y0, y1, x0, x1):
    seg = a[y0:y1, x0:x1]
    lav = (np.abs(seg - np.array([0xD8,0xBF,0xD8])).max(axis=2) <= 30)
    rows = np.where(lav.sum(axis=1) > 10)[0]
    return (rows.min()+y0, rows.max()+y0) if len(rows) else None
print('045 rows lav (cert: top 175.0/17.5, mid 286.0/16.7, cont 394.8/18.0, X 502.6/17.2):')
for nm, y0,y1 in [('top',160,200),('mid',265,310),('cont',370,420),('X',475,525)]:
    b = lavband(a45, y0,y1, 185,228)
    print(f'  {nm}: frame {b} -> slide {sy(b[0]):.1f}..{sy(b[1]+1):.1f}')
print('046 rows lav (my earlier: final 65..81, postFFN 173..188, postLN 278..295, outatt 384..400, X 487..503):')
for nm, y0,y1 in [('final',55,95),('postFFN',165,200),('postLN',270,305),('outatt',375,410),('X',480,512)]:
    b = lavband(a, y0,y1, 185,228)
    print(f'  {nm}: frame {b} -> slide {sy(b[0]):.1f}..{sy(b[1]+1):.1f}')
# 046 MHA bar right edge at clean row 428
row = a[428]
nvy = [x for x in range(100,915) if row[x][2]>90 and row[x][0]<80 and row[x][1]<80]
print('046 MHA navy @428:', nvy[0], '..', nvy[-1], ' gaps:', [ (s,e) for s,e in zip(nvy, nvy[1:]) if e-s>3 ][:8])
