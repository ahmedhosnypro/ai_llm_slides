from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

ink = (r<160)&(g<160)&(b<170) | ((r>120)&(r>g+50)&(r>b+50)) | ((b>90)&(b>r+35))
ink = ndimage.binary_dilation(ink, iterations=1)

def comps(x0,y0,x1,y1,minpx=6):
    sub = ink[y0:y1, x0:x1]
    lab, n = ndimage.label(sub)
    out = []
    for i in range(1, n+1):
        ys, xs = np.nonzero(lab==i)
        if len(xs) < minpx: continue
        bx = (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()))
        cx, cy = int(xs.mean())+x0, int(ys.mean())+y0
        # modal color of the component's darkest pixels
        px = a[y0:y1, x0:x1][lab==i]
        rr, gg, bb = px[:,0].mean(), px[:,1].mean(), px[:,2].mean()
        col = 'RED' if (rr>gg+40 and rr>bb+40) else ('BLU' if (bb>rr+30) else 'DRK')
        out.append((bx, len(xs), col, (round(rr),round(gg),round(bb))))
    return sorted(out, key=lambda t:(t[0][1]//10, t[0][0]))

print("== LEFT BOX components (x84..430 y88..246) ==")
for bx, n, col, mean in comps(84,88,430,246):
    print(f"bbox={bx} n={n:4d} {col} mean={mean}")
