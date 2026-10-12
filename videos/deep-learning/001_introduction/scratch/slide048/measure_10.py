from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
blue = (B>120)&((B-R)>60)&((B-G)>40)
dark = (R<120)&(G<120)&(B<120)

def bbox(mask, y0,y1,x0=0,x1=W,name=''):
    m = mask[y0:y1, x0:x1]
    ys,xs = np.nonzero(m)
    if len(xs)==0: print(f'{name}: EMPTY'); return None
    print(f'{name}: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}')
    return (x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max())

print('== label box text color probes (NN box interior) ==')
for y in range(160,180,2):
    row=[]
    for x in range(250,378,6): row.append(f'{x}:{tuple(a[y,x])}')
    print(f' y{y}: '+' '.join(row))
print('== CNN label interior probes ==')
for y in range(283,304,3):
    row=[]
    for x in range(250,478,10): row.append(f'{x}:{tuple(a[y,x])}')
    print(f' y{y}: '+' '.join(row))
print('== tag interior probes (yellow tag y157..183 x387..422) ==')
for y in range(158,184,2):
    row=[]
    for x in range(388,423,3): row.append(f'{x}:{tuple(a[y,x])}')
    print(f' y{y}: '+' '.join(row))
print('== Conv overlines: strict red in CNN upper area ==')
bbox(red, 296,316, 230,890, 'red y296..316')
bbox(red, 290,316, 230,890, 'red y290..316')
bbox(red, 300,340, 230,890, 'red y300..340 (slab area? Conv ON slabs?)')
print('== FC/OP above CNN blocks 7/8 ==')
bbox(red, 300,335, 730,860, 'FC/OP above 7/8')
bbox(red, 306,333, 730,770, 'FC above block7')
bbox(red, 306,333, 775,815, 'OP above block8')
print('== dark ink (arrows) ==')
bbox(dark, 200,245, 340,405, 'arrow photo->dots')
bbox(dark, 200,245, 425,452, 'arrow dots->block1')
for i,(g0,g1) in enumerate([(477,496),(523,543),(571,590),(618,638),(665,685)]):
    bbox(dark, 205,240, g0,g1+1, f'NN gap arrow {i+1}')
bbox(dark, 350,400, 195,258, 'arrow photo->slab1')
for i,(g0,g1) in enumerate([(287,310),(369,398),(457,476),(535,552),(611,634),(692,734)]):
    bbox(dark, 350,400, g0,g1+1, f'CNN gap arrow {i+1}')
print('== photo edges refined ==')
white = (R>235)&(G>235)&(B>230)
nonwhite = ~white
# NN photo: column profile
occ = nonwhite[191:253, 240:402].sum(axis=0)
prof = ''.join('#' if v>40 else ('+' if v>10 else ('.' if v>2 else ' ')) for v in occ)
print('NN photo cols 240..401:', prof)
occ2 = nonwhite[319:428, 120:232].sum(axis=0)
prof2 = ''.join('#' if v>40 else ('+' if v>10 else ('.' if v>2 else ' ')) for v in occ2)
print('CNN photo cols 120..231:', prof2)
# rows of NN photo
occr = nonwhite[186:258, 249:356].sum(axis=1)
print('NN photo rows 186..257:', ''.join('#' if v>60 else ('+' if v>15 else ('.' if v>2 else ' ')) for v in occr))
occrc = nonwhite[315:432, 130:210].sum(axis=1)
print('CNN photo rows 315..431:', ''.join('#' if v>50 else ('+' if v>12 else ('.' if v>2 else ' ')) for v in occrc))
print('== NL1 wider window ==')
bbox(blue, 410,445, 250,420, 'NL1 wide')
bbox(blue, 410,445, 540,680, 'NL2 wide')
print('== dot column low-threshold rescan ==')
sat = (np.maximum(np.maximum(R,G),B)-np.minimum(np.minimum(R,G),B))>25
ys,xs = np.nonzero(sat[186:265, 386:432])
pts = sorted(zip(ys+186,xs+386))
rows={}
for y,x in pts: rows.setdefault(y,[]).append(x)
for y in sorted(rows):
    if len(rows[y])>2: print(f'  y{y}: x {min(rows[y])}..{max(rows[y])} n={len(rows[y])} c={tuple(a[y,(min(rows[y])+max(rows[y]))//2])}')
