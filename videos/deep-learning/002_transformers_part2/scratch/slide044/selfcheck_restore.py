#!/usr/bin/env python3
"""Slide 044 — closed-loop self-check (warp-aware): render is in SLIDE space (960x540 pt
after resize); the original frame is FRAME space. Warp the RENDER to frame space
(x_f = x_s*0.96123 + 18.63, y_f = y_s*0.95556) then compare element bboxes in frame space."""
import numpy as np
from PIL import Image

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
orig = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
rimg = Image.open(f'{BASE}/recreated_pptx/../scratch/slide044/render_restore/slide-1.png').convert('RGB').resize((960, 540), Image.LANCZOS)
# warp render (slide space) -> frame space
AX, BX, AY = 0.96123, 18.63, 0.95556
# affine: out(x,y) = in(a*x + b, c*y)  ->  use Image.transform with AFFINE (a,b,c,d,e,f):
# in_x = a*out_x + b*out_y + c = AX*out_x + BX ; in_y = AY*out_y
warped = rimg.transform((960, 540), Image.AFFINE, (1 / AX, 0, -BX / AX, 0, 1 / AY, 0), resample=Image.BILINEAR, fillcolor=(232, 232, 232))
ren = np.asarray(warped).astype(int)

r0, g0, b0 = orig[:, :, 0], orig[:, :, 1], orig[:, :, 2]
r1, g1, b1 = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
lum0 = 0.299 * r0 + 0.587 * g0 + 0.114 * b0
lum1 = 0.299 * r1 + 0.587 * g1 + 0.114 * b1
D = []

def bbox(mask, x0, y0, x1, y1):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) == 0: return None
    return (int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0)

def cmp(label, bo, br, tol=4):
    if bo is None or br is None:
        D.append((label, bo, br, 'MISSING')); return
    dd = max(abs(bo[i] - br[i]) for i in range(4))
    D.append((label, bo, br, 'OK' if dd <= tol else f'DIFF{dd}'))

red0 = (r0 > 150) & (g0 < 90) & (b0 < 90); red1 = (r1 > 150) & (g1 < 90) & (b1 < 90)
mag0 = (r0 > 140) & (b0 > 140) & (g0 < 120); mag1 = (r1 > 140) & (b1 > 140) & (g1 < 120)
sal0 = (r0 > 190) & (r0 - g0 > 60) & (g0 - b0 > 5); sal1 = (r1 > 190) & (r1 - g1 > 60) & (g1 - b1 > 5)
blue0 = (b0 > 120) & (b0 - r0 > 40) & (b0 - g0 > 30); blue1 = (b1 > 120) & (b1 - r1 > 40) & (b1 - g1 > 30)
dark0 = lum0 < 120; dark1 = lum1 < 120
yellow0 = (r0 > 190) & (g0 > 170) & (b0 < 140); yellow1 = (r1 > 190) & (g1 > 170) & (b1 < 140)
grn0 = (g0 > 110) & (g0 - r0 > 40) & (g0 - b0 > 40); grn1 = (g1 > 110) & (g1 - r1 > 40) & (g1 - b1 > 40)

cmp('title red ink', bbox(red0, 120, 46, 845, 95), bbox(red1, 120, 46, 845, 95))
cmp('header L1 blue', bbox(blue0, 50, 105, 300, 138), bbox(blue1, 50, 105, 300, 138))
cmp('header L2 blue', bbox(blue0, 50, 139, 300, 168), bbox(blue1, 50, 139, 300, 168))
cmp('left front salmon', bbox(sal0, 40, 200, 210, 440), bbox(sal1, 40, 200, 210, 440))
cmp('left bands dark', bbox(dark0, 110, 180, 280, 240), bbox(dark1, 110, 180, 280, 240))
cmp('GN front magenta', bbox(mag0, 265, 150, 336, 345), bbox(mag1, 265, 150, 336, 345))
cmp('GN front salmon(right)', bbox(sal0, 336, 150, 420, 345), bbox(sal1, 336, 150, 420, 345))
cmp('GN bands dark', bbox(dark0, 280, 90, 470, 182), bbox(dark1, 280, 90, 470, 182))
cmp('GN strips (g/o/y)', bbox(grn0, 405, 175, 470, 340), bbox(grn1, 405, 175, 470, 340))
cmp('Inst front magenta', bbox(mag0, 450, 180, 555, 360), bbox(mag1, 450, 180, 555, 360))
cmp('Inst salmon col', bbox(sal0, 548, 190, 600, 360), bbox(sal1, 548, 190, 600, 360))
cmp('Inst bands dark', bbox(dark0, 440, 92, 615, 202), bbox(dark1, 440, 92, 615, 202))
cmp('Inst strips', bbox(grn0, 585, 195, 660, 355), bbox(grn1, 585, 195, 660, 355))
cmp('RT front magenta', bbox(mag0, 660, 140, 825, 340), bbox(mag1, 660, 140, 825, 340))
cmp('RT bands dark', bbox(dark0, 700, 92, 875, 168), bbox(dark1, 700, 92, 875, 168))
cmp('RT strips', bbox(grn0, 818, 160, 890, 335), bbox(grn1, 818, 160, 890, 335))

