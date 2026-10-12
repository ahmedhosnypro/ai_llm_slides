#!/usr/bin/env python3
"""Attempt-2 closed-loop ink check (clean zones, fixed scans)."""
from PIL import Image
import numpy as np

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide053/render_2.png'
im = Image.open(REN).convert('RGB')
a = np.asarray(im).astype(int)
S = 72.0/150.0
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
masks = {
 'red':   (r-(g+b)/2 > 55), 'blue': (b-(r+g)/2 > 55),
 'green': (g>r+6)&(g>b+6)&(g>195)&(r>150), 'yellow': (r>228)&(g>228)&(b>150)&(b<225),
 'dark': (r<110)&(g<110)&(b<110),
}
def bbox(mn, x0, y0, x1, y1, label, tx0, ty0, tx1, ty1):
    m = masks[mn]
    z = np.zeros_like(m); z[int(y0/S):int(y1/S), int(x0/S):int(x1/S)] = True
    ys, xs = np.where(m & z)
    if len(xs)==0: print(f'  FAIL {label}: NO INK'); return None
    mx0, mx1, my0, my1 = xs.min()*S, xs.max()*S, ys.min()*S, ys.max()*S
    d = [mx0-tx0, my0-ty0, mx1-tx1, my1-ty1]
    w = max(abs(v) for v in d)
    st = 'PASS' if w<=2.0 else ('WARN' if w<=3.0 else 'FAIL')
    print(f'  {st} {label}: x {mx0:.1f}..{mx1:.1f} y {my0:.1f}..{my1:.1f} vs tgt {tx0:.1f}..{tx1:.1f} / {ty0:.1f}..{ty1:.1f}  d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})')

print('=== selfcheck attempt 2 (tol 2.0pt = ~4px @150dpi) ===')
bbox('red',   200, 50, 700, 79,  'L1 title',      249.6, 62.0, 617.3, 80.8)
bbox('red',   200, 82, 458, 112, 'L2 red part',   249.6, 89.2, 454.8, 110.1)
bbox('blue',  459, 82, 620, 112, 'L2 blue part',  463.1, 89.2, 579.8, 108.0)
bbox('red',   730, 100, 810, 129,'Softmax label', 744.4, 115.4, 798.6, 124.8)
bbox('dark',  742, 134, 898, 206,'Equation ink',  751.7, 141.5, 871.5, 186.5)
m = masks['blue']
rowtop = [y*S for y in range(int(112/S), int(120/S)) if m[y, int(400/S):int(600/S)].any()]
colL = [x*S for x in range(int(318/S), int(334/S)) if m[int(150/S):int(290/S), x].any()]
colR = [x*S for x in range(int(700/S), int(720/S)) if m[int(150/S):int(400/S), x].any()]
rowbot = [y*S for y in range(int(426/S), int(435/S)) if m[y, int(400/S):int(600/S)].any()]
print(f'  container: top {min(rowtop):.1f}(115.4) left {min(colL):.1f}(326.6) right {max(colR):.1f}(711.1) bottom {max(rowbot):.1f}(430.2)')
bbox('green', 336, 202, 442, 410,'Row chips',     347.5, 216.8, 434.2, 405.1)
# tags total span (windows overlap; outer edges are the checkable signal)
bbox('green', 400, 126, 690, 210, 'Tags span',    415.5, 134.2, 672.7, 208.5)
bbox('red',   452, 218, 678, 408,'Red blocks',    503.2, 222.2, 675.6, 364.5)
# arrow: tail band + head depth probes
ys_t = [y*S for y in range(int(296/S), int(330/S)) if masks['blue'][y, int(300/S)]]
ys_h = [y*S for y in range(int(296/S), int(330/S)) if masks['blue'][y, int(322/S)]]
xs_h = [x*S for x in range(int(288/S), int(325/S)) if masks['blue'][int(312/S), x]]
print(f'  arrow: tail col x=300 y {min(ys_t):.1f}..{max(ys_t):.1f} (tgt ~305.7..317.8) | head col x=322 y {min(ys_h):.1f}..{max(ys_h):.1f} (tgt ~303..321.5) | head row y=312 x {min(xs_h):.1f}..{max(xs_h):.1f} (tgt 294.4..~324clipped)')
bbox('blue',  40, 433, 910, 540, 'Statement box', 47.5, 436.5, 895.4, 530.9)
bbox('blue',  60, 440, 890, 470, 'Stmt L1 ink',   65.2, 447.0, 552.0, 464.7)
bbox('red',   60, 484, 890, 508, 'Stmt L2 ink',   65.2, 490.9, 813.1, 506.6)
bbox('red',   60, 509, 890, 532, 'Stmt L3 ink',   65.2, 511.8, 823.6, 527.5)
for lbl, cx, cy in [('r0c0', 469.5, 231.4), ('r2c2', 565.9, 313.4), ('r4c0', 469.5, 395.4), ('r4c4', 662.3, 395.4)]:
    bbox('dark', cx-6, cy-7.5, cx+6, cy+7.5, f'Digit {lbl}', cx-2.1, cy-4.4, cx+2.1, cy+4.6)
n = int(masks['blue'][int(460/S):int(466/S), int(240/S):int(300/S)].sum())
print(f'  ADDED underline: {n} blue px')
n2 = int(masks['red'][int(523/S):int(530/S), int(725/S):int(775/S)].sum())
print(f'  future underline: {n2} red px')
