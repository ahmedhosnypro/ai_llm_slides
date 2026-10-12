#!/usr/bin/env python3
"""PIL ink-forensics measurement of the ORIGINAL frame slide_029.jpg (960x540, 1px=1pt).
Measures: backgrounds, title ink, content frame, bullet lines + ring markers, meme bbox,
close-up bbox, RGB card bboxes, arrow strokes, cursor, bottom bar. Banked output."""
import numpy as np
from PIL import Image

ORIG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_029.jpg'
im = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
print(f'original {W}x{H}')

def bbox(mask, x0, y0, x1, y1, min_row=1, min_col=1, label=''):
    sub = mask[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) >= min_row)[0]
    cols = np.where(sub.sum(axis=0) >= min_col)[0]
    if not len(rows) or not len(cols):
        print(f'{label}: NO INK in ({x0},{y0})-({x1},{y1})')
        return None
    bb = (x0 + cols.min(), y0 + rows.min(), x0 + cols.max(), y0 + rows.max())
    print(f'{label}: x {bb[0]}..{bb[2]} (w={bb[2]-bb[0]+1})  y {bb[1]}..{bb[3]} (h={bb[3]-bb[1]+1})')
    return bb

print('--- background samples ---')
for (x, y, lbl) in [(480, 15, 'canvas top'), (480, 160, 'panel mid'), (300, 205, 'inside frame upper'),
                    (600, 460, 'inside frame lower'), (30, 300, 'left of panel'), (480, 536, 'very bottom'),
                    (200, 330, 'bullet zone bg'), (560, 250, 'frame interior mid')]:
    print(f'{lbl} ({x},{y}): #{r[y,x]:02X}{g[y,x]:02X}{b[y,x]:02X}')

print('--- title (red mask) ---')
red = (r > 140) & (g < 90) & (b < 90)
tb = bbox(red, 60, 50, 900, 160, min_row=2, label='title ink')

print('--- content frame (thin red rect) ---')
# vertical strokes: columns with long red runs between y 200..480
colcnt = red[210:470, :].sum(axis=0)
vcands = [x for x in range(40, 930) if colcnt[x] > 150]
print('vertical red stroke columns:', vcands)
rowcnt = red[:, 100:880].sum(axis=1)
hcands = [y for y in range(150, 540) if rowcnt[y] > 300]
print('horizontal red stroke rows:', hcands)

print('--- bullet text lines (dark mask) ---')
dark = (r < 130) & (g < 130) & (b < 130)
sub = dark[200:400, 80:580]
rowsum = sub.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rowsum):
    if v > 3 and not inb:
        inb = True; s = i
    elif v <= 3 and inb:
        inb = False; bands.append((s, i - 1))
if inb: bands.append((s, len(rowsum) - 1))
print('text bands (y offsets +200):')
for (s, e) in bands:
    bb = bbox(dark, 80, 200 + s, 580, 200 + e + 1, min_row=1, label=f'  band y{200+s}-{200+e}')
    if bb:
        # ring marker: tan mask in band
        tan = (r > 170) & (r < 235) & (g > 120) & (g < 190) & (b < 130)
        mb = bbox(tan, 80, 200 + s - 4, 200, 200 + e + 5, min_row=1, label=f'    ring')
print('band pitch (top->top):', [bands[i+1][0] - bands[i][0] for i in range(len(bands) - 1)])

print('--- meme photo bbox (non-background, top-right) ---')
# background inside frame ~ white; photo differs
bg = (np.abs(r - g) < 12) & (np.abs(g - b) < 12) & (r > 225)
nonbg = ~bg
mb = bbox(nonbg, 620, 195, 916, 350, min_row=3, label='meme')

print('--- close-up photo (bottom-left) ---')
cb = bbox(nonbg, 190, 375, 500, 505, min_row=3, label='closeup region incl arrows')

print('--- RGB cards ---')
redc = (r > 140) & (g < 90) & (b < 90)
rb = bbox(redc, 600, 330, 916, 510, min_row=3, label='red card')
greenc = (g > 110) & (r < 110) & (b < 110)
gb = bbox(greenc, 600, 330, 916, 510, min_row=3, label='green card')
bluec = (b > 110) & (r < 110) & (g < 110)
bb2 = bbox(bluec, 600, 330, 916, 510, min_row=3, label='blue card')

print('--- arrows (colored strokes outside closeup) ---')
orange = (r > 190) & (g > 100) & (g < 190) & (b < 90)
yellow = (r > 200) & (g > 190) & (b < 140)
cyan = (b > 150) & (g > 130) & (r < 120)
brightred = (r > 170) & (g < 90) & (b < 90)
for nm, m, win in [('orange', orange, (200, 370, 350, 470)), ('yellow', yellow, (280, 370, 480, 470)),
                   ('cyan', cyan, (200, 370, 350, 500)), ('arrow-red', brightred, (200, 420, 350, 510))]:
    bbox(m, *win, min_row=1, label=f'arrow {nm}')

print('--- cursor (white blob over cards) ---')
white = (r > 235) & (g > 235) & (b > 235)
bbox(white, 700, 340, 850, 430, min_row=1, label='cursor whites')

print('--- bottom bar ---')
darkrow = dark.sum(axis=1)
print('dark rows near bottom:', [y for y in range(500, H) if darkrow[y] > 300])

print('--- meme interior details ---')
print('sample meme caption row px (top):', f'#{r[225,700]:02X}{g[225,700]:02X}{b[225,700]:02X}')
nose = red
bbox(nose, 690, 250, 790, 310, min_row=1, label='nose red box')
