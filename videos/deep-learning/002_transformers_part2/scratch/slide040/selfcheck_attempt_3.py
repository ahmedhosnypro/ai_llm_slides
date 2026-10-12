#!/usr/bin/env python3
"""Closed-loop ink check, attempt 1: render_3.png (150dpi, 2000x1125) vs original
slide_040.jpg mapped through frame->slide->render transforms.
  render_x = (fx-18.63) * (150/72) / 0.96123 = (fx-18.63)*2.16766
  render_y = fy * (150/72) / 0.95556         = fy*2.18013
Tolerance ~4px @150dpi (equations/text bands). Prints per-region deltas."""
import numpy as np
from PIL import Image

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide040/render_3.png'
im = np.asarray(Image.open(REN).convert('RGB')).astype(int)
H, W, _ = im.shape
print('render size', W, H)
lum = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3.0
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def R(fx, fy): return (fx-18.63)*2.16766, fy*2.18013

# color classes in render space
redm   = (r>130) & (r-g>60) & (r-b>60)
dark   = lum < 150
lavm   = (np.abs(r-0x99)<45) & (np.abs(g-0x99)<45) & (np.abs(b-0xCC)<45) & (b-r>15)
pinkm  = (r>215) & (r-g>40) & (r-b>40) & (np.abs(g-0x9C)<55)
orangm = (r>215) & (g>140) & (g<225) & (r-b>60)
greenm = (g>190) & (g-r>25) & (g-b>25)

def bbox_of(mask, fx0, fx1, fy0, fy1, label, tol=4):
    x0, y0 = R(fx0, fy0); x1, y1 = R(fx1, fy1)
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    win = mask[max(y0-8,0):y1+8, max(x0-8,0):x1+8]
    ys, xs = np.where(win)
    if len(xs) == 0:
        print(f'{label:24s} EMPTY in window  (target x {x0}..{x1} y {y0}..{y1})')
        return
    ax0, ax1 = xs.min()+max(x0-8,0), xs.max()+max(x0-8,0)
    ay0, ay1 = ys.min()+max(y0-8,0), ys.max()+max(y0-8,0)
    dx0, dx1 = ax0-x0, ax1-x1
    dy0, dy1 = ay0-y0, ay1-y1
    flag = '' if (abs(dx0)<=tol and abs(dx1)<=tol and abs(dy0)<=tol and abs(dy1)<=tol) else '  <-- CHECK'
    print(f'{label:24s} x {ax0}..{ax1} y {ay0}..{ay1}  dx[{dx0:+d},{dx1:+d}] dy[{dy0:+d},{dy1:+d}]{flag}')

print('== TITLE ==')
bbox_of(redm, 261, 675, 66, 89, 'title')
print('== INTRO BOX (red border) ==')
bbox_of(redm, 88, 892, 104, 185, 'intro box border')
print('== INTRO LINES (dark+colored ink) ==')
ink_any = dark | redm | lavm | greenm  # blue included in dark-ish? blue cores are dark
bluem = (b-r>50) & (b>120) & (lum<170)
bbox_of(dark | bluem | greenm | redm, 105, 822, 117, 134, 'intro L1')
bbox_of(dark | bluem | greenm | redm, 105, 828, 142, 159, 'intro L2')
bbox_of(redm, 105, 434, 167, 181, 'intro L3 (red)')
print('== PANEL BORDER (dark) ==')
bbox_of(dark, 145, 552, 204, 497, 'panel border')
print('== PANEL HEADERS (dark) ==')
bbox_of(dark, 152, 518, 213, 228, 'h1 line')
bbox_of(dark, 207, 415, 233, 249, 'h2 line')
bbox_of(dark, 151, 344, 255, 270, 'h3 line')
print('== EQUATIONS (dark ink) ==')
bbox_of(dark, 163, 283, 292, 339, 'eq1 math')
bbox_of(dark, 163, 339, 350, 397, 'eq2 math')
bbox_of(dark, 171, 287, 400, 447, 'eq3 math')
bbox_of(dark, 172, 371, 452, 475, 'eq4 math')
print('== COMMENTS (dark) ==')
bbox_of(dark, 417, 546, 307, 319, 'c1 comment')
bbox_of(dark, 397, 546, 365, 377, 'c2 comment')
bbox_of(dark, 464, 547, 415, 428, 'c3 comment')
bbox_of(dark, 434, 546, 456, 469, 'c4 comment')
print('== HIGHLIGHT FILLS ==')
bbox_of(greenm, 389, 531, 145, 158, 'intro green hl')
bbox_of(greenm, 203, 425, 226, 249, 'params green hl')
bbox_of(lavm, 164, 188, 302, 327, 'lav mu_B eq1')
bbox_of(lavm, 166, 191, 360, 384, 'lav sig_B eq2')
bbox_of(lavm, 254, 280, 398, 423, 'lav mu_B eq3num')
bbox_of(lavm, 231, 255, 424, 447, 'lav sig_B eq3den')
bbox_of(pinkm, 169, 193, 410, 434, 'pink xhat eq3')
bbox_of(pinkm, 458, 547, 411, 432, 'pink //normalize')
bbox_of(pinkm, 225, 243, 452, 475, 'pink xhat eq4')
bbox_of(orangm, 426, 547, 452, 473, 'orange //scale')
bbox_of(orangm, 170, 191, 454, 475, 'orange ellipse y_i')
print('== EQ3 UNDERLINE (lavender line) ==')
bbox_of(lavm, 164, 287, 445, 447, 'eq3 underline')
print('== INTRO PITCH ==')
# find the 3 intro line bands in render
x0, y0 = R(100, 110)
win = (dark | bluem | greenm | redm)[int(y0):int(y0)+170, int(x0):int(x0)+1550]
prof = win.sum(axis=1)
bands, in_b = [], False
for i, v in enumerate(prof):
    if v > 6 and not in_b: st, in_b = i, True
    elif v <= 6 and in_b: bands.append((st, i-1)); in_b = False
if in_b: bands.append((st, len(prof)-1))
bands = [(a, bb) for a, bb in bands if bb-a > 8]
print('intro line bands (render y):', bands)
if len(bands) >= 2:
    pitches = [bands[i+1][0]-bands[i][0] for i in range(len(bands)-1)]
    print('pitches:', pitches, '(target 52.3 = 25.11pt)')
