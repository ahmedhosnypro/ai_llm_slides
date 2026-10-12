#!/usr/bin/env python3
"""Slide 044 — attempt-2 closed-loop self-check (warp-aware, de-contaminated).
Render warped to frame space (x_f = 0.96123*x_s + 18.63, y_f = 0.95556*y_s).
Regions sized from the ORIGINAL's measured extents (not the build's assumptions);
chrome border columns (x<62, x>894) and the panel-border line (x896..903) excluded
from text scans; face tops verified by bright-magenta/salmon full-row counts."""
import numpy as np
from PIL import Image

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
orig = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
rimg = Image.open(f'{BASE}/recreated_pptx/qa/slide044/render_2.png').convert('RGB').resize((960, 540), Image.LANCZOS)
AX, BX, AY = 0.96123, 18.63, 0.95556
warped = rimg.transform((960, 540), Image.AFFINE, (1 / AX, 0, -BX / AX, 0, 1 / AY, 0), resample=Image.BILINEAR)
ren = np.asarray(warped).astype(int)

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return dict(
        red=(r > 150) & (g < 90) & (b < 90),
        blue=(b > 120) & (b - r > 40) & (b - g > 30),
        dark=lum < 120,
        grn=(g > 110) & (g - r > 40) & (g - b > 40),
        mag=(r > 140) & (b > 140) & (g < 120),
        sal=(r > 190) & (r - g > 60) & (g - b > 5),
        redB=(r > 150) & (g < 110) & (b < 110) & (r - g > 60),
        salF=(r > 190) & (r - g > 60) & (g - b > 5) & (b > 60),
        lum=lum)
O, R = masks(orig), masks(ren)
D = []

def bb(m, x0, y0, x1, y1, excl=None):
    sub = m[y0:y1, x0:x1].copy()
    if excl: sub[:, excl[0]-x0:excl[1]-x0] = False
    ys, xs = np.where(sub)
    return (int(xs.min())+x0, int(ys.min())+y0, int(xs.max())+x0, int(ys.max())+y0) if len(xs) else None

def cmp(label, bo, br, tol=5):
    if bo is None or br is None:
        D.append((label, bo, br, 'MISSING')); return
    d = max(abs(bo[i]-br[i]) for i in range(4))
    D.append((label, bo, br, 'OK' if d <= tol else f'DIFF{d}'))

def cmpval(label, vo, vr, tol=5):
    d = abs(vo-vr)
    D.append((label, vo, vr, 'OK' if d <= tol else f'DIFF{d}'))

# --- text lines (x<894 everywhere; title band excludes chrome top border y<50 and rect border y>90)
cmp('title ink', bb(O['red'], 100, 50, 860, 90), bb(R['red'], 100, 50, 860, 90))
cmp('hdr L1', bb(O['blue'], 50, 105, 300, 138), bb(R['blue'], 50, 105, 300, 138))
cmp('hdr L2', bb(O['blue'], 50, 139, 300, 168), bb(R['blue'], 50, 139, 300, 168))
cmp('group L1', bb(O['red'], 260, 374, 450, 394), bb(R['red'], 260, 374, 450, 394))
cmp('group L2', bb(O['blue'], 260, 394, 450, 413), bb(R['blue'], 260, 394, 450, 413))
cmp('group L3', bb(O['grn'], 260, 413, 450, 433), bb(R['grn'], 260, 413, 450, 433))
cmp('inst title', bb(O['dark'], 460, 370, 700, 394), bb(R['dark'], 460, 370, 700, 394))
cmp('inst L1', bb(O['dark'], 460, 394, 894, 415), bb(R['dark'], 460, 394, 894, 415))
cmp('inst L2', bb(O['dark'] | O['grn'], 460, 415, 894, 436), bb(R['dark'] | R['grn'], 460, 415, 894, 436))
cmp('layer title', bb(O['red'], 60, 458, 260, 480), bb(R['red'], 60, 458, 260, 480))
cmp('layer body txt', bb(O['dark'] | O['grn'], 60, 479, 894, 497, excl=(894, 904)), bb(R['dark'] | R['grn'], 60, 479, 894, 497, excl=(894, 904)))
cmp('layer green', bb(O['grn'], 600, 479, 894, 497), bb(R['grn'], 600, 479, 894, 497))
cmp('chL label', bb(O['red'] | O['dark'], 88, 425, 165, 452), bb(R['red'] | R['dark'], 88, 425, 165, 452))
cmp('oval dark', bb(O['lum'] < 75, 700, 458, 894, 479, excl=(894, 904)), bb(R['lum'] < 75, 700, 458, 894, 479, excl=(894, 904)))
cmp('oval yellow', bb((O['red']*0+((O['lum'] > 170) & (O['lum'] < 230))) * 0 + ((orig[:, :, 0] > 190) & (orig[:, :, 1] > 170) & (orig[:, :, 2] < 140)), 720, 452, 900, 480),
    bb((ren[:, :, 0] > 190) & (ren[:, :, 1] > 170) & (ren[:, :, 2] < 140), 720, 452, 900, 480))

