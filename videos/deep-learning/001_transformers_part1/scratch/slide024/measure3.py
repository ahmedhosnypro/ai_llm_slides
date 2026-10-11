# Pass 3: structural understanding — icon maps, node circles, red strokes, fills.
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def cls(px):
    r, g, b = px
    if r > 200 and g < 140 and b < 140: return 'R'          # red
    if r > 235 and g > 230 and 170 < b < 240: return 'y'    # pale yellow node
    if abs(r-g) < 25 and abs(g-b) < 25 and 120 < r < 200: return 'g'  # green node
    if b > 140 and b - r > 40 and g < b: return 'B'         # blue-ish
    if r > 200 and 100 < g < 180 and b < 120: return 'O'    # orange
    if r > 220 and 150 < g < 215 and 150 < b < 215: return 'p'  # pink
    if r > 228 and g > 228 and b > 228: return '.'          # white/gray bg
    if r < 90 and g < 90 and b < 90: return '#'             # black text
    return ' '

def amap(x0, y0, x1, y1, label, step=1):
    print(f"== {label} x[{x0},{x1}] y[{y0},{y1}] ({(x1-x0)//step}x{(y1-y0)//step})")
    for yy in range(y0, y1, step):
        print(''.join(cls(a[yy, xx]) for xx in range(x0, x1, step)))

# Boy input vector icon (x300-360, y310-375)
amap(300, 308, 362, 372, 'ICON Boy-input region')
