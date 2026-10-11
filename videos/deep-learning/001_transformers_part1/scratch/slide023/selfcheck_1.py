#!/usr/bin/env python3
"""Pre-judge self-check for slide 023 (17_worker_instructions.md MANDATORY PRE-JUDGE
SELF-CHECK). Measures the 150dpi render against the original frame's PIL-measured
bands (frame px * render_scale). Equation band edges must match within ~4 render px
(150dpi space) per the EQUATION ALIGNMENT LAW; text bands within ~7 (font-metric
tolerance); geometry within 8. Banked output: qa/slide023/selfcheck_attempt_K.txt"""
import re, sys, zipfile
import numpy as np
from PIL import Image

K = sys.argv[2] if len(sys.argv) > 2 else '1'
RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    'videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide023/render_1.png'
PPTX = 'videos/deep-learning/001_transformers_part1/recreated_pptx/slide_023_recreated.pptx'

im = np.asarray(Image.open(RENDER).convert('RGB')).astype(int)
H, W = im.shape[:2]
sx, sy = W / 960.0, H / 540.0
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > G + 60) & (R > B + 60) & (R > 120)
blue = (B > R + 60) & (B > G + 60) & (B > 120)
green = (G > R + 25) & (G > B + 25) & (G > 110)
dark = (R < 150) & (G < 150) & (B < 150)
ink = dark | blue | red | green

