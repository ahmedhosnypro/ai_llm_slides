# selfcheck_attempt_2.py — mandatory pre-judge self-check, slide 037, attempt 2.
# Fixes vs attempt 1: red-only equation classifier, black-only question classifier
# (attempt 1's scans cross-contaminated), band grouping gap 12, eq clearance >= 6.
from PIL import Image
import json

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
ren = Image.open(f'{BASE}/recreated_pptx/qa/slide037/render_2.png').convert('RGB')
orig = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
rp, op = ren.load(), orig.load()
SC = 150 / 72.0
fr = lambda v: v * SC
results = {}
fails = []

def bbox(p, pred, x0, y0, x1, y1, step=1):
    xs, ys = [], []
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if pred(p[x, y]):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None

red = lambda c: c[0] > 130 and c[1] < 115 and c[2] < 115 and c[0] > c[1] + 50
black = lambda c: sum(c) < 300 and not (c[0] > c[1] + 40 and c[0] > 110)

# ---- containment
cont = {'chrome_ok': True}
for (x0, y0, x1, y1, name) in [
    (fr(64), fr(136), fr(905), fr(245), 'yellowbox'),
    (fr(65), fr(262), fr(896), fr(511), 'white_panel'),
]:
    if not (x0 >= fr(42) - 2 and x1 <= fr(918) + 2 and y0 >= fr(45) - 2 and y1 <= fr(540)):
        cont['chrome_ok'] = False; fails.append(f'containment: {name} outside chrome')
d = bbox(rp, lambda c: sum(c) < 400, int(fr(70)), int(fr(264)), int(fr(892)), int(fr(452)), 2)
cont['diagram_inside_panel'] = bool(d) and d[0] >= fr(66) - 2 and d[2] <= fr(895) + 2 and d[1] >= fr(263) - 2 and d[3] <= fr(512) + 2
if not cont['diagram_inside_panel']: fails.append(f'containment: diagram {d}')
q = bbox(rp, black, int(fr(70)), int(fr(448)), int(fr(640)), int(fr(486)))
cont['question_inside_panel'] = bool(q) and q[2] <= fr(895) and q[3] <= fr(510)
if not cont['question_inside_panel']: fails.append(f'containment: question {q}')
results['containment'] = cont

# ---- equations exist (red-only)
e = bbox(rp, red, int(fr(150)), int(fr(470)), int(fr(500)), int(fr(509)))
results['eq_ink_render'] = e
if not e or e[4] < 50:
    fails.append(f'equation empty/sparse: {e}')
else:
    ef = [round(e[0] / SC, 1), round(e[1] / SC, 1), round(e[2] / SC, 1), round(e[3] / SC, 1)]
    results['eq_frame'] = ef
    results['eq_delta_vs_placed'] = [round(ef[0] - 196, 1), round(ef[1] - 487, 1),
                                     round(ef[2] - 417, 1), round(ef[3] - 504.2, 1)]
    if abs(ef[0] - 196) > 5 or abs(ef[1] - 487) > 5:
        fails.append(f'eq anchor off: {ef}')
    if q:
        gap = (e[1] - q[3]) / SC
        results['band_gap_q_eq_frame'] = round(gap, 1)
        if gap < 4: fails.append(f'q->eq band gap {gap:.1f} < 4 frame px')
    clr = (fr(511) - e[3]) / SC
    results['eq_border_clearance_frame'] = round(clr, 1)
    if clr < 6: fails.append(f'eq clearance {clr:.1f} < 6')

# ---- yellow box: 3 bands, pitch 33, left edge 75, L1 width, L3 bracket
rows = []
for y in range(int(fr(140)), int(fr(243))):
    cnt = sum(1 for x in range(int(fr(80)), int(fr(880)), 2) if sum(rp[x, y]) < 300)
    rows.append((y, cnt))
bands = []
for y, c in rows:
    if c > 3:
        if bands and y - bands[-1][1] <= 12: bands[-1][1] = y
        else: bands.append([y, y])
results['ybox_bands_frame'] = [[round(b[0]/SC,1), round(b[1]/SC,1)] for b in bands]
if len(bands) != 3:
    fails.append(f'yellow box: {len(bands)} bands (want 3)')
