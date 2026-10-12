# m6 (slide005): diff MY frame against the CERTIFIED 002:19 render (render_5.png,
# the judge-PASS composition) mapped into my frame space. Render px -> build pt is
# x*72/150 (zero offset, selfcheck lesson); build pt -> my frame px via the certified
# mapping. Components >=25px reported: my-additions vs render-only (skip candidates).
from PIL import Image
import numpy as np
from collections import deque

RX2F = 0.961084 * 72.0 / 150.0   # render px -> frame px scale
RY2F = 0.957187 * 72.0 / 150.0
FX0, FY0 = 18.0787, 0.4700

def to_build(fx, fy):
    return (fx - FX0) / 0.961084, (fy - FY0) / 0.957187

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
rI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019/render_5.png').convert('RGB')
my = np.asarray(myI).astype(np.float32)
coeffs = (1.0/RX2F, 0.0, -FX0/RX2F, 0.0, 1.0/RY2F, -FY0/RY2F)
rw = np.asarray(rI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)
Image.fromarray(rw.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_render5.png')

dd = np.abs(my - rw).sum(axis=2)
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
    cr = np.array([rw[p] for p in pts]).mean(axis=0)
    # which side is "content"? compare mean abs from panel gray
    def graydist(c): return abs(c[0]-233)+abs(c[1]-233)+abs(c[2]-231)
    side = 'MINE' if graydist(cm) > graydist(cr) else 'REND'
    print(f'  {len(pts):6d}px {side} frame x{x0}..{x1} y{y0}..{y1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  my={tuple(int(v) for v in cm)} rend={tuple(int(v) for v in cr)}')

vis = np.asarray(myI).copy()
vis[strong] = [255, 0, 255]
Image.fromarray(vis).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/render_diff_overlay.png')
