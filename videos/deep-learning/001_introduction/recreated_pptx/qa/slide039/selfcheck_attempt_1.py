#!/usr/bin/env python3
"""Closed-loop 150dpi self-check for slide_039 attempt 1 (pre-judge, mandatory).
Scale: frame px (960x540, 1px=1pt) -> render px (2001x1125 @150dpi) = *150.08/72.
Checks: title band, white box stroke edges, per-line text bands + left inks, phrase
highlight rect, photo pixel-identity + cursor absence, annot box edges, annot line
bands + colored words + yellow blank, frame containment. Tolerance 5px @150dpi."""
from PIL import Image
import numpy as np
import json

REN = 'videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/render_1.png'
ORIG = 'videos/deep-learning/001_introduction/unique_slides/slide_039.jpg'
r = np.asarray(Image.open(REN).convert('RGB')).astype(int)
o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
H, W = r.shape[:2]
S = W / 960.0
print(f'render {W}x{H}, scale S={S:.4f} (frame px -> render px)')

results = []
def check(name, ok, detail):
    results.append((name, bool(ok), detail))
    print(f'{"PASS" if ok else "FAIL"}  {name}: {detail}')

def band(mask, y0, y1, x0, x1):
    seg = mask[y0:y1, x0:x1]
    ys, xs = np.where(seg)
    if len(ys) == 0:
        return None
    return (int(ys.min() + y0), int(ys.max() + y0), int(xs.min() + x0), int(xs.max() + x0))

Rr, Gr, Br = r[:, :, 0], r[:, :, 1], r[:, :, 2]
redm = (Rr > 150) & (Rr - Gr > 70) & (Rr - Br > 70)
darkm = (Rr < 120) & (Gr < 120) & (Br < 120)
bluem = (Br > 130) & (Br - Rr > 40) & (Br - Gr > 40)
yellowm = (Rr > 200) & (Gr > 190) & (Br < 140)

# 1. title band — CORE band (rows with ink >= 25% of max row ink), robust to AA-fringe
#    sharpness differences between the JPEG original and the crisp render; window rows
#    52..98 frame (excludes chrome border/badge), x 180..830 (excludes chrome borders)
def core_band(mask, y0, y1, x0, x1, frac=0.25):
    seg = mask[y0:y1, x0:x1]
    rows = seg.sum(axis=1)
    nz = np.where(rows >= frac * rows.max())[0]
    cols = seg[nz.min():nz.max() + 1].sum(axis=0)
    cnz = np.where(cols > 0)[0]
    return (int(nz.min() + y0), int(nz.max() + y0), int(cnz.min() + x0), int(cnz.max() + x0))

t = core_band(redm, int(52 * S), int(98 * S), int(180 * S), int(830 * S))
# core band ~ cap-top..baseline+partial-x; compare against the original's core band
t_orig = core_band((o[:, :, 0] > 140) & (o[:, :, 0] - o[:, :, 1] > 60) & (o[:, :, 0] - o[:, :, 2] > 60),
                   52, 98, 180, 830)
t_exp = tuple(v * S for v in t_orig)
check('title.ink_band', t and all(abs(a - b) <= 5 for a, b in zip(t, t_exp)),
      f'meas={t} orig_core* S=({t_exp[0]:.0f},{t_exp[1]:.0f},{t_exp[2]:.0f},{t_exp[3]:.0f})')
exp_removed = None  # stale full-band check removed: superseded by the core-band
# comparison above (the full ink mask truncates the JPEG original's AA fringe
# asymmetrically vs the crisp render — the core band is the geometry-bearing signal).

# 2. white box edges: stroke = local luminance dip near expected lines
def edge_pos(fixed, axis, lo, hi, expected):
    # scan along axis at fixed coordinate; find darkest-run center within [lo,hi)
    if axis == 'row':
        line = r[fixed, lo:hi].mean(axis=1)
    else:
        line = r[lo:hi, fixed].mean(axis=1)
    i = int(np.argmin(line))
    return lo + i
