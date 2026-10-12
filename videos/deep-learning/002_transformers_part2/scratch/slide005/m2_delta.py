# m2 (slide005): delta isolation. Warp 001's slide-019 frame into MY (002:5) frame
# space with the F21 affine (validated for this capture position; landmarks match
# 002:19's within ~1px), diff, label connected delta components, report bboxes in
# frame px AND build pt (composite mapping from certified slide_019.js header:
# frame_x = 18.0787 + 0.961084*build_x ; frame_y = 0.4700 + 0.957187*build_y).
from PIL import Image
import numpy as np
from collections import deque

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651  # 001frame -> 002frame (F21)

def to_build(fx, fy):
    return (fx - 18.0787) / 0.961084, (fy - 0.4700) / 0.957187

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
parI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')
my = np.asarray(myI).astype(np.float32)
coeffs = (1.0/Bx, 0.0, -A/Bx, 0.0, 1.0/D, -C/D)
w = np.asarray(parI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)

Image.fromarray(w.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_f21.png')

dd = np.abs(my - w).sum(axis=2)
print('panel diff mean %.2f' % dd[46:514, 60:900].mean())
strong = dd > 130
strong[:46, :] = False; strong[514:, :] = False; strong[:, :60] = False; strong[:, 900:] = False

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
print(f'{len(comps)} components; those with >=25 px:')
for pts in comps:
    if len(pts) < 25: break
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    bx0, by0 = to_build(x0, y0); bx1, by1 = to_build(x1, y1)
    cols_m = np.array([my[p] for p in pts])
    cols_w = np.array([w[p] for p in pts])
    print(f'  comp {len(pts):6d}px  frame x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  my={tuple(int(v) for v in cols_m.mean(axis=0))} warpgt={tuple(int(v) for v in cols_w.mean(axis=0))}')

vis = np.asarray(myI).copy()
vis[strong] = [255, 0, 255]
Image.fromarray(vis).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/delta_mask_overlay.png')
np.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/delta_mask.npy', strong)
