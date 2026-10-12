# m12: leader-path scans, chevron grid, yellow band runs, pin blob extraction.
from PIL import Image
import numpy as np
from collections import deque

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')).astype(int)
wa = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB').transform((960,540), Image.AFFINE, (1.0/Bx,0,-A/Bx,0,1.0/D,-C/D), resample=Image.BILINEAR)).astype(int)

def f2(bx, by):  # build pt -> my frame px
    return 18.0787 + 0.961084*bx, 0.4700 + 0.957187*by

def sample_path(pts, tag):
    print(f'-- leader {tag}:')
    for (bx, by) in pts:
        fx, fy = f2(bx, by); xi, yi = int(round(fx)), int(round(fy))
        best_my = min((int(my[yy,xx].sum()), (xx,yy)) for yy in range(yi-2,yi+3) for xx in range(xi-2,xi+3))
        best_wa = min((int(wa[yy,xx].sum()), (xx,yy)) for yy in range(yi-2,yi+3) for xx in range(xi-2,xi+3))
        print(f'   build({bx},{by}) MY darkest {best_my[0]} @{best_my[1]} {tuple(my[best_my[1][1],best_my[1][0]])} | 001 {best_wa[0]} {tuple(wa[best_wa[1][1],best_wa[1][0]])}')

sample_path([(342,118),(470,120),(570,124),(622,138),(680,147),(726,152),(751,161)], 'L1')
sample_path([(464,122),(538,134),(570,143),(622,167),(700,172),(726,173),(740,181),(751,186)], 'L2')
sample_path([(514,157),(570,161),(622,183),(654,193),(676,224),(700,231),(738,236)], 'L3')
sample_path([(513,152),(538,161),(562,176),(578,206),(594,264),(610,290),(622,296),(638,301)], 'L4')
sample_path([(460,195),(506,201),(526,210),(538,225),(550,251),(562,296),(570,318),(584,330),(597,337)], 'L5')

# chevron region raw grid (build 776..792 x, 192..208 y -> frame)
fx0, fy0 = f2(774, 190); fx1, fy1 = f2(794, 210)
print(f'-- chevron grid frame x{int(fx0)}..{int(fx1)} y{int(fy0)}..{int(fy1)}')
for tag, img in [('MY', my), ('001', wa)]:
    print(tag)
    for y in range(int(fy0), int(fy1)):
        row = ''
        for x in range(int(fx0), int(fx1)):
            r, g, b = img[y, x]
            if r < 80 and g < 80 and b > 90: row += 'N'      # navy
            elif r < 100 and g < 130 and b < 100: row += 'd' # dark
            elif r > 180 and g > 200 and b > 180: row += '.' # panel green
            else: row += '?'
        print('   ', row)

# yellow band runs at three cuts (MY)
def runs(img, fy, x0, x1):
    out = []; cur = None
    for x in range(x0, x1):
        r, g, b = img[fy, x]
        yel = r > 170 and g > 170 and b < 150
        if yel and cur is None: cur = x
        elif not yel and cur is not None:
            out.append((cur, x-1)); cur = None
    if cur is not None: out.append((cur, x1-1))
    return [seg for seg in out if seg[1]-seg[0] >= 2]

for fy in (405, 430, 450, 470, 485):
    rm = runs(my, fy, 480, 920); rw = runs(wa, fy, 480, 920)
    fmt = lambda segs: ', '.join(f'{a}-{b}(b{(a-18.08)/0.961084:.0f}..{(b-18.08)/0.961084:.0f})' for a, b in segs)
    print(f'fy={fy} build_y={(fy-0.47)/0.957187:.0f} MY yellow runs: {fmt(rm)}')
    print(f'          001 yellow runs: {fmt(rw)}')

# pin blob: largest red connected component in window
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
ys = [p[0] for p in pin]; xs = [p[1] for p in pin]
print(f'-- pin blob: {len(pin)}px bbox frame x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} -> build x{(min(xs)-18.08)/0.961084:.1f}..{(max(xs)-18.08)/0.961084:.1f} y{(min(ys)-0.47)/0.957187:.1f}..{(max(ys)-0.47)/0.957187:.1f}')
# per-row width to find head vs tail
widths = {}
for y in set(ys):
    xr = [x for x in xs if p[0]==y for p in [(y,x)]]
widths = {}
for y in set(ys):
    xr = [x for (yy, x) in pin if yy == y]
    widths[y] = (min(xr), max(xr))
for y in sorted(widths):
    if y % 6 == 0 or y in (min(ys), max(ys)):
        a, bb = widths[y]
        print(f'   y{y} (b{(y-0.47)/0.957187:.1f}): x{a}..{bb} w{bb-a+1}')
# white text inside pin
wt = [(y,x) for (y,x) in pin if my[y,x,0]>200 and my[y,x,1]>200 and my[y,x,2]>200]
if wt:
    wys = [p[0] for p in wt]; wxs = [p[1] for p in wt]
    print(f'   white text bbox frame x{min(wxs)}..{max(wxs)} y{min(wys)}..{max(wys)} -> build x{(min(wxs)-18.08)/0.961084:.1f}..{(max(wxs)-18.08)/0.961084:.1f} y{(min(wys)-0.47)/0.957187:.1f}..{(max(wys)-0.47)/0.957187:.1f}')