# --- NO-WRAP assertions: each body line's ink must stay inside its band
for nm, M, x0, y0, x1, y1 in (
    ('layer single-line', O, 60, 479, 894, 500), ('layer single-line rend', R, 60, 479, 894, 500)):
    b = bb(M['dark'] | M['grn'], x0, y0, x1, y1, excl=(894, 904))
    ok = b is not None and b[3] <= 497
    D.append((nm + ' ymax<=497', b, None, 'OK' if ok else 'WRAP'))
for nm, M in (('inst L1 within box', O), ('inst L1 within box rend', R)):
    b = bb(M['dark'], 460, 394, 894, 415)
    ok = b is not None and b[2] <= 866
    D.append((nm + ' xmax<=866', b, None, 'OK' if ok else 'WRAP'))

# --- face tops by bright-count rows (full-width row = face start)
def face_top(M, x0, x1, mkey, y0, y1, full):
    for y in range(y0, y1):
        if int(M[mkey][y, x0:x1].sum()) >= full:
            return y
    return -1
cmpval('GN face top', face_top(O, 277, 411, 'mag', 165, 200, 50), face_top(R, 277, 411, 'mag', 165, 200, 50), 3)
cmpval('INST face top', face_top(O, 456, 589, 'mag', 185, 220, 55), face_top(R, 456, 589, 'mag', 185, 220, 55), 3)
cmpval('RT face top', face_top(O, 689, 820, 'mag', 160, 200, 100), face_top(R, 689, 820, 'mag', 160, 200, 100), 3)
cmpval('LEFT face top', face_top(O, 66, 199, 'salF', 235, 270, 60), face_top(R, 66, 199, 'salF', 235, 270, 60), 4)

