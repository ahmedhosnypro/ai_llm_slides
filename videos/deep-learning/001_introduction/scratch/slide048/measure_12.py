from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)

print('== label box border core colors ==')
for x,y in [(300,156),(300,157),(250,156),(300,181),(243,168),(378,168),(300,279),(300,304),(243,291),(477,291)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== label text color histogram (NN box y164..174 x251..365, lum<150) ==')
lum = 0.299*R+0.587*G+0.114*B
m = (lum<150)[164:175, 251:366]
ys,xs = np.nonzero(m)
px = a[164:175, 251:366][m]
print('  darkest 8:', [tuple(p) for p in px[np.argsort(lum[164:175,251:366][m])[:8]]])
print('  mean:', px.mean(axis=0).round(1))
m2 = (lum<150)[286:297, 249:472]
px2 = a[286:297, 249:472][m2]
print('CNN text darkest 8:', [tuple(p) for p in px2[np.argsort(lum[286:297,249:472][m2])[:8]]], 'mean:', px2.mean(axis=0).round(1), 'n=',len(px2))
print('== arrows color probes ==')
for x,y in [(444,221),(446,221),(492,221),(540,221),(588,221),(634,221),(681,221),(218,369),(730,368),(290,370),(460,370),(536,370),(612,370),(380,222)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== NN gap arrows red? ==')
m = red[215:228, 480:700]
ys,xs = np.nonzero(m)
print('  red px in NN gaps y215..228 x480..700:', len(xs), 'x:', sorted(set((xs+480).tolist()))[:20])
print('== block text probes (NN block1 interior) ==')
for y in range(195,255,5):
    row=[]
    for x in [455,458,461,464,467,470,473]:
        row.append(f'{x}:{tuple(a[y,x])}')
    print(f'  y{y}: '+' '.join(row))
print('== block 3-D side probes ==')
for x,y in [(474,220),(475,220),(473,200),(521,220),(569,220),(710,220),(472,230)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== slab front color + 3D side ==')
for x,y in [(300,370),(305,370),(283,340),(660,370),(700,370),(758,370),(806,370),(851,370)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
print('== slab1 white text (interior only x255..280 y330..410) ==')
wt = (R>225)&(G>225)&(B>215)
m = wt[330:410, 255:281]
ys,xs = np.nonzero(m)
if len(xs): print(f'  slab1 text: x {255+xs.min()}..{255+xs.max()} y {330+ys.min()}..{330+ys.max()} n={len(xs)}')
else: print('  EMPTY')
m = wt[195:250, 455:472]
ys,xs = np.nonzero(m)
if len(xs): print(f'  NNblock1 text: x {455+xs.min()}..{455+xs.max()} y {195+ys.min()}..{195+ys.max()} n={len(xs)}')
else: print('  NNblock1 text EMPTY (no white)')
print('== title cap-height measure: column scans ==')
for x0,x1,name in [(130,146,'S'),(260,276,'N2'),(390,404,'k?')]:
    m = red[55:130, x0:x1]
    ys,xs = np.nonzero(m)
    if len(xs): print(f'  {name} x{x0}..{x1}: y {55+ys.min()}..{55+ys.max()}')
print('== title core color ==')
m = red[63:124, 130:834]
px = a[63:124, 130:834][m]
print('  mean:', px.mean(axis=0).round(1), 'n=', len(px))
print('== divider dash pattern (row 269 strict-red x-clusters) ==')
xs = np.nonzero(red[269, 60:895])[0]+60
groups=[]; s=xs[0]; p=xs[0]
for c in xs[1:]:
    if c>p+2: groups.append((s,p)); s=c
    p=c
groups.append((s,p))
print('  clusters:', groups[:24])
print('== caption text height ==')
m = red[464:484, 350:585]
ys,xs = np.nonzero(m)
print(f'  caption: x {350+xs.min()}..{350+xs.max()} y {464+ys.min()}..{464+ys.max()}')
# per-column max rows for cap measure
colr = {}
for c in range(350,585):
    ys2 = np.nonzero(red[460:488, c])[0]
    if len(ys2): colr[c] = (460+ys2.min(), 460+ys2.max())
items = list(colr.items())
print('  sample col spans:', items[::12])
