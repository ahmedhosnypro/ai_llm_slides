from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# scanline y=200: find transitions from white to gray/red
row = a[200]
print('scanline y=200, x 45..70:', [(x, tuple(row[x])) for x in range(45, 70)])
print('scanline y=200, x 895..912:', [(x, tuple(row[x])) for x in range(895, 913)])
col = a[:,500]
print('col x=500, y 38..55:', [(y, tuple(col[y])) for y in range(38, 56)])
print('col x=500, y 505..525:', [(y, tuple(col[y])) for y in range(505, 526)])
# badge zone colors: print a grid of the crop
crop = a[40:100, 850:910]
# find the circle: print rows 40..100 summary of distinct colors
for y in range(45, 100, 5):
    seg = a[y, 850:915]
    nz = [(x+850, tuple(seg[x])) for x in range(0, 65, 4)]
    print('y', y, nz)
