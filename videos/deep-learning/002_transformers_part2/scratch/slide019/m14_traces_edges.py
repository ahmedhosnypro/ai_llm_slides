# m14: raw colors for chevron-zone verticals, band right edge, yellow trace map, pin text.
from PIL import Image
import numpy as np

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')).astype(int)
wa = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB').transform((960,540), Image.AFFINE, (1.0/Bx,0,-A/Bx,0,1.0/D,-C/D), resample=Image.BILINEAR)).astype(int)
def bld_x(fx): return (fx-18.0787)/0.961084
def bld_y(fy): return (fy-0.4700)/0.957187

print('== chevron zone1 vertical raw (x768..778, y184..202) MY:')
for y in range(184, 203, 2):
    print(f'  y{y}: ' + ' '.join(f'{x}:{my[y,x,0]},{my[y,x,1]},{my[y,x,2]}' for x in range(768, 779)))
print('== same 001:')
for y in range(184, 203, 2):
    print(f'  y{y}: ' + ' '.join(f'{x}:{wa[y,x,0]},{wa[y,x,1]},{wa[y,x,2]}' for x in range(768, 779)))

print('== band right edge fy=450, x876..906 MY:')
print('  ' + ' '.join(f'{x}:{my[450,x,0]},{my[450,x,1]},{my[450,x,2]}' for x in range(876, 907, 2)))
print('== band top edge at x=700 vertical fy393..403 MY:')
print('  ' + ' '.join(f'{y}:{my[y,690,0]},{my[y,690,1]},{my[y,690,2]}' for y in range(393, 404)))
print('== band bottom edge x=700 fy470..482 MY:')
print('  ' + ' '.join(f'{y}:{my[y,690,0]},{my[y,690,1]},{my[y,690,2]}' for y in range(470, 483)))

def is_yel(px): return px[0] > 170 and px[1] > 170 and px[2] < 150
print('== yellow trace map (rows with yellow runs in x600..870):')
for tag, img in [('MY', my), ('001', wa)]:
    print(' ', tag)
    prev = None
    for y in range(300, 400):
        runs = []; cur = None
        for x in range(600, 871):
            if is_yel(img[y, x]):
                if cur is None: cur = x
            else:
                if cur is not None and x - cur >= 3: runs.append((cur, x-1))
                cur = None
        if cur is not None and 870 - cur >= 3: runs.append((cur, 870))
        if runs:
            print(f'   y{y} (b{bld_y(y):.1f}): ' + ', '.join(f'{a}-{b}(bx{bld_x(a):.0f}..{bld_x(b):.0f})' for a, b in runs))

# pin white text bbox (redo)
r, g, b = my[...,0], my[...,1], my[...,2]
red = (r > 120) & (g < 95) & (b < 95)
sub = red[290:460, 500:640]
ys, xs = np.where(sub)
inpin = [(y+290, x+500) for y, x in zip(ys, xs)]
wt = [(y, x) for (y, x) in inpin if my[y, x, 0] > 190 and my[y, x, 1] > 190 and my[y, x, 2] > 190]
if wt:
    wys = sorted(p[0] for p in wt); wxs = sorted(p[1] for p in wt)
    print(f'== pin white text: frame x{wxs[0]}..{wxs[-1]} y{wys[0]}..{wys[-1]} -> build x{bld_x(wxs[0]):.1f}..{bld_x(wxs[-1]):.1f} y{bld_y(wys[0]):.1f}..{bld_y(wys[-1]):.1f}')
    rows = sorted(set(wys)); groups = []; cur = [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 2: cur.append(y)
        else: groups.append(cur); cur = [y]
    groups.append(cur)
    for gq in groups:
        xs_g = [x for (y, x) in wt if y in gq]
        print(f'   line rows {gq[0]}..{gq[-1]} (b{bld_y(gq[0]):.1f}..{bld_y(gq[-1]):.1f}) x {min(xs_g)}..{max(xs_g)} (b{bld_x(min(xs_g)):.1f}..{bld_x(max(xs_g)):.1f})')
