#!/usr/bin/env python3
"""Closed-loop PIL ink check for slide_053 attempt 1 (150dpi render vs mapped targets).
Tolerance ~4px @150dpi = 1.92pt in slide space; WARN band 3pt."""
from PIL import Image
import numpy as np
import sys

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide053/render_1.png'
im = Image.open(REN).convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
S = 72.0 / 150.0  # render px -> slide pt
print(f'render {W}x{H} px')
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
masks = {
    'red':   (r - (g + b) / 2 > 55),
    'blue':  (b - (r + g) / 2 > 55),
    'green': (g > r + 6) & (g > b + 6) & (g > 195) & (r > 150),
    'yellow': (r > 228) & (g > 228) & (b > 150) & (b < 225),
    'dark':  (r < 110) & (g < 110) & (b < 110),
    'mauve': (r > 150) & (g > 100) & (b > 100) & (r > g + 12) & (r > b + 12),
}

def bbox(mask_name, x0, y0, x1, y1, label, tx0, ty0, tx1, ty1):
    z = np.zeros_like(masks[mask_name]); z[int(y0/S):int(y1/S), int(x0/S):int(x1/S)] = True
    ys, xs = np.where(masks[mask_name] & z)
    if len(xs) == 0:
        print(f'  FAIL {label}: NO INK in zone'); return
    mx0, mx1 = xs.min() * S, xs.max() * S
    my0, my1 = ys.min() * S, ys.max() * S
    d = [mx0-tx0, my0-ty0, mx1-tx1, my1-ty1]
    worst = max(abs(v) for v in d)
    stat = 'PASS' if worst <= 2.0 else ('WARN' if worst <= 3.0 else 'FAIL')
    print(f'  {stat} {label}: ink x {mx0:.1f}..{mx1:.1f} y {my0:.1f}..{my1:.1f} vs target x {tx0:.1f}..{tx1:.1f} y {ty0:.1f}..{ty1:.1f}  d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})')

print('=== closed-loop ink check (attempt 1), tol 2.0pt ===')
bbox('red',   200, 50, 700, 95,  'L1 title',      249.6, 62.0, 617.3, 80.8)
bbox('red',   200, 95, 460, 116, 'L2 red part',   249.6, 89.2, 454.8, 110.1)
bbox('blue',  460, 95, 700, 116, 'L2 blue part',  463.1, 89.2, 579.8, 108.0)
bbox('red',   700, 100, 930, 130,'Softmax label', 744.4, 115.4, 798.6, 124.8)
bbox('dark',  730, 128, 910, 212,'Equation ink',  751.7, 141.5, 871.5, 186.5)
bbox('blue',  300, 100, 730, 440,'Container',     326.6, 115.4, 711.1, 430.2)
bbox('green', 330, 200, 445, 412,'Row chips',     347.5, 216.8, 434.2, 405.1)
bbox('green', 400, 120, 700, 220,'Col tags',      416.2, 133.2, 673.6, 215.1)
bbox('red',   430, 200, 700, 425,'Matrix border', 445.4, 210.9, 686.6, 416.0)
bbox('yellow',440, 215, 690, 410,'Yellow chips',  459.6, 225.4, 671.0, 400.9)
bbox('red',   495, 215, 690, 372,'Red blocks',    503.2, 222.2, 675.6, 364.5)
bbox('blue',  280, 295, 336, 330,'Arrow',         294.4, 302.6, 328.4, 321.8)
bbox('blue',  40, 425, 910, 540, 'Statement box', 47.5, 436.5, 895.4, 530.9)
bbox('blue',  60, 440, 890, 470, 'Stmt L1 ink',   65.2, 447.0, 552.0, 464.7)
bbox('red',   60, 484, 890, 509, 'Stmt L2 ink',   65.2, 490.9, 813.1, 506.6)
bbox('red',   60, 508, 890, 532, 'Stmt L3 ink',   65.2, 511.8, 823.6, 527.5)
# '0' digit in cell (0,0) and (4,4)
bbox('dark',  455, 218, 485, 246, 'Digit r0c0',   465.2, 226.2, 471.5, 235.7)
bbox('dark',  645, 382, 680, 410, 'Digit r4c4',   647.7, 391.5, 654.4, 400.9)
# equation region ink existence (pre-judge check 3)
z = np.zeros_like(masks['dark']); z[int(128/S):int(212/S), int(730/S):int(910/S)] = True
n = int((masks['dark'] & z).sum())
print(f'  {"PASS" if n > 500 else "FAIL"} Eq ink exists: {n} dark px in eq box zone')
# frame containment (pre-judge check 2): all content inside house frame
for name, m in masks.items():
    ys, xs = np.where(m)
    if len(xs) == 0: continue
    x0, x1, y0, y1 = xs.min()*S, xs.max()*S, ys.min()*S, ys.max()*S
    ok = x0 >= 9.0 and x1 <= 923.0 and y0 >= 9.0 and y1 <= 545.0
    print(f'  {"PASS" if ok else "FAIL"} containment {name}: x {x0:.1f}..{x1:.1f} y {y0:.1f}..{y1:.1f}')
