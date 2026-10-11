# Pass 8: final disambiguation crops.
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def amap(x0, y0, x1, y1, label):
    print(f"== {label} x[{x0},{x1}] y[{y0},{y1}]  (col i -> x={x0}+i)")
    hdr = ''.join(str(((x0 + i) // 10) % 10) for i in range(x1 - x0))
    print("    " + hdr)
    for yy in range(y0, y1):
        row = []
        for xx in range(x0, x1):
            p = a[yy, xx]
            if b[yy, xx] > 120 and b[yy, xx] - p[0] > 40 and p[1] < b[yy, xx]: c = 'B'
            elif p[0] > 190 and 60 < p[1] < 190 and p[2] < 110: c = 'O'
            elif p[0] > 140 and p[1] < 120 and p[2] < 120: c = 'R'
            elif p[0] > 228 and p[1] > 228 and p[2] > 228: c = 'w'
            elif p[0] < 90 and p[1] < 90 and p[2] < 90: c = '#'
            else: c = '.'
            row.append(c)
        print(f"y{yy:3d} " + ''.join(row))

amap(225, 178, 292, 262, "in<->Boy corridor + blob")
amap(288, 382, 400, 438, "climbs<->tree corridor")
amap(300, 183, 348, 235, "garden icon check")

print("\n-- orange icon outline samples --")
for x, y in [(792, 375), (795, 375), (796, 350), (817, 375), (820, 375), (816, 350), (806, 333), (806, 416), (794, 340), (819, 340)]:
    p = a[y, x]
    print(f"   ({x},{y}) rgb=({p[0]},{p[1]},{p[2]}) #{p[0]:02X}{p[1]:02X}{p[2]:02X}")