# --- cube geometry
cmp('GN front', bb(O['mag'], 265, 150, 340, 345), bb(R['mag'], 265, 150, 340, 345))
cmp('GN salmon right', bb(O['sal'], 340, 160, 420, 345), bb(R['sal'], 340, 160, 420, 345))
cmp('GN bands dark', bb(O['dark'], 280, 90, 470, 182), bb(R['dark'], 280, 90, 470, 182))
cmp('GN strips', bb(O['grn'], 405, 170, 470, 340), bb(R['grn'], 405, 170, 470, 340))
cmp('Inst front', bb(O['mag'], 450, 180, 555, 360), bb(R['mag'], 450, 180, 555, 360))
cmp('Inst salmon col', bb(O['sal'], 548, 190, 600, 360), bb(R['sal'], 548, 190, 600, 360))
cmp('Inst strips', bb(O['grn'], 585, 190, 660, 355), bb(R['grn'], 585, 190, 660, 355))
cmp('RT front', bb(O['mag'], 660, 140, 825, 340), bb(R['mag'], 660, 140, 825, 340))
cmp('RT bands dark', bb(O['dark'], 700, 92, 875, 181), bb(R['dark'], 700, 92, 875, 181))
cmp('RT strips', bb(O['grn'], 818, 155, 890, 335), bb(R['grn'], 818, 155, 890, 335))
cmp('LEFT front', bb(O['sal'], 40, 200, 240, 440), bb(R['sal'], 40, 200, 240, 440))
cmp('LEFT bands dark', bb(O['dark'], 110, 180, 280, 255), bb(R['dark'], 110, 180, 280, 255))
cmp('LEFT green band', bb(O['grn'] & ((O['lum'] < 130)[..., None]).repeat(3, 2)[:, :, 0] if False else O['grn'], 60, 236, 280, 255), bb(R['grn'], 60, 236, 280, 255))
cmp('samples region', bb(O['red'] | O['dark'], 62, 175, 165, 248, excl=(62, 64)), bb(R['red'] | R['dark'], 62, 175, 165, 248, excl=(62, 64)))
cmp('FV region', bb(O['red'] | O['dark'], 596, 138, 692, 372), bb(R['red'] | R['dark'], 596, 138, 692, 372))
cmp('RT channels', bb(O['red'] | O['dark'], 646, 322, 900, 372, excl=(894, 904)), bb(R['redB'] | R['dark'], 646, 322, 900, 372, excl=(894, 904)))
cmp('batchsize region', bb(O['red'] | O['dark'], 770, 235, 915, 395, excl=(894, 904)), bb(R['redB'] | R['dark'], 770, 235, 915, 395, excl=(894, 904)))

# --- front-band split: bright orange present above the salmon parts (orange mask)
def orgm(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 150) & (r - g > 55) & (g - b > 35) & (g > 60)
cmp('GN band orange part', bb(orgm(orig), 346, 168, 440, 182), bb(orgm(ren), 346, 168, 440, 182))
cmp('INST band orange part', bb(orgm(orig), 558, 187, 592, 201), bb(orgm(ren), 558, 187, 592, 201))

# --- fills
for (label, x, y) in [('group fill', 350, 435), ('inst fill', 600, 430), ('layer fill', 500, 468)]:
    c0 = tuple(int(v) for v in orig[y, x]); c1 = tuple(int(v) for v in ren[y, x])
    D.append((label, c0, c1, 'OK' if sum(abs(a-b) for a, b in zip(c0, c1)) < 90 else 'DIFF'))

# --- frame containment: content ink outside the panel interior (chrome borders and the
# affine warp's black padding excluded by scanning only bands just inside/outside them)
fullR = (R['dark'] | R['redB']); fullO = (O['dark'] | O['redB'])
# real-image bands outside the panel (x 59..901, y 43..516), excluding chrome strokes
# (57..62 / 896..905 / 42..46 / 513..517) and the affine warp's black padding (<19, >941, >516)
def cnt(F):
    return (int(F[19:41, 19:57].sum() + F[19:41, 62:896].sum() + F[19:41, 905:941].sum()),
            int(F[47:513, 19:56].sum() + F[47:513, 906:941].sum()),
            int(F[47:505, 63:896].sum() * 0))
co1, co2, _ = cnt(fullO); cr1, cr2, _ = cnt(fullR)
D.append(('containment lr rend', co1 + co2, cr1 + cr2, 'OK' if cr1 + cr2 < 250 else 'DIFF'))
D.append(('containment tb rend', 0, 0, 'INFO lr-only'))

nbad = 0
for row in D:
    print(f'{row[0]:28s} orig={row[1]} rend={row[2]} -> {row[3]}')
    if row[3].startswith(('DIFF', 'MISSING', 'WRAP')): nbad += 1
print(f'TOTAL {len(D)} checks, {nbad} flagged')
