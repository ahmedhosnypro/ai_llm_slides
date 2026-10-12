#!/usr/bin/env python3
"""Attempt-1 self-check v2: tight, contamination-free zones."""
from PIL import Image
import numpy as np

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide053/render_1.png'
im = Image.open(REN).convert('RGB')
a = np.asarray(im).astype(int)
S = 72.0 / 150.0
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
masks = {
    'red':   (r - (g + b) / 2 > 55),
    'blue':  (b - (r + g) / 2 > 55),
    'green': (g > r + 6) & (g > b + 6) & (g > 195) & (r > 150),
    'yellow': (r > 228) & (g > 228) & (b > 150) & (b < 225),
    'dark':  (r < 110) & (g < 110) & (b < 110),
}

def bbox(mask_name, x0, y0, x1, y1, label, tx0, ty0, tx1, ty1):
    m = masks[mask_name]
    z = np.zeros_like(m); z[int(y0/S):int(y1/S), int(x0/S):int(x1/S)] = True
    ys, xs = np.where(m & z)
    if len(xs) == 0:
        print(f'  FAIL {label}: NO INK'); return
    mx0, mx1 = xs.min() * S, xs.max() * S
    my0, my1 = ys.min() * S, ys.max() * S
    d = [mx0-tx0, my0-ty0, mx1-tx1, my1-ty1]
    worst = max(abs(v) for v in d)
    stat = 'PASS' if worst <= 2.0 else ('WARN' if worst <= 3.0 else 'FAIL')
    print(f'  {stat} {label}: ink x {mx0:.1f}..{mx1:.1f} y {my0:.1f}..{my1:.1f} vs tgt x {tx0:.1f}..{tx1:.1f} y {ty0:.1f}..{ty1:.1f}  d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})')

print('=== selfcheck v2 (tight zones) ===')
bbox('red',   200, 50, 700, 92,  'L1 title',      249.6, 62.0, 617.3, 80.8)
bbox('red',   200, 80, 458, 116, 'L2 red part',   249.6, 89.2, 454.8, 110.1)
bbox('blue',  459, 80, 620, 116, 'L2 blue part',  463.1, 89.2, 579.8, 108.0)
bbox('red',   730, 100, 810, 129,'Softmax label', 744.4, 115.4, 798.6, 124.8)
bbox('dark',  742, 134, 896, 204,'Equation ink',  751.7, 141.5, 871.5, 186.5)
# container: top/bottom/right borders via rows/cols in clean spans
m = masks['blue']
rowtop = [y*S for y in range(int(118/S), int(125/S)) if m[y, int(400/S):int(600/S)].any()]
colL = [x*S for x in range(int(318/S), int(334/S)) if m[int(200/S):int(400/S), x].any()]
colR = [x*S for x in range(int(700/S), int(720/S)) if m[int(200/S):int(400/S), x].any()]
rowbot = [y*S for y in range(int(425/S), int(436/S)) if m[y, int(400/S):int(600/S)].any()]
print(f'  container borders: top {min(rowtop):.1f} (tgt 115.4) left {min(colL):.1f} (tgt 326.6) right {max(colR):.1f} (tgt 711.1) bottom {max(rowbot):.1f} (tgt 430.2)')
bbox('green', 336, 202, 442, 410,'Row chips',     347.5, 216.8, 434.2, 405.1)
# tags: measure each tag's green bbox in 5 tight windows around expected rotated bboxes
for i, cx in enumerate([451.6, 495.7, 542.2, 592.6, 636.6]):
    bbox('green', cx-40, 128, cx+40, 212, f'tag{i}', cx-36.1, 136.4, cx+36.1, 208.5)
bbox('red',   450, 215, 680, 410,'Red blocks',    503.2, 222.2, 675.6, 364.5)
bbox('blue',  288, 296, 324, 330,'Arrow',         294.4, 302.6, 328.4, 321.8)
bbox('blue',  40, 433, 910, 540, 'Statement box', 47.5, 436.5, 895.4, 530.9)
bbox('blue',  60, 440, 890, 470, 'Stmt L1 ink',   65.2, 447.0, 552.0, 464.7)
bbox('red',   60, 484, 890, 508, 'Stmt L2 ink',   65.2, 490.9, 813.1, 506.6)
bbox('red',   60, 509, 890, 532, 'Stmt L3 ink',   65.2, 511.8, 823.6, 527.5)
# digits: tight center zones (chip +-6pt)
bbox('dark',  463.5, 225.4, 475.5, 237.4, 'Digit r0c0', 465.2, 226.2, 471.5, 235.7)
bbox('dark',  646.5, 389.4, 658.5, 401.4, 'Digit r4c4', 647.7, 391.5, 654.4, 400.9)
# ADDED underline presence: blue ink row band under ADDED (y ~461.5..465) x 235..305
m = masks['blue']
n = int(m[int(460/S):int(466/S), int(240/S):int(300/S)].sum())
print(f'  {"PASS" if n > 30 else "FAIL"} ADDED underline: {n} blue px at y 460..466 x 240..300')
# future underline: red ink y 524..529 x 730..770?
n2 = int(masks['red'][int(523/S):int(530/S), int(725/S):int(775/S)].sum())
print(f'  {"PASS" if n2 > 20 else "WARN"} future underline: {n2} red px at y 523..530 x 725..775')
