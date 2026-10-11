# Pass 9: definitive map of left-middle region (all strokes between in/garden/the/Boy).
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

x0, x1, y0, y1, st = 140, 342, 138, 302, 2
print(f"map x[{x0},{x1}] y[{y0},{y1}] step {st}; col i -> x={x0}+{st}i")
print("     " + ''.join(str(((x0 + i * st) // 10) % 10) for i in range((x1 - x0) // st)))
for yy in range(y0, y1, st):
    row = []
    for i in range((x1 - x0) // st):
        xx = x0 + i * st
        blk = a[yy:yy + st, xx:xx + st]
        rr, gg, bb = blk[..., 0], blk[..., 1], blk[..., 2]
        redn = int(((rr > 140) & (gg < 120) & (bb < 120)).sum())
        row.append('#' if redn >= 3 else ('+' if redn >= 1 else '.'))
    print(f"y{yy:3d} " + ''.join(row))
