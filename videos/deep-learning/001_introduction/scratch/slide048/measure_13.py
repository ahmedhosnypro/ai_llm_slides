from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
loose = ((R-G)>28)&((R-B)>28)&(R>150)
dark = (R<140)&(G<140)&(B<140)
orange = (R>170)&(R<240)&(G>90)&(G<170)&(B<70)

def amap(mask, y0,y1,x0,x1,bx=2,by=2,label=''):
    print(label)
    for byy in range(y0,y1,by):
        line=''
        for bxx in range(x0,x1,bx):
            frac = mask[byy:byy+by, bxx:bxx+bx].mean()
            line += '#' if frac>0.5 else ('+' if frac>0.2 else ('.' if frac>0.05 else ' '))
        print(f'{byy:4d} '+line)

print('==== Conv labels region: y308..335 x228..520 (loose red, 2px blocks) ====')
amap(loose, 308,336, 228,520, 2,2)
print('==== caption region: y460..486 x340..600 (loose red, 2px) ====')
amap(loose, 460,486, 340,600, 2,2)
print('==== arrow photo->dots: dark in y200..245 x358..405 ====')
m = dark[200:245, 358:405]
ys,xs = np.nonzero(m)
if len(xs): print(f'bbox x {358+xs.min()}..{358+xs.max()} y {200+ys.min()}..{200+ys.max()} n={len(xs)}')
amap(dark, 200,245, 358,405, 2,2)
print('==== CNN arrows: dark clusters row y368..372, x230..730 (excl orange) ====')
m = dark[368:373, 230:730] & ~orange[368:373, 230:730]
ys,xs = np.nonzero(m)
if len(xs):
    cols = sorted(set(xs+230)); groups=[]; s=cols[0]; p=cols[0]
    for c in cols[1:]:
        if c>p+3: groups.append((s,p)); s=c
        p=c
    groups.append((s,p))
    print('clusters:', groups)
print('==== slab4 top region y308..335 x450..560 (loose) ====')
amap(loose, 308,336, 450,560, 2,2)
