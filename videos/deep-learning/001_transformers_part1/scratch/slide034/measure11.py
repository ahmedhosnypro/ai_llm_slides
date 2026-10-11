from PIL import Image
import numpy as np
from scipy import ndimage
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

# Warning text: classify ink pixels in y 289..307 x 395..870
band = a[289:307, 395:870]
R,G,B = band[:,:,0],band[:,:,1],band[:,:,2]
ink = (R+G+B < 480) | ((B-R>40)&(B>120)) | ((R-B>40)&(R>140))
ys,xs = np.where(ink)
cols = band[ys,xs]
blueish = (cols[:,2]-cols[:,0] > 30)
reddish = (cols[:,0]-cols[:,2] > 50) & (cols[:,0]>130)
darkish = (cols.sum(axis=1) < 300)
print("warning ink px:", len(xs), " blue:",blueish.sum(), " red:",reddish.sum(), " dark:",darkish.sum())
if len(xs):
    xr = xs+395
    print("blue x-range:", xr[blueish].min() if blueish.any() else None, xr[blueish].max() if blueish.any() else None)
    print("red x-range:", xr[reddish].min() if reddish.any() else None, xr[reddish].max() if reddish.any() else None)
    # histogram of x in 20px bins
    hist,edges = np.histogram(xr, bins=np.arange(395,875,20))
    print("ink x hist:", {int(edges[i]):int(hist[i]) for i in range(len(hist)) if hist[i]>0})

# warning strip box edges: white region rows 284..314
white=(r>235)&(g>235)&(b>225)
row=white[300, 380:890]
xs2=np.where(row)[0]+380
print("warning white row300 x:", xs2.min(), "..", xs2.max())
col=white[270:330, 600]
ys2=np.where(col)[0]+270
print("warning white col600 y:", ys2.min(), "..", ys2.max())

# col1 input stack detail: col x=150 through boxes
print("col x=150 y355..490 runs:")
prev=None;start=0
for y in range(355,492):
    c=tuple(a[y,150]//28)
    if c!=prev:
        if prev is not None and y-start>=2: print(f"   y {start}..{y-1} ~{tuple(a[(start+y)//2,150])}")
        prev=c;start=y
print(f"   y {start}..491 ~{tuple(a[490,150])}")
# col1 output stack: col x=280
print("col x=280 y355..490 runs:")
prev=None;start=0
for y in range(355,492):
    c=tuple(a[y,280]//28)
    if c!=prev:
        if prev is not None and y-start>=2: print(f"   y {start}..{y-1} ~{tuple(a[(start+y)//2,280])}")
        prev=c;start=y
print(f"   y {start}..491 ~{tuple(a[490,280])}")
