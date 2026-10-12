#!/usr/bin/env python3
"""Supplementary measurements for slide_009 (frame px 960x540).
Mapping to slide pts (verified vs chrome landmarks below):
  slide_x = (fx - 18.628) / 0.961232 ; slide_y = (fy + 0.091) / 0.957576
"""
import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB')
im = np.asarray(IM).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def med(x0, y0, x1, y1, label=''):
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    m = np.median(reg, axis=0).astype(int)
    print(f'{label:38s} @({x0},{y0},{x1},{y1})  #{m[0]:02X}{m[1]:02X}{m[2]:02X}  n={len(reg)}')

def medif(x0, y0, x1, y1, mask, label=''):
    sub_m = mask[y0:y1, x0:x1]
    reg = im[y0:y1, x0:x1][sub_m]
    if len(reg) == 0:
        print(f'{label:38s}  NO MATCH'); return None
    m = np.median(reg, axis=0).astype(int)
    print(f'{label:38s}  #{m[0]:02X}{m[1]:02X}{m[2]:02X}  n={len(reg)}')
    return m

def bbox(mask, x0, y0, x1, y1, label):
    sub = np.zeros_like(mask); sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(sub)
    out = []
    for sl in ndimage.find_objects(lab):
        npx = int(mask[sl].sum())
        if npx < 6: continue
        out.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop, npx))
    out.sort(key=lambda t: (t[1] // 10, t[0]))
    print(f'--- {label}: {len(out)} comps')
    for c in out:
        print(f'    x {c[0]:4d}..{c[2]:4d}  y {c[1]:4d}..{c[3]:4d}  w{c[2]-c[0]} h{c[3]-c[1]} ({c[4]}px)')
    return out

print('=== CHROME LANDMARKS (verify mapping) ===')
redm = (r > 110) & (r - g > 55) & (r - b > 55)
row = np.where(redm[300, :])[0]
row = row[(row > 40) & (row < 930)]
print('panel verticals @y300:', row.min(), '..', row.max())
col = np.where(redm[:, 480])[0]
col = col[(col > 20) & (col < 535)]
print('panel top/bottom @x480:', col.min(), '..', col.max())

print('\n=== FILLS / BORDERS ===')
med(300, 470, 310, 480, 'chrome panel gray')
med(150, 220, 165, 235, 'left panel fill')
med(320, 245, 340, 260, 'right panel fill')
# left panel border: just outside white bbox x82..276 y102..509
med(79, 300, 82, 306, 'left panel border W')
med(277, 300, 280, 306, 'left panel border E')
med(150, 99, 200, 102, 'left panel border N')
# right panel border: white-ish bbox x289..894 y99..297
med(286, 200, 289, 206, 'right panel border W')
med(895, 200, 898, 206, 'right panel border E')
med(400, 96, 500, 99, 'right panel border N')
med(400, 298, 500, 301, 'right panel border S')
med(132, 76, 146, 84, 'title ink core (U stem)')
med(525, 180, 534, 215, 'left brace core')
med(826, 180, 833, 215, 'right brace core')
med(458, 195, 468, 201, '"=" sign core')
med(468, 196, 510, 205, 'Sigmoid word core')
med(590, 158, 595, 168, 'big X core')
med(358, 160, 368, 170, 'Y of Y^T core')

print('\n=== INPUT CIRCLES ===')
med(97, 148, 102, 152, 'input circle fill (upper-left of c1)')
med(103, 144, 108, 147, 'input circle rim (top of c1)')
med(99, 152, 109, 161, 'X1 label patch')

print('\n=== NEURON 1 ===')
med(226, 155, 231, 166, 'neuron fill (left of divider)')
med(232, 145, 236, 149, 'neuron rim top')
med(222, 154, 232, 168, 'Sigma glyph patch')

print('\n=== CONNECTION LINE color ===')
# lines radiate from input1 (115,157) to neurons; sample midpoints away from labels
pts = [(150, 262), (166, 312), (183, 363), (170, 250), (160, 350)]
cols = []
for px, py in pts:
    patch = im[py-2:py+3, px-2:px+3].reshape(-1, 3)
    # pick the most saturated-purple pixel in patch
    sc = patch[:, 2] - (patch[:, 0] + patch[:, 1]) / 2
    cols.append(patch[np.argmax(sc)])
cols = np.array(cols)
m = np.median(cols, axis=0).astype(int)
print(f'connection line  #{m[0]:02X}{m[1]:02X}{m[2]:02X}')

print('\n=== WEIGHT STACKS 2/3/4: ellipse scan at x=123 and label colors ===')
for y in range(225, 500, 5):
    px = im[y, 123]; print(f'  x=123 y={y}: #{px[0]:02X}{px[1]:02X}{px[2]:02X}') if y % 25 == 0 else None
def colruns(x, y0, y1, label):
    print(f'--- column runs {label} x={x}')
    prev = None; start = y0
    def cls(p):
        R, G, B = p
        if R > 245 and G > 245 and B > 245: return 'white'
        if B > 200 and G > 200 and R < 200: return 'cyan'
        if R > 230 and G > 200 and B > 200 and R - B > 20: return 'pinkish'
        if R > 230 and G > 215 and B < 190: return 'cream/yellow'
        if R > 240 and G > 225 and B > 200 and B - R < -15: return 'peach'
        if G > 225 and B > 215 and R < 235 and G - R > 8: return 'mint'
        return f'other#{R:02X}{G:02X}{B:02X}'
    for y in range(y0, y1):
        c = cls(im[y, x])
        if c != prev:
            if prev is not None and y - start > 2: print(f'    y {start}..{y}  {prev}')
            prev = c; start = y
    print(f'    y {start}..{y1}  {prev}')
colruns(123, 135, 500, 'left edge of stacks')
colruns(148, 135, 500, 'right edge of stacks')

print('\n=== STACK 3 ORANGE LABELS (looser mask) ===')
orm = (r > 180) & (g > 90) & (g < 200) & (b < 150) & (r - b > 60) & (r - g > 30)
bbox(orm, 95, 330, 200, 445, 'stack3 orange')
bbox((r > 150) & (r - g > 40) & (r - b > 60), 95, 330, 200, 445, 'stack3 reddish/orange loose')

print('\n=== STACK LABEL COLOR PATCHES ===')
med(130, 156, 137, 162, 'W11 blue text')
med(130, 243, 137, 250, 'W12 purple text')
med(130, 405, 138, 413, 'W14 green text')

print('\n=== MATRIX: 16 cell fills + borders ===')
# cell x-ranges from yellow-mask rows 3/4; rows y approx: r1 122-148, r2 160-188, r3 202-230, r4 240-268
cols_x = [(683, 699), (719, 735), (756, 772), (790, 806)]
rows_y = [(124, 146), (162, 184), (204, 226), (242, 264)]
for ri, (ry0, ry1) in enumerate(rows_y):
    for ci, (cx0, cx1) in enumerate(cols_x):
        # sample 4 corner patches inside cell, take the mode-ish median of the lightest
        patches = []
        for sx, sy in [(cx0+2, ry0+2), (cx1-4, ry0+2), (cx0+2, ry1-4), (cx1-4, ry1-4)]:
            patches.append(im[sy:sy+2, sx:sx+2].reshape(-1, 3))
        allp = np.vstack(patches)
        m = np.median(allp, axis=0).astype(int)
        print(f'  cell r{ri+1}c{ci+1} ({cx0},{ry0})  #{m[0]:02X}{m[1]:02X}{m[2]:02X}')
med(671, 190, 674, 210, 'matrix container border W')
med(815, 190, 818, 210, 'matrix container border E')
med(700, 128, 704, 132, 'cell border top r1c1')

print('\n=== B COLUMN ===')
med(856, 200, 860, 215, 'b container mint fill')
med(851, 190, 853, 215, 'b paren left stroke')
med(888, 190, 891, 215, 'b paren right stroke')
med(860, 134, 870, 142, 'b1 box fill')
med(858, 131, 878, 133, 'b1 box border top')
med(861, 134, 876, 143, 'b1 text patch')
med(843, 194, 847, 200, '+ sign core')

print('\n=== Y ROW ===')
med(310, 186, 330, 190, 'y pill pink fill')
med(306, 196, 310, 200, 'y pill pink fill 2')
med(313, 191, 323, 202, 'y1 box fill')
med(311, 189, 325, 191, 'y1 box border top')
med(295, 185, 298, 205, 'left bracket stroke')
med(427, 185, 430, 210, 'right bracket stroke')

print('\n=== X PILL ===')
med(540, 120, 545, 132, 'x pill fill (left of circles)')
med(553, 118, 565, 121, 'x circle1 rim top')
med(554, 122, 564, 130, 'x circle1 fill')
med(556, 121, 566, 131, 'x1 label patch')

print('\n=== NEURON 1 REGION detail crop + classify (y1 label / b1 label / arrows) ===')
reg = im[130:230, 245:320]
redc = ((reg[:, :, 0] > 110) & (reg[:, :, 0] - reg[:, :, 1] > 55) & (reg[:, :, 0] - reg[:, :, 2] > 55)).sum()
grnc = ((reg[:, :, 1] > 100) & (reg[:, :, 1] - reg[:, :, 0] > 40) & (reg[:, :, 1] - reg[:, :, 2] > 40)).sum()
darkc = ((reg[:, :, 0] < 110) & (reg[:, :, 1] < 110) & (reg[:, :, 2] < 110)).sum()
print(f'  red px {redc}, green px {grnc}, dark px {darkc} in (245..320, 130..230)')
bbox(redm, 245, 130, 320, 230, 'red comps neuron1 region')
grnm = (g > 100) & (g - r > 40) & (g - b > 40)
bbox(grnm, 240, 130, 320, 230, 'green comps neuron1 region')
bbox((r < 110) & (g < 110) & (b < 110), 240, 130, 320, 235, 'dark comps neuron1 region')

print('\n=== CROPS for visual read ===')
def save(x0, y0, x1, y1, name, scale=3):
    c = IM.crop((x0, y0, x1, y1))
    c = c.resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.LANCZOS)
    c.save(f'/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide009/{name}')
    print('saved', name)
save(240, 130, 325, 235, 'm2_neuron1_y1b1.png', 4)
save(90, 320, 205, 500, 'm2_stack34.png', 3)
save(655, 95, 835, 300, 'm2_matrix.png', 3)
save(520, 95, 680, 185, 'm2_xpill.png', 4)
save(285, 95, 460, 230, 'm2_yrow.png', 3)
