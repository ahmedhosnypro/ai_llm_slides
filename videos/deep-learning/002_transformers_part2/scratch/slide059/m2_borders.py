from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# reddish: red channel dominates green&blue by a margin
red = (r - g > 55) & (r - b > 55)

colcnt = red[150:350, :].sum(axis=0)
cand = [x for x in range(0, 960) if colcnt[x] > 150]
print("col candidates:", [(x, int(colcnt[x])) for x in cand])

rowcnt = red[:, 120:800].sum(axis=1)
cand = [y for y in range(0, 540) if rowcnt[y] > 350]
print("row candidates:", [(y, int(rowcnt[y])) for y in cand])

# panel border is C00000 (bright red vs darker 8B0000): sample candidate columns
for x in cand:
    col = im[200:300, x]
    print("col", x, "mean rgb", col.mean(axis=0).round(0))