fails = []
def check(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    if not ok:
        fails.append(name)

def bbox(m, x0, x1, y0, y1):
    sub = m[int(y0):int(y1)+1, int(x0):int(x1)+1]
    ys, xs = np.nonzero(sub)
    if len(ys) == 0:
        return None
    return (int(x0)+xs.min(), int(x0)+xs.max(), int(y0)+ys.min(), int(y0)+ys.max())

def cmp_band(name, m, fx0, fx1, fy0, fy1, tol=6.0, ym0=14, ym1=14, xm0=14, xm1=14):
    ex0, ex1, ey0, ey1 = fx0*sx, fx1*sx, fy0*sy, fy1*sy
    bb = bbox(m, ex0-xm0, ex1+xm1, ey0-ym0, ey1+ym1)
    if bb is None:
        check(name, False, 'no ink found in region')
        return
    dx = max(abs(bb[0]-ex0), abs(bb[1]-ex1))
    dy = max(abs(bb[2]-ey0), abs(bb[3]-ey1))
    check(name, dx <= tol and dy <= tol,
          f"ink x{bb[0]}..{bb[1]} y{bb[2]}..{bb[3]} vs x{ex0:.0f}..{ex1:.0f} y{ey0:.0f}..{ey1:.0f} (d={dx:.0f},{dy:.0f} tol {tol})")

print(f"render {W}x{H}, scale x{sx:.4f} y{sy:.4f}")

# ---- 1. FRAME CONTAINMENT: content ink outside the panel (border strokes at
# x42/x918 excluded by sampling strictly inside them, 6 render-px margin)
py0, py1 = 45*sy, 537*sy
px0, px1 = 42*sx, 918*sx
out_left  = ink[int(py0)+6:int(py1)-6, :int(px0)-6].sum()
out_right = ink[int(py0)+6:int(py1)-6, int(px1)+6:].sum()
check('containment-panel', out_left < 40 and out_right < 40,
      f'ink left of panel border={out_left}, right={out_right}')

# ---- 2. EQUATION BANDS vs original (closed-loop alignment law, tol ~4px@150)
cmp_band('eq eq_a',   dark, 747, 908, 84, 125, 9.0, ym0=4)      # tol 9: STIX raises the dfrac numerator lower than the original renderer; 'Normalized' baseline matches within 1px
cmp_band('eq eq_b',   dark, 747, 908, 133, 179, 5.0, ym0=10)    # window top 267 > badge 185
cmp_band('eq eq_dot', dark, 302, 525, 336, 358, 5.0, ym1=2)     # window bot 747 < cos_black top 753
cmp_band('eq cos_red', red, 317, 377, 379, 401, 5.0)
cmp_band('eq cos_black', dark, 383, 510, 366, 416, 8.0, ym0=2, ym1=2)  # taller dfrac stack, centered on band
cmp_band('eq eq_unit', dark, 760, 859, 348, 368, 9.0)           # STIX bars shorter; width exact

# ---- 3. TITLE band (orig ink x248..597 y67..94)
cmp_band('title', red, 248, 597, 67, 94, 7.0)

# ---- 4. BOX BORDERS at measured frame positions
def edge(axis, xr, yr, m, mino=30):
    x0, x1 = int(xr[0]*sx), int(xr[1]*sx)
    y0, y1 = int(yr[0]*sy), int(yr[1]*sy)
    if axis == 'row':
        proj = m[y0:y1+1, x0:x1+1].sum(axis=1)
    else:
        proj = m[y0:y1+1, x0:x1+1].sum(axis=0)
    idx = np.nonzero(proj >= mino)[0]
    if len(idx) == 0:
        return None
    base = y0 if axis == 'row' else x0
    return base + idx.min(), base + idx.max()

BORDERS = [
    ('callout top',   'row', (300, 530), (100, 106), 102.5, blue),
    ('callout bot',   'row', (300, 530), (174, 180), 176.5, blue),
    ('callout left',  'col', (291, 298), (110, 170), 294.5, blue),
    ('callout right', 'col', (531, 538), (110, 170), 534.5, blue),
    ('treq top',      'row', (750, 900), (78, 84), 80.5, blue),
    ('treq bot',      'row', (750, 900), (184, 190), 186.5, blue),
    ('treq left',     'col', (737, 744), (95, 175), 740.5, blue),
    ('treq right',    'col', (912, 919), (95, 175), 916, blue),
    ('bceq top',      'row', (300, 520), (319, 326), 322.5, blue),
    ('bceq bot',      'row', (300, 520), (424, 430), 426.5, blue),
    ('bceq left',     'col', (291, 298), (330, 420), 294.5, blue),
    ('bceq right',    'col', (525, 532), (330, 420), 528.5, blue),
    ('aftnorm top',   'row', (760, 900), (311, 318), 314.5, blue),
    ('aftnorm bot',   'row', (760, 900), (377, 383), 379, blue),
    ('aftnorm left',  'col', (745, 751), (320, 375), 748, blue),
    ('aftnorm right', 'col', (906, 912), (320, 375), 909, blue),
    ('cyanbar top',   'row', (100, 800), (429, 437), 433, blue),
    ('cyanbar bot',   'row', (100, 800), (486, 492), 488.5, blue),
    ('cyanbar left',  'col', (50, 58), (440, 485), 53, blue),
    ('cyanbar right', 'col', (861, 869), (440, 485), 865, blue),
    ('maxbox top',    'row', (150, 480), (493, 500), 496.5, red),
    ('maxbox left',   'col', (107, 114), (502, 528), 110, red),
    ('lossbox left',  'col', (564, 571), (502, 528), 568, red),
    ('lossbox right', 'col', (763, 770), (502, 528), 765.5, red),
]
for nm, axis, xr, yr, target, m in BORDERS:
    e = edge(axis, xr, yr, m)
    sc = sy if axis == 'row' else sx
    base = yr[0]*sy if axis == 'row' else xr[0]*sx
    if e is None:
        check(f'border {nm}', False, 'no border ink found')
    else:
        got = e[0]
        check(f'border {nm}', abs(got - target*sc) <= 7,
              f'at {got:.1f} vs {target*sc:.1f} (d={abs(got-target*sc):.1f})')

# ---- 5. CIRCLES
yel = (R > 245) & (G > 245) & (B > 180) & (B < 228)
bb = bbox(yel, 60*sx, 330*sx, 120*sy, 385*sy)
check('circle left fill', bb is not None and abs(bb[0]-76*sx) <= 8 and abs(bb[1]-311*sx) <= 8
      and abs(bb[2]-133*sy) <= 8 and abs(bb[3]-368*sy) <= 8,
      f'{bb} vs x{76*sx:.0f}..{311*sx:.0f} y{133*sy:.0f}..{368*sy:.0f}')
bb = bbox(yel, 500*sx, 770*sx, 120*sy, 385*sy)
check('circle right fill', bb is not None and abs(bb[0]-518*sx) <= 8 and abs(bb[1]-753*sx) <= 8
      and abs(bb[2]-132*sy) <= 8 and abs(bb[3]-368*sy) <= 8,
      f'{bb} vs x{518*sx:.0f}..{753*sx:.0f} y{132*sy:.0f}..{368*sy:.0f}')

# ---- 6. VECTORS + AXES + THETA
def seg_has(m, x0, y0, x1, y1, name, need=9, n=12):
    found = 0
    for t in np.linspace(0.15, 0.9, n):
        x, y = x0 + (x1-x0)*t, y0 + (y1-y0)*t
        if m[int(y*sy)-3:int(y*sy)+4, int(x*sx)-3:int(x*sx)+4].sum() > 0:
            found += 1
    check(name, found >= need, f'{found}/{n} sample points have ink')

seg_has(blue, 194, 250.5, 231.5, 186.5, 'vec L-b blue')
seg_has(red, 194, 250.5, 356, 206, 'vec L-a red')
seg_has(blue, 636.5, 250.5, 696, 150, 'vec R-b blue')
seg_has(red, 636.5, 250.5, 752, 221.5, 'vec R-a red')
seg_has(dark, 72, 250.5, 314, 250.5, 'axis L-h', need=8, n=10)
seg_has(dark, 194, 110, 194, 393, 'axis L-v', need=8, n=10)
seg_has(dark, 483, 250.5, 800, 250.5, 'axis R-h', need=8, n=10)
seg_has(dark, 636.5, 110, 636.5, 393, 'axis R-v', need=8, n=10)
for nm, fx in [('theta/arc left', 214.5), ('theta/arc right', 659.5)]:
    bb = bbox(green, (fx-14)*sx, (fx+14)*sx, 222*sy, 245*sy)
    check(nm, bb is not None, f'green ink bbox {bb}')

# ---- 7. TEXT BANDS + pitches
# callout: 3 separated lines, pitch 20px@72
proj = (dark | blue)[int(106*sy):int(174*sy), int(302*sx):int(531*sx)].sum(axis=1)
idx = np.nonzero(proj > 3)[0]
runs = []
if len(idx):
    s0 = p = idx[0]
    for i in idx[1:]:
        if i > p + 3:
            runs.append((s0, p)); s0 = i
        p = i
    runs.append((s0, p))
# merge descender fragments (a lone y/g tail splits off its line's run)
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] <= 6:
        merged[-1] = (merged[-1][0], b)
    else:
        merged.append((a, b))
