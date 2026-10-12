from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
dark = (R<140)&(G<140)&(B<140)
anyink = (np.maximum(np.maximum(R,G),B)-np.minimum(np.minimum(R,G),B))>40
lum = 0.299*R+0.587*G+0.114*B

def bbox(mask, y0,y1,x0=0,x1=W,name=''):
    m = mask[y0:y1, x0:x1]
    ys,xs = np.nonzero(m)
    if len(xs)==0: print(f'{name}: EMPTY'); return None
    print(f'{name}: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}')
    return (x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max())

print('== ANY ink inside NN label box (interior y158..179 x246..376) ==')
bbox(lum<200, 158,180, 246,376, 'NN box interior ink')
print('== ANY ink inside CNN label box (interior y281..303 x246..477) ==')
bbox(lum<200, 281,304, 246,477, 'CNN box interior ink')
print('== Conv labels: strict red inside slab band (excl borders) ==')
bbox(red, 318,424, 232,730, 'red in slab band')
# cluster columns
m = red[318:424, 232:730]
ys,xs = np.nonzero(m)
if len(xs):
    cols = sorted(set(xs+232))
    groups=[]; s=cols[0]; p=cols[0]
    for c in cols[1:]:
        if c>p+4: groups.append((s,p)); s=c
        p=c
    groups.append((s,p))
    print('red col clusters in slab band:', groups)
    for g in groups:
        mm = red[318:424, g[0]:g[1]+1]
        ys2,xs2 = np.nonzero(mm)
        print(f'  cluster x{g[0]}..{g[1]}: y {318+ys2.min()}..{318+ys2.max()} n={len(xs2)}')
print('== dark arrows in CNN row (slant-corrected scan) ==')
bbox(dark, 355,385, 287,425, 'gap slab1-slab2..3 dark')
bbox(dark, 350,390, 369,425, 'gap2 wide')
bbox(dark, 355,385, 425,478, 'gap slab3 slab3-slab4')
print('== label text hunt: ink rows between y140..192 x235..400 (above photo) ==')
occr = (lum<170)[140:195, 235:400].sum(axis=1)
print([f'{140+i}:{v}' for i,v in enumerate(occr) if v>0])
print('== ink rows y252..320 x235..500 (below meme/above CNN box) ==')
occr = (lum<170)[252:320, 235:500].sum(axis=1)
print([f'{252+i}:{v}' for i,v in enumerate(occr) if v>0])
print('== parallelogram corners (CNN photo) ==')
white = (R>235)&(G>235)&(B>230)
for r in [319,325,340,360,380,400,415,424,427]:
    xs = np.nonzero(~white[r,120:228])[0]
    if len(xs): print(f'  row {r}: x {120+xs.min()}..{120+xs.max()}')
print('== NN block white text check (vertical text) ==')
# white pixels inside block1 x450..476 y186..255
wt = (R>230)&(G>230)&(B>225)
m = wt[190:252, 452:475]
ys,xs = np.nonzero(m)
if len(xs): print(f'  block1 white text: x {452+xs.min()}..{452+xs.max()} y {190+ys.min()}..{190+ys.max()} n={len(xs)}')
m = wt[318:422, 232:284]
ys,xs = np.nonzero(m)
if len(xs): print(f'  slab1 white text: x {232+xs.min()}..{232+xs.max()} y {318+ys.min()}..{318+ys.max()} n={len(xs)}')
print('== meme photo border? edge colors ==')
for x,y in [(248,220),(249,220),(358,220),(359,220),(300,191),(300,192),(300,251),(300,252)]:
    print(f'  ({x},{y}) {tuple(a[y,x])}')
