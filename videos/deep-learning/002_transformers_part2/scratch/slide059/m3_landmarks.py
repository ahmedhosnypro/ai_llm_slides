from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red = (r - g > 55) & (r - b > 55)

# right panel border: cols 880..915, rows 150..350
colcnt = red[150:350, :].sum(axis=0)
print("right candidates:", [(x, int(colcnt[x])) for x in range(885, 915) if colcnt[x] > 50])
# top panel border: rows 30..70, cols 300..700
rowcnt = red[:, 300:700].sum(axis=1)
print("top candidates:", [(y, int(rowcnt[y])) for y in range(30, 75) if rowcnt[y] > 200])
# bottom stroke: rows 505..530, cols 300..700
print("bottom candidates:", [(y, int(rowcnt[y])) for y in range(505, 530) if rowcnt[y] > 200])

# sample the border colors
for (x, y, lbl) in [(58, 250, "left border"), (901, 250, "right border?"), (480, 43, "top border?"), (480, 517, "bottom stroke")]:
    print((x, y), lbl, tuple(im[y, x]))
# check columns 899..904 at a clean row
print("row250 cols 896..906:", [tuple(im[250, x]) for x in range(896, 907)])
print("col480 rows 40..48:", [tuple(im[y, 480]) for y in range(40, 49)])
print("col480 rows 513..521:", [tuple(im[y, 480]) for y in range(513, 522)])
