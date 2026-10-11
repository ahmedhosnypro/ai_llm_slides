#!/usr/bin/env python3
# selfcheck_attempt_1.py — mandatory pre-judge PIL self-checks for slide 028 (attempt 1).
# Render: 2001x1125 @150dpi (1 frame px = 1pt -> render px = frame px * 150/72).
# Reference-aware: chrome-edge + title baselines are compared against the CERTIFIED
# parent render (qa/slide026/render_1.png) per the dependency law (inherited regions
# must be pixel-comparable to the parent's certified render).
# Checks: (1) frame containment vs parent reference; (2) closed-loop calibration of the
# delta text (title L1, box1, box2 L1/L2) vs the original frame's measured ink;
# (3) strip X2 highlight cells + sysDot border; (4) wrap/containment of the new boxes.
from PIL import Image
import numpy as np
import sys

R = np.asarray(Image.open('videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide028/render_1.png').convert('RGB')).astype(int)
P = np.asarray(Image.open('videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide026/render_1.png').convert('RGB')).astype(int)
S = 150 / 72.0

def f2r(v): return v * S

def bbox(m, y0, x0):
    ys, xs = np.where(m)
    if not len(xs):
        return None
    return (y0 + ys.min(), y0 + ys.max(), x0 + xs.min(), x0 + xs.max(), int(m.sum()))

fails = []
def check(name, cond, detail):
    print(('PASS ' if cond else 'FAIL ') + name + '  ' + detail)
    if not cond:
        fails.append(name)

# ---- (1) house containment: match the certified parent's chrome-edge values ----
for name, img in [('parent_ref', P), ('mine', R)]:
    m = img.sum(axis=2) < 330
    ys, xs = np.where(m)
    if name == 'parent_ref':
        pref = (xs.min(), xs.max(), ys.min(), ys.max())
m = R.sum(axis=2) < 330
ys, xs = np.where(m)
mine = (xs.min(), xs.max(), ys.min(), ys.max())
check('house_containment_vs_parent', all(abs(a - b) <= 2 for a, b in zip(mine, pref)),
      f'mine x{mine[0]}..{mine[1]} y{mine[2]}..{mine[3]} vs certified parent x{pref[0]}..{pref[1]} y{pref[2]}..{pref[3]}')

# ---- (2) title L1 (tight window above the subtitle; thr 330 like parent ref) ----
mb = R[int(f2r(50)):int(f2r(80)), int(f2r(150)):int(f2r(850))].sum(axis=2) < 330
tb = bbox(mb, f2r(50), f2r(150))
t = (f2r(58), f2r(76), f2r(233), f2r(772))
check('title_L1_ink', tb is not None and abs(tb[0] - t[0]) < 5 and abs(tb[1] - t[1]) < 6,
      f'L1 ink y{tb[0]:.0f}..{tb[1]:.0f} x{tb[2]:.0f}..{tb[3]:.0f} (target y{t[0]:.0f}..{t[1]:.0f} x{t[2]:.0f}..{t[3]:.0f})' if tb else 'no ink')
if tb:
    w_t = t[3] - t[2]; w_g = tb[3] - tb[2]
    check('title_L1_width_cal', abs(w_g - w_t) / w_t < 0.05, f'width {w_g:.0f} vs {w_t:.0f} ({(w_g-w_t)/w_t*100:+.1f}%)')
    check('title_L1_hcenter', abs((tb[2]+tb[3])/2 - (t[2]+t[3])/2) < 8,
          f'cx {((tb[2]+tb[3])/2):.0f} vs {(t[2]+t[3])/2:.0f}')
# yellow highlight present in L1 band
ym = (R[:, :, 0] > 235) & (R[:, :, 1] > 230) & (R[:, :, 2] < 200) & (R[:, :, 2] > 120)
yb = bbox(ym[int(f2r(48)):int(f2r(84)), int(f2r(150)):int(f2r(850))], f2r(48), f2r(150))
check('title_highlight', yb is not None and yb[4] > 3000,
      f'highlight bbox {tuple(round(v) for v in yb[:4])} n={yb[4]}' if yb else 'no highlight')