else:
    tops = [b[0] / SC for b in bands]
    results['ybox_tops_frame'] = [round(t, 1) for t in tops]
    for i, (t, tgt) in enumerate(zip(tops, [150, 183, 216])):
        if abs(t - tgt) > 4: fails.append(f'ybox L{i+1} top {t:.1f} vs {tgt}')
    pit = [round((bands[1][0]-bands[0][0])/SC,1), round((bands[2][0]-bands[1][0])/SC,1)]
    results['ybox_pitches_frame'] = pit
    for p in pit:
        if abs(p - 33) > 2.5: fails.append(f'ybox pitch {p} vs 33')
    l1 = bbox(rp, black, int(fr(66)), bands[0][0], int(fr(890)), bands[0][1])
    results['L1_frame'] = [round(v/SC,1) for v in l1[:4]]
    if abs(l1[0]/SC - 75) > 5: fails.append(f'L1 left {l1[0]/SC:.1f} vs 75')
    results['L1_right_frame'] = round(l1[2]/SC, 1)
    if abs(l1[2]/SC - 878) > 14: fails.append(f'L1 right {l1[2]/SC:.1f} vs 878 (+1% fit, doc)')
    l3 = bbox(rp, black, int(fr(66)), bands[2][0], int(fr(130)), bands[2][1] + 2)
    results['L3_bracket_ink'] = l3
    if not l3: fails.append('L3 [ missing')
stray = bbox(rp, lambda c: sum(c) < 400, int(fr(70)), int(fr(247)), int(fr(890)), int(fr(259)))
results['stray_below_ybox'] = stray
if stray and stray[4] > 12: fails.append(f'stray ink below ybox: {stray}')

# ---- title (red-only), target ink x128..837 y80..112
t = bbox(rp, red, int(fr(70)), int(fr(70)), int(fr(900)), int(fr(120)), 2)
results['title_frame'] = [round(v/SC,1) for v in t[:4]] if t else None
if t:
    dd = [round((t[0]/SC - 128),1), round((t[1]/SC - 80),1), round((t[2]/SC - 837),1), round((t[3]/SC - 112),1)]
    results['title_delta_frame'] = dd
    if max(abs(dd[0]), abs(dd[2])) > 9 or abs(dd[1]) > 5 or abs(dd[3]) > 5:
        fails.append(f'title delta: {dd}')

# ---- panel borders
def first_red_run(p, rng, vertical, lo, hi, need):
    for v in rng:
        cnt = 0
        if vertical:
            for y in range(int(fr(280)), int(fr(500)), 2):
                if (lambda c: c[0] > 110 and c[1] < 90 and c[2] < 100)(p[v, y]): cnt += 1
        else:
            for x in range(int(fr(80)), int(fr(880)), 2):
                if (lambda c: c[0] > 110 and c[1] < 90 and c[2] < 100)(p[x, v]): cnt += 1
        if cnt > need: return v
    return None
pt_ = first_red_run(rp, range(int(fr(256)), int(fr(270))), False, 0, 0, 150)
pb_ = first_red_run(rp, range(int(fr(516)), int(fr(500)), -1), False, 0, 0, 150)
pl_ = first_red_run(rp, range(int(fr(58)), int(fr(75))), True, 0, 0, 40)
pr_ = first_red_run(rp, range(int(fr(905)), int(fr(885)), -1), True, 0, 0, 40)
results['panel_borders_frame'] = dict(top=round(pt_/SC,1) if pt_ else None,
    bottom=round(pb_/SC,1) if pb_ else None, left=round(pl_/SC,1) if pl_ else None,
    right=round(pr_/SC,1) if pr_ else None)
for k, v, tgt in [('top', pt_, 262), ('bottom', pb_, 511), ('left', pl_, 65), ('right', pr_, 896)]:
    if v is None or abs(v/SC - tgt) > 4: fails.append(f'panel border {k} off: {v}')

# ---- diagram tile pixel identity
dd_ = 0; tot = 0
for y in range(int(fr(270)), int(fr(448)), 2):
    for x in range(int(fr(72)), int(fr(890)), 2):
        a = rp[x, y]; b = op[int(x/SC), int(y/SC)]
        dd_ += abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]); tot += 1
results['diagram_tile_meandiff'] = round(dd_/tot, 2)
if dd_/tot > 25: fails.append(f'diagram tile diff {dd_/tot:.1f}')

# ---- question (black-only), target x73..583 y453..483
results['question_frame'] = [round(v/SC,1) for v in q[:4]] if q else None
if q:
    dd = [round((q[0]/SC - 73),1), round((q[1]/SC - 453),1), round((q[2]/SC - 583),1), round((q[3]/SC - 483),1)]
    results['question_delta_frame'] = dd
    if max(abs(dd[0]), abs(dd[2])) > 9 or abs(dd[1]) > 5 or abs(dd[3]) > 6:
        fails.append(f'question delta: {dd}')

print(json.dumps(results, indent=1, default=str))
print('FAILS:', len(fails))
for f in fails: print('  FAIL:', f)
