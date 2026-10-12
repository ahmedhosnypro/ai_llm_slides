from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
ink = (r<170)&(g<170)&(b<180) | ((r>120)&(r>g+50)&(r>b+50)) | ((b>90)&(b>r+35))
inkd = ndimage.binary_dilation(ink, iterations=1)

def comps(x0,y0,x1,y1,minpx=5):
    sub = inkd[y0:y1, x0:x1]
    lab, n = ndimage.label(sub)
    out = []
    for i in range(1, n+1):
        ys, xs = np.nonzero(lab==i)
        if len(xs) < minpx: continue
        bx = (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()))
        px = a[y0:y1, x0:x1][lab==i]
        rr, gg, bb = px[:,0].mean(), px[:,1].mean(), px[:,2].mean()
        col = 'RED' if (rr>gg+40 and rr>bb+40) else ('BLU' if (bb>rr+30) else ('CYN' if (gg>200 and bb>200 and rr<200) else 'DRK'))
        out.append((bx, len(xs), col))
    return sorted(out, key=lambda t:(t[0][1]//8, t[0][0]))

print("== DIAGRAM BOX (x225..630 y348..508) ==")
for bx, n, col in comps(225,348,630,508,minpx=4):
    print(f"bbox={bx} n={n:4d} {col}")
