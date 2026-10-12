from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
blue = (B>120)&((B-R)>60)&((B-G)>40)
orange = (R>170)&(R<240)&(G>90)&(G<170)&(B<70)
yellow = (R>200)&(G>180)&(B<120)

def bbox(mask, y0,y1,x0=0,x1=W,name=''):
    m = mask[y0:y1, x0:x1]
    ys,xs = np.nonzero(m)
    if len(xs)==0: print(f'{name}: EMPTY'); return None
    print(f'{name}: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}')
    return (x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max())

print('== caption precise ==')
bbox(red, 467,490, 60,800, 'caption')
print('== NN label box (blue rect) ==')
# scan blue rows in NN region x242..385
for name,(y0,y1,x0,x1) in {'NN label blue':(150,195,235,390),'NN blue dots area':(195,265,385,430),
                            'CNN label blue':(275,320,235,490),'CNN NL1':(400,440,300,400),'CNN NL2':(400,440,540,650)}.items():
    bbox(blue,y0,y1,x0,x1,name)
print('== blue row profile NN label region ==')
occ = blue[150:195,235:390].sum(axis=1)
print([f'{150+i}:{v}' for i,v in enumerate(occ) if v>0][:40])
print('== blue row profile CNN label region ==')
occ = blue[275:325,235:490].sum(axis=1)
print([f'{275+i}:{v}' for i,v in enumerate(occ) if v>0][:50])
print('== Non Linearity blue (below slabs) ==')
occ = blue[395:445,60:890].sum(axis=1)
print([f'{395+i}:{v}' for i,v in enumerate(occ) if v>0][:50])
bbox(blue,395,445,290,420,'NL under slab2')
bbox(blue,395,445,520,660,'NL under slab5')

print('== dot column: saturated pixels x383..430 y185..262 ==')
sat = (np.maximum(np.maximum(R,G),B)-np.minimum(np.minimum(R,G),B))>60
sub = sat[185:262,383:432]
ys,xs = np.nonzero(sub)
if len(xs):
    # cluster by y
    pts = sorted(zip(ys+185,xs+383))
    rows={}
    for y,x in pts: rows.setdefault(y,[]).append(x)
    for y in sorted(rows): 
        xs_=rows[y]; print(f'  y{y}: x {min(xs_)}..{max(xs_)} colors:', end=' ')
        seen=[]
        for x in sorted(set(xs_)):
            c=a[y,x]; seen.append(f'{x}:{tuple(c)}')
        print(' '.join(seen[:6]))

print('== meme photo bbox (NN row, non-white non-chrome) ==')
white = (R>235)&(G>235)&(B>230)
nonwhite = ~white
bbox(nonwhite, 186,258, 240,385, 'NN photo region nonwhite')
print('== siamese photo bbox (CNN row left of slab1) ==')
bbox(nonwhite, 300,432, 120,230, 'CNN photo region nonwhite')
print('== per-slab geometry ==')
for i,(x0,x1) in enumerate([(229,286),(311,368),(399,456),(477,534),(553,610),(635,691),(735,760),(782,808),(829,854)]):
    m = orange[300:440, x0:x1+1]
    ys,xs = np.nonzero(m)
    if len(xs):
        ytop, ybot = 300+ys.min(), 300+ys.max()
        # left x at top rows and bottom rows
        toprow = 300+ys.min()+2; botrow = 300+ys.max()-2
        r1 = np.nonzero(orange[toprow, x0:x1+1])[0]
        r2 = np.nonzero(orange[botrow, x0:x1+1])[0]
        t = f'x{x0+r1.min()}..{x0+r1.max()}' if len(r1) else '-'
        b = f'x{x0+r2.min()}..{x0+r2.max()}' if len(r2) else '-'
        print(f'  block{i+1} x{x0}..{x1}: y {ytop}..{ybot}  top[{t}] bot[{b}]')
print('== NN per-block y extent ==')
for i,(x0,x1) in enumerate([(450,476),(497,522),(544,570),(591,617),(639,664),(686,712)]):
    m = orange[170:270, x0:x1+1]
    ys,xs = np.nonzero(m)
    if len(xs): print(f'  NNblock{i+1} x{x0}..{x1}: y {170+ys.min()}..{170+ys.max()}')
print('== flatten tag: red text inside yellow ==')
bbox(red, 155,186, 385,425, 'tag red text')
print('== FC/OP/Conv overlines (strict red above blocks) ==')
bbox(red, 160,186, 440,720, 'NN overlines band')
bbox(red, 288,318, 220,700, 'CNN Conv overlines band')
for name,(y0,y1,x0,x1) in {'FC1?':(160,186,444,486),'FC2?':(160,186,490,532),'FC3?':(160,186,538,580),'FC4?':(160,186,585,626),'OP?':(160,186,632,674),'Loss NN':(160,186,680,720)}.items():
    bbox(red,y0,y1,x0,x1,name)
