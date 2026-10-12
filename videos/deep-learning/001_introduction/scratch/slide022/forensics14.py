from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# 1) fan lines: pink/red-ish thin lines between weights (x306..400) and junction
pinkish = (r>150)&(r-b>25)&(r-g>20)&(g<210)
sub = pinkish[350:505, 305:400]
ys, xs = np.nonzero(sub)
print("fan-lines pinkish bbox:", (305+xs.min(), 350+ys.min(), 305+xs.max(), 350+ys.max()), "n=", len(xs))
# sample a few line pixels
from collections import Counter
px = a[350:505, 305:400][sub]
print("fan line modal colors:", Counter(map(tuple, px)).most_common(5))

# wider: whole diagram box, catch ANY non-white, non-bg pixel columns 306..414
diff = (np.abs(r-232)>18)|(np.abs(g-232)>18)|(np.abs(b-232)>18)
sub2 = diff[350:505, 306:400]
ys, xs = np.nonzero(sub2)
print("non-bg ink bbox in x306..400:", (306+xs.min(), 350+ys.min(), 306+xs.max(), 350+ys.max()), "n=", len(xs))

# 2) callout region map: x600..830 y390..478
tanf = (r>170)&(r<235)&(g>140)&(g<215)&(b<205)&(r-b>15)
sub3 = tanf[390:478, 600:830]
ys, xs = np.nonzero(sub3)
print("\ncallout tan-fill bbox:", (600+xs.min(), 390+ys.min(), 600+xs.max(), 390+ys.max()), "n=", len(xs))

# callout borders: scan rows/cols at edges
print("callout left edge samples x605..635 @y=420:", [tuple(a[420,x]) for x in range(605,636,2)])
print("callout top edge samples @x=700, y392..406:", [tuple(a[y,700]) for y in range(392,407,2)])
print("callout bottom edge @x=700, y440..452:", [tuple(a[y,700]) for y in range(440,453,2)])
print("callout right edge @y=420, x800..822:", [tuple(a[420,x]) for x in range(800,823,2)])

# 3) black bar
blk = (r<70)&(g<70)&(b<70)
sub4 = blk[505:540, 0:960]
ys, xs = np.nonzero(sub4)
print("\nblack bar bbox:", (int(xs.min()), 505+int(ys.min()), int(xs.max()), 505+int(ys.max())), "n=", len(xs))

# 4) title components
ink = (r<170)&(g<170)&(b<180) | ((r>120)&(r>g+50)&(r>b+50))
inkd = ndimage.binary_dilation(ink, iterations=1)
lab, n = ndimage.label(inkd[55:90, 200:760])
out = []
for i in range(1, n+1):
    ys, xs = np.nonzero(lab==i)
    if len(xs) < 8: continue
    out.append((200+int(xs.min()), 55+int(ys.min()), 200+int(xs.max()), 55+int(ys.max()), len(xs)))
out.sort()
print("\ntitle glyph components (first/last few):")
print("count:", len(out))
if out:
    print("first 3:", out[:3]); print("last 3:", out[-3:])
    x0 = min(o[0] for o in out); x1 = max(o[2] for o in out)
    y0 = min(o[1] for o in out); y1 = max(o[3] for o in out)
    print("title ink bbox:", (x0,y0,x1,y1))
