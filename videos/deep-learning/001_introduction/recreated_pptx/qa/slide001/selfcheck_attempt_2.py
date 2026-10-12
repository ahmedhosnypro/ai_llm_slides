#!/usr/bin/env python3
"""Closed-loop geometry check v3 (attempt 2) + frame containment.
Fixes attempt 1's window contamination: y-windows are midpoint-split between adjacent
lines so no neighbor's descenders/ascenders bleed into a measurement.
Scale: render px = frame px * (H/540). Tolerances: position +/-8.3 render px (~4 frame px),
width +/-12 render px (the pipeline closed-loop standard, same as attempt 1's check)."""
from PIL import Image
import numpy as np
import sys

REN = sys.argv[1] if len(sys.argv) > 1 else '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide001/render_2.png'
im = np.asarray(Image.open(REN).convert('RGB')).astype(int)
H, W, _ = im.shape
S = H / 540.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red  = (r > 120) & (g < 90) & (b < 90)
blue = (b > 110) & (r < 110) & (g < 110)

# name: (mask, y-window frame px [tight, midpoint-split], x-window frame px, target band, target xspan)
ELS = [
    ('titleL1',  red,  (124.0, 192.0), (218, 715),  (126.5, 184.5), (243, 690)),
    ('titleL2',  red,  (192.0, 266.0), (309, 626),  (198.5, 242.5), (334, 601)),
    ('prepared', red,  (288.0, 314.0), (431, 598),  (291.5, 311.5), (456, 573)),
    ('credname', blue, (314.0, 341.5), (338, 690),  (316.5, 340.0), (363, 665)),
    ('credemail',blue, (342.0, 376.0), (373, 653),  (343.5, 358.5), (398, 628)),
    ('head',     red,  (394.0, 418.0), (50, 227),   (397.5, 411.5), (75, 202)),
    ('name1',    blue, (419.0, 448.0), (92, 418),   (425.5, 445.0), (117, 393)),
    ('email1',   blue, (449.0, 469.5), (93, 359),   (451.5, 466.0), (118, 334)),
    ('name2',    blue, (470.0, 494.5), (92, 379),   (472.0, 487.5), (117, 354)),
    ('email2',   blue, (495.0, 515.0), (93, 350),   (497.0, 511.0), (118, 325)),
]
fails = []
print(f'render {W}x{H}, scale {S:.4f}')
for k, mask, (wy0, wy1), (wx0, wx1), (fy0, fy1), (fx0, fx1) in ELS:
    y0, y1 = int(wy0 * S), int(wy1 * S)
    x0, x1 = int(wx0 * S), int(wx1 * S)
    sub = mask[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) > 2)[0]
    if not len(rows):
        fails.append(f'{k}: NO INK in tight window'); continue
    ry0, ry1 = rows.min() + y0, rows.max() + y0
    cols = np.where(sub.sum(axis=0) > 0)[0]
    rx0, rx1 = cols.min() + x0, cols.max() + x0
    ey0, ey1, ex0, ex1 = fy0 * S, fy1 * S, fx0 * S, fx1 * S
    d = (ry0 - ey0, ry1 - ey1, rx0 - ex0, rx1 - ex1)
    wr, wf = rx1 - rx0, ex1 - ex0
    ok = all(abs(v) <= 8.3 for v in d) and abs(wr - wf) <= 12
    print(f'{k:10s} render y {ry0}-{ry1} x {rx0}-{rx1} | d(y0,y1,x0,x1)=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) w {wr:.0f} vs {wf:.0f} -> {"OK" if ok else "FAIL"}')
    if not ok:
        fails.append(f'{k}: d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) w {wr:.0f} vs {wf:.0f}')

# --- frame containment (playlist chrome: panel x 42..918, top y 45; content ink must stay
#     strictly inside; white margin must hold no content ink other than the chrome strokes)
panel_l, panel_r, panel_t = int(42 * S), int(918 * S), int(45 * S)
nonwhite = (r < 245) | (g < 245) | (b < 245)
margin_l = nonwhite[:, :panel_l - 6]
margin_r = nonwhite[:, panel_r + 7:]
margin_t = nonwhite[panel_t - 6, panel_l + 6:panel_r - 6]
cl, cr = margin_l.sum(), margin_r.sum()
# left/right margin ink must be the chrome border strokes (thin vertical red lines) only
def thin(v):  # column count of a 1-2px stroke over 1125 rows <= ~2.2 rows*stroke
    return v <= int(2.5 * H)
ok_cont = True
if cl and not thin(cl / max(1, (panel_l - 6))):
    fails.append(f'containment: {cl} ink px in LEFT white margin (expected <= a 2px border stroke)')
    ok_cont = False
if cr and not thin(cr / max(1, W - panel_r - 7)):
    fails.append(f'containment: {cr} ink px in RIGHT white margin (expected <= a 2px border stroke)')
    ok_cont = False
if margin_t.sum() > 30:
    fails.append(f'containment: {margin_t.sum()} ink px ABOVE panel top border row')
    ok_cont = False
# content ink bbox inside panel interior
inner = nonwhite[panel_t + 8:H, panel_l + 8:panel_r - 8]
ys, xs = np.where(inner)
if len(ys):
    print(f'content ink bbox: x {panel_l + 8 + xs.min()}-{panel_l + 8 + xs.max()}, y {panel_t + 8 + ys.min()}-{panel_t + 8 + ys.max()} (panel interior x {panel_l}-{panel_r}, y {panel_t}-{H})')
    if panel_l + 8 + xs.min() <= panel_l + 2 or panel_l + 8 + xs.max() >= panel_r - 2:
        fails.append('containment: content ink touches panel left/right border'); ok_cont = False
print(f'containment: {"OK" if ok_cont else "FAIL"} (margin ink L {cl} R {cr} px; thin-stroke allowance = 2.5px stroke)')

print()
if fails:
    print('CLOSED-LOOP: FAIL')
    for f in fails: print('  -', f)
    sys.exit(1)
print('CLOSED-LOOP: PASS (all elements within tolerance)')
