#!/usr/bin/env python3
"""PIL forensics for slide_039.jpg (960x540, 1px=1pt) — slide 39 "How many filters we should apply".
Banks measured geometry for the build. Attempt 1, 2026-10-12."""
from PIL import Image
import numpy as np
import json

P = 'videos/deep-learning/001_introduction/unique_slides/slide_039.jpg'
img = Image.open(P).convert('RGB')
a = np.asarray(img).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = 540, 960

red = (R > 140) & (R - G > 60) & (R - B > 60)
blue = (B > 130) & (B - R > 40) & (B - G > 40)
dark = (R < 110) & (G < 110) & (B < 110)
yellow = (R > 200) & (G > 190) & (B < 140)
green = (G > 110) & (G - R > 40) & (G - B > 40)
white = (R > 248) & (G > 248) & (B > 245)

out = {}
def put(k, v):
    out[k] = v
    print(f'{k}: {v}')

# ---- chrome: panel borders ----
col58 = red[:, 58] | red[:, 59]
ys = np.where(col58)[0]
put('chrome.red_vline_x58', {'rows': [int(ys.min()), int(ys.max())], 'coverage': round(float(col58.mean()), 3)})
# left of x=57: canvas color?
put('canvas_sample_x30_row300', [int(v) for v in a[300, 30]])
put('panel_sample_x100_row300', [int(v) for v in a[300, 100]])
# panel top border: red-ish rows 40..50 full width
for y in range(38, 55):
    row = red[y]
    if row.sum() > 50:
        xs = np.where(row)[0]
        print(f'  topborder row y={y}: red count={int(row.sum())} x=[{int(xs.min())}..{int(xs.max())}] sample={a[y, 500]}')
# right border? columns 900..950 red fraction
rcols = [(x, round(float(red[:, x].mean()), 3)) for x in range(900, 955) if red[:, x].mean() > 0.05]
put('chrome.right_red_cols', rcols)
# gray panel horizontal extent at row 300: first/last non-white col
row300 = a[300]
nonwhite = np.where(~((row300[:, 0] > 246) & (row300[:, 1] > 246) & (row300[:, 2] > 246)))[0]
put('panel_nonwhite_x_row300', [int(nonwhite.min()), int(nonwhite.max())])
# gray panel top edge at x=100: first gray row
col100 = a[:, 100]
grayrows = np.where((np.abs(col100[:, 0] - 233) < 8) & (np.abs(col100[:, 1] - 231) < 8) & (np.abs(col100[:, 2] - 232) < 8))[0]
put('panel_gray_rows_at_x100', [int(grayrows.min()), int(grayrows.max())] if len(grayrows) else None)

# ---- title ----
tmask = red[40:120, 62:]  # exclude the x58 vline
ys2, xs2 = np.where(tmask)
put('title.ink_bbox', {'y': [int(ys2.min() + 40), int(ys2.max() + 40)], 'x': [int(xs2.min() + 62), int(xs2.max() + 62)]})
# row profile of title (cap height / baseline)
trows = red[40:120, 62:].sum(axis=1)
put('title.row_ink_counts', {int(y + 40): int(c) for y, c in enumerate(trows) if c > 3})
put('title.color_samples', [[int(v) for v in a[y, x]] for y, x in [(70, 210), (75, 300), (80, 500)]])

# ---- white box (hypothesis/conclusion) ----
# white-fill region bounds in panel, rows 100..300
wm = white[95:305, 62:915]
ys3, xs3 = np.where(wm)
put('whitebox.fill_bbox', {'y': [int(ys3.min() + 95), int(ys3.max() + 95)], 'x': [int(xs3.min() + 62), int(xs3.max() + 62)]})
# border: sample pixels on the fill bbox edges
y0, y1 = int(ys3.min() + 95), int(ys3.max() + 95)
x0, x1 = int(xs3.min() + 62), int(xs3.max() + 62)
put('whitebox.edge_samples', {
    'top': [[int(v) for v in a[y, x]] for y, x in [(y0 - 2, 400), (y0 - 1, 400), (y0, 400), (y0 + 1, 400)]],
    'bottom': [[int(v) for v in a[y, x]] for y, x in [(y1 - 1, 400), (y1, 400), (y1 + 1, 400), (y1 + 2, 400)]],
    'left': [[int(v) for v in a[y, x]] for y, x in [(200, x0 - 2), (200, x0 - 1), (200, x0), (200, x0 + 1)]],
    'right': [[int(v) for v in a[y, x]] for y, x in [(200, x1 - 1), (200, x1), (200, x1 + 1), (200, x1 + 2)]],
})
# text rows inside box: dark-pixel row profile rows y0..y1
inner = dark[y0 + 3:y1 - 3, x0 + 3:x1 - 3]
trows2 = inner.sum(axis=1)
bands = []
inb = False
for i, c in enumerate(trows2):
    if c > 2 and not inb:
        s = i; inb = True
    elif c <= 2 and inb:
        bands.append((s + y0 + 3, i - 1 + y0 + 3)); inb = False
if inb:
    bands.append((s + y0 + 3, len(trows2) - 1 + y0 + 3))
put('whitebox.text_bands', bands)
# per-band x extent
tb = []
for (bs, be) in bands:
    seg = dark[bs:be + 1, x0:x1 + 1]
    xs4 = np.where(seg.any(axis=0))[0]
    tb.append({'rows': [bs, be], 'x': [int(xs4.min() + x0), int(xs4.max() + x0)], 'h': be - bs + 1})
put('whitebox.text_bands_x', tb)

