# targeted closed-loop checks, CORRECT build->render map: render_px = build_pt * 150/72
from PIL import Image
import numpy as np
from collections import Counter

S = 150.0 / 72.0  # 2.08333
fw = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/frame_in_render_space.png').convert('RGB')).astype(int)
r = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019/render_1.png').convert('RGB')).astype(int)
def R(bx, by): return bx * S, by * S

def census(img, bx0, by0, bx1, by1, n=4):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)].reshape(-1, 3)
    q = reg // 32 * 32
    c = Counter(map(tuple, q)); tot = len(reg)
    return ', '.join(f'{a},{b_},{c_} {int(100*k/tot)}%' for (a, b_, c_), k in c.most_common(n))

print('== A. legend regions (must be panel-gray in BOTH):')
for name, bb in [('legend1', (141, 100, 344, 132)), ('legend2', (309, 141, 516, 173)), ('legend3', (262, 179, 467, 211))]:
    print(f'  {name}: REND {census(r, *bb)} | FRAME {census(fw, *bb)}')

print('== C. chevron zones navy count:')
def navy_count(img, bx0, by0, bx1, by1):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    return int(((reg[...,0] < 80) & (reg[...,1] < 80) & (reg[...,2] > 90)).sum())
for name, bb in [('zone1', (776, 190, 792, 208)), ('zone2', (776, 249, 792, 266)), ('zone3', (765, 306, 780, 324))]:
    print(f'  {name}: REND navy={navy_count(r, *bb)}  FRAME navy={navy_count(fw, *bb)}')

print('== D. band edges (tol ~4px@150dpi = ~2 build pt):')
yel = lambda p: p[0] > 170 and p[1] > 170 and p[2] < 150
def first_last_v(img, bx, y0, y1):
    x, _ = R(bx, 0); first = last = None
    for by in range(y0, y1):
        _, y = R(0, by)
        if 0 <= int(y) < img.shape[0] and yel(img[int(y), int(x)]):
            if first is None: first = by
            last = by
    return first, last
def first_last_h(img, by, x0, x1):
    _, y = R(0, by); first = last = None
    for bx in range(x0, x1):
        x, _ = R(bx, 0)
        if yel(img[int(y), int(x)]):
            if first is None: first = bx
            last = bx
    return first, last
for bx in (600, 700, 800, 860):
    print(f'  bx{bx}: top R/F {first_last_v(r, bx, 395, 440)} / {first_last_v(fw, bx, 395, 440)}  bottom R/F {first_last_v(r, bx, 460, 508)} / {first_last_v(fw, bx, 460, 508)}')
for by in (430, 460, 485):
    print(f'  by{by}: left R/F {first_last_h(r, by, 540, 620)} / {first_last_h(fw, by, 540, 620)}  right R/F {first_last_h(r, by, 860, 922)} / {first_last_h(fw, by, 860, 922)}')

print('== E. pin geometry:')
def red_blob(img, bx0, by0, bx1, by1):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    msk = (reg[...,0] > 120) & (reg[...,1] < 95) & (reg[...,2] < 95)
    ys, xs = np.where(msk)
    if not len(xs): return None
    return (round(min(xs)/S,1), round(min(ys)/S,1), round(max(xs)/S,1), round(max(ys)/S,1), int(msk.sum()))
print('  head+tail bbox REND', red_blob(r, 520, 325, 620, 445))
print('  head+tail bbox FRAME', red_blob(fw, 520, 325, 620, 445))
def white_in_head(img):
    x0, y0 = R(540, 340); x1, y1 = R(600, 400)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    return int(((reg[...,0] > 185) & (reg[...,1] > 165) & (reg[...,2] > 165)).sum())
print('  white text px: REND', white_in_head(r), ' FRAME', white_in_head(fw))

print('== F. inherited spot checks (should closely match):')
for name, bb in [('title', (400, 40, 560, 80)), ('N x circle', (795, 265, 830, 295)), ('enc FF box', (655, 290, 718, 314))]:
    print(f'  {name}: REND {census(r, *bb, 3)}')
    print(f'  {name}: FRAME {census(fw, *bb, 3)}')
