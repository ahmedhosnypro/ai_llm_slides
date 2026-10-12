#!/usr/bin/env python3
"""c1_closedloop.py — closed-loop ink check: 150dpi render (attempt K) vs original-frame targets.

render px = slide_pt * 150/72 (= *2.08333). Tolerance ~4 render px.
Targets = measured ink/fill bboxes in slide_041.jpg mapped to slide pts (scratch m3..m7).
"""
from PIL import Image
import numpy as np
import sys

K = sys.argv[1] if len(sys.argv) > 1 else '1'
RN = f'/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide041/render_attempt{K}.png'
im = np.asarray(Image.open(RN).convert('RGB')).astype(int)
H, W, _ = im.shape
print('render size:', W, H)
S = 150 / 72.0
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# pure render masks
redink = (R > 130) & (G < 90) & (B < 90)
navy   = (R < 80) & (G < 80) & (B > 95)
white  = (R > 215) & (G > 215) & (B > 215)
dkgreen= (R < 130) & (G > 60) & (G < 180) & (B < 150)
peach  = (np.abs(R - 250) < 12) & (np.abs(G - 230) < 12) & (np.abs(B - 214) < 14)
blue   = (np.abs(R - 0) < 40) & (np.abs(G - 0) < 40) & (np.abs(B - 166) < 40)
green  = (np.abs(R - 10) < 45) & (np.abs(G - 134) < 40) & (np.abs(B - 58) < 40)
cyan   = (np.abs(R - 224) < 18) & (G > 240) & (B > 240)
leaf   = (np.abs(R - 214) < 18) & (G > 240) & (np.abs(B - 230) < 20)

def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(len(xs))]

FAILS = []
def check(name, mask, target_pts, region, tol=4.0):
    """target_pts = [x0,y0,x1,y1] in slide pts; region = render-px search window"""
    t = [round(v * S, 1) for v in target_pts]
    bb = bbox(mask, *region)
    if bb is None:
        print('%-10s EMPTY  (target %s)' % (name, t)); FAILS.append(name + ':EMPTY'); return
    d = [bb[i] - t[i] for i in range(4)]
    ok = all(abs(v) <= tol for v in d)
    print('%-10s got[%d,%d -> %d,%d] tgt[%s] d[%+.1f %+.1f %+.1f %+.1f] %s' % (
        name, bb[0], bb[1], bb[2], bb[3], ','.join(str(v) for v in t),
        d[0], d[1], d[2], d[3], 'OK' if ok else '**FAIL**'))
    if not ok: FAILS.append(name)

# --- boxes (fill bboxes)
check('root_box', peach, [347.5, 124.4, 565.1, 176.6], [650, 220, 1250, 420])
check('blue_box', blue, [113.3, 231.9, 335.0, 286.2], [180, 440, 760, 640])
check('green_box', green, [572.4, 229.8, 795.1, 284.1], [1120, 440, 1720, 640])
check('cyan1', cyan, [254.9, 308.2, 493.3, 348.9], [470, 600, 1100, 760])
check('cyan2', cyan, [254.9, 362.5, 493.3, 403.2], [470, 740, 1100, 880])
check('cyan3', cyan, [254.9, 416.8, 493.3, 457.5], [470, 850, 1100, 990])
check('cyan4', cyan, [254.9, 474.2, 493.3, 514.9], [470, 960, 1100, 1105])
check('leaf_box', leaf, [565.1, 342.6, 801.4, 381.3], [1100, 690, 1730, 830])

# --- texts (ink bboxes)
check('title', redink, [340.2, 71.1, 568.2, 96.2], [600, 120, 1300, 230])
check('root_txt', redink, [384.0, 129.6, 526.6, 169.3], [720, 240, 1180, 370])
check('blue_txt', white, [166.4, 239.2, 280.9, 282.1], [250, 470, 690, 600])
check('green_txt', white, [643.1, 250.7, 724.3, 268.5], [1210, 490, 1640, 580])
check('cyan1_txt', navy, [274.7, 320.7, 473.5, 335.3], [500, 630, 1080, 745])
check('leaf_txt', dkgreen, [577.6, 354.1, 788.9, 374.0], [1120, 700, 1700, 810])

# --- connectors (ink bands)
# drop line x band 453.7 -> 945.2 ; y 176.6->213.7 -> 367.9..445.2
bb = bbox(redink, 920, 350, 975, 448)
print('drop_line  got', bb[:4] if bb else None, ' target x[945.2] y[367.9..445.2]')
# hbar y 213.7 -> 445.2 ; x 224.7->684.3 -> 468.1..1425.6
bb = bbox(redink, 400, 438, 1500, 452)
print('hbar       got', bb[:4] if bb else None, ' target y[445.2] x[468.1..1425.6]')
# spine x 225.9 -> 470.6 ; y 286.2->500.3 -> 596.2..1042.3
bb = bbox(redink, 455, 610, 486, 1045)
print('spine      got', bb[:4] if bb else None, ' target x[470.6] y[596.2..1042.3]')
# right shaft x 684.3 -> 1425.6 ; y 284.1->326.5 -> 591.9..680.2
bb = bbox(redink, 1410, 585, 1442, 685)
print('right_shft got', bb[:4] if bb else None, ' target x[1425.6] y[591.9..680.2]')
# heads: headL ~ cx 224.7 y 217.9..229.4 -> px cx 468.1 y 453.9..477.9
bb = bbox(redink, 440, 448, 500, 482)
print('headL      got', bb[:4] if bb else None, ' target cx[468.1] y[453.9..477.9]')
# cyan head1: apex 253.9->529.0 base 240.9->501.9 cy 328.6 -> 684.6 (y 673.0..696.3)
bb = bbox(redink, 495, 670, 534, 700)
print('cyanHead1  got', bb[:4] if bb else None, ' target x[501.9..529.0] cy[684.6]')
# right head: cx 684.3 y 327.0..339.5 -> px cx 1425.6 y 681.2..707.3
bb = bbox(redink, 1400, 678, 1450, 712)
print('rightHead  got', bb[:4] if bb else None, ' target cx[1425.6] y[681.2..707.3]')

print()
print('RESULT:', 'ALL OK' if not FAILS else 'FAILS: ' + ', '.join(FAILS))
