#!/usr/bin/env python3
"""Targeted scans for slide_053 fine structure."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_053.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def s(fx): return (fx - 18.45) / 0.95991
def sy(fy): return (fy + 0.29) / 0.95600

print('=== 1. statement box: blue rows y 410..515 (count per row, x 50..910) ===')
blue = (b - (r + g) / 2 > 55)
for y in range(410, 516):
    n = blue[y, 50:910].sum()
    if n > 0:
        xs = np.where(blue[y, 50:910])[0] + 50
        print(f'  row {y} (slide {sy(y):6.1f}): n={n:4d} x {xs.min()}..{xs.max()}')

print('=== 2. equation box interior census (x 728..882, y 128..195) ===')
z = a[128:196, 728:883].reshape(-1, 3)
cnt = Counter((tuple(p // 32 * 32) for p in z))
for c, n in cnt.most_common(12):
    print('  ', c, n)
# darker threshold scan inside box
dark2 = (r < 165) & (g < 165) & (b < 165)
z2 = dark2[128:196, 730:881]
ys, xs = np.where(z2)
if len(xs):
    print('  dark-ish ink bbox inside box: x', xs.min()+730, '..', xs.max()+730, ' y', ys.min()+128, '..', ys.max()+128, ' n', len(xs))
    from scipy import ndimage
    lab, n = ndimage.label(z2, structure=np.ones((3,3)))
    comps = []
    for i in range(1, n+1):
        yy, xx = np.where(lab == i)
        if len(xx) < 8: continue
        comps.append((len(xx), xx.min()+730, xx.max()+730, yy.min()+128, yy.max()+128))
    comps.sort(key=lambda c: c[1])
    for npx, x0, x1, y0, y1 in comps:
        print(f'    glyph n={npx:4d} x {x0}..{x1} y {y0}..{y1}  (slide x {s(x0):.1f}..{s(x1):.1f} y {sy(y0):.1f}..{sy(y1):.1f})')

print('=== 3. matrix border: red/dark rows & cols profile ===')
redm = (r - (g + b) / 2 > 55)
darkm = (r < 110) & (g < 110) & (b < 110)
print(' left border zone x 440..456, rows 195..405: red col counts',
      {x: int(redm[195:405, x].sum()) for x in range(440, 458)})
print(' right border zone x 668..686:',
      {x: int((redm[195:405, x] | darkm[195:405, x]).sum()) for x in range(668, 686)})
print(' top border zone y 195..210, x 440..690: red row counts',
      {y: int(redm[y, 440:690].sum()) for y in range(195, 212)})
print(' bottom border zone y 378..402, x 440..690: red|dark row counts',
      {y: int((redm[y, 440:690] | darkm[y, 440:690]).sum()) for y in range(378, 403)})

print('=== 4. diagonal line: dark pixels inside matrix (x 450..672, y 205..382) ===')
inner = np.zeros_like(darkm); inner[205:383, 450:673] = True
dm = darkm & inner
ys, xs = np.where(dm)
print('  dark inner pixels: n', len(xs))
if len(xs):
    for xq in range(455, 675, 20):
        yy = ys[(xs > xq - 10) & (xs < xq + 10)]
        if len(yy): print(f'   x~{xq}: dark y {yy.min()}..{yy.max()} (expected diag ~{201 + (xq-446)/(677-446)*185:.0f})')

print('=== 5. tag corners (green comps in y 120..205) ===')
green = (g > r + 6) & (g > b + 6) & (g > 195) & (r > 150)
from scipy import ndimage
band = np.zeros_like(green); band[120:206, 410:700] = True
lab, n = ndimage.label(green & band, structure=np.ones((3, 3)))
for i in range(1, n + 1):
    yy, xx = np.where(lab == i)
    if len(xx) < 400: continue
    top_x = xx[yy == yy.min()]; bot_x = xx[yy == yy.max()]
    left_y = yy[xx == xx.min()]; right_y = yy[xx == xx.max()]
    print(f'  tag comp n={len(xx)} bbox x {xx.min()}..{xx.max()} y {yy.min()}..{yy.max()} | top edge x {top_x.min()}..{top_x.max()} | bottom edge x {bot_x.min()}..{bot_x.max()} | left edge y {left_y.min()}..{left_y.max()} | right edge y {right_y.min()}..{right_y.max()}')

print('=== 6. row chips: red text bbox per chip + chip fill sample ===')
redm2 = redm
for i, (y0, y1) in enumerate([(207, 233), (246, 272), (283, 309), (321, 352), (362, 388)]):
    zone = np.zeros_like(redm2); zone[y0:y1, 345:445] = True
    ys, xs = np.where(redm2 & zone)
    if len(xs):
        print(f'  chip r{i} text: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)} | fill sample {a[(y0+y1)//2, 360]}')
    else:
        print(f'  chip r{i}: NO red text; fill sample {a[(y0+y1)//2, 360]}')

print('=== 7. col tags: red text bboxes (y 125..205, x 410..700) ===')
for i in range(5):
    x0 = 415 + i * 45
    zone = np.zeros_like(redm2); zone[125:206, x0:x0+50] = True
    ys, xs = np.where(redm2 & zone)
    if len(xs):
        print(f'  tag col{i} zone x {x0}..{x0+50}: red text x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}')

print('=== 8. bottom green strip y 505..516, x 200..490 ===')
for y in range(505, 517):
    row = a[y, 200:490]
    nz = [(x+200, tuple(row[x])) for x in range(0, 290, 40)]
    print(f'  row {y}:', nz)

print('=== 9. triangle fill census (exclude chips/glyphs/borders) ===')
low = a[250:380, 455:640]; upp = a[205:300, 560:672]
def census(z, label):
    z = z.reshape(-1, 3)
    cnt = Counter(tuple(p // 16 * 16) for p in z)
    print(f'  {label}:', cnt.most_common(6))
census(low, 'lower-tri interior')
census(upp, 'upper-tri interior')

print('=== 10. arrow shape: blue rows x 295..335, y 280..315 ===')
for y in range(280, 316):
    xs = np.where(blue[y, 290:340])[0]
    if len(xs): print(f'  row {y} (slide {sy(y):.1f}): x {xs.min()+290}..{xs.max()+290} n={len(xs)}')
