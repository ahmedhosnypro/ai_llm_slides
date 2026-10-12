from PIL import Image
import numpy as np
try:
    from scipy import ndimage
    HAVE=True
except Exception:
    HAVE=False
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def comps(mask, minpx=6, name=''):
    if not HAVE:
        print('no scipy'); return []
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(xs) < minpx: continue
        out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
    out.sort(key=lambda t: t[0])
    print(f'--- {name}: {len(out)} components')
    for c in out: print('   x %d..%d y %d..%d n%d  w%g h%g cx %.1f cy %.1f' % (c[0],c[1],c[2],c[3],c[4],c[1]-c[0]+1,c[3]-c[2]+1,(c[0]+c[1])/2,(c[2]+c[3])/2))
    return out

# softmax tan bar core (233..245, 195..205, 155..175)
tan = (abs(R-238)<10)&(abs(G-199)<12)&(abs(B-162)<12)
m = np.zeros_like(tan); m[80:120, :] = tan[80:120, :]
comps(m, 500, 'softmax tan bar')

# navy circles: core navy (26,35,126) generous
navy = (R<70)&(G<75)&(B>90)&(B<190)
m = np.zeros_like(navy); m[75:125, 380:700] = navy[75:125, 380:700]
comps(m, 40, 'navy circles')

# red base nodes C0392B under circles: (192,57,43)
rbase = (abs(R-192)<35)&(abs(G-57)<35)&(abs(B-43)<35)
m = np.zeros_like(rbase); m[100:125, 380:700] = rbase[100:125, 380:700]
comps(m, 20, 'red base nodes')

# pooled row squares y 138..164: find distinct fills
band = slice(138,165)
yel = (R>225)&(G>185)&(G<225)&(B<110)
grn = (abs(R-88)<45)&(abs(G-214)<35)&(abs(B-141)<45)
pnk = (abs(R-236)<30)&(abs(G-112)<45)&(abs(B-99)<45)
for nm, mk in (('pool yellow', yel), ('pool green', grn), ('pool pink', pnk)):
    m = np.zeros_like(mk); m[band, 350:640] = mk[band, 350:640]
    comps(m, 8, nm)
