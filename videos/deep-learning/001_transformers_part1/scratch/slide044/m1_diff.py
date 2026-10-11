from PIL import Image
import numpy as np
a = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("RGB"), dtype=np.int16)
b = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
print("43 size", a.shape, "44 size", b.shape)
d = np.abs(a-b).max(axis=2)
mask = d > 30
ys, xs = np.where(mask)
print("delta px count:", mask.sum())
if mask.sum():
    print("delta bbox: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
# column/row profile of the delta
colcount = mask.sum(axis=0)
rowcount = mask.sum(axis=1)
nz = np.where(colcount>2)[0]
nzr = np.where(rowcount>2)[0]
print("cols with >2 px:", nz.min() if len(nz) else None, "..", nz.max() if len(nz) else None)
print("rows with >2 px:", nzr.min() if len(nzr) else None, "..", nzr.max() if len(nzr) else None)
# dense subregions: print a coarse grid 20x11 of counts
H,W = mask.shape
gh, gw = H//11, W//20
for gy in range(11):
    row=[]
    for gx in range(20):
        row.append(int(mask[gy*gh:(gy+1)*gh, gx*gw:(gx+1)*gw].sum()))
    print("row%02d"%(gy*gh), row)
