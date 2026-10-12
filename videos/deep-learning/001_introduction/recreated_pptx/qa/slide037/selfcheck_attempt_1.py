# selfcheck_attempt_1.py — mandatory pre-judge self-check for slide 037 (attempt 1).
# Render space: 150dpi, frame->render scale = 150/72 (x2.08333).
from PIL import Image
import json

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
ren = Image.open(f'{BASE}/recreated_pptx/qa/slide037/render_1.png').convert('RGB')
orig = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
rp, op = ren.load(), orig.load()
RW, RH = ren.size
SC = 150 / 72.0
results = {}
fails = []

def fr(v):  # frame px -> render px
    return v * SC

def ink_bbox(p, x0, y0, x1, y1, thr=260, step=1):
    xs, ys = [], []
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if sum(p[x, y]) < thr:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None

# ---- 2) FRAME CONTAINMENT: all content inside the white panel (65..896 x 262..511)
# and inside the chrome gray panel (42..918 x 45..539). Render-scale check.
cont = {}
cont['chrome_ok'] = True
for (x0, y0, x1, y1, name) in [
    (fr(64), fr(136), fr(905), fr(245), 'yellowbox'),
    (fr(65), fr(262), fr(896), fr(511), 'white_panel'),
]:
    if not (x0 >= fr(42) - 2 and x1 <= fr(918) + 2 and y0 >= fr(45) - 2 and y1 <= fr(540)):
        cont['chrome_ok'] = False
        fails.append(f'containment: {name} outside chrome panel')
# diagram tile + question/equation ink inside the white panel (render px)
d = ink_bbox(rp, int(fr(70)), int(fr(264)), int(fr(892)), int(fr(452)), thr=400, step=2)
if d:
    ok = d[0] >= fr(66) - 2 and d[2] <= fr(895) + 2 and d[1] >= fr(263) - 2 and d[3] <= fr(512) + 2
    cont['diagram_inside_panel'] = bool(ok)
    if not ok: fails.append(f'containment: diagram ink {d} outside panel')
q = ink_bbox(rp, int(fr(70)), int(fr(452)), int(fr(640)), int(fr(510)), thr=260, step=1)
if q:
    ok = q[2] <= fr(895) and q[3] <= fr(510)
    cont['question_inside_panel'] = bool(ok)
    if not ok: fails.append(f'containment: question ink {q} outside panel')
results['containment'] = cont

# ---- 3) EQUATIONS EXIST: ink in the equation region (target ink top 487 frame px)
eq = ink_bbox(rp, int(fr(180)), int(fr(482)), int(fr(440)), int(fr(508)), thr=430, step=1)
results['eq_ink'] = eq
if not eq or eq[4] < 50:
    fails.append(f'equation region empty/too sparse: {eq}')

# ---- 7/8) YELLOW BOX: 3 line bands, pitch 33 frame px, no wrap, no 4th line
# scan dark-ink rows inside the box (render space)
rows = []
for y in range(int(fr(140)), int(fr(243))):
    cnt = sum(1 for x in range(int(fr(80)), int(fr(880)), 2) if sum(rp[x, y]) < 300)
    rows.append((y, cnt))
bands = []
for y, c in rows:
    if c > 3:
        if bands and y - bands[-1][1] <= 5: bands[-1][1] = y
        else: bands.append([y, y])
results['ybox_line_bands_render'] = bands
if len(bands) != 3:
    fails.append(f'yellow box: expected 3 line bands, got {len(bands)}: {bands}')
else:
    pitches = [bands[1][0] - bands[0][0], bands[2][0] - bands[1][0]]
    results['ybox_pitches_render'] = pitches
    for i, p in enumerate(pitches):
        if abs(p - fr(33)) > 6:
            fails.append(f'yellow box line pitch {i}: {p} vs {fr(33):.1f}')
# L1 left edge: first ink col of band 1
l1 = ink_bbox(rp, int(fr(66)), bands[0][0], int(fr(890)), bands[0][1], thr=300) if bands else None
results['L1_ink'] = l1
if l1 and abs(l1[0] - fr(75)) > 8:
    fails.append(f'L1 left ink {l1[0]} vs target {fr(75):.1f}')
if l1 and abs(l1[2] - fr(878)) > 14:
    fails.append(f'L1 right ink {l1[2]} vs target {fr(878):.1f} (wrap? size?)')
# no ink below the box bottom border before the panel (wrap check)
stray = ink_bbox(rp, int(fr(70)), int(fr(247)), int(fr(890)), int(fr(259)), thr=400, step=1)
results['stray_below_ybox'] = stray
if stray and stray[4] > 12:
    fails.append(f'stray ink between yellow box and panel: {stray}')

# ---- closed-loop vs ORIGINAL (scaled): title, panel border, diagram tile, question, eq
def bbox_of(pred, x0, y0, x1, y1, p, step=1):
    xs, ys = [], []
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if pred(p[x, y]):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None

red = lambda c: c[0] > 120 and c[1] < 110 and c[2] < 110 and c[0] > c[1] + 40
dark = lambda c: sum(c) < 300

