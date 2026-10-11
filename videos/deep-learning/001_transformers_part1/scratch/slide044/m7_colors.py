from PIL import Image
import numpy as np
from collections import Counter
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"))
x0,x1,y0,y1 = 742, 904, 84, 294
sub = im[y0:y1, x0:x1].reshape(-1,3)
# quantize to 16-levels
q = (sub//24*24)
cnt = Counter(map(tuple, q))
for c, n in cnt.most_common(18):
    print(c, n)
print("--- sample scanline colors at specific y ---")
for y in [100, 118, 133, 148, 160, 175, 190, 205, 222, 240, 258, 270, 278, 288]:
    row = im[y, 742:904]
    # count non-white-ish
    nz = [(742+i, tuple(int(v) for v in row[i])) for i in range(0,162,1) if not (row[i]>225).all()]
    print(f"y{y}: {nz[:14]}")