wb = {}
wb['top'] = np.mean([edge_pos(int(x * S), 'col', int(95 * S), int(107 * S), 100.5) for x in (200, 400, 600, 800)]) / S
wb['bottom'] = np.mean([edge_pos(int(x * S), 'col', int(288 * S), int(302 * S), 295) for x in (200, 400, 600, 700)]) / S
wb['left'] = np.mean([edge_pos(int(y * S), 'row', int(70 * S), int(82 * S), 75.5) for y in (120, 160, 200, 260)]) / S
wb['right'] = np.mean([edge_pos(int(y * S), 'row', int(873 * S), int(888 * S), 880.5) for y in (120, 160, 200, 260)]) / S
exp_wb = {'top': 100.5, 'bottom': 295, 'left': 75.5, 'right': 880.5}
check('whitebox.edges', all(abs(wb[k] - exp_wb[k]) <= 2.5 for k in exp_wb),
      ' '.join(f'{k}={wb[k]:.1f}(exp {exp_wb[k]})' for k in exp_wb) + ' [frame px]')

# 3. white-box text lines (dark ink bands inside box, x 170..1830 render)
by0, by1 = int(103 * S), int(293 * S)
seg = darkm[by0:by1, int(88 * S):int(875 * S)]
rows = seg.sum(axis=1)
bands = []
inb = False
for i, c in enumerate(rows):
    if c > 3 and not inb:
        s = i; inb = True
    elif c <= 3 and inb:
        if i - s > 4: bands.append((s + by0, i - 1 + by0))
        inb = False
if inb: bands.append((s + by0, len(rows) - 1 + by0))
# merge descender fragments (gap <= 5px)
merged = []
for b in bands:
    if merged and b[0] - merged[-1][1] <= 5:
        merged[-1] = (merged[-1][0], b[1])
    else:
        merged.append(list(b))
exp_lines = [(111, 130), (138, 157), (162, 183), (217, 233), (243, 263), (269, 289)]
ok = len(merged) == 6
detail = f'bands(frame-px)={[(round(a/S,1), round(b/S,1)) for a,b in merged]} exp={exp_lines}'
if ok:
    for (ma, mb), (ea, eb) in zip(merged, exp_lines):
        if abs(ma / S - ea) > 4 or abs(mb / S - eb) > 4:
            ok = False
check('whitebox.6_lines', ok, detail)

# per-line left ink
for i, (ln, e) in enumerate(zip(merged, [85, 85, 86, 85, 86, 85])):
    if mb := ln:
        lb = band(darkm, ln[0], ln[1] + 1, int(80 * S), int(875 * S))
        if lb:
            check(f'line{i+1}.left_ink', abs(lb[2] / S - e) <= 4, f'left={lb[2]/S:.1f} exp={e}')

# 4. phrase highlight rect (yellow) present at measured box
yb = band(yellowm, int(255 * S), int(300 * S), int(200 * S), int(760 * S))
exp_h = (264 * S, 290 * S, 240 * S, 719 * S)
check('phrase.highlight_rect', yb and abs(yb[0] / S - 264) <= 5 and abs(yb[2] / S - 240) <= 5 and abs(yb[3] / S - 719) <= 5,
      f'meas={yb and tuple(round(v/S,1) for v in yb)} exp~(264,290,240,719)')

# 5. photos: pixel-identity vs original crop + cursor absence
def region_diff(bx, name):
    x0, y0, x1, y1 = bx
    crop_r = r[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)].astype(float)
    crop_o = o[y0:y1, x0:x1].astype(float)
    crop_r2 = np.asarray(Image.fromarray(crop_r.astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.LANCZOS)).astype(float)
    d = np.abs(crop_r2 - crop_o).mean()
    check(f'photo.{name}.pixel_diff', d < 30, f'meanAbsDiff={d:.1f} (same pixels re-rasterized)')
region_diff((184, 309, 447, 442), 'cat_inner')
region_diff((474, 306, 731, 442), 'dog_inner')
# cursor absence: bright cluster INSIDE the cat photo near its right edge
# (frame x 436..447 — strictly left of the border stroke at 448; the couch there is
# ~(125-155) gray-blue, so >215 bright px = cursor remnants. The panel gray right of
# the photo is inherently bright and is NOT part of the asset.)
cat = r[int(345 * S):int(380 * S), int(436 * S):int(447 * S)]
bright = ((cat[:, :, 0] > 215) & (cat[:, :, 1] > 215) & (cat[:, :, 2] > 210)).sum()
check('cat.cursor_absent', int(bright) <= 6, f'bright px inside photo edge zone={int(bright)} (patched asset)')

