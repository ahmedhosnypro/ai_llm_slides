# selfcheck attempt 3: gap shafts + pin geometry on render_3 vs frame
from PIL import Image
import numpy as np
KX, KY, OX, OY = 2.16788, 2.17655, 18.0787, 0.4700
frame = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
fw = np.asarray(frame.transform((2001, 1125), Image.AFFINE, (1.0/KX, 0, OX, 0, 1.0/KY, OY), resample=Image.BILINEAR)).astype(int)
r = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019/render_3.png').convert('RGB')).astype(int)
S = 150.0/72.0
print('== gap shafts (darkest in x778..792 per build row):')
for tag, (by0, by1) in [('gap1', (194, 206)), ('gap2', (251, 263))]:
    for img, name in [(r, 'REND'), (fw, 'FRAM')]:
        dk = []
        for by in range(by0, by1):
            best = 999
            for bx in range(778, 792):
                best = min(best, int(img[int(by*S), int(bx*S)].sum()))
            dk.append(best)
        print(f'  {tag} {name}: {dk}')
print('== pin red blob (build pt):')
def red_blob(img, bx0, by0, bx1, by1):
    reg = img[int(by0*S):int(by1*S), int(bx0*S):int(bx1*S)]
    msk = (reg[...,0] > 120) & (reg[...,1] < 95) & (reg[...,2] < 95)
    ys, xs = np.where(msk)
    if not len(xs): return None
    return (round(min(xs)/S+bx0,1), round(min(ys)/S+by0,1), round(max(xs)/S+bx0,1), round(max(ys)/S+by0,1), int(msk.sum()))
print('  REND', red_blob(r, 525, 330, 615, 442))
print('  FRAM', red_blob(fw, 525, 330, 615, 442))
print('== tail tip: red rows near y420-436 (x extent) REND vs FRAM:')
for img, name in [(r, 'REND'), (fw, 'FRAM')]:
    for by in (420, 426, 432, 435):
        xs = [bx for bx in range(560, 620) if img[int(by*S), int(bx*S)][0] > 120 and img[int(by*S), int(bx*S)][1] < 95]
        print(f'  {name} y{by}: x {min(xs) if xs else None}..{max(xs) if xs else None}')
print('== white text px (3-line block):')
def white_ct(img, bx0, by0, bx1, by1):
    reg = img[int(by0*S):int(by1*S), int(bx0*S):int(bx1*S)]
    return int(((reg[...,0] > 185) & (reg[...,1] > 165) & (reg[...,2] > 165)).sum())
print('  REND', white_ct(r, 540, 340, 600, 400), ' FRAM', white_ct(fw, 540, 340, 600, 400))
print('== full-panel agreement: mean %.2f strong %.2f%% (certified baseline 23.05%%)' % (
    np.abs(r-fw).sum(axis=2)[100:1070,130:1880].mean(),
    100*(np.abs(r-fw).sum(axis=2)>130)[100:1070,130:1880].mean()))