# ---- (3) subtitle band: red tokens present, same band as parent ----
rm2 = (R[:, :, 0] - R[:, :, 1] > 60) & (R[:, :, 0] - R[:, :, 2] > 40) & (R[:, :, 0] > 110)
sb = bbox(rm2[int(f2r(79)):int(f2r(104)), int(f2r(150)):int(f2r(850))], f2r(79), f2r(150))
t = (f2r(82), f2r(101), f2r(405), f2r(804))
check('subtitle_red_ink', sb is not None and abs(sb[0] - t[0]) < 5 and abs(sb[1] - t[1]) < 6,
      f'red bbox y{sb[0]:.0f}..{sb[1]:.0f} x{sb[2]:.0f}..{sb[3]:.0f} (target y{t[0]:.0f}..{t[1]:.0f} x{t[2]:.0f}..{t[3]:.0f})' if sb else 'no red ink')

# ---- (4) box1: white fill + green text (interior window, border excluded) ----
sub = R[int(f2r(430)):int(f2r(456)), int(f2r(390)):int(f2r(712))]
white = ((sub[:, :, 0] > 235) & (sub[:, :, 1] > 235) & (sub[:, :, 2] > 235)).mean()
check('box1_white_fill', white > 0.5, f'white frac={white:.2f}')
gm = (R[:, :, 1] - R[:, :, 0] > 40) & (R[:, :, 1] - R[:, :, 2] > 40) & (R[:, :, 1] > 90)
gb = bbox(gm[int(f2r(430)):int(f2r(457)), int(f2r(388)):int(f2r(714))], f2r(430), f2r(388))
t = (f2r(437), f2r(451), f2r(392), f2r(705))
if gb is None:
    check('box1_text_ink', False, 'no green ink')
else:
    w_t = t[3] - t[2]; w_g = gb[3] - gb[2]
    check('box1_text_cal', abs(w_g - w_t) / w_t < 0.06 and abs((gb[0]+gb[1])/2 - (t[0]+t[1])/2) < 7,
          f'ink y{gb[0]:.0f}..{gb[1]:.0f} x{gb[2]:.0f}..{gb[3]:.0f} w{w_g:.0f} (target y{t[0]:.0f}..{t[1]:.0f} x{t[2]:.0f}..{t[3]:.0f} w{w_t:.0f})')
    r = (f2r(426), f2r(460), f2r(382), f2r(719))
    check('box1_text_inside', gb[0] > r[0] + 4 and gb[3] < r[3] - 2,
          f'text inside rect y{r[0]:.0f}..{r[1]:.0f} x{r[2]:.0f}..{r[3]:.0f}')

# ---- (5) box2: red L1 + blue L2, pitch, inside rect ----
rm = (R[:, :, 0] - R[:, :, 1] > 60) & (R[:, :, 0] - R[:, :, 2] > 50) & (R[:, :, 0] > 110)
rb = bbox(rm[int(f2r(462)):int(f2r(493)), int(f2r(728)):int(f2r(893))], f2r(462), f2r(728))
t1 = (f2r(476), f2r(491), f2r(734), f2r(888))
if rb is None:
    check('box2_L1_ink', False, 'no red ink')
else:
    w_t = t1[3] - t1[2]; w_g = rb[3] - rb[2]
    check('box2_L1_cal', abs(w_g - w_t) / w_t < 0.07 and abs((rb[0]+rb[1])/2 - (t1[0]+t1[1])/2) < 8,
          f'L1 y{rb[0]:.0f}..{rb[1]:.0f} x{rb[2]:.0f}..{rb[3]:.0f} w{w_g:.0f} (target y{t1[0]:.0f}..{t1[1]:.0f} x{t1[2]:.0f}..{t1[3]:.0f} w{w_t:.0f})')
bm = (R[:, :, 2] - R[:, :, 0] > 50) & (R[:, :, 2] - R[:, :, 1] > 40) & (R[:, :, 2] > 110)
bb = bbox(bm[int(f2r(493)):int(f2r(516)), int(f2r(728)):int(f2r(893))], f2r(493), f2r(728))
t2 = (f2r(494), f2r(506), f2r(736), f2r(886))
if bb is None:
    check('box2_L2_ink', False, 'no blue ink')
