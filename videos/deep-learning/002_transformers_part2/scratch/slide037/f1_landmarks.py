# f1: locate MY frame's (002:37) four chrome landmarks (red panel border + badge).
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 130) & (g < 90) & (b < 90)

def col_red_counts(x0, x1, y0=60, y1=500):
    return {x: int(red[y0:y1, x].sum()) for x in range(x0, x1)}

def row_red_counts(y0, y1, x0=80, x1=880):
    return {y: int(red[y, x0:x1].sum()) for y in range(y0, y1)}

left = {x: c for x, c in col_red_counts(30, 95).items() if c > 200}
right = {x: c for x, c in col_red_counts(865, 945).items() if c > 200}
top = {y: c for y, c in row_red_counts(20, 70).items() if c > 300}
bot = {y: c for y, c in row_red_counts(470, 540).items() if c > 300}
print('LEFT candidates (x:count):', left)
print('RIGHT candidates:', right)
print('TOP candidates:', top)
print('BOTTOM candidates:', bot)

# badge: yellow circle top-right + purple ring
yel = (r > 190) & (g > 190) & (b < 170)
ys, xs = np.where(yel[0:130, 820:960])
if len(xs):
    print('badge yellow bbox x', xs.min()+820, xs.max()+820, 'y', ys.min(), ys.max(),
          'center', (xs.min()+xs.max())/2+820, (ys.min()+ys.max())/2)
pur = (b > r + 30) & (b > g + 40) & (b > 120) & (r > 60) & (r < 190)
seg = pur[50:95, 840:915]
ys2, xs2 = np.where(seg)
if len(xs2):
    print('purple ring bbox x', xs2.min()+840, xs2.max()+840, 'y', ys2.min()+50, ys2.max()+50,
          'center', (xs2.min()+xs2.max())/2+840, (ys2.min()+ys2.max())/2+50)

# letterbox black bar at bottom?
print('row 520 sample:', [tuple(a[520, x]) for x in (100, 480, 900)])
print('row 512 sample:', [tuple(a[512, x]) for x in (100, 480, 900)])
