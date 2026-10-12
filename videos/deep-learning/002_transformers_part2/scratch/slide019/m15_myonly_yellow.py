# m15: MY-only yellow pixels (delta strokes) + pin white text bbox.
from PIL import Image
import numpy as np
from collections import deque

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')).astype(int)
wa = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB').transform((960,540), Image.AFFINE, (1.0/Bx,0,-A/Bx,0,1.0/D,-C/D), resample=Image.BILINEAR)).astype(int)
def bld_x(fx): return (fx-18.0787)/0.961084
def bld_y(fy): return (fy-0.4700)/0.957187

def ymask(img):
    r, g, b = img[...,0], img[...,1], img[...,2]
    return (r > 170) & (g > 170) & (b < 150)

ym = ymask(my); yw = ymask(wa)
# dilate 001's mask by 2 to forgive misalignment
yd = yw.copy()
for _ in range(2):
    yd = yd | np.roll(yd,1,0) | np.roll(yd,-1,0) | np.roll(yd,1,1) | np.roll(yd,-1,1)
only = ym & ~yd
only[:300, :] = False; only[400:, :] = False   # study the trace zone y300..400 first
only[:, :600] = False; only[:, 871:] = False
ys, xs = np.where(only)
print(f'MY-only yellow px in trace zone: {len(xs)}')
# cluster
lab = np.zeros(only.shape, np.int32); comps = []
for y, x in zip(ys, xs):
    if lab[y, x] == 0:
        nid = len(comps)+1; q = deque([(y,x)]); lab[y,x] = nid; pts = []
        while q:
            cy, cx = q.popleft(); pts.append((cy,cx))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < 540 and 0 <= nx < 960 and only[ny,nx] and lab[ny,nx]==0:
                        lab[ny,nx] = nid; q.append((ny,nx))
        comps.append(pts)
comps.sort(key=len, reverse=True)
for pts in comps:
    if len(pts) < 12: break
    ys_ = [p[0] for p in pts]; xs_ = [p[1] for p in pts]
    print(f'  {len(pts):4d}px frame x{min(xs_)}..{max(xs_)} y{min(ys_)}..{max(ys_)} -> build x{bld_x(min(xs_)):.0f}..{bld_x(max(xs_)):.0f} y{bld_y(min(ys_)):.0f}..{bld_y(max(ys_)):.0f}')

# also full-slide MY-only yellow EXCLUDING the bottom band area (y395+) to catch any other adds
only2 = ym & ~yd
only2[:46,:] = False; only2[514:,:] = False; only2[:, :60] = False; only2[:, 900:] = False
ys2, xs2 = np.where(only2 & (np.arange(540)[:,None] < 395))
print(f'MY-only yellow above y395 frame: {len(xs2)}')

# pin white text
r, g, b = my[...,0], my[...,1], my[...,2]
red = (r > 120) & (g < 95) & (b < 95)
ys3, xs3 = np.where(red[290:460, 500:640])
inpin = [(y+290, x+500) for y, x in zip(ys3, xs3)]
wt = [(y, x) for (y, x) in inpin if my[y, x, 0] > 190 and my[y, x, 1] > 190 and my[y, x, 2] > 190]
wys = sorted(p[0] for p in wt); wxs = sorted(p[1] for p in wt)
print(f'pin white text: frame x{wxs[0]}..{wxs[-1]} y{wys[0]}..{wys[-1]} -> build x{bld_x(wxs[0]):.1f}..{bld_x(wxs[-1]):.1f} y{bld_y(wys[0]):.1f}..{bld_y(wys[-1]):.1f}')
rows = sorted(set(wys)); groups = []; cur = [rows[0]]
for y in rows[1:]:
    if y - cur[-1] <= 2: cur.append(y)
    else: groups.append(cur); cur = [y]
groups.append(cur)
for gq in groups:
    xs_g = [x for (y, x) in wt if y in gq]
    print(f'   line rows {gq[0]}..{gq[-1]} (b{bld_y(gq[0]):.1f}..{bld_y(gq[-1]):.1f}) x {min(xs_g)}..{max(xs_g)} (b{bld_x(min(xs_g)):.1f}..{bld_x(max(xs_g)):.1f})')
