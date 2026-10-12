from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
# relaxed reddish
reddish = (R>140)&((R-G)>50)&((R-B)>50)

for c in [58,65,894,893,895,57,59]:
    ys = np.nonzero(red[:,c])[0]
    ys2 = np.nonzero(reddish[:,c])[0]
    def runs(ys):
        out=[]; s=None; p=None
        for y in ys:
            if s is None: s=y
            elif y!=p+1: out.append((s,p)); s=y
            p=y
        if s is not None: out.append((s,p))
        return out
    print(f'col {c} red runs:', runs(ys)[:12])
    print(f'col {c} reddish runs:', runs(ys2)[:12])

# horizontal extent of red in key rows
for r in [135,269,448,449,136]:
    xs = np.nonzero(red[r,:])[0]
    if len(xs): print(f'row {r}: x {xs.min()}..{xs.max()} n={len(xs)}')

# find frame top/bottom border with relaxed mask: rows where reddish spans most of x 60..890
rr = reddish[:, 60:890].sum(axis=1)
cand = [r for r in range(H) if rr[r]>500]
print('rows with >500 reddish px (frame borders?):', cand)
for r in cand:
    xs = np.nonzero(reddish[r,:])[0]
    print(f'  row {r}: x {xs.min()}..{xs.max()} n={len(xs)}')

# vertical extent of reddish in col 58/894 full
for c in [58,894]:
    ys = np.nonzero(reddish[:,c])[0]
    print(f'col {c} reddish y-extent: {ys.min()}..{ys.max()} n={len(ys)}')
