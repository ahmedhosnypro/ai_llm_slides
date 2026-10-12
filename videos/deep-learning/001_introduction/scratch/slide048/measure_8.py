from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
loose = ((R-G)>28)&((R-B)>28)&(R>150)

def bbox(mask, y0,y1,x0=0,x1=W,name=''):
    m = mask[y0:y1, x0:x1]
    ys,xs = np.nonzero(m)
    if len(xs)==0: print(f'{name}: EMPTY'); return None
    print(f'{name}: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}')
    return (x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max())

print('== TITLE (strict red, excluding border cols) ==')
bbox(red, 55,92, 66,890, 'title line1')
bbox(red, 92,125, 66,890, 'title line2')

print('== ARROW + CAPTION (below frame bottom 450) ==')
bbox(loose, 452,470, 60,890, 'arrow band loose')
bbox(red, 452,470, 60,890, 'arrow band strict')
bbox(red, 465,495, 60,890, 'caption strict')
bbox(loose, 465,495, 60,890, 'caption loose')
# arrow shaft rows precise
for r in range(455,470):
    xs=np.nonzero(loose[r,60:890])[0]
    if len(xs)>5: print(f'  row {r}: x {60+xs.min()}..{60+xs.max()} n={len(xs)}')

print('== ORANGE blocks column profile ==')
orange = (R>170)&(R<240)&(G>90)&(G<170)&(B<70)
def colbands(mask,y0,y1,minw=3):
    occ = mask[y0:y1,:].sum(axis=0)
    bands=[]; s=None
    for c in range(W):
        if occ[c]>=minw and s is None: s=c
        elif occ[c]<minw and s is not None:
            bands.append((s,c-1)); s=None
    if s is not None: bands.append((s,W-1))
    return bands
print('NN band y186..256 orange col-bands:', colbands(orange,186,256))
print('CNN band y316..425 orange col-bands:', colbands(orange,316,425))
# CNN slab slant: orange row extent at several rows
for r in [316,330,350,370,390,410,424]:
    xs=np.nonzero(orange[r,:])[0]
    if len(xs): print(f'  CNN row {r}: x {xs.min()}..{xs.max()} n={len(xs)}')
for r in [186,200,220,240,255]:
    xs=np.nonzero(orange[r,:])[0]
    if len(xs): print(f'  NN row {r}: x {xs.min()}..{xs.max()} n={len(xs)}')

print('== BLUE elements ==')
blue = (B>120)&((B-R)>60)&((B-G)>40)
bbox(blue, 140,270, 60,890, 'NN row blue')
bbox(blue, 275,440, 60,890, 'CNN row blue')
print('NN blue col-bands:', colbands(blue,140,265,minw=2))
print('CNN blue col-bands:', colbands(blue,275,440,minw=2))
