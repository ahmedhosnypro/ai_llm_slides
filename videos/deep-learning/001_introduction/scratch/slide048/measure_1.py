from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
print('size', im.size)
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]

# red ink mask (C00000-ish): strong red, low G/B
red = (R>120)&(R<235)&(G<80)&(B<80)
ys,xs = np.nonzero(red)
print('red px count', len(xs))

# column profile of red: find vertical lines (frame borders) — cols with many red px
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
top_cols = [c for c in range(W) if colcount[c]>100]
top_rows = [r for r in range(H) if rowcount[r]>100]
print('cols with >100 red px:', top_cols[:20], '...', top_cols[-20:] if len(top_cols)>20 else '')
print('rows with >100 red px:', top_rows[:20], '...', top_rows[-20:] if len(top_rows)>20 else '')

# orange block mask (D4821E-ish)
orange = (R>170)&(R<240)&(G>90)&(G<170)&(B<70)
ys,xs = np.nonzero(orange)
print('orange px', len(xs))
if len(xs):
    print('orange bbox x', xs.min(), xs.max(), 'y', ys.min(), ys.max())
    # orange row profile: find rows containing orange (blocks bands)
    orow = orange.sum(axis=1)
    bands=[]
    inb=False
    for r in range(H):
        if orow[r]>3 and not inb: inb=True; s=r
        elif orow[r]<=3 and inb: inb=False; bands.append((s,r-1))
    print('orange row bands:', bands)

# yellow mask (FFFF00 + FFD700-ish)
yellow = (R>200)&(G>180)&(B<120)
ys,xs = np.nonzero(yellow)
print('yellow px', len(xs))
if len(xs):
    # cluster yellow regions coarsely
    from scipy import ndimage
    lab,n = ndimage.label(yellow)
    print('yellow clusters:', n)
    for i in range(1,min(n,15)+1):
        m = lab==i
        if m.sum()>30:
            ys2,xs2 = np.nonzero(m)
            print(f'  cluster {i}: x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} n={m.sum()}')
