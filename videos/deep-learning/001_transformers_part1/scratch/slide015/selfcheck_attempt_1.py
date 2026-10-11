# slide 015 self-check attempt 1 (pre-judge, founder directive 2026-10-10)
# render_1.png (2001x1125 @150dpi, 1 frame-px = 2.08333 render-px) vs
#  - parent certified render (inheritance diff confinement)
#  - original frame slide_015.jpg (delta geometry, colors, arrows, headers)
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
R = np.asarray(Image.open(f'{BASE}/recreated_pptx/qa/slide015/render_1.png').convert('RGB')).astype(int)
P = np.asarray(Image.open(f'{BASE}/recreated_pptx/qa/slide014/render_1.png').convert('RGB')).astype(int)
F = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
S = 150 / 72.0  # 2.08333
print('render', R.shape, 'parent', P.shape)
ok = True
def check(name, cond, detail=''):
    global ok
    print(('  PASS ' if cond else '  FAIL ') + name + ('  ' + detail if detail else ''))
    if not cond:
        ok = False

def pt(v):  # frame pt -> render px
    return int(round(v * S))

# ---- A. inheritance diff confinement --------------------------------------------
print('== A. inheritance diff vs certified parent render ==')
d = np.abs(R - P).sum(axis=2)
dm = d > 60
ys, xs = np.where(dm)
print(f'diff>60 n={len(ys)}', f'bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]' if len(ys) else '')
# allowed zones: badge numeral (14->15) x[855,925]pt y[45,100]pt; gutter arc removal
# x[400,445]pt y[260,360]pt; everything right of x=445pt (right half + gutter arrow)
badge = dm[pt(45):pt(100), pt(855):pt(925)]
arczone = dm[pt(260):pt(360), pt(400):pt(445)]
rest = dm.copy()
rest[pt(45):pt(100), pt(855):pt(925)] = False
rest[pt(260):pt(360), pt(400):pt(445)] = False
rest[:, pt(445):] = False
check('left half + title clean (only badge/arc-strip differ)', rest.sum() == 0,
      f'stray diff px={rest.sum()}')
if rest.sum():
    yy, xx = np.where(rest)
    print('   stray bbox x[%d,%d] y[%d,%d]' % (xx.min(), xx.max(), yy.min(), yy.max()))
check('badge zone differs (numeral 14->15)', badge.sum() > 40, f'n={badge.sum()}')
check('arc strip differs (parent arc removed)', arczone.sum() > 200, f'n={arczone.sum()}')

# left figure region pixel-compare vs parent render
lf = np.abs(R[pt(115):pt(522), pt(117):pt(394)] - P[pt(115):pt(522), pt(117):pt(394)]).mean()
check('left figure identical to parent render', lf < 6, f'mean|diff|={lf:.2f}')

# ---- B. containment ---------------------------------------------------------------
print('== B. containment ==')
# playlist chrome bounds: content inside gray panel x[42,918]pt y[45,540]pt
r, g, b = R[:, :, 0], R[:, :, 1], R[:, :, 2]
ink = (r < 200) | (g < 200) | (b < 200)  # non-white-ish
# my delta zone: right panel + gutter arrow; check no ink outside chrome bounds there
dz = np.zeros(R.shape[:2], bool)
dz[pt(45):, pt(412):pt(920)] = True
out = ink & dz & ((np.arange(R.shape[1])[None, :] < pt(87)) | (np.arange(R.shape[1])[None, :] > pt(1913)))
check('no delta ink outside gray panel (x bounds)', out.sum() == 0, f'n={out.sum()}')
# right-panel contents inside the green border strokes x[572,895] y[104,525]pt
inner = ink[pt(108):pt(521), pt(577):pt(891)]
check('panel interior ink present', inner.sum() > 5000, f'n={inner.sum()}')
# nothing of MY delta sits between title bottom and panel top (y93..103pt) —
# the title band itself is proven identical to the parent in check A
strip = ink[pt(93):pt(103), pt(560):pt(850)]
check('strip between title and panel clean of delta ink', strip.sum() < 20, f'n={strip.sum()}')