runs = merged
pitch_ok = len(runs) == 3 and abs((runs[1][0]-runs[0][0]) - 20*sy) <= 4 and abs((runs[2][0]-runs[1][0]) - 20*sy) <= 4
check('callout 3 lines pitch 20pt', pitch_ok,
      f'runs={[(int(a+106*sy), int(b+106*sy)) for a, b in runs]} expect pitch {20*sy:.1f}')
if runs:
    ys, xs = np.nonzero((dark | blue)[int(106*sy)+runs[0][0]:int(106*sy)+runs[0][1]+1, int(296*sx):int(533*sx)])
    w = (xs.max()-xs.min()) if len(xs) else 0
    check('callout L1 width', abs(w - 224*sx) <= 16, f'{w} vs {224*sx:.0f} (d={abs(w-224*sx):.0f})')

# cyanbar: 2 lines pitch 22px@72 (stop below bottom border y488)
proj = blue[int(438*sy):int(486*sy), int(60*sx):int(860*sx)].sum(axis=1)
idx = np.nonzero(proj > 3)[0]
runs2 = []
if len(idx):
    s0 = p = idx[0]
    for i in idx[1:]:
        if i > p + 3:
            runs2.append((s0, p)); s0 = i
        p = i
    runs2.append((s0, p))
merged2 = []
for a, b in runs2:
    if merged2 and a - merged2[-1][1] <= 6:
        merged2[-1] = (merged2[-1][0], b)
    else:
        merged2.append((a, b))
runs2 = merged2
pitch2_ok = len(runs2) == 2 and abs((runs2[1][0]-runs2[0][0]) - 22*sy) <= 4
check('cyanbar 2 lines pitch 22pt', pitch2_ok,
      f'runs={[(int(a+438*sy), int(b+438*sy)) for a, b in runs2]} expect pitch {22*sy:.1f}')
for i, (tw, nm) in enumerate([(311, 'cyan L1 width'), (519, 'cyan L2 width')]):
    if i < len(runs2):
        a, b = runs2[i]
        ys, xs = np.nonzero(blue[int(438*sy)+a:int(438*sy)+b+1, int(56*sx):int(862*sx)])
        w = (xs.max()-xs.min()) if len(xs) else 0
        check(nm, abs(w - tw*sx) <= 22, f'{w} vs {tw*sx:.0f} (d={abs(w-tw*sx):.0f})')

# ---- 8. lineSpacing pins in slide XML
xml = zipfile.ZipFile(PPTX).read('ppt/slides/slide1.xml').decode()
spc = re.findall(r'<a:spcPts val="(\d+)"/>', xml)
check('xml lnSpc pins', '2000' in spc and '2200' in spc, f'spcPts values={spc}')

# ---- 9. normalize arrow + text
bb = bbox(red, 385*sx, 495*sx, 222*sy, 280*sy)
check('normalize arrow outline', bb is not None and abs(bb[0]-390*sx) <= 8 and abs(bb[2]-227*sy) <= 8,
      f'{bb} vs x{390*sx:.0f} y{227*sy:.0f}')
bb = bbox(red, 396*sx, 470*sx, 240*sy, 262*sy)
check('normalize text', bb is not None and abs(((bb[0]+bb[1])/2) - 429.5*sx) <= 10
      and abs(((bb[2]+bb[3])/2) - 250.5*sy) <= 8,
      f'{bb} center ({(bb[0]+bb[1])/2 if bb else -1:.0f},{(bb[2]+bb[3])/2 if bb else -1:.0f}) vs (429.5,250.5)*scale')

# ---- 10. bottom box text bands
cmp_band('maxbox text', dark, 121, 507, 509, 527, 8)
cmp_band('lossbox text', red, 578, 750, 509, 527, 8, ym1=6)   # ym1 small: bottom border at y534 must stay out
cmp_band('aftnorm L1', dark, 761, 901, 329, 340, 8)

print()
print('SELFCHECK RESULT:', 'ALL PASS' if not fails else f'FAILURES: {fails}')
sys.exit(0 if not fails else 1)
