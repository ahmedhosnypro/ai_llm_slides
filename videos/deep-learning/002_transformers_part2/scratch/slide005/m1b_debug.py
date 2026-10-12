# m1b (slide005): debug — sample pixel profiles near expected chrome landmarks.
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# scan for reddish columns anywhere (looser thresholds, wider sweep)
red = (r > 110) & (r - g > 50) & (r - b > 40)
colsum = red[60:500, :].sum(axis=0)
rowsum = red[:, 80:880].sum(axis=1)
print('columns with red count > 150:', {x: int(c) for x, c in enumerate(colsum) if c > 150})
print('rows with red count > 250:', {y: int(c) for y, c in enumerate(rowsum) if c > 250})

# sample colors: top-left corner area (letterbox?), border near x58?
for (x, y) in [(5, 5), (5, 270), (30, 270), (58, 270), (60, 270), (901, 270), (910, 270), (955, 270),
               (300, 40), (300, 43), (300, 46), (480, 517), (480, 514), (300, 520)]:
    print((x, y), tuple(a[y, x]))

# yellow pixels in top-right corner region x800..960 y30..140
yel = (r > 200) & (g > 190) & (b < 150)
ys, xs = np.where(yel[0:150, 780:960])
if len(xs):
    print('yellow corner bbox x', xs.min()+780, xs.max()+780, 'y', ys.min(), ys.max(), 'n=', len(xs))
# column histogram of yellow in that region
import collections
colc = collections.Counter(xs + 780)
print('yellow col counts:', sorted(colc.items()))
