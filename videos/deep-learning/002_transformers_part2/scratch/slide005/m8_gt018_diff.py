# m8 (slide005): diff MY frame against 001's slide-018 frame (the certified composition
# that matches my annotation state). Affine fitted from the two frames' chrome landmarks.
from PIL import Image
import numpy as np
from collections import deque

def landmarks(path):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 110) & (r - g > 50) & (r - b > 40)
    colsum = red[60:500, :].sum(axis=0)
    rowsum = red[:, 80:880].sum(axis=1)
    lc = [x for x in range(0, 120) if colsum[x] > 150]
    rc = [x for x in range(860, 960) if colsum[x] > 150]
    tc = [y for y in range(20, 70) if rowsum[y] > 300]
    bc = [y for y in range(470, 540) if rowsum[y] > 300]
    return (np.mean(lc), np.mean(rc), np.mean(tc), np.mean(bc))

Lm, Rm, Tm, Bm = landmarks('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg')
L1, R1, T1, B1 = landmarks('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg')
print(f'my landmarks  L{Lm:.2f} R{Rm:.2f} T{Tm:.2f} B{Bm:.2f}')
print(f'001:18 landmk L{L1:.2f} R{R1:.2f} T{T1:.2f} B{B1:.2f}')

sx = (Rm - Lm) / (R1 - L1)
sy = (Bm - Tm) / (B1 - T1)
ox = Lm - sx * L1
oy = Tm - sy * T1
print(f'affine: frame_x = {ox:.4f} + {sx:.6f} * f1x ; frame_y = {oy:.4f} + {sy:.6f} * f1y')

def to_build(fx, fy):
    # through the certified 002 mapping (landmarks matched 002:19 within ~1px)
    return (fx - 18.0787) / 0.961084, (fy - 0.4700) / 0.957187

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
pI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
my = np.asarray(myI).astype(np.float32)
coeffs = (1.0/sx, 0.0, -ox/sx, 0.0, 1.0/sy, -oy/sy)
w = np.asarray(pI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)
Image.fromarray(w.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_018.png')

dd = np.abs(my - w).sum(axis=2)
print('panel diff mean %.2f' % dd[46:514, 60:900].mean())
strong = dd > 120
strong[:46, :] = False; strong[514:, :] = False; strong[:, :60] = False; strong[:, 900:] = False

lab = np.zeros(strong.shape, np.int32); nid = 0; comps = []
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
print(f'{len(comps)} components; >=25px:')
for pts in comps:
    if len(pts) < 25: break
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    bx0, by0 = to_build(x0, y0); bx1, by1 = to_build(x1, y1)
    cm = np.array([my[p] for p in pts]).mean(axis=0)
    cw = np.array([w[p] for p in pts]).mean(axis=0)
    def gd(c): return abs(c[0]-233)+abs(c[1]-233)+abs(c[2]-231)
    side = 'MINE' if gd(cm) > gd(cw) else 'GT18'
    print(f'  {len(pts):6d}px {side} frame x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  my={tuple(int(v) for v in cm)} gt18={tuple(int(v) for v in cw)}')

vis = np.asarray(myI).copy()
vis[strong] = [255, 0, 255]
Image.fromarray(vis).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/gt018_diff_overlay.png')
