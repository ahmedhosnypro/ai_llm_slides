from PIL import Image
import numpy as np
r = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/render_1.png').convert('RGB')).astype(int)
print('render size', r.shape)
# placeholder check: LO broken-image text renders as black "Image 0 1" glyphs — look for
# unexpected dark text rows in empty zones (e.g. y 0..80 outside badge/title area)
dark = (r.max(axis=2) < 100)
rows = [(y, int(dark[y].sum())) for y in range(0, 120) if dark[y].sum() > 30]
print('dark rows in top band (placeholder scan):', rows[:6])
# 150dpi: 1pt = 150/72 = 2.0833 px. render px -> slide pt: pt = px / 2.0833
S = 150/72
def rpx(v): return v * S   # slide pt -> render px
def rpt(p): return p / S   # render px -> slide pt
# frame -> slide mapping: slide = (fx-17.582)/0.962329 (x), fy/0.955556 (y)
# frame -> render px: rp = slide_pt * S
import math
def f2r_fx(fx): return (fx-17.582)/0.962329*S
def f2r_fy(fy): return fy/0.955556*S
# element ink checks: measured frame band -> expected render band; assert ink present & edges within ~4px (=8.3 render px)
checks = []
def inkband(img, x0, x1, y0, y1, test):
    seg = img[y0:y1, x0:x1]
    m = test(seg)
    rows = np.where(m.sum(axis=1) > 3)[0]
    return (rows.min()+y0, rows.max()+y0) if len(rows) else None
navy_t = lambda s: (s[:,:,2]>110)&(s[:,:,0]<100)&(s[:,:,1]<100)
gray_t = lambda s: (np.abs(s[:,:,0]-s[:,:,1])<=12)&(np.abs(s[:,:,1]-s[:,:,2])<=12)&(s[:,:,0]>=168)&(s[:,:,0]<=238)
# MHA bar: frame 419..468 -> render y 657..737
b = inkband(r, int(f2r_fx(300)), int(f2r_fx(700)), 630, 770, navy_t)
print('MHA bar render band:', b, 'expected', round(f2r_fy(419*1)), round(f2r_fy(468)))
# gray bars: top frame 102..128.5; bottom 312..338.5
for tag, f0, f1 in [('top bar', 102, 128.5), ('bottom bar', 312, 338.5)]:
    bb = inkband(r, int(f2r_fx(250)), int(f2r_fx(400)), int(f2r_fy(f0))-25, int(f2r_fy(f1))+25, gray_t)
    print(f'{tag}: render {bb} expected ~{f2r_fy(f0):.0f}..{f2r_fy(f1):.0f}')
# token rows (lavender cell col1): frame tops 65,173,278,384,487
lav_t = lambda s: (np.abs(s - np.array([0xD8,0xBF,0xD8])).max(axis=2) <= 35)
for tag, f0, f1 in [('final',65,81),('postFFN',173,188),('postLN',278,295),('outatt',384,400),('X',487,503)]:
    x0 = int(f2r_fx(216)); x1 = int(f2r_fx(228))
    bb = inkband(r, x0, x1, int(f2r_fy(f0))-12, int(f2r_fy(f1))+12, lav_t)
    print(f'row {tag}: render {bb} expected ~{f2r_fy(f0):.0f}..{f2r_fy(f1):.0f}')
# plus discs: dark red at col1, top cy 155.4, bottom cy 376.25 slide -> render y 323.8 / 783.9
dr_t = lambda s: (s[:,:,0]>110)&(s[:,:,1]<70)&(s[:,:,2]<70)
for tag, cy in [('top plus', 155.4), ('bottom plus', 376.25)]:
    yc = int(rpx(cy))
    bb = inkband(r, int(rpx(194.9-10)), int(rpx(194.9+10)), yc-20, yc+20, dr_t)
    print(f'{tag}: render {bb} expected ~{yc-7}..{yc+7}')
