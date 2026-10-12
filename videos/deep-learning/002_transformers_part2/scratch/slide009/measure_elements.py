#!/usr/bin/env python3
"""Comprehensive element measurement for slide_009.jpg.

All coords in FRAME px (960x540). Mapping to slide pts:
  slide_x = (fx - 18.628) / 0.961232 ; slide_y = (fy + 0.091) / 0.957576
"""
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def region_comps(mask, x0, y0, x1, y1, minpx=8, label=''):
    sub = np.zeros_like(mask)
    sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(sub)
    out = []
    for sl in ndimage.find_objects(lab):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        npx = int(mask[sl].sum())
        if npx < minpx:
            continue
        out.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop, npx))
    out.sort(key=lambda t: (t[1] // 10, t[0] // 30, t[1]))
    print(f'--- {label} (region {x0},{y0}..{x1},{y1}): {len(out)} comps')
    for c in out:
        print(f'    x {c[0]:4d}..{c[2]:4d}  y {c[1]:4d}..{c[3]:4d}  ({c[4]}px)  w{c[2]-c[0]} h{c[3]-c[1]}')
    return out

def mean_color(x0, y0, x1, y1, maskfn=None):
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    if maskfn is not None:
        m = (maskfn[y0:y1, x0:x1] if isinstance(maskfn, np.ndarray) else maskfn(im[y0:y1, x0:x1])).reshape(-1)
        reg = reg[m]
    if len(reg) == 0:
        return None
    med = np.median(reg, axis=0).astype(int)
    return f'#{med[0]:02X}{med[1]:02X}{med[2]:02X}  n={len(reg)}'

# ---------- masks ----------
redm   = (r > 110) & (r - g > 55) & (r - b > 55)
bluem  = (b > 120) & (b - r > 50) & (b - g > 30)
purpm  = (r > 90) & (r < 210) & (b > 140) & (b - g > 60) & (r - g > 20)
orangm = (r > 190) & (g > 100) & (g < 195) & (b < 120) & (r - b > 90)
greenm = (g > 100) & (g - r > 40) & (g - b > 40)
darkm  = (r < 110) & (g < 110) & (b < 110)
pinkf  = (r > 230) & (b > 200) & (r - g > 25) & (b - g > 25)          # light pink fills
cyanf  = (b > 200) & (g > 200) & (r < 200) & (b - r > 30)             # light cyan fill
mintf  = (g > 225) & (b > 200) & (r < 235) & (g - r > 12)             # light mint fill
yelf   = (r > 220) & (g > 210) & (b < 200) & (r - b > 35)             # pale yellow fill

print('=== PANEL FILLS ===')
print('chrome gray   @ (300,470):', mean_color(295, 465, 310, 475))
print('left panel    @ (150,220):', mean_color(150, 215, 165, 225))
print('right panel   @ (320,250):', mean_color(320, 245, 335, 255))
print('cyan ellipse  @ (128,190):', mean_color(124, 186, 134, 196))

print('\n=== TITLE ink (red) ===')
tc = region_comps(redm, 100, 55, 820, 100, 15, 'title glyphs')
tx0 = min(c[0] for c in tc); tx1 = max(c[2] for c in tc)
ty0 = min(c[1] for c in tc); ty1 = max(c[3] for c in tc)
print(f'TITLE BBOX: x {tx0}..{tx1}  y {ty0}..{ty1}  (w {tx1-tx0} h {ty1-ty0})')

print('\n=== LEFT PANEL bbox (white fill) ===')
white = (r > 245) & (g > 245) & (b > 245)
lp = region_comps(white, 60, 95, 300, 515, 4000, 'left white panel')
print('left panel border sample:', mean_color(76, 300, 80, 306))

print('\n=== HEADER "Input Word X" ===')
region_comps(darkm, 80, 105, 230, 135, 8, 'header dark ink')
region_comps(redm, 175, 105, 230, 135, 8, 'header red ink')

print('\n=== INPUT CIRCLES (pink fill) ===')
pc = region_comps(pinkf, 75, 130, 130, 500, 30, 'pink input circles')
for c in pc:
    cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
    print(f'    center ({cx:.1f},{cy:.1f}) d=({c[2]-c[0]},{c[3]-c[1]})')
print('input fill:', mean_color(95, 155, 105, 160))
print('input border:', mean_color(84, 152, 88, 158))

print('\n=== INPUT LABELS (dark) ===')
region_comps(darkm, 80, 130, 130, 500, 8, 'input labels')

print('\n=== CYAN ELLIPSE (stack1 bg) ===')
cy = region_comps(cyanf, 100, 130, 180, 300, 200, 'cyan ellipse')
print('cyan ellipse fill:', mean_color(120, 180, 140, 200, cyanf))

print('\n=== ORANGE ELLIPSE outline (stack3) ===')
oe = region_comps(orangm, 100, 300, 190, 430, 10, 'orange ellipse+labels')

print('\n=== WEIGHT STACKS (4 colors) ===')
bl = region_comps(bluem, 100, 130, 200, 300, 8, 'stack1 blue labels')
pu = region_comps(purpm, 100, 230, 200, 370, 8, 'stack2 purple labels')
orl = region_comps(orangm, 100, 300, 200, 430, 8, 'stack3 orange labels')
gr = region_comps(greenm, 100, 380, 200, 500, 8, 'stack4 green labels')
print('stack colors: blue', mean_color(128, 153, 145, 165, bluem),
      ' purple', mean_color(128, 253, 145, 265, purpm),
      ' orange', mean_color(128, 353, 145, 365, orangm),
      ' green', mean_color(128, 425, 145, 437, greenm))

print('\n=== NEURONS (red border circles) ===')
nc = region_comps(redm, 200, 130, 270, 510, 100, 'neuron red rims')
for c in nc:
    print(f'    x {c[0]}..{c[2]} y {c[1]}..{c[3]} center ({(c[0]+c[2])/2:.1f},{(c[1]+c[3])/2:.1f})')
print('neuron rim color:', mean_color(212, 152, 218, 158, redm))

print('\n=== Y LABELS (red) near neurons ===')
region_comps(redm, 265, 130, 300, 510, 8, 'y labels red')

print('\n=== B LABELS (dark) below neurons ===')
region_comps(darkm, 265, 160, 300, 515, 8, 'b labels dark')

print('\n=== GREEN arrows ===')
region_comps(greenm, 240, 130, 300, 515, 8, 'green arrows+labels')

print('\n=== RIGHT PANEL bbox ===')
rp = region_comps((r > 235) & (g > 235) & (b > 230) & ~white, 285, 95, 905, 310, 20000, 'right panel fill')
print('right panel fill color:', mean_color(320, 250, 340, 265))

print('\n=== Y^T ===')
region_comps(redm, 340, 140, 400, 180, 8, 'YT glyphs')

print('\n=== Y-ROW PINK PILL ===')
yp = region_comps(pinkf, 280, 165, 450, 230, 100, 'y pill')
print('pill fill:', mean_color(310, 175, 330, 180, pinkf))
region_comps(redm, 280, 165, 460, 230, 8, 'y-row red: parens/brackets/labels')
yb = region_comps(white, 285, 175, 445, 225, 60, 'y white boxes')

print('\n=== = Sigmoid (blue) ===')
region_comps(bluem, 435, 180, 530, 225, 8, 'sigmoid ink')

print('\n=== BLUE BRACES ===')
region_comps(bluem, 515, 95, 555, 300, 30, 'left brace')
region_comps(bluem, 800, 95, 845, 300, 30, 'right brace')
print('brace color:', mean_color(524, 150, 532, 180, bluem))

print('\n=== X PILL + circles ===')
xp = region_comps(pinkf, 530, 100, 680, 150, 100, 'x pill')
region_comps(redm, 530, 100, 680, 150, 8, 'x circles rims/brackets')
region_comps(redm, 550, 140, 640, 180, 30, 'big X below')
print('pill2 fill:', mean_color(545, 110, 560, 115, pinkf))

print('\n=== MATRIX container ===')
mc = region_comps(mintf, 660, 95, 830, 300, 3000, 'mint matrix container')
print('mint fill:', mean_color(690, 160, 700, 170, mintf))
yl = region_comps(yelf, 660, 95, 830, 300, 25, '16 yellow cells')
print('cell fill:', mean_color(688, 125, 696, 130, yelf))
# grid lines: sample greenish verticals inside container
print('\n=== + sign ===')
region_comps(redm, 830, 180, 860, 220, 8, 'plus')

print('\n=== B-COLUMN ===')
bc = region_comps(mintf, 845, 95, 900, 300, 500, 'mint b container')
bb = region_comps(yelf, 845, 95, 900, 300, 25, 'b yellow boxes')
region_comps(darkm, 850, 100, 900, 300, 8, 'b labels')
region_comps(redm, 840, 95, 900, 300, 8, 'b red parens')
