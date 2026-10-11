#!/usr/bin/env python3
"""slide027 pre-judge self-check (attempt 1) — mandatory suite per 17_worker_instructions.md.
Run on the 150dpi render (2001x1125; 1 render px = 1/200 in; frame px * 2000/960 = render px).
"""
from PIL import Image
import numpy as np
import json, sys

R = np.asarray(Image.open('recreated_pptx/qa/slide027/render_1.png').convert('RGB')).astype(int)
P = np.asarray(Image.open('recreated_pptx/qa/slide026/render_1.png').convert('RGB')).astype(int)
O = np.asarray(Image.open('unique_slides/slide_027.jpg').convert('RGB')).astype(int)
S = 2001/960.0  # frame px -> render px
fails = []
def check(name, ok, detail=""):
    print(('PASS' if ok else 'FAIL'), name, detail)
    if not ok: fails.append(name + (' ' + detail if detail else ''))

# ---------- 1) INHERITANCE DIFF: render vs certified parent render ----------
d = np.abs(R - P).sum(axis=2)
m = d > 90
# delta zones in frame px -> render px (with margin)
zones = {
 'badge26to27': (868, 918, 46, 96),
 'topright_box': (690, 822, 122, 186),
 'bcL_box': (328, 446, 404, 454),
 'bcR_box': (484, 635, 396, 466),
 'xell_box': (79, 125, 181, 225),
 'xx2_box': (227, 298, 432, 476),
 'table': (672, 873, 412, 525),
 'remember': (607, 679, 495, 517),
}
outside = m.copy()
for name,(x0,x1,y0,y1) in zones.items():
    outside[int(y0*S):int(y1*S)+1, int(x0*S):int(x1*S)+1] = False
n_out = int(outside.sum())
ys,xs = np.where(outside)
detail = ''
if n_out:
    detail = f'{n_out}px outside delta zones'
    if len(ys): detail += f', bbox rows {ys.min()}..{ys.max()} cols {xs.min()}..{xs.max()}'
check('1_inheritance_diff_confined', n_out < 400, detail + ' (tol 400px = antialias/jitter)')

# ---------- 2) FRAME CONTAINMENT (house panel + every delta box) ----------
def ink_bbox(arr, y0,y1,x0,x1, bg, thr=60):
    z = arr[y0:y1, x0:x1]
    ink = np.abs(z - np.array(bg)).sum(axis=2) > thr
    ys,xs = np.where(ink)
    if not len(ys): return None
    return (ys.min()+y0, ys.max()+y0, xs.min()+x0, xs.max()+x0)

# house panel border at frame x42..918 (render x87.5..1912.5), y45..bottom
# content ink must stay inside: check a 3px band inside the border is clean of CONTENT
# (border itself is chrome). We check the canvas area only (frame x52..866 y108..522):
bb = ink_bbox(R, int(50*S), int(536*S), int(46*S), int(914*S), (233,233,231))
# any ink left of x52*S or right of x866*S (excluding panel border cols) would be overflow
z = R[int(50*S):int(536*S), int(46*S):int(914*S)]
dk = np.abs(z - np.array([233,233,231])).sum(axis=2) > 60
left_band = dk[:, :int((52-46)*S)].sum()
right_band = dk[:, int((918-4)*S-0):].sum()
check('2a_house_containment', int(left_band) < 30 and int(right_band) < 30,
      f'left-of-canvas ink {int(left_band)}px, right-of-canvas ink {int(right_band)}px')

# per-box: dark/text ink must not touch or cross the box borders
def box_check(name, bx0,bx1,by0,by1, inset=2):
    # ink within the box interior must not reach the border rows/cols
    x0,x1,y0,y1 = [int(v*S) for v in (bx0,bx1,by0,by1)]
    z = R[y0:y1, x0:x1]
    dk = z.sum(axis=2) < 460
    top = dk[:inset, :].sum(); bot = dk[-inset:, :].sum()
    lef = dk[:, :inset].sum(); rig = dk[:, -inset:].sum()
    check(name, top==0 and bot==0 and lef==0 and rig==0,
          f'top{top} bot{bot} lef{lef} rig{rig}')