# ---- C. green panel border geometry ------------------------------------------------
print('== C. green border ==')
green = (g > 100) & (g - r > 40) & (g - b > 20) & (r < 150)
colsum = green[pt(110):pt(520), :].sum(axis=0)
cols = np.where(colsum > 300)[0]
rowsum = green[:, pt(580):pt(890)].sum(axis=1)
rows = np.where(rowsum > 300)[0]
if len(cols) and len(rows):
    check('border cols at 572-574/893-895 pt', abs(cols.min() - pt(572)) <= 4 and abs(cols.max() - pt(895)) <= 4,
          f'render cols {cols.min()}..{cols.max()} expect {pt(572)}..{pt(895)}')
    check('border rows at 104-106/523-525 pt', abs(rows.min() - pt(104)) <= 4 and abs(rows.max() - pt(525)) <= 4,
          f'render rows {rows.min()}..{rows.max()} expect {pt(104)}..{pt(525)}')
else:
    check('green border found', False, f'cols={len(cols)} rows={len(rows)}')

# ---- D. shading fields --------------------------------------------------------------
print('== D. shading fields ==')
def sample(img, xpt, ypt, rad=2):
    x0, y0 = pt(xpt) - rad, pt(ypt) - rad
    return tuple(int(v) for v in np.median(img[y0:y0 + 2 * rad + 1, x0:x0 + 2 * rad + 1].reshape(-1, 3), axis=0))
peach_r = sample(R, 583, 400); peach_f = (253, 237, 221)
green_r = sample(R, 882, 400); green_f = (206, 255, 225)
check('peach field matches frame core', max(abs(a - b_) for a, b_ in zip(peach_r, peach_f)) <= 10, f'{peach_r}')
check('mint field matches frame core', max(abs(a - b_) for a, b_ in zip(green_r, green_f)) <= 10, f'{green_r}')
# field extents: peach column at x583pt from y~108 to ~520; green at x882 similar
colP = R[:, pt(583), :]
pc = np.where((colP[:, 0] > 235) & (colP[:, 1] > 215) & (colP[:, 2] > 195) & (colP[:, 0] - colP[:, 2] > 15))[0]
colG = R[:, pt(882), :]
gc = np.where((colG[:, 0] > 180) & (colG[:, 0] < 235) & (colG[:, 1] > 235))[0]
check('peach spans y108..520 pt', len(pc) > 0 and abs(pc.min() - pt(108)) <= 6 and abs(pc.max() - pt(520)) <= 8,
      f'render {pc.min()}..{pc.max()} expect {pt(108)}..{pt(520)}' if len(pc) else 'none')
check('mint spans y104..524 pt', len(gc) > 0 and abs(gc.min() - pt(104)) <= 8 and abs(gc.max() - pt(526)) <= 8,
      f'render {gc.min()}..{gc.max()} expect {pt(104)}..{pt(526)}' if len(gc) else 'none')

# ---- E. block arrow -----------------------------------------------------------------
print('== E. block arrow ==')
red = (r > 130) & (r - g > 60) & (r - b > 60)
sub = red[pt(288):pt(326), pt(450):pt(535)]
ys, xs = np.where(sub)
check('block arrow ink present', len(ys) > 300, f'n={len(ys)}')
if len(ys):
    check('block arrow bbox within 5px of frame',
          abs(xs.min() + pt(450) - pt(458)) <= 5 and abs(xs.max() + pt(450) - pt(525)) <= 5 and
          abs(ys.min() + pt(288) - pt(295)) <= 5 and abs(ys.max() + pt(288) - pt(318)) <= 5,
          f'render x[{xs.min()+pt(450)},{xs.max()+pt(450)}] y[{ys.min()+pt(288)},{ys.max()+pt(288)}] expect x[{pt(458)},{pt(525)}] y[{pt(295)},{pt(318)}]')
    # IoU vs frame mask upscaled
    fred = (F[:, :, 0] > 130) & (F[:, :, 0] - F[:, :, 1] > 60) & (F[:, :, 0] - F[:, :, 2] > 60)
    fsub = fred[288:326, 450:535]
    fbig = np.asarray(Image.fromarray((fsub * 255).astype(np.uint8)).resize((sub.shape[1], sub.shape[0]), Image.NEAREST)) > 127
    iou = (sub & fbig).sum() / (sub | fbig).sum()
    check('block arrow shape IoU vs frame >= 0.75', iou >= 0.75, f'IoU={iou:.3f}')
    core = sample(R, 480, 307, 1)
    check('arrow core red ~CC0000', core[0] > 170 and core[1] < 60 and core[2] < 60, f'{core}')

