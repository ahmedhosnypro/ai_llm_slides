from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
# dark pixels (cursor is black)
dark = (r < 90) & (g < 90) & (b < 90)
ys, xs = np.nonzero(dark)
print("dark px:", len(xs))
if len(xs):
    print("dark bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max())
    # cluster roughly: histogram by 40px cells
    from collections import Counter
    cells = Counter((x//40*40, y//40*40) for x, y in zip(xs, ys))
    print("dark clusters (cell, count):", cells.most_common(10))
# non-white, non-gray, non-red, non-yellow, non-purple pixels anywhere?
other = ~(((r>225)&(g>225)&(b>225)) | ((abs(r-233)<12)&(abs(g-233)<12)&(abs(b-231)<14)) |
          ((r>120)&(r-g>60)&(r-b>60)) | ((r>200)&(g>200)&(b<170)) |
          ((b>140)&(r>70)&(r<190)&(b-g>35)))
ys2, xs2 = np.nonzero(other)
print("other px:", len(xs2))
if len(xs2):
    from collections import Counter
    cells2 = Counter((x//60*60, y//60*60) for x, y in zip(xs2, ys2))
    print("other clusters:", cells2.most_common(12))