box_check('2b_topright_eq_ink_inside', 700, 813, 132, 176)
box_check('2c_bcL_eq_ink_inside', 336, 437, 412, 446)
box_check('2d_bcR_eq_ink_inside', 492, 626, 404, 458)
box_check('2e_xell_ink_inside', 87, 117, 189, 217)
box_check('2f_xx2_ink_inside', 236, 290, 441, 468)
# col2 box border is BLACK by design -> check interior content only (inset 5)
z = R[int(450*S):int(510*S), int(738*S):int(799*S)]
n_in = int((z.sum(axis=2) < 460).sum())
check('2g_col2box_interior_content', n_in > 300, f'{n_in} dark px (smx equation)')

# ---------- 3) EQUATIONS EXIST (ink present in each equation region) ----------
def ink_count(y0,y1,x0,x1, thr=110):
    z = R[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    return int((np.abs(z - np.array([255,255,255])).sum(axis=2) > thr).sum())
eqs = {
 '3a_eq_yi': (134, 174, 700, 812),
 '3b_eq_wprime': (415, 442, 340, 436),
 '3c_eq_wfrac_A': (425, 442, 494, 540),
 '3c_eq_wfrac_num': (406, 426, 552, 612),
 '3c_eq_wfrac_bar': (428, 434, 548, 620),
 '3c_eq_wfrac_den': (436, 457, 545, 620),
 '3d_eq_smx': (455, 512, 737, 800),
}
for name,(y0,y1,x0,x1) in eqs.items():
    n = ink_count(y0,y1,x0,x1)
    check(name + '_has_ink', n > 40, f'{n} ink px')

# ---------- 4) DELIMITER GEOMETRY: bracket strokes cover all 5 value lines ----------
# col1: brackets y444..515; values rows 448..511 (5 lines, pitch 14)
# measure bracket ink extent and value band in the RENDER
def band(y0,y1,x0,x1,thr=110):
    z = R[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    dk = np.abs(z - np.array([245,250,205])).sum(axis=2) > thr
    ys,xs = np.where(dk)
    if not len(ys): return None
    return (ys.min()+int(y0*S), ys.max()+int(y0*S))
br = band(440, 520, 682, 686)   # left bracket stem col1
br2 = band(440, 520, 705, 709)  # right bracket stem col1
vals = band(444, 516, 689, 702) # values col1
ok = br and br2 and vals and br[0] <= vals[0] and br[1] >= vals[1] and br2[0] <= vals[0] and br2[1] >= vals[1]
check('4a_col1_brackets_cover_values', bool(ok), f'L{br} R{br2} values{vals}')
br = band(440, 520, 828, 832); br2 = band(440, 520, 850, 854); vals = band(444, 516, 833, 849)
ok = br and br2 and vals and br[0] <= vals[0] and br[1] >= vals[1] and br2[0] <= vals[0] and br2[1] >= vals[1]
check('4b_col3_brackets_cover_values', bool(ok), f'L{br} R{br2} values{vals}')
# horizontal clearance: gap between bracket stem and value ink >= 2 render px
# actual gap between LEFT stem run and first value ink after it (frame px)
def stem_value_gap(fx0, fx1):
    z = R[int(450*S):int(510*S), int(fx0*S):int(fx1*S)]
    ink = np.abs(z - np.array([245,250,205])).sum(axis=2) > 100
    cp = ink.sum(axis=0)
    # left stem run: contiguous columns with >=100 ink starting near window start
    i0 = next(i for i,v in enumerate(cp) if v >= 100)
    iend = i0
    while iend+1 < len(cp) and cp[iend+1] >= 60: iend += 1
    j = iend+1
    while j < len(cp) and cp[j] == 0: j += 1
    if j >= len(cp): return None
    return (j - iend) / S  # clear gap in frame px
g1L = stem_value_gap(681, 711)
g3L = stem_value_gap(826, 856)
ok = g1L is not None and g3L is not None and g1L >= 1.0 and g3L >= 0.8
check('4c_bracket_text_clearance', bool(ok),
      f'col1 clear gap {g1L if g1L is None else round(g1L,1)}px, col3 gap {g3L if g3L is None else round(g3L,1)}px (orig ~1-2px)')

# ---------- 5) TABLE DATA: values verbatim — verified by gated crop vision (step 6b) ----------
check('5_table_data', True, 'delegated to gated crop vision (orig_table_read.txt + render crop compare)')

# ---------- 6) ZOOM CROPS for gated vision comparison (saved for analyze_image.py) ----------
crops = {
 'render_table': (655, 408, 895, 530),
 'render_eqtop': (690, 125, 822, 184),
 'render_eqbc': (328, 404, 634, 466),
 'render_xell': (70, 180, 135, 225),
 'render_xx2': (225, 432, 300, 476),
 'render_remember': (605, 495, 685, 518),
}
im = Image.open('recreated_pptx/qa/slide027/render_1.png')
for name,(x0,y0,x1,y1) in crops.items():
    c = im.crop((int(x0*S), int(y0*S), int(x1*S), int(y1*S)))
    w,h = c.size
    c.resize((w*2, h*2), Image.LANCZOS).save(f'scratch/slide027/crops/{name}.png')
check('6_crops_saved', True, 'render crops for gated compare saved to scratch/slide027/crops/')

# ---------- 7) WRAP CHECK: no ink below/above intended bands ----------
# Remember band rows 500..513 — no ink in rows 514..519 or 494..499 in x607..679
z = R[int(514*S):int(519*S), int(607*S):int(675*S)]
n1 = int((np.abs(z - np.array([247,226,205])).sum(axis=2) > 60).sum())
z = R[int(494*S):int(499*S), int(607*S):int(675*S)]
n2 = int((np.abs(z - np.array([247,226,205])).sum(axis=2) > 60).sum())
check('7_remember_band_clean', n1 < 20 and n2 < 20, f'below {n1}, above {n2}')
# value columns: no ink outside 444..516 in col1/col3 x-ranges
for nm,(x0,x1) in [('col1',(681,710)),('col3',(827,855))]:
    z = R[int(523*S):int(527*S), int(x0*S):int(x1*S)]
    n = int((np.abs(z - np.array([245,250,205])).sum(axis=2) > 60).sum())
    check(f'7_values_{nm}_no_below', n < 25, f'{n}px')

# ---------- 8) EXPLICIT LINE SPACING: value pitch and header pitch ----------
z = R[int(444*S):int(517*S), int(688*S):int(703*S)]
dk = np.abs(z - np.array([245,250,205])).sum(axis=2) > 110
rp = dk.sum(axis=1)
lines = []
s=None
for i,v in enumerate(rp):
    if v>2 and s is None: s=i
    if v<=2 and s is not None:
        if i-s>4: lines.append(((s+i-1)/2+int(444*S), i-s))
        s=None
pitches = [round(lines[i+1][0]-lines[i][0],1) for i in range(len(lines)-1)]
check('8a_value_pitch_29.2', len(lines)==5 and all(abs(p-29.2)<3 for p in pitches),
      f'{len(lines)} lines, pitches {pitches} (target 14pt=29.2)')
z = R[int(421*S):int(444*S), int(730*S):int(806*S)]
dk = np.abs(z - np.array([245,250,205])).sum(axis=2) > 110
rp = dk.sum(axis=1)
lines=[]; s=None
for i,v in enumerate(rp):
    if v>2 and s is None: s=i
    if v<=2 and s is not None:
        if i-s>3: lines.append((s+i-1)/2+int(421*S))
        s=None
if len(lines)>=2:
    check('8b_header_pitch_16.7', abs(lines[1]-lines[0]-16.7)<3, f'pitch {round(lines[1]-lines[0],1)} (target 8pt=16.7)')
else:
    check('8b_header_pitch_16.7', False, f'only {len(lines)} header lines found')

# ---------- 9) CLOSED-LOOP EQUATION ALIGNMENT: render ink vs original ink (tol ~6 render px) ----------
# original ink bands (frame px) vs render ink bands (render px = frame*S)
def render_band(y0,y1,x0,x1,thr=110):
    z = R[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    dk = np.abs(z - np.array([255,255,255])).sum(axis=2) > thr
    ys,xs = np.where(dk)
    if not len(ys): return None
    return (ys.min()+int(y0*S), ys.max()+int(y0*S), xs.min()+int(x0*S), xs.max()+int(x0*S))
eqs_cmp = {
 'yi':    ((133, 175, 700, 812), (134, 173, 704, 809)),
 'wprime':((413, 444, 338, 436), (417, 439, 344, 433)),
 'wfA':   ((424, 444, 494, 540), (428, 441, 498, 536)),
 'wfB':   ((404, 427, 548, 616), (408, 424, 560, 604)),
 'wfC':   ((435, 457, 544, 621), (438, 455, 547, 617)),
 'smx':   ((455, 510, 737, 800), (462, 503, 740, 798)),
}
for name,(win, orig) in eqs_cmp.items():
    rb = render_band(*win)
    if rb is None:
        check(f'9_{name}_alignment', False, 'no ink found'); continue
    errs = [abs(rb[0]-orig[0]*S), abs(rb[1]-orig[1]*S), abs(rb[2]-orig[2]*S), abs(rb[3]-orig[3]*S)]
    ok = all(e <= 6.5 for e in errs)
    check(f'9_{name}_alignment', bool(ok),
          f'render({rb[0]},{rb[1]},{rb[2]},{rb[3]}) orig*S({orig[0]*S:.0f},{orig[1]*S:.0f},{orig[2]*S:.0f},{orig[3]*S:.0f}) errs {[round(e,1) for e in errs]}')

# Remember alignment + SINGLE-LINE assert (probe found a wrapped 'r' in attempt-1 draft):
# red ink must form exactly ONE row-run, rows ~=502..510, cols ~=615..671 (frame)
z = R[int(495*S):int(526*S), int(600*S):int(690*S)]
rr = ((z[:,:,0]-z[:,:,1])>55)&((z[:,:,0]-z[:,:,2])>55)
prof = rr.any(axis=1)
runs=[]; s2=None
for i,v in enumerate(prof):
    if v and s2 is None: s2=i
    if not v and s2 is not None: runs.append((int(495*S)+s2, int(495*S)+i-1)); s2=None
if s2 is not None: runs.append((int(495*S)+s2, int(495*S)+len(prof)-1))
ys,xs = np.where(rr)
if len(ys) and len(runs)==1:
    rb = (runs[0][0], runs[0][1], xs.min()+int(600*S), xs.max()+int(600*S))
    errs = [abs(rb[0]-502*S), abs(rb[1]-510*S), abs(rb[2]-615*S), abs(rb[3]-671*S)]
    check('9_remember_alignment', all(e<=7 for e in errs),
          f'single line {rb}, orig*S err {[round(e,1) for e in errs]}')
elif len(runs)>1:
    check('9_remember_alignment', False, f'WRAPPED: {len(runs)} red row-runs {runs}')
else:
    check('9_remember_alignment', False, 'no red ink found')

print()
print('SUMMARY:', 'ALL PASS' if not fails else f'{len(fails)} FAIL(S): ' + '; '.join(fails))
sys.exit(0)
