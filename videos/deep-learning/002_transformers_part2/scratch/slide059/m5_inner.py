from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# --- encoder container: white text + ellipsis inside (y 277..371, x 144..876)
# white-ish px on red: R,G,B all > 190
wht = (R>190)&(G>170)&(B>170)
sub = np.zeros_like(wht); sub[277:372, 150:875] = wht[277:372, 150:875]
lab, n = ndimage.label(sub)
objs = ndimage.find_objects(lab)
clusters = []
for i, sl in enumerate(objs):
    m = (lab[sl] == i+1)
    npx = m.sum()
    if npx < 8: continue
    y0,y1 = sl[0].start, sl[0].stop; x0,x1 = sl[1].start, sl[1].stop
    clusters.append((x0,x1,y0,y1,npx))
clusters.sort(key=lambda c: c[0])
print('white clusters in encoder (%d):' % len(clusters))
for c in clusters: print('   x %d..%d y %d..%d n%d' % c)

# --- pure pink container x extent at y 390..408 (above word row) and y 506..514
pink = (abs(R-250)<14)&(abs(G-219)<16)&(abs(B-216)<16)
for y0,y1 in ((388,408),(506,515)):
    ys,xs = np.where(pink[y0:y1,:])
    print('pink pure y%d..%d: x %d..%d' % (y0,y1,xs.min(),xs.max()))
# pink vertical extent at x=100 (left of word/pos rows)
ys,xs = np.where(pink[:, 70:120])
print('pink at x70..120: y %d..%d' % (ys.min(), ys.max()))

# --- plus circle: strong red cluster y 435..478 x 460..540
red = (R>140)&(G<100)&(B<100)
sub = np.zeros_like(red); sub[435:478, 460:540] = red[435:478, 460:540]
ys,xs = np.where(sub)
print('plus circle red bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))

# --- block arrows: blue outline 1F3BB3 (31,59,179)
blu = (B>130)&(B<230)&(R<100)&(G<120)&(B-R>60)
for nm,(y0,y1) in (('arrow4 GAP->pool',(160,182)),('arrow3 out->GAP',(205,225)),('arrow2 enc->out',(258,278)),('arrow1 in->enc',(370,390))):
    sub = np.zeros_like(blu); sub[y0:y1, 440:560] = blu[y0:y1, 440:560]
    lab,n = ndimage.label(sub)
    if n:
        sizes = ndimage.sum(sub, lab, range(1,n+1))
        i = int(np.argmax(sizes))
        ys,xs = np.where(lab==i+1)
        print(nm, 'main blue bbox x %d..%d y %d..%d n%d' % (xs.min(),xs.max(),ys.min(),ys.max(),len(xs)))
    else:
        print(nm, 'none')
# arrows pale fill: near-white
# find arrow fill (between outline) — sample center x=499
for y in range(160,182):
    pass
print('arrow4 strip x495..505 y162..180:', [tuple(a[y,500]) for y in range(160,182,2)])

# --- word row: white X-boxes with borders inside green border y 413..444
# X-box borders? sample a box edge — find dark-ish vertical lines in y 418..440
dk = (R<150)&(G<150)&(B<150)
cnt = dk[418:440, 260:900].sum(axis=0)
cols = [260+i for i in range(640) if cnt[i]>12]
print('word row dark cols:', cols[:40], '...' if len(cols)>40 else '')

# --- position row: white Vector boxes inside orange border y 471..505
cnt = dk[476:500, 260:900].sum(axis=0)
cols = [260+i for i in range(640) if cnt[i]>12]
print('pos row dark cols:', cols[:40], '...' if len(cols)>40 else '')

# --- output row: Y boxes: blue-ish border cols in y 225..255
blub = (B>130)&(R<120)&(G<130)&(B-R>40)
cnt = blub[228:252, 170:900].sum(axis=0)
cols = [170+i for i in range(730) if cnt[i]>12]
print('output row blue cols:', cols[:40], '...' if len(cols)>40 else '')
