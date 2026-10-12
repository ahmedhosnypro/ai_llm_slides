# targeted closed-loop checks on render_1 vs MY frame (both in render space)
from PIL import Image
import numpy as np
from collections import Counter

KX, KY, OX, OY = 2.16788, 2.17655, 18.0787, 0.4700
fw = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/frame_in_render_space.png').convert('RGB')).astype(int)
r = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019/render_1.png').convert('RGB')).astype(int)
def R(bx, by): return (bx - OX) * KX, (by - OY) * KY  # build pt -> render px

def census(img, bx0, by0, bx1, by1, n=4):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)].reshape(-1, 3)
    q = reg // 32 * 32
    c = Counter(map(tuple, q))
    tot = len(reg)
    return ', '.join(f'{a},{b_},{c_} {int(100*k/tot)}%' for (a, b_, c_), k in c.most_common(n))

print('== A. legend regions must be panel-gray in RENDER (like frame):')
for name, bb in [('legend1', (141, 100, 344, 132)), ('legend2', (309, 141, 516, 173)), ('legend3', (262, 179, 467, 211))]:
    print(f'  {name}: REND {census(r, *bb)}')
    print(f'  {name}: FRAME {census(fw, *bb)}')

print('== B. leader paths: max darkness along paths (200 = clean gray):')
def path_dark(img, pts):
    worst = 800; wp = None
    for (bx, by) in pts:
        x, y = R(bx, by); xi, yi = int(x), int(y)
        for yy in range(yi-3, yi+4):
            for xx in range(xi-3, xi+4):
                s = int(img[yy, xx].sum())
                if s < worst: worst, wp = s, (xx, yy)
    return worst, wp
L = {
 'L1': [(342,118),(470,120),(570,124),(622,138),(680,147),(726,152),(751,161)],
 'L2': [(464,122),(538,134),(570,143),(622,167),(700,172),(726,173),(740,181),(751,186)],
 'L3': [(514,157),(570,161),(622,183),(654,193),(676,224),(700,231),(738,236)],
 'L4': [(513,152),(538,161),(562,176),(578,206),(594,264),(610,290),(622,296),(638,301)],
 'L5': [(460,195),(506,201),(526,210),(538,225),(550,251),(562,296),(570,318),(584,330),(597,337)],
}
for k, pts in L.items():
    print(f'  {k}: REND darkest {path_dark(r, pts)}  FRAME {path_dark(fw, pts)}')

print('== C. chevron zones navy check:')
def navy_count(img, bx0, by0, bx1, by1):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    return int(((reg[...,0] < 80) & (reg[...,1] < 80) & (reg[...,2] > 90)).sum())
for name, bb in [('zone1 (783.5,197/202)', (776, 190, 792, 208)), ('zone2 (783.5,255/259)', (776, 249, 792, 266)), ('zone3 (772,313/318)', (765, 306, 780, 324))]:
    print(f'  {name}: REND navy={navy_count(r, *bb)}  FRAME navy={navy_count(fw, *bb)}')

print('== D. band edges (render vs frame), tolerance ~4px@150dpi:')
def edge_scan(img, fixed, along, axis, rng, pred):
    hits = []
    for v in rng:
        x, y = (fixed, v) if axis == 'y' else (v, fixed)
        if pred(img[int(y), int(x)]): hits.append(v)
    return (min(hits), max(hits)) if hits else None
yel = lambda p: p[0] > 170 and p[1] > 170 and p[2] < 150
for label, fixed, rng, axis in [('top edge @bx700', 700, range(R(0, 400)[1] and int(R(700,400)[1])-14, int(R(700,430)[1])), 'y'),
                                 ('bottom edge @bx700', 700, range(int(R(700,480)[1]), int(R(700,510)[1])), 'y')]:
    pass
# simpler: explicit scans
def first_yel_v(img, bx, y_from, y_to):
    x, _ = R(bx, 0)
    for by in range(y_from, y_to):
        _, y = R(0, by)
        if yel(img[int(y), int(x)]): return by
    return None
def last_yel_v(img, bx, y_from, y_to):
    x, _ = R(bx, 0)
    last = None
    for by in range(y_from, y_to):
        _, y = R(0, by)
        if yel(img[int(y), int(x)]): last = by
    return last
for bx in (600, 700, 800, 860):
    print(f'  bx{bx}: top REND {first_yel_v(r, bx, 395, 440)} FRAME {first_yel_v(fw, bx, 395, 440)} | bottom REND {last_yel_v(r, bx, 460, 520)} FRAME {last_yel_v(fw, bx, 460, 520)}')
def first_yel_h(img, by, x_from, x_to):
    _, y = R(0, by)
    for bx in range(x_from, x_to):
        x, _ = R(bx, 0)
        if yel(img[int(y), int(x)]): return bx
    return None
def last_yel_h(img, by, x_from, x_to):
    _, y = R(0, by)
    last = None
    for bx in range(x_from, x_to):
        x, _ = R(bx, 0)
        if yel(img[int(y), int(x)]): last = bx
    return last
for by in (430, 460, 485):
    print(f'  by{by}: left REND {first_yel_h(r, by, 540, 620)} FRAME {first_yel_h(fw, by, 540, 620)} | right REND {last_yel_h(r, by, 860, 925)} FRAME {last_yel_h(fw, by, 860, 925)}')

print('== E. pin geometry:')
def red_blob_bbox(img, bx0, by0, bx1, by1):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    msk = (reg[...,0] > 120) & (reg[...,1] < 95) & (reg[...,2] < 95)
    ys, xs = np.where(msk)
    if not len(xs): return None
    bx_a = min(xs)/KX + OX; bx_b = max(xs)/KX + OX
    by_a = min(ys)/KY + OY; by_b = max(ys)/KY + OY
    return (round(bx_a,1), round(by_a,1), round(bx_b,1), round(by_b,1), int(msk.sum()))
print('  pin head+tail bbox REND', red_blob_bbox(r, 520, 325, 620, 445), ' FRAME', red_blob_bbox(fw, 520, 325, 620, 445))
def white_in_head(img):
    x0, y0 = R(540, 340); x1, y1 = R(600, 400)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    return int(((reg[...,0] > 185) & (reg[...,1] > 165) & (reg[...,2] > 165)).sum())
print('  white text px in head: REND', white_in_head(r), ' FRAME', white_in_head(fw))

print('== F. containment: pin/band inside house frame (x>15, x<919, y<540):')
print('  pin right edge', 603.4, '< 919 ; band right edge', 910.5, '< 919 ; band bottom', 495.5, '< 540 : OK by construction')