# ---- yellow highlight in white box ----
ym = yellow[95:305, 62:915]
ys5, xs5 = np.where(ym)
if len(ys5):
    put('highlight.bbox', {'y': [int(ys5.min() + 95), int(ys5.max() + 95)], 'x': [int(xs5.min() + 62), int(xs5.max() + 62)],
                           'fill_sample': [int(v) for v in a[int(ys5.min() + 95) + 2, int(xs5.min() + 62) + 2]]})
# red phrase ink inside highlight
if len(ys5):
    hy0, hy1 = int(ys5.min() + 95), int(ys5.max() + 95)
    hx0, hx1 = int(xs5.min() + 62), int(xs5.max() + 62)
    rm = red[hy0:hy1 + 1, hx0:hx1 + 1]
    ys6, xs6 = np.where(rm)
    put('highlight.red_ink_bbox', {'y': [int(ys6.min() + hy0), int(ys6.max() + hy0)], 'x': [int(xs6.min() + hx0), int(xs6.max() + hx0)]})

# ---- photos ----
def rect_from_hlines(y_top, y_bot):
    return None
put('photo.left_frame_rows', {'top_y306_310': {y: int(red[y, 150:460].sum()) for y in range(304, 312)},
                              'bot_y439_446': {y: int(red[y, 150:460].sum()) for y in range(438, 447)}})
# left frame vertical strokes: columns with many red rows in 300..450
lcols = [(x, int(red[300:450, x].sum())) for x in range(150, 470) if red[300:450, x].sum() > 60]
put('photo.left_vcols', lcols)
rcols2 = [(x, int(red[298:450, x].sum())) for x in range(450, 760) if red[298:450, x].sum() > 60]
put('photo.right_vcols', rcols2)
put('photo.right_frame_rows', {'top': {y: int(red[y, 460:750].sum()) for y in range(300, 310)},
                               'bot': {y: int(red[y, 460:750].sum()) for y in range(438, 447)}})
put('photo.left_border_sample', [int(v) for v in a[308, 300]])
put('photo.left_inner_sample', [int(v) for v in a[375, 300]])

# ---- annotation box ----
# light-yellow fill: FFFFE1-ish
ly = (R > 240) & (G > 240) & (B > 210) & (B < 245) & (R - B > 12)
lym = ly[440:525, 40:940]
ys7, xs7 = np.where(lym)
put('annotbox.fill_bbox', {'y': [int(ys7.min() + 440), int(ys7.max() + 440)], 'x': [int(xs7.min() + 40), int(xs7.max() + 40)],
                           'fill_samples': [[int(v) for v in a[int(ys7.min() + 440) + 3, 200]], [int(v) for v in a[470, 850]]]})
ay0, ay1 = int(ys7.min() + 440), int(ys7.max() + 440)
ax0, ax1 = int(xs7.min() + 40), int(xs7.max() + 40)
put('annotbox.edge_samples', {
    'top': [[int(v) for v in a[y, 400]] for y in range(ay0 - 2, ay0 + 2)],
    'bottom': [[int(v) for v in a[y, 400]] for y in range(ay1 - 1, ay1 + 3)],
    'left': [[int(v) for v in a[480, x]] for x in range(ax0 - 2, ax0 + 2)],
    'right': [[int(v) for v in a[480, x]] for x in range(ax1 - 1, ax1 + 3)],
})
# annotation text lines (dark or colored ink inside box)
am = dark[ay0:ay1, ax0:ax1] | blue[ay0:ay1, ax0:ax1] | red[ay0:ay1, ax0:ax1] | green[ay0:ay1, ax0:ax1]
trows3 = am.sum(axis=1)
bands3 = []
inb = False
for i, c in enumerate(trows3):
    if c > 2 and not inb:
        s = i; inb = True
    elif c <= 2 and inb:
        bands3.append((s + ay0, i - 1 + ay0)); inb = False
if inb:
    bands3.append((s + ay0, ay1 - 1 - ay0 + ay0))
ab = []
for (bs, be) in bands3:
    seg_r = red[bs:be + 1, ax0:ax1]; seg_b = blue[bs:be + 1, ax0:ax1]; seg_g = green[bs:be + 1, ax0:ax1]
    xsr = np.where(seg_r.any(axis=0))[0]; xsb = np.where(seg_b.any(axis=0))[0]; xsg = np.where(seg_g.any(axis=0))[0]
    xs4 = np.where((dark[bs:be + 1, ax0:ax1] | seg_b | seg_r | seg_g).any(axis=0))[0]
    ab.append({'rows': [bs, be], 'x_all': [int(xs4.min() + ax0), int(xs4.max() + ax0)],
               'red_x': [int(xsr.min() + ax0), int(xsr.max() + ax0)] if len(xsr) else None,
               'blue_x': [int(xsb.min() + ax0), int(xsb.max() + ax0)] if len(xsb) else None,
               'green_x': [int(xsg.min() + ax0), int(xsg.max() + ax0)] if len(xsg) else None,
               'h': be - bs + 1})
put('annotbox.text_lines', ab)
# yellow highlight blank in line 2 region
ym2 = yellow[ay0:ay1, ax0:ax1]
ys8, xs8 = np.where(ym2)
if len(ys8):
    put('annotbox.yellow_bits', {'y': [int(ys8.min() + ay0), int(ys8.max() + ay0)], 'x': [int(xs8.min() + ax0), int(xs8.max() + ax0)],
                                 'n': int(len(ys8))})

# ---- bottom black bar ----
put('blackbar.rows_darkfrac', {y: round(float(dark[y].mean()), 3) for y in range(505, 540, 2)})

with open('videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/measure_original1_out.json', 'w') as f:
    json.dump(out, f, indent=1, default=str)
print('BANKED -> qa/slide039/measure_original1_out.json')
