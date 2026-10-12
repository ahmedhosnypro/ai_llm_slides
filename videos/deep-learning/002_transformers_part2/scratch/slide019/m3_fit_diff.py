# m3: sub-pixel border centroids -> fit frame<->slide mapping; then warp 001's
# certified slide-019 frame into MY frame space and diff (delta isolation).
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg'
P = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg'
my = np.asarray(Image.open(F).convert('RGB')).astype(float)
par = Image.open(P).convert('RGB')

def redness(px):  # how "C00000 red" a pixel is
    r, g, b = px[...,0], px[...,1], px[...,2]
    return np.clip(r - (g + b)/2, 0, None)

def v_centroid(img, y0, y1, x0, x1):
    band = img[y0:y1, x0:x1]
    w = redness(band).sum(axis=1)
    ys = np.arange(y0, y1)
    m = w > w.max()*0.15
    return float((ys[m]*w[m]).sum()/w[m].sum())

def h_centroid(img, x0, x1, y0, y1):
    band = img[y0:y1, x0:x1]
    w = redness(band).sum(axis=0)
    xs = np.arange(x0, x1)
    m = w > w.max()*0.15
    return float((xs[m]*w[m]).sum()/w[m].sum())

L = h_centroid(my, 54, 64, 100, 450)   # frame left border center
R = h_centroid(my, 896, 906, 100, 450) # frame right border center
T = v_centroid(my, 39, 48, 100, 850)   # frame top border center
B = v_centroid(my, 513, 520, 100, 850) # frame bottom border center
print(f'landmarks L={L:.2f} R={R:.2f} T={T:.2f} B={B:.2f}')

# slide chrome landmarks (house): panel left 42, right edge 919 (rect x42 w877+1),
# top 45, bottom 540 (stroke half-visible)
b_x = (R - L) / (919 - 42)
a_x = L - b_x * 42
d_y = (B - T) / (540 - 45)
c_y = T - d_y * 45
print(f'MAP frame_x = {a_x:.4f} + {b_x:.5f}*slide_x ; frame_y = {c_y:.4f} + {d_y:.5f}*slide_y')
# inverse
print(f'INV slide_x = (frame_x - {a_x:.4f})/{b_x:.5f} ; slide_y = (frame_y - {c_y:.4f})/{d_y:.5f}')
# badge cross-check: frame ring center (875.5, 71.0)
bx = (875.5 - a_x)/b_x; by = (71.0 - c_y)/d_y
print(f'badge frame(875.5,71.0) -> slide ({bx:.1f},{by:.1f})  [house 893,71]')

# warp 001 frame -> MY frame space: out(fx,fy) = in(sx,sy), sx=(fx-a)/b, sy=(fy-c)/d
coeffs = (1/b_x, 0, -a_x/b_x, 0, 1/d_y, -c_y/d_y)
warped = par.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)
warped.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/warped_001_in_002frame.png')

wa = np.asarray(warped).astype(float)
# diff only inside the panel (borders excluded): x 60..899, y 46..514
d = np.abs(my - wa).sum(axis=2)
mask = np.zeros(d.shape, bool)
mask[46:514, 60:900] = True
dm = np.where(mask, d, 0)
print('diff stats inside panel: mean %.2f  p99 %.0f  max %.0f' % (dm.mean(), np.percentile(dm[mask], 99), dm[mask].max()))
strong = dm > 150
ys, xs = np.where(strong)
if len(xs):
    print('strong-diff pixel count:', len(xs))
    # cluster by coarse grid cells of 20px to name regions
    from collections import Counter
    cells = Counter((int(x)//20*20, int(y)//20*20) for x, y in zip(xs, ys))
    top = sorted(cells.items(), key=lambda kv: -kv[1])[:40]
    print('top 20px-cells (x,y):count:')
    for (cx, cy), n in top:
        print(f'  ({cx:4d},{cy:4d}) {n}')
