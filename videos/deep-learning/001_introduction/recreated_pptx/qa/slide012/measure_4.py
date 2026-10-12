from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)

# ink rows inside content box (x 100..878, y 160..388): dark-ish px per row
print("== ink rows in content box ==")
bands = []
cur = None
for y in range(160, 389):
    ink = [x for x in range(100, 879) if a[y,x].sum() < 420]
    if len(ink) >= 3:
        if cur is None: cur = [y, y, ink[0], ink[-1], len(ink)]
        else:
            cur[1] = y; cur[2] = min(cur[2], ink[0]); cur[3] = max(cur[3], ink[-1]); cur[4] += len(ink)
    else:
        if cur: bands.append(cur); cur = None
if cur: bands.append(cur)
for b in bands: print(" band rows", b[0],"..",b[1], "x", b[2],"..",b[3], "ink px", b[4])

# red ink per row (header red run)
print("\n== red ink rows (R-G>70, R>130) in content box ==")
for y in range(160, 389):
    red = [x for x in range(100, 879) if a[y,x,0]-a[y,x,1]>70 and a[y,x,0]>130]
    if len(red) >= 3: print(" row", y, "n=", len(red), red[0], "..", red[-1], "modal", Counter(tuple(a[y,x]) for x in red).most_common(1))