# title
rt = bbox_of(red, int(fr(70)), int(fr(70)), int(fr(900)), int(fr(120)), rp, 2)
results['title_ink_render'] = rt
if rt:
    dx0 = rt[0] - fr(128); dx1 = rt[2] - fr(837); dy0 = rt[1] - fr(80); dy1 = rt[3] - fr(112)
    results['title_delta_frame_px'] = [round(v / SC, 1) for v in (dx0, dy0, dx1, dy1)]
    if max(abs(dx0), abs(dx1)) > 9 or abs(dy0) > 9 or abs(dy1) > 9:
        fails.append(f'title ink offset (frame px): {results["title_delta_frame_px"]}')

# white panel border rows/cols
def border_check(p, px_scale):
    top = None; bot = None; lef = None; rig = None
    for y in range(int(fr(256)), int(fr(270))):
        cnt = sum(1 for x in range(int(fr(80)), int(fr(880)), 2)
                  if (lambda c: c[0] > 110 and c[1] < 90 and c[2] < 100)(p[x, y]))
        if cnt > int(300 * px_scale): top = y; break
    for y in range(int(fr(516)), int(fr(500)), -1):
        cnt = sum(1 for x in range(int(fr(80)), int(fr(880)), 2)
                  if (lambda c: c[0] > 110 and c[1] < 90 and c[2] < 100)(p[x, y]))
        if cnt > int(300 * px_scale): bot = y; break
    for x in range(int(fr(58)), int(fr(75))):
        cnt = sum(1 for y in range(int(fr(280)), int(fr(500)), 2)
                  if (lambda c: c[0] > 110 and c[1] < 90 and c[2] < 100)(p[x, y]))
        if cnt > int(80 * px_scale): lef = x; break
    for x in range(int(fr(905)), int(fr(885)), -1):
        cnt = sum(1 for y in range(int(fr(280)), int(fr(500)), 2)
                  if (lambda c: c[0] > 110 and c[1] < 90 and c[2] < 100)(p[x, y]))
        if cnt > int(80 * px_scale): rig = x; break
    return top, bot, lef, rig
rt_, rb_, rl_, rr_ = border_check(rp, 1.0)
results['panel_borders_render'] = dict(top=rt_, bottom=rb_, left=rl_, right=rr_)
exp = dict(top=fr(262), bottom=fr(511), left=fr(65), right=fr(896))
for k, v, e in [('top', rt_, exp['top']), ('bottom', rb_, exp['bottom']),
                ('left', rl_, exp['left']), ('right', rr_, exp['right'])]:
    if v is None or abs(v - e) > 8:
        fails.append(f'panel border {k}: {v} vs {e:.1f}')

# diagram tile: pixel diff between render region and original region (baked pixels)
dd = 0; tot = 0
for y in range(int(fr(270)), int(fr(448)), 2):
    for x in range(int(fr(72)), int(fr(890)), 2):
        a = rp[x, y]; b = op[int(x / SC), int(y / SC)]
        dd += abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]); tot += 1
results['diagram_tile_meandiff'] = round(dd / tot, 2)
if dd / tot > 25:
    fails.append(f'diagram tile mean diff too high: {dd/tot:.1f}')

# question
rq = bbox_of(dark, int(fr(70)), int(fr(452)), int(fr(640)), int(fr(512)), rp, 1)
results['question_ink_render'] = rq
if rq:
    d_ = [round((rq[0] - fr(73)) / SC, 1), round((rq[1] - fr(453)) / SC, 1),
          round((rq[2] - fr(583)) / SC, 1), round((rq[3] - fr(483)) / SC, 1)]
    results['question_delta_frame_px'] = d_
    if max(abs(d_[0]), abs(d_[2])) > 9 or abs(d_[1]) > 9 or abs(d_[3]) > 9:
        fails.append(f'question ink offset (frame px): {d_}')

# equation: ink bbox + crowding-fix assertions
if eq:
    d_ = [round((eq[0] - fr(196)) / SC, 1), round((eq[1] - fr(487)) / SC, 1),
          round((eq[2] - fr(417)) / SC, 1), round((eq[3] - fr(494) + 8) / SC, 1)]
    results['eq_delta_frame_px_vs_placed'] = d_
    if abs(d_[0]) > 5 or abs(d_[1]) > 5:
        fails.append(f'equation ink anchor off: {d_}')
    # band gap: question ink bottom vs equation ink top (render px)
    if q and eq:
        gap = eq[1] - q[3]
        results['band_gap_q_to_eq_render'] = gap
        if gap < 2:
            fails.append(f'question/equation band gap {gap} < 2 render px')
    # clearance to panel bottom border
    if eq:
        clr = fr(511) - eq[3]
        results['eq_to_border_clearance_render'] = round(clr, 1)
        if clr < 8:
            fails.append(f'equation too close to panel border: {clr:.1f}')

# ---- 4) DELIMITER GEOMETRY: L3 starts with '[' — verify the bracket ink exists at L3 left
l3 = None
if len(bands) == 3:
    l3 = ink_bbox(rp, int(fr(66)), bands[2][0], int(fr(120)), bands[2][1] + 2, thr=300)
results['L3_bracket_ink'] = l3
if not l3:
    fails.append('L3 leading [ not found')

print(json.dumps(results, indent=1, default=str))
print('FAILS:', len(fails))
for f in fails: print('  FAIL:', f)
