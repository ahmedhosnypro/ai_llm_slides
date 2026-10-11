# Surgical pass 2: sample actual fills of nodes, icons, arrow, box; find red arrow strokes.
from PIL import Image
import numpy as np
from collections import Counter
from scipy import ndimage

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def crop_hist(x0, y0, x1, y1, label, topn=8):
    c = a[y0:y1, x0:x1].reshape(-1, 3)
    q = (c // 24 * 24)
    cnt = Counter(map(tuple, q))
    print(f"== {label} crop x[{x0},{x1}] y[{y0},{y1}] top colors (quantized/24):")
    for col, n in cnt.most_common(topn):
        print(f"   rgb{col} ~ #{col[0]:02X}{col[1]:02X}{col[2]:02X}  n={n}")

# node center samples (spec positions, px)
for name, cx, cy in [('in',192,140),('garden',355,157),('the',115,286),('Boy',259,281),('tree',422,356),('climbs',250,437)]:
    patch = a[cy-4:cy+4, cx-4:cx+4].reshape(-1,3).mean(axis=0).round().astype(int)
    print(f"node {name:7s} @({cx},{cy}) avg rgb={tuple(patch)} #{patch[0]:02X}{patch[1]:02X}{patch[2]:02X}")

crop_hist(490, 260, 660, 340, 'block arrow region')
crop_hist(480, 100, 900, 150, 'sentence box region')
crop_hist(290, 305, 350, 375, 'Boy vector icon region')

# find the sentence box border: dark blue 2233CC
db = (np.abs(a - np.array([0x22, 0x33, 0xCC])).sum(axis=2) < 150)
ys, xs = np.nonzero(db)
if len(xs):
    print(f"darkblue mask bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(xs)}")
    lab, n = ndimage.label(db)
    sizes = ndimage.sum(db, lab, range(1, n+1))
    for i in np.argsort(sizes)[::-1][:6]:
        m = lab == i+1
        ys2, xs2 = np.nonzero(m)
        print(f"  db[{i+1}] x[{xs2.min()},{xs2.max()}] y[{ys2.min()},{ys2.max()}] n={int(sizes[i])}")

# red arrows: cluster strokes
red = (np.abs(a - np.array([0xEE, 0x00, 0x00])).sum(axis=2) < 160)
lab, n = ndimage.label(red, structure=np.ones((3,3)))
print(f"red clusters (n={n}, >=30px):")
for i in range(1, n+1):
    m = lab == i
    if m.sum() < 30: continue
    ys2, xs2 = np.nonzero(m)
    print(f"  red[{i:3d}] x[{xs2.min():3d},{xs2.max():3d}] y[{ys2.min():3d},{ys2.max():3d}] w={xs2.max()-xs2.min()+1:3d} h={ys2.max()-ys2.min()+1:3d} n={m.sum()}")
