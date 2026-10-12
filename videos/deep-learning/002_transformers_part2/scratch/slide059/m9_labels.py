from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def clusters(mask, y0, y1, x0, x1, minpx, name, axis='x'):
    sub = np.zeros_like(mask); sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(sub)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(xs) < minpx: continue
        out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
    out.sort(key=lambda c: c[0])
    print(f'--- {name}: {len(out)}')
    for c in out: print('   x %d..%d y %d..%d n%d cx %.1f cy %.1f' % (c[0],c[1],c[2],c[3],c[4],(c[0]+c[1])/2,(c[2]+c[3])/2))
    return out

# word row: dark-red label text in y 418..440
dred = (R>120)&(R<215)&(G<95)&(B<95)&(R-G>55)
clusters(dred, 416, 442, 240, 910, 6, 'word row red label glyphs')
# position row: navy text y 474..502
navy = (B>85)&(R<120)&(G<120)&(B-R>50)
clusters(navy, 472, 505, 150, 910, 6, 'position row navy glyphs')
# output row: blue text y 226..258
blue = (B>110)&(R<130)&(G<130)&(B-R>50)
clusters(blue, 224, 260, 170, 910, 6, 'output row blue glyphs')
# dots: green dots word row (y 418..440), position row (y 474..505)
grn = (G>110)&(G-R>25)&(G-B>25)
clusters(grn, 418, 441, 560, 780, 6, 'word row green dots')
clusters(grn, 474, 505, 600, 800, 6, 'position row green dots')
clusters(grn, 224, 260, 560, 800, 6, 'output row green dots?')
# blue dots output row
clusters(blue, 224, 260, 560, 800, 6, 'output row blue dots')
# the red line in position row: rows with wide dark-red coverage x 250..900
dred2 = (R>120)&(R<215)&(G<110)&(B<110)&(R-G>50)
cnt = dred2[:, 250:900].sum(axis=1)
print('red-line rows 480..515 (x250..900):', {y:int(cnt[y]) for y in range(480,516) if cnt[y]>40})
cnt2 = dred2[:, 250:900].sum(axis=1)
print('red-line rows 410..445 (word row):', {y:int(cnt2[y]) for y in range(410,446) if cnt2[y]>40})