else:
    w_t = t2[3] - t2[2]; w_g = bb[3] - bb[2]
    check('box2_L2_cal', abs(w_g - w_t) / w_t < 0.07 and abs((bb[0]+bb[1])/2 - (t2[0]+t2[1])/2) < 8,
          f'L2 y{bb[0]:.0f}..{bb[1]:.0f} x{bb[2]:.0f}..{bb[3]:.0f} w{w_g:.0f} (target y{t2[0]:.0f}..{t2[1]:.0f} x{t2[2]:.0f}..{t2[3]:.0f} w{w_t:.0f})')
if rb is not None and bb is not None:
    pitch = bb[0] - rb[0]
    check('box2_line_pitch_top', abs(pitch - 18 * S) < 6, f'top-to-top pitch {pitch:.1f} vs {18*S:.1f}')
    r2 = (f2r(459), f2r(523), f2r(725), f2r(896))
    check('box2_text_inside', rb[0] > r2[0] + 4 and bb[1] < r2[1] - 4 and rb[2] > r2[2] + 2 and rb[3] < r2[3] - 2,
          f'lines inside rect y{r2[0]:.0f}..{r2[1]:.0f} x{r2[2]:.0f}..{r2[3]:.0f}')

# ---- (6) strip: X2 solid cells + sysDot border (band-scoped, frame-referenced) ----
F = np.asarray(Image.open('videos/deep-learning/001_transformers_part1/unique_slides/slide_028.jpg').convert('RGB')).astype(int)
def pinkfrac(img, fy0, fy1, fx0, fx1):
    sub = img[int(f2r(fy0)):int(f2r(fy1)), int(f2r(fx0)):int(f2r(fx1))]
    m = (np.abs(sub[:, :, 0] - 225) < 30) & (np.abs(sub[:, :, 1] - 135) < 35) & (np.abs(sub[:, :, 2] - 206) < 30)
    return m.mean()
# frame is 960x540 (72dpi): index in FRAME px directly, not render px
sub = F[488:500, 266:324]
fm = (np.abs(sub[:, :, 0] - 225) < 30) & (np.abs(sub[:, :, 1] - 135) < 35) & (np.abs(sub[:, :, 2] - 206) < 30)
fr = fm.mean()
mn = pinkfrac(R, 488, 500, 266, 324)
check('strip_X2_cells', abs(mn - fr) < 0.15, f'X2 cell pink frac mine={mn:.2f} vs frame={fr:.2f}')
# sysDot border: dark magenta pixels along the highlight box edge band
sub = R[int(f2r(471)):int(f2r(508)), int(f2r(260)):int(f2r(338))]
dm = ((sub[:, :, 0] > 110) & (sub[:, :, 1] < 70) & (sub[:, :, 2] > 40) & (sub[:, :, 2] < 130)).sum()
check('strip_X2_sysdot_border', dm > 150, f'dark magenta border px={dm}')

# ---- (7) new-box occlusion: right feed curve hidden behind box2's top-left ----
# in the original the curve vanishes under the box; assert no red curve ink INSIDE
# box2's interior (excluding its text bands)
sub = R[int(f2r(462)):int(f2r(522)), int(f2r(728)):int(f2r(893))]
red_in = ((sub[:, :, 0] - sub[:, :, 1] > 60) & (sub[:, :, 0] - sub[:, :, 2] > 50) & (sub[:, :, 0] > 110) &
          ~((np.arange(int(f2r(462)), int(f2r(522)))[:, None] > rb[0] - 4) & (np.arange(int(f2r(462)), int(f2r(522)))[:, None] < rb[1] + 4))).sum()
check('box2_occludes_curve', red_in == 0, f'stray red px in box2 interior (outside text band)={red_in}')

print()
print('SELFCHECK_ATTEMPT_1:', 'ALL PASS' if not fails else 'FAILS: ' + ', '.join(fails))
sys.exit(1 if fails else 0)
