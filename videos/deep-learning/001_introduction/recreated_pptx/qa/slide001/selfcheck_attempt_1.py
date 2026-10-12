#!/usr/bin/env python3
"""Closed-loop geometry check v2: tight per-element windows, border columns excluded.
Scale: render px = frame px * (H/540). Tolerance ~8.3 render px = 4 frame px."""
from PIL import Image
import numpy as np
import sys

REN = sys.argv[1] if len(sys.argv) > 1 else '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide001/render_1-1.png'
im = np.asarray(Image.open(REN).convert('RGB')).astype(int)
H, W, _ = im.shape
S = H / 540.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red  = (r > 120) & (g < 90) & (b < 90)
blue = (b > 110) & (r < 110) & (g < 110)

# name: (mask, frame yband, frame xspan, kind)  kind: cap=y0 is cap/asc top, y1 desc bottom
ELS = {
    'titleL1':  (red,  (126, 184), (243, 690)),
    'titleL2':  (red,  (198, 242), (334, 601)),
    'prepared': (red,  (292, 311), (456, 573)),
    'credname': (blue, (317, 339), (363, 665)),
    'credemail':(blue, (344, 358), (398, 628)),
    'head':     (red,  (397, 411), (75, 202)),
    'name1':    (blue, (425, 440), (117, 393)),
    'email1':   (blue, (449, 463), (118, 334)),
    'name2':    (blue, (473, 487), (117, 354)),
    'email2':   (blue, (497, 510), (118, 325)),
}
PAD = 8  # frame px search pad around expected band
fails = []
print(f'render {W}x{H}, scale {S:.4f}')
for k, (mask, (fy0, fy1), (fx0, fx1)) in ELS.items():
    y0 = int((fy0 - PAD) * S); y1 = int((fy1 + PAD) * S)
    x0 = max(int((fx0 - 30) * S), 110); x1 = min(int((fx1 + 60) * S), 1890)
    sub = mask[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) > 2)[0]
    if not len(rows):
        fails.append(f'{k}: NO INK in tight window'); continue
    ry0, ry1 = rows.min() + y0, rows.max() + y0
    cols = np.where(sub.sum(axis=0) > 0)[0]
    rx0, rx1 = cols.min() + x0, cols.max() + x0
    ey0, ey1 = fy0 * S, fy1 * S
    ex0, ex1 = fx0 * S, fx1 * S
    d = (ry0 - ey0, ry1 - ey1, rx0 - ex0, rx1 - ex1)
    wr, wf = rx1 - rx0, ex1 - ex0
    ok = all(abs(v) <= 8.3 for v in d) and abs(wr - wf) <= 12
    print(f'{k:10s} render y {ry0}-{ry1} x {rx0}-{rx1} | d(y0,y1,x0,x1)=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) w {wr:.0f} vs {wf:.0f} -> {"OK" if ok else "FAIL"}')
    if not ok:
        fails.append(f'{k}: d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) w {wr:.0f} vs {wf:.0f}')

print()
if fails:
    print('CLOSED-LOOP: FAIL')
    for f in fails: print('  -', f)
    sys.exit(1)
print('CLOSED-LOOP: PASS (all elements within tolerance)')