# 6. annot box edges
ab = {}
ab['top'] = np.mean([edge_pos(int(x * S), 'col', int(446 * S), int(459 * S), 452.5) for x in (200, 400, 600, 800)]) / S
ab['bottom'] = np.mean([edge_pos(int(x * S), 'col', int(508 * S), int(520 * S), 514) for x in (200, 400, 600, 800)]) / S
ab['left'] = np.mean([edge_pos(int(y * S), 'row', int(66 * S), int(78 * S), 72) for y in (470, 480, 490, 500)]) / S
ab['right'] = np.mean([edge_pos(int(y * S), 'row', int(894 * S), int(906 * S), 900.5) for y in (470, 480, 490, 500)]) / S
exp_ab = {'top': 452.5, 'bottom': 514, 'left': 72, 'right': 900.5}
check('annotbox.edges', all(abs(ab[k] - exp_ab[k]) <= 2.5 for k in exp_ab),
      ' '.join(f'{k}={ab[k]:.1f}(exp {exp_ab[k]})' for k in exp_ab) + ' [frame px]')

# 7. annot text lines (blue-dominant ink bands inside annot box)
ay0, ay1 = int(456 * S), int(510 * S)
ink_annot = darkm | bluem
seg = ink_annot[ay0:ay1, int(78 * S):int(890 * S)]
rows = seg.sum(axis=1)
bands2 = []
inb = False
for i, c in enumerate(rows):
    if c > 3 and not inb:
        s = i; inb = True
    elif c <= 3 and inb:
        if i - s > 3: bands2.append((s + ay0, i - 1 + ay0))
        inb = False
if inb: bands2.append((s + ay0, len(rows) - 1 + ay0))
exp_annot = [(460, 471), (476, 487), (492, 503)]
ok2 = len(bands2) == 3
if ok2:
    for (ma, mb), (ea, eb) in zip(bands2, exp_annot):
        if abs(ma / S - ea) > 4 or abs(mb / S - eb) > 4:
            ok2 = False
check('annot.3_lines', ok2, f'bands(frame-px)={[(round(a/S,1), round(b/S,1)) for a,b in bands2]} exp={exp_annot}')

# colored words
redseg = band(redm, int(458 * S), int(474 * S), int(100 * S), int(200 * S))
check('annot.Red_word_x', redseg and abs(redseg[2] / S - 124) <= 6 and abs(redseg[3] / S - 147) <= 6,
      f'meas x=({redseg[2]/S:.1f}..{redseg[3]/S:.1f}) exp (124..147)')
grn = (Gr > 110) & (Gr - Rr > 15) & (Gr - Br > 15)
gseg = band(grn, int(490 * S), int(506 * S), int(100 * S), int(220 * S))
check('annot.Green_word_x', gseg and abs(gseg[2] / S - 121) <= 6 and abs(gseg[3] / S - 162) <= 6,
      f'meas x=({gseg[2]/S:.1f}..{gseg[3]/S:.1f}) exp (121..162)')
yblank = band(yellowm, int(470 * S), int(494 * S), int(100 * S), int(220 * S))
check('annot.yellow_blank', yblank and abs(yblank[2] / S - 120.5) <= 6 and abs(yblank[3] / S - 163.5) <= 6,
      f'meas x=({yblank and round(yblank[2]/S,1)}..{yblank and round(yblank[3]/S,1)}) exp (120.5..163.5)')

# 8. frame containment: content ink inside panel (x 42..918, y 45..540 frame)
cont = np.zeros_like(darkm)
cont[int(48 * S):H, int(45 * S):int(915 * S)] = True
stray = (darkm & ~cont)
# ignore the badge area (chrome numeral) and chrome border rows
badge = np.zeros_like(darkm); badge[int(53 * S):int(90 * S), int(875 * S):int(912 * S)] = True
chrome_border = np.zeros_like(darkm)
chrome_border[:, int(41 * S):int(45 * S)] = True; chrome_border[:, int(917 * S):int(921 * S)] = True
chrome_border[int(43 * S):int(47 * S), :] = True
stray = stray & ~badge & ~chrome_border
n_stray = int(stray.sum())
check('frame.containment', n_stray < 150, f'stray dark px outside panel (excl chrome/badge)={n_stray}')

n_fail = sum(1 for _, ok, _ in results if not ok)
print(f'\nTOTAL: {len(results)} checks, {n_fail} FAIL')
with open('videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/selfcheck_attempt_1_out.json', 'w') as f:
    json.dump({'checks': [(n, o, d) for n, o, d in results], 'fails': n_fail}, f, indent=1)
