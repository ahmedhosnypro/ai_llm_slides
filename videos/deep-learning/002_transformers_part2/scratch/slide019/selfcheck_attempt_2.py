# selfcheck attempt 2: re-verify delta regions on render_2 + frame_in_render_space
from PIL import Image
import numpy as np
KX, KY, OX, OY = 2.16788, 2.17655, 18.0787, 0.4700
frame = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
fw = np.asarray(frame.transform((2001, 1125), Image.AFFINE, (1.0/KX, 0, OX, 0, 1.0/KY, OY), resample=Image.BILINEAR)).astype(int)
r = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019/render_2.png').convert('RGB')).astype(int)
S = 150.0/72.0
def R(bx, by): return bx*S, by*S
yel = lambda p: p[0] > 170 and p[1] > 170 and p[2] < 150
def fl_v(img, bx, y0, y1):
    x, _ = R(bx, 0); f = l = None
    for by in range(y0, y1):
        _, y = R(0, by)
        if yel(img[int(y), int(x)]):
            if f is None: f = by
            l = by
    return f, l
def fl_h(img, by, x0, x1):
    _, y = R(0, by); f = l = None
    for bx in range(x0, x1):
        x, _ = R(bx, 0)
        if yel(img[int(y), int(x)]):
            if f is None: f = bx
            l = bx
    return f, l
print('band edges (REND / FRAME), tol ~2 build pt:')
for bx in (600, 700, 800, 860):
    print(f'  bx{bx}: top {fl_v(r,bx,395,440)} / {fl_v(fw,bx,395,440)}  bottom {fl_v(r,bx,460,506)} / {fl_v(fw,bx,460,506)}')
for by in (430, 460, 485):
    print(f'  by{by}: left {fl_h(r,by,540,620)} / {fl_h(fw,by,540,620)}  right {fl_h(r,by,860,922)} / {fl_h(fw,by,860,922)}')
# pin blob (absolute build coords this time)
def red_blob(img, bx0, by0, bx1, by1):
    x0, y0 = R(bx0, by0); x1, y1 = R(bx1, by1)
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    msk = (reg[...,0] > 120) & (reg[...,1] < 95) & (reg[...,2] < 95)
    ys, xs = np.where(msk)
    if not len(xs): return None
    return (round(min(xs)/S+bx0,1), round(min(ys)/S+by0,1), round(max(xs)/S+bx0,1), round(max(ys)/S+by0,1), int(msk.sum()))
print('pin blob REND', red_blob(r, 525, 330, 615, 442))
print('pin blob FRAME', red_blob(fw, 525, 330, 615, 442))
# full-panel agreement rate vs certified baseline
d2 = np.abs(r - fw).sum(axis=2)
print(f'render_2 vs frame: mean {d2[100:1070,130:1880].mean():.2f} strong {100*(d2>130)[100:1070,130:1880].mean():.2f}% (baseline 23.05%)')
