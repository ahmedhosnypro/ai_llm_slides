# m9: delta isolation. Warp 001's frame into MY frame space with the CONVERGED F21
# (a=20.9473 b=0.95679 c=2.2031 d=0.95651), diff, label connected delta components,
# report bboxes in frame px AND build pt (composite mapping).
from PIL import Image
import numpy as np
from collections import deque

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
# composite frame2 -> build (derived m8: b1=1.004491 a1=-2.998 d1=1.000708 c1=-1.812)
B1, A1, D1, C1 = 1.004491, -2.998, 1.000708, -1.812
def to_build(fx, fy):
    f1x = (fx - A)/Bx; f1y = (fy - C)/D
    bx = (f1x - A1)/B1; by = (f1y - C1)/D1
    return bx, by

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
parI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')
my = np.asarray(myI).astype(np.float32)
coeffs = (1.0/Bx, 0.0, -A/Bx, 0.0, 1.0/D, -C/D)
w = np.asarray(parI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)

Image.fromarray(w.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/warped_001_f21.png')

dd = np.abs(my - w).sum(axis=2)
print('panel diff mean %.2f' % dd[46:514, 60:900].mean())
strong = dd > 130
strong[:46, :] = False; strong[514:, :] = False; strong[:, :60] = False; strong[:, 900:] = False

# connected components (8-conn BFS)
lab = np.zeros(strong.shape, np.int32); nid = 0; comps = []
H, W = strong.shape
for y in range(46, 514):
    for x in range(60, 900):
        if strong[y, x] and lab[y, x] == 0:
            nid += 1; q = deque([(y, x)]); lab[y, x] = nid; pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy+dy, cx+dx
                        if 46 <= ny < 514 and 60 <= nx < 900 and strong[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = nid; q.append((ny, nx))
            comps.append(pts)

comps.sort(key=len, reverse=True)
print(f'{len(comps)} components; showing those with >=30 px:')
for pts in comps:
    if len(pts) < 30: break
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    bx0, by0 = to_build(x0, y0); bx1, by1 = to_build(x1, y1)
    # mean color of MY pixels in comp
    cols = np.array([my[p] for p in pts])
    print(f'  comp {len(pts):6d}px  frame bbox x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  meancolor {tuple(int(v) for v in cols.mean(axis=0))}')

# Save a red-overlay visualization of the strong mask for the record
vis = np.asarray(myI).copy()
vis[strong] = [255, 0, 255]
Image.fromarray(vis).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/delta_mask_overlay.png')
np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/delta_mask.npy', strong)
