from PIL import Image
import numpy as np
a = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("RGB"), dtype=np.int16)
b = np.asarray(Image.open("unique_slides/slide_045.jpg").convert("RGB"), dtype=np.int16)
print("43 size", a.shape, "45 size", b.shape)
d = np.abs(a-b).max(axis=2)
mask = d > 30
ys, xs = np.where(mask)
print("delta px count:", mask.sum())
if mask.sum():
    print("delta bbox: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
colcount = mask.sum(axis=0)
rowcount = mask.sum(axis=1)
nz = np.where(colcount>2)[0]
nzr = np.where(rowcount>2)[0]
print("cols with >2 px:", nz.min() if len(nz) else None, "..", nz.max() if len(nz) else None)
print("rows with >2 px:", nzr.min() if len(nzr) else None, "..", nzr.max() if len(nzr) else None)
H,W = mask.shape
gh, gw = H//11, W//20
for gy in range(11):
    row=[]
    for gx in range(20):
        row.append(int(mask[gy*gh:(gy+1)*gh, gx*gw:(gx+1)*gw].sum()))
    print("row%02d"%(gy*gh), row)
# connected components (coarse, via labeling on a 4x downsample)
from scipy import ndimage
small = mask[::4,::4]
lab, n = ndimage.label(small, structure=np.ones((3,3)))
print("components:", n)
sizes = ndimage.sum(small, lab, range(1, n+1))
order = np.argsort(sizes)[::-1]
for i in order[:20]:
    if sizes[i] < 8: break
    sl = ndimage.find_objects(lab)[i]
    y0,y1 = sl[0].start*4, sl[0].stop*4
    x0,x1 = sl[1].start*4, sl[1].stop*4
    print("  comp size=%d bbox x %d..%d y %d..%d (w=%d h=%d)" % (sizes[i], x0, x1, y0, y1, x1-x0, y1-y0))