def redrows(rd, x0, x1, y0, y1, thr=20):
    return [y for y in range(y0, y1) if int(rd[y, x0:x1].sum()) > thr]
D.append(('rect top border rows', redrows(red0, 700, 800, 85, 100), redrows(red1, 700, 800, 85, 100), 'OK'))
D.append(('rect bottom border rows', redrows(red0, 700, 800, 355, 372, 100), redrows(red1, 700, 800, 355, 372, 100), 'OK'))
def redcols(rd, y0, y1, x0, x1, thr=20):
    return [x for x in range(x0, x1) if int(rd[y0:y1, x].sum()) > thr]
D.append(('rect left border cols', redcols(red0, 200, 340, 640, 680), redcols(red1, 200, 340, 640, 680), 'OK'))
D.append(('rect right border cols', redcols(red0, 200, 340, 880, 905), redcols(red1, 200, 340, 880, 905), 'OK'))

for (label, x, y) in [('group fill', 350, 435), ('inst fill', 600, 430), ('layer fill', 450, 470)]:
    c0 = tuple(int(v) for v in orig[y, x]); c1 = tuple(int(v) for v in ren[y, x])
    D.append((label, c0, c1, 'OK' if sum(abs(a - b) for a, b in zip(c0, c1)) < 90 else 'DIFF'))

cmp('oval black fill', bbox(lum0 < 75, 700, 448, 915, 479), bbox(lum1 < 75, 700, 448, 915, 479))
cmp('oval yellow text', bbox(yellow0, 720, 452, 900, 480), bbox(yellow1, 720, 452, 900, 480))
cmp('group L1 ink', bbox(dark0, 260, 375, 450, 394), bbox(dark1, 260, 375, 450, 394))
cmp('group L2 blue', bbox(blue0, 260, 394, 450, 413), bbox(blue1, 260, 394, 450, 413))
cmp('group L3 green', bbox(grn0, 260, 413, 450, 433), bbox(grn1, 260, 413, 450, 433))
cmp('inst title ink', bbox(dark0, 460, 370, 700, 394), bbox(dark1, 460, 370, 700, 394))
cmp('inst body L2', bbox(dark0, 460, 395, 900, 415), bbox(dark1, 460, 395, 900, 415))
cmp('inst body L3', bbox(dark0 | grn0, 460, 415, 900, 434), bbox(dark1 | grn1, 460, 415, 900, 434))
cmp('layer title red', bbox(red0, 60, 455, 250, 478), bbox(red1, 60, 455, 250, 478))
cmp('layer body L2', bbox(dark0, 60, 478, 700, 500), bbox(dark1, 60, 478, 700, 500))
cmp('layer green phrase', bbox(grn0, 600, 478, 820, 500), bbox(grn1, 600, 478, 820, 500))
cmp('left channels arrow+label', bbox(red0 | dark0, 40, 425, 240, 495), bbox(red1 | dark1, 40, 425, 240, 495))
cmp('samples arrow region', bbox(red0 | dark0, 40, 175, 160, 245), bbox(red1 | dark1, 40, 175, 160, 245))
cmp('FV arrow region', bbox(red0 | dark0, 596, 138, 692, 372), bbox(red1 | dark1, 596, 138, 692, 372))
cmp('RT channels region', bbox(red0 | dark0, 640, 322, 900, 372), bbox(red1 | dark1, 640, 322, 900, 372))
cmp('batchsize region', bbox(red0 | dark0, 770, 235, 915, 395), bbox(red1 | dark1, 770, 235, 915, 395))
# frame containment
out1 = int((dark1 | red1)[:, 0:57].sum() + (dark1 | red1)[:, 903:960].sum())
D.append(('containment lr ink px', 0, out1, 'OK' if out1 < 120 else 'DIFF'))
outy1 = int((dark1 | red1)[0:42, 57:903].sum() + (dark1 | red1)[517:540, 57:903].sum())
D.append(('containment tb ink px', 0, outy1, 'OK' if outy1 < 120 else 'DIFF'))

nbad = 0
for row in D:
    print(f'{row[0]:26s} orig={row[1]} rend={row[2]} -> {row[3]}')
    if row[3].startswith('DIFF') or row[3] == 'MISSING': nbad += 1
print(f'TOTAL {len(D)} checks, {nbad} flagged')
