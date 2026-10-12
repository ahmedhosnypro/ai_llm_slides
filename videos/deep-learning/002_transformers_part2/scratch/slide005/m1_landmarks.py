# m1 (slide005): locate MY frame's four chrome landmarks (red panel border + badge)
# and compare with 002:19's measured landmarks (L 58.3, R 901.4, T 43.3, B 516.9).
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
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

yel = (r > 190) & (g > 190) & (b < 170)
ys, xs = np.where(yel[0:130, 820:960])
if len(xs):
    print('badge yellow bbox x', xs.min()+820, xs.max()+820, 'y', ys.min(), ys.max(),
          'center', (xs.min()+xs.max())/2+820, (ys.min()+ys.max())/2)

# letterbox black strip: bottom rows full-width dark
dark = (r < 60) & (g < 60) & (b < 60)
for y in (515, 518, 520, 522, 524, 526, 530, 539):
    print('row', y, 'dark frac %.3f' % dark[y, :].mean())
