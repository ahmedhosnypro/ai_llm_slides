# selfcheck attempt 1: render_1 (2001x1125 @150dpi) vs MY frame mapped to render space.
# render_px = (frame_px - offset) * k ; kx = (150/72)/0.961084 = 2.16788 (x), ky = 2.17655 (y)
from PIL import Image
import numpy as np
from collections import deque

FR = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg'
frame = Image.open(FR).convert('RGB')
rend = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019/render_1.png').convert('RGB')).astype(np.float32)

KX, KY, OX, OY = 2.16788, 2.17655, 18.0787, 0.4700
coeffs = (1.0/KX, 0, OX, 0, 1.0/KY, OY)
fw = np.asarray(frame.transform((2001, 1125), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)
Image.fromarray(fw.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/frame_in_render_space.png')

dd = np.abs(rend - fw).sum(axis=2)
panel = dd[100:1070, 130:1880]
print(f'panel diff: mean {panel.mean():.2f}  p99 {np.percentile(panel, 99):.0f}  max {panel.max():.0f}')
strong = dd > 130
strong[:100, :] = False; strong[1070:, :] = False; strong[:, :130] = False; strong[:, 1880:] = False
ys, xs = np.where(strong)
print(f'strong-diff px: {len(xs)} ({100*len(xs)/strong.size:.2f}% of panel)')
lab = np.zeros(strong.shape, np.int32); comps = []
for y, x in zip(ys, xs):
    if lab[y, x] == 0:
        nid = len(comps)+1; q = deque([(y, x)]); lab[y, x] = nid; pts = []
        while q:
            cy, cx = q.popleft(); pts.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy+dy, cx+dx
                    if 100 <= ny < 1070 and 130 <= nx < 1880 and strong[ny, nx] and lab[ny, nx] == 0:
                        lab[ny, nx] = nid; q.append((ny, nx))
        comps.append(pts)
comps.sort(key=len, reverse=True)
def bld(rx, ry): return rx/2.16788 + OX, ry/2.17655 + OY
print('components >=60px (build pt):')
for pts in comps:
    if len(pts) < 60: break
    ys_ = [p[0] for p in pts]; xs_ = [p[1] for p in pts]
    bx0, by0 = bld(min(xs_), min(ys_)); bx1, by1 = bld(max(xs_), max(ys_))
    cols = np.array([fw[p] for p in pts[:400]]).mean(axis=0)
    print(f'  {len(pts):6d}px render x{min(xs_)}..{max(xs_)} y{min(ys_)}..{max(ys_)} -> build ({bx0:.0f},{by0:.0f})..({bx1:.0f},{by1:.0f}) mean frame-col {tuple(int(v) for v in cols)}')
