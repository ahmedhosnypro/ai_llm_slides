# m13: pin rows/white-text; chevron raw colors; band edge colors; yellow trace map.
from PIL import Image
import numpy as np
from collections import deque

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')).astype(int)
wa = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB').transform((960,540), Image.AFFINE, (1.0/Bx,0,-A/Bx,0,1.0/D,-C/D), resample=Image.BILINEAR)).astype(int)
def bld_x(fx): return (fx-18.0787)/0.961084
def bld_y(fy): return (fy-0.4700)/0.957187
def f2x(bx): return 18.0787 + 0.961084*bx
def f2y(by): return 0.4700 + 0.957187*by

# --- pin rows
r, g, b = my[...,0], my[...,1], my[...,2]
red = (r > 120) & (g < 95) & (b < 95)
win = np.zeros_like(red); win[290:500, 495:690] = red[290:500, 495:690]
lab = np.zeros(win.shape, np.int32); comps = []
for y in range(290, 500):
    for x in range(495, 690):
        if win[y, x] and lab[y, x] == 0:
            nid = len(comps)+1; q = deque([(y,x)]); lab[y,x] = nid; pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy,cx))
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        ny, nx = cy+dy, cx+dx
                        if 290 <= ny < 500 and 495 <= nx < 690 and win[ny,nx] and lab[ny,nx]==0:
                            lab[ny,nx] = nid; q.append((ny,nx))
            comps.append(pts)
comps.sort(key=len, reverse=True)
pin = comps[0]
print(f'-- pin: {len(pin)}px')
byrow = {}
for (y, x) in pin: byrow.setdefault(y, []).append(x)
for y in sorted(byrow):
    xs_ = byrow[y]
    if y % 4 == 0 or y == min(byrow) or y == max(byrow):
        print(f'   y{y} (b{bld_y(y):.1f}): x{min(xs_)}..{max(xs_)} (b{bld_x(min(xs_)):.1f}..{bld_x(max(xs_)):.1f}) w{max(xs_)-min(xs_)+1}')
wt = [(y,x) for (y,x) in pin if my[y,x,0]>190 and my[y,x,1]>190 and my[y,x,2]>190]
if wt:
    wys = sorted(p[0] for p in wt); wxs = sorted(p[1] for p in wt)
    print(f'   white text bbox frame x{wxs[0]}..{wxs[-1]} y{wys[0]}..{wys[-1]} -> build x{bld_x(wxs[0]):.1f}..{bld_x(wxs[-1]):.1f} y{bld_y(wys[0]):.1f}..{bld_y(wys[-1]):.1f}')
    # white row groups (two text lines?)
    rows = sorted(set(wys)); groups = []; cur = [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 2: cur.append(y)
        else: groups.append(cur); cur = [y]
    groups.append(cur)
    for gq in groups:
        xs_g = [x for (y, x) in wt if y in gq]
        print(f'     text line rows {gq[0]}..{gq[-1]} (b{bld_y(gq[0]):.1f}..{bld_y(gq[-1]):.1f}) x {min(xs_g)}..{max(xs_g)} (b{bld_x(min(xs_g)):.1f}..{bld_x(max(xs_g)):.1f})')

# --- chevron regions raw (3 locations in build pt): (783.5,197),(783.5,202) / (783.5,255.5),(783.5,259.5) / (772,313),(772,318)
for (cx, cy) in [(783.5, 199), (783.5, 257.5), (772, 315.5)]:
    fx, fy = int(f2x(cx)), int(f2y(cy))
    print(f'-- chevron zone build({cx},{cy}) frame({fx},{fy}) MY vs 001 (7x11 grid, N=navy d=dark .=light):')
    for tag, img in [('MY', my), ('001', wa)]:
        rows_ = []
        for y in range(fy-5, fy+6):
            row_ = ''
            for x in range(fx-3, fx+4):
                rr, gg, bb = img[y, x]
                if rr < 80 and gg < 80 and bb > 90: row_ += 'N'
                elif rr < 110 and gg < 140 and bb < 110: row_ += 'd'
                elif rr > 170 and gg > 200: row_ += '.'
                else: row_ += '?'
            rows_.append(row_)
        print('  ', tag, ' | '.join(rows_))

# --- bottom band: exact colors along a vertical cut at build x=700 (frame ~691) and x=860 (frame ~845)
for bxc in (700, 780, 860):
    fx = int(f2x(bxc))
    print(f'-- vertical cut at build x={bxc} (frame {fx}), fy 395..495 step 5:')
    for fy in range(395, 496, 5):
        print(f'   fy{fy} (b{bld_y(fy):.1f}) MY {tuple(my[fy,fx])}  001 {tuple(wa[fy,fx])}')
# horizontal cut at fy=450 from x 540..920 step 4 (MY only, classify)
print('-- fy450 MY colors x540..920:')
s = ''
for x in range(540, 921, 4):
    rr, gg, bb = my[450, x]
    if rr>170 and gg>170 and bb<150: s += 'Y'
    elif abs(rr-gg)<18 and abs(gg-bb)<18 and rr>200: s += '.'
    else: s += '?'
print('  ', s)
