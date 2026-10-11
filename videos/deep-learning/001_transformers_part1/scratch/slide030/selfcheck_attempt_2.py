#!/usr/bin/env python3
# selfcheck_attempt_2.py — slide 030 pre-judge self-checks (17_worker_instructions 5-8)
# Render: qa/slide030/render_2.png (2001x1125 @150dpi; 1 frame-px = 2.0844 render-px)
# Frame ground truth: unique_slides/slide_030.jpg (960x540, 1px = 1pt)
# Parent certified render: qa/slide029/render_2.png (inheritance-diff base)
from PIL import Image
import numpy as np

ROOT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
REN = np.asarray(Image.open(f'{ROOT}/recreated_pptx/qa/slide030/render_2.png').convert('RGB')).astype(int)
PAR = np.asarray(Image.open(f'{ROOT}/recreated_pptx/qa/slide029/render_2.png').convert('RGB')).astype(int)
FR = np.asarray(Image.open(f'{ROOT}/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SC = REN.shape[1] / 960.0  # 2.0844 render px per frame px
ok = True
def check(name, cond, detail=''):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok = False

# ---------- 1) HOUSE CHROME CHECK (shared checker) ----------
import subprocess, sys
r = subprocess.run([sys.executable, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome_check.py',
                    f'{ROOT}/recreated_pptx/qa/slide030/render_2.png'], capture_output=True, text=True)
print('--- house_chrome_check.py output ---')
print(r.stdout.strip())
print(r.stderr.strip())
check('house_chrome_check.py exit 0', r.returncode == 0)

# ---------- 2) INHERITANCE DIFF: render vs certified parent render ----------
# delta zones in frame px -> render px; everything else must be ~identical
def z(x0, y0, x1, y1):
    return (int(x0*SC)-3, int(y0*SC)-3, int(x1*SC)+4, int(y1*SC)+4)
zones = {
 'titleL1':  z(95, 44, 862, 82),      # L1 text replaced (incl. badge numeral zone separate)
 'badgeNum': z(870, 48, 916, 94),     # numeral 30 vs 29
 'circleL':  z(60, 286, 141, 367),
 'circleR':  z(763, 289, 843, 370),
 'circleQ':  z(254, 452, 335, 534),
 'boxKey':   z(173, 257, 292, 312),
 'boxVal':   z(601, 264, 720, 319),
 'boxQry':   z(373, 410, 492, 466),
 'qbox':     z(552, 428, 845, 511),   # includes parent resultBox remnant region
 'cursorPar':z(724, 343, 761, 373),
 'leadKey': z(128, 262, 185, 295), 'leadVal': z(705, 268, 780, 312), 'leadQry': z(295, 415, 385, 472),   # parent frame cursor (absent in 30 frame AND render)
}
d = np.abs(REN - PAR).max(axis=2)
mask = d > 45
acc = np.zeros_like(mask)
for n, (x0, y0, x1, y1) in zones.items():
    acc[y0:y1, x0:x1] = True
un = mask & ~acc
check('inheritance diff confined to delta zones', un.sum() < 60, f'unaccounted diff px = {un.sum()}')
ys, xs = np.where(un)
if un.sum():
    print('   unaccounted bbox: x%d..%d y%d..%d' % (xs.min(), xs.max(), ys.min(), ys.max()))

# ---------- 3) CLOSED-LOOP DELTA GEOMETRY: render vs original frame ----------
def ink_bbox(M, x0, y0, x1, y1, thr=110):
    reg = M[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    lum = 0.299*reg[:,:,0] + 0.587*reg[:,:,1] + 0.114*reg[:,:,2]
    ys, xs = np.where(lum < thr)
    if not len(ys): return None
    return (x0 + xs.min()/SC, y0 + ys.min()/SC, x0 + xs.max()/SC, y0 + ys.max()/SC)

# 3a. title L1: ink + highlight extents (frame-px units); scan y46..78 to skip the
# house panel's top chrome line (y~44.6, present in both renders) and the subtitle
def ink_bbox(M, x0, y0, x1, y1, thr=110):
    reg = M[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    lum = 0.299*reg[:,:,0] + 0.587*reg[:,:,1] + 0.114*reg[:,:,2]
    ys, xs = np.where(lum < thr)
    if not len(ys): return None
    return (x0 + xs.min()/SC, y0 + ys.min()/SC, x0 + xs.max()/SC, y0 + ys.max()/SC)

tib = ink_bbox(REN, 95, 46, 866, 78)
fyb = (FR[:, :, 0] > 215) & (FR[:, :, 1] > 205) & (FR[:, :, 2] < 175) & ((FR[:, :, 0] - FR[:, :, 2]) > 70)
ysF, xsF = np.where(fyb[44:82, 100:862]); f_hl = (100+xsF.min(), 44+ysF.min(), 100+xsF.max(), 44+ysF.max())
ryb = (REN[:,:,0] > 215) & (REN[:,:,1] > 205) & (REN[:,:,2] < 175) & ((REN[:,:,0] - REN[:,:,2]) > 70)
ysR, xsR = np.where(ryb[int(44*SC):int(82*SC), int(100*SC):int(862*SC)])
r_hl = (100+xsR.min()/SC, 44+ysR.min()/SC, 100+xsR.max()/SC, 44+ysR.max()/SC)
check('title ink x-center ~= 466.5', tib and abs((tib[0]+tib[2])/2 - 466.5) < 6, f'render ink x{tib[0]:.0f}..{tib[2]:.0f} center {(tib[0]+tib[2])/2:.1f} vs frame 466.5')
check('title ink y band', tib and abs(tib[1] - 58) < 3 and abs(tib[3] - 76) < 4, f'y{tib[1]:.1f}..{tib[3]:.1f} vs 58..76')
check('title highlight extent', all(abs(a-b) < 8 for a, b in zip(r_hl, f_hl)), f'render x{r_hl[0]:.0f}..{r_hl[2]:.0f} y{r_hl[1]:.0f}..{r_hl[3]:.0f} vs frame x{f_hl[0]}..{f_hl[2]} y{f_hl[1]}..{f_hl[3]}')

# 3b. circles: yellow-mask center + diameter in render vs frame targets
def circle_stats(M, cx, cy):
    R, G, B = M[:,:,0], M[:,:,1], M[:,:,2]
    ym = (R > 215) & (G > 205) & (B < 175) & ((R - B) > 70)
    reg = ym[int((cy-45)*SC):int((cy+45)*SC), int((cx-45)*SC):int((cx+45)*SC)]
    ys, xs = np.where(reg)
    if not len(ys): return None
    return ((cx-45) + (xs.min()+xs.max())/2/SC, (cy-45) + (ys.min()+ys.max())/2/SC,
            (xs.max()-xs.min()+1)/SC, (ys.max()-ys.min()+1)/SC)
for nm, cx, cy in (('circleL', 100, 326), ('circleR', 803, 329), ('circleQ', 294, 492.5)):
    st = circle_stats(REN, cx, cy)
    check(f'{nm} center', st and abs(st[0]-cx) < 4 and abs(st[1]-cy) < 4,
          f'render center ({st[0]:.1f},{st[1]:.1f}) d=({st[2]:.1f},{st[3]:.1f}) vs target ({cx},{cy}) d=70')
    check(f'{nm} diameter ~70', st and abs(st[2]-70) < 6 and abs(st[3]-70) < 6)

# 3c. annotation boxes: border-line centers + interior text bands
def box_edges(M, cx, cy, span=75, rowy=None):
    # scan the given row for the dark border-line centers (non-white, red-ish);
    # rowy (frame px) chosen per box to avoid the inherited red node/triangle ink
    R, G, B = M[:,:,0], M[:,:,1], M[:,:,2]
    redm = (R - np.maximum(G, B) > 40) & (R > 110)
    ry = int((rowy if rowy is not None else cy)*SC)
    row = redm[ry, int((cx-span)*SC):int((cx+span)*SC)]
    col = redm[int((cy-30)*SC):int((cy+30)*SC), int(cx*SC)]
    xs = np.where(row)[0]; ys = np.where(col)[0]
    return ((cx-span) + xs.min()/SC, (cx-span) + xs.max()/SC,
            (cy-30) + ys.min()/SC, (cy-30) + ys.max()/SC) if len(xs) and len(ys) else None
for nm, cx, cy, tx0, tx1, ty0, ty1, rowy in (
    ('KEY', 232, 285, 178, 286, 263, 307, 285),
    ('VALUE', 660, 292, 606, 714, 270, 314, 311),   # y311: below text, clear of node ink
    ('QUERY', 432.5, 437, 378, 487, 415, 459.5, 437)):
    be = box_edges(REN, cx, cy, rowy=rowy)
    if nm == 'VALUE':  # row y311 also crosses the INHERITED red vertical at x591
        R_, G_, B_ = REN[:,:,0], REN[:,:,1], REN[:,:,2]
        rm_ = (R_ - np.maximum(G_, B_) > 40) & (R_ > 110)
        seg = np.where(rm_[int(311*SC), int(598*SC):int(622*SC)])[0]
        be = (598 + seg.min()/SC if len(seg) else float('nan'), be[1], be[2], be[3])
    check(f'{nm} box border centers', be and abs(be[0]-tx0) < 4 and abs(be[1]-tx1) < 4 and abs(be[2]-ty0) < 4 and abs(be[3]-ty1) < 4,
          f'render x{be[0]:.1f}..{be[1]:.1f} y{be[2]:.1f}..{be[3]:.1f} vs frame x{tx0}..{tx1} y{ty0}..{ty1}' if be else 'no border found')

# 3d. annotation text ink bands (two lines, cap tops) in frame px
def text_bands(M, x0, y0, x1, y1):
    lum = 0.299*M[:,:,0] + 0.587*M[:,:,1] + 0.114*M[:,:,2]
    reg = lum[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)] < 150
    rows = reg.sum(axis=1) > 1
    bands, inb = [], False
    for i, v in enumerate(rows):
        if v and not inb: inb, st = True, i
        elif not v and inb: inb = False; bands.append((y0+st/SC, y0+(i-1)/SC))
    if inb: bands.append((y0+st/SC, y0+(len(rows)-1)/SC))
    return bands
for nm, (x0, x1, y0, y1), expect in (
    ('KEY',   (186, 279, 264, 306), [(270, 279), (290, 299)]),
    ('VALUE', (613, 703, 271, 313), [(278, 287), (297, 307)]),
    ('QUERY', (386, 476, 416, 458), [(422, 432), (442, 452)])):
    bb = text_bands(REN, x0, y0, x1, y1)
    got = [(round(a), round(b)) for a, b in bb]
    check(f'{nm} text 2 lines', len(bb) == 2, f'bands={got} expect~{expect}')

# 3e. question box: border + text bands
Rn, Gn, Bn = REN[:,:,0], REN[:,:,1], REN[:,:,2]
blum = (Bn - np.maximum(Rn, Gn) > 30) & (Bn > 110)
def qborder():
    row = blum[int(473*SC), int(560*SC):int(855*SC)]
    xs = np.where(row)[0]
    col = blum[int(430*SC):int(520*SC), int(706*SC)]
    ys = np.where(col)[0]
    return (560+xs.min()/SC, 560+xs.max()/SC, 430+ys.min()/SC, 430+ys.max()/SC) if len(xs) and len(ys) else None
qb = qborder()
check('question box border centers', qb and abs(qb[0]-573.5) < 4 and abs(qb[1]-839.5) < 5 and abs(qb[2]-440.5) < 4 and abs(qb[3]-506.5) < 5,
      f'render x{qb[0]:.1f}..{qb[1]:.1f} y{qb[2]:.1f}..{qb[3]:.1f} vs frame 573.5/839.5 440.5/506.5' if qb else 'no border')
qb_bands = text_bands(REN, 580, 442, 834, 505)
check('question text 2 lines', len(qb_bands) == 2, f'bands={[(round(a),round(b)) for a,b in qb_bands]} expect ~[(447,461),(469,484)]')

# ---------- 4) CONTAINMENT: no ink crosses the house frame ----------
# house frame inner area x42..918 y45..540 (frame px); chrome content stays inside
lumR = 0.299*REN[:,:,0] + 0.587*REN[:,:,1] + 0.114*REN[:,:,2]
nonwhite = lumR < 235
outside = 0
for (x0, y0, x1, y1) in [(0, 0, 42, 1125), (919*int(SC), 0, 2001, 1125)]:
    pass
# content ink must sit within x42..918 / y45..539 (frame px): check the delta content specifically
for nm, (x0, y0, x1, y1) in (('titleL1', (95, 46, 866, 78)), ('circleL', (60, 286, 141, 367)),
                             ('circleR', (763, 289, 843, 370)), ('circleQ', (254, 452, 335, 534)),
                             ('boxKey', (173, 257, 292, 312)), ('boxVal', (601, 264, 720, 319)),
                             ('boxQry', (373, 410, 492, 466)), ('qbox', (552, 428, 845, 511))):
    reg = nonwhite[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    ys, xs = np.where(reg)
    if len(ys):
        gx0, gx1 = x0 + xs.min()/SC, x0 + xs.max()/SC
        gy0, gy1 = y0 + ys.min()/SC, y0 + ys.max()/SC
        check(f'{nm} inside house frame', gx0 >= 42 and gx1 <= 918 and gy0 >= 45 and gy1 <= 539,
              f'ink x{gx0:.1f}..{gx1:.1f} y{gy0:.1f}..{gy1:.1f}')
    else:
        check(f'{nm} inside house frame', False, 'no ink found')

# ---------- 5) LINE WRAP: annotation line1 ink width ~= 87px (no wrap to 3 lines) ----
for nm, (x0, x1, y0, y1), wexp in (('KEY', (186, 279, 266, 287), 87), ('VALUE', (613, 703, 274, 295), 87),
                                    ('QUERY', (386, 476, 418, 439), 87), ('qboxL1', (580, 834, 444, 465), 247),
                                    ('qboxL2', (580, 834, 466, 490), 161)):
    lum = 0.299*REN[:,:,0] + 0.587*REN[:,:,1] + 0.114*REN[:,:,2]
    reg = lum[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)] < 150
    cols = np.where(reg.sum(axis=0) > 0)[0]
    w = (cols.max()-cols.min()+1)/SC if len(cols) else 0
    check(f'{nm} ink width ~{wexp} (no wrap)', abs(w - wexp) < 14, f'render w={w:.1f}')

print('\nSELFCHECK RESULT:', 'ALL PASS' if ok else 'FAILURES PRESENT')
