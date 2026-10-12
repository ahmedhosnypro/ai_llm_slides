from PIL import Image
import numpy as np, sys
im = Image.open(sys.argv[1]).convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]
red = (r > 120) & (r - g > 60) & (r - b > 60)
# exclude chrome: side borders (x<130, x>1875), top border (y<100), bottom rule (y>1100), badge zone
inner = red.copy()
inner[:, :130] = False; inner[:, 1880:] = False
inner[:100, :] = False; inner[1100:, :] = False
inner[80:230, 1750:1900] = False  # badge
ys, xs = np.nonzero(inner)
if not len(xs):
    print("no title ink found"); sys.exit(1)
SC = 960/2001.0  # render px -> frame px
print("RENDER title ink: x", xs.min(), xs.max(), "y", ys.min(), ys.max())
print("  -> frame-px equiv: x %.1f..%.1f (w %.1f) y %.1f..%.1f" % (
    xs.min()*SC, xs.max()*SC, (xs.max()-xs.min()+1)*SC, ys.min()*SC, ys.max()*SC))
print("  ORIG frame:       x 184..774 (w 591) y 261..297")
cx_r = (xs.min()+xs.max())/2*SC; cy_r = (ys.min()+ys.max())/2*SC
print("  ink center: (%.1f, %.1f) frame-px vs orig (479.0, 279.0)" % (cx_r, cy_r))
# 'S' cap height: first run
cc = inner.sum(axis=0)
cols = [x for x in range(130, 1880) if cc[x] > 0]
runs, start = [], cols[0]
for i in range(1, len(cols)):
    if cols[i] - cols[i-1] > 8: runs.append((start, cols[i-1])); start = cols[i]
runs.append((start, cols[-1]))
sx0, sx1 = runs[0]
rows = np.nonzero(inner[:, sx0:sx1+1].sum(axis=1))[0]
print("  'S' cap: %.1f frame-px vs orig 35; ascender-band %.1f vs orig 37" % (
    (rows.max()-rows.min()+1)*SC, (ys.max()-ys.min()+1)*SC))
