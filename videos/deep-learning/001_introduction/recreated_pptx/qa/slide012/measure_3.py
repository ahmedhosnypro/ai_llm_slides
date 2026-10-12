from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# red col 58 y-range
ys = [y for y in range(H) if a[y,58,0]-a[y,58,1]>60 and a[y,58,0]>110]
print("col58 red y-range:", ys[0], "..", ys[-1], "count", len(ys))

# content box borders: rows 150..165 and 385..395 core rows
print("\n== content box top border rows 150..165 ==")
for y in range(150, 166):
    bl = [x for x in range(85, 895) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80]
    if bl and len(bl)>50: print(" row", y, bl[0],"..",bl[-1], "modal", Counter(tuple(a[y,x]) for x in bl).most_common(1))
print("== content box bottom border rows 383..396 ==")
for y in range(383, 397):
    bl = [x for x in range(85, 895) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80]
    if bl and len(bl)>50: print(" row", y, bl[0],"..",bl[-1], "modal", Counter(tuple(a[y,x]) for x in bl).most_common(1))
print("== content box left/right cols ==")
for x in range(88, 102):
    bl = sum(1 for y in range(157, 392) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80)
    if bl>100: print(" colL", x, bl, tuple(a[270,x]))
for x in range(875, 890):
    bl = sum(1 for y in range(157, 392) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80)
    if bl>100: print(" colR", x, bl, tuple(a[270,x]))

# fill colors inside boxes
print("\ncontent box fill modal:", Counter(tuple(a[y,x]) for y in range(200,380,7) for x in range(400,800,11)).most_common(2))
print("title box fill modal:", Counter(tuple(a[y,x]) for y in range(90,130,3) for x in range(130,200,5)).most_common(2))
print("canvas above panel row 20 modal:", Counter(tuple(a[20,x]) for x in range(100,900,13)).most_common(1))
print("panel bg row 470 (empty zone) modal:", Counter(tuple(a[470,x]) for x in range(200,800,11)).most_common(1))

# black bar top/bottom precise
print("\nblack bar: row 518 dark count:", sum(1 for x in range(W) if a[518,x].sum()<150), " row 519:", sum(1 for x in range(W) if a[519,x].sum()<150))