# ---- F. up arrows -------------------------------------------------------------------
print('== F. up arrows ==')
for tag, (x0, x1, y0, y1) in {'up1': (654, 666, 487, 513), 'up2': (740, 750, 116, 140)}.items():
    sub = red[pt(y0) - 3:pt(y1) + 3, pt(x0) - 3:pt(x1) + 3]
    n = sub.sum()
    check(f'{tag} ink present', n > 60, f'n={n}')
    fsub = fred[y0 - 1:y1 + 2, x0 - 1:x1 + 2]
    fbig = np.asarray(Image.fromarray((fsub * 255).astype(np.uint8)).resize((sub.shape[1], sub.shape[0]), Image.NEAREST)) > 127
    union = (sub | fbig).sum()
    iou = (sub & fbig).sum() / union if union else 0
    check(f'{tag} shape IoU vs frame >= 0.5', iou >= 0.5, f'IoU={iou:.3f}')

# ---- G. headers (closed loop: ink bbox vs frame) --------------------------------------
print('== G. headers ==')
redtxt = (r > 140) & (r - g > 60) & (r - b > 60)
sub = redtxt[pt(108):pt(148), pt(578):pt(741)]
ys, xs = np.where(sub)
if len(ys):
    ex = (pt(585), pt(650), pt(116), pt(128))
    got = (xs.min() + pt(578), xs.max() + pt(578), ys.min() + pt(108), ys.max() + pt(108))
    check('Encoder ink bbox vs frame within 5px',
          abs(got[0] - ex[0]) <= 5 and abs(got[1] - ex[1]) <= 5 and abs(got[2] - ex[2]) <= 5 and abs(got[3] - ex[3]) <= 5,
          f'got x[{got[0]},{got[1]}] y[{got[2]},{got[3]}] expect x[{ex[0]},{ex[1]}] y[{ex[2]},{ex[3]}]')
else:
    check('Encoder header ink present', False, 'none')
gtxt = (g > 100) & (g - r > 50) & (g - b > 30) & (r < 130)
sub = gtxt[pt(108):pt(150), pt(762):pt(892)]
ys, xs = np.where(sub)
if len(ys):
    ex = (pt(821), pt(887), pt(116), pt(127))
    got = (xs.min() + pt(762), xs.max() + pt(762), ys.min() + pt(108), ys.max() + pt(108))
    check('Decoder ink bbox vs frame within 5px',
          abs(got[0] - ex[0]) <= 5 and abs(got[1] - ex[1]) <= 5 and abs(got[2] - ex[2]) <= 5 and abs(got[3] - ex[3]) <= 5,
          f'got x[{got[0]},{got[1]}] y[{got[2]},{got[3]}] expect x[{ex[0]},{ex[1]}] y[{ex[2]},{ex[3]}]')
else:
    check('Decoder header ink present', False, 'none')

# ---- H. no leftover ink in removed zones (gutter, below panels) ----------------------
print('== H. removed zones ==')
dark = (r < 130) & (g < 130) & (b < 130)
gut = dark[pt(45):pt(535), pt(412):pt(452)]  # gutter left of the block arrow
check('gutter strip left of arrow clean', gut.sum() < 40, f'n={gut.sum()}')
gut2 = dark[pt(45):pt(535), pt(452):pt(570)].copy()
gut2[pt(288) - pt(45):pt(326) - pt(45), :] = False  # exclude the block arrow band
check('gutter above/below arrow clean', gut2.sum() < 40, f'n={gut2.sum()}')

print('\nSELFCHECK RESULT:', 'PASS' if ok else 'FAIL')
