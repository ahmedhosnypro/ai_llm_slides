#!/usr/bin/env python3
"""c2_closedloop2.py — attempt-K closed loop with per-element tight windows."""
from PIL import Image
import numpy as np
import sys

K = sys.argv[1] if len(sys.argv) > 1 else '1'
RN = f'/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide041/render_attempt{K}.png'
im = np.asarray(Image.open(RN).convert('RGB')).astype(int)
H, W, _ = im.shape
S = 150 / 72.0
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

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

# boxes (windows clamped to midpoints between adjacent boxes)
check('root_box', peach, [347.5, 124.4, 565.1, 176.6], [650, 220, 1250, 420])
check('blue_box', blue, [113.3, 231.9, 335.0, 286.2], [180, 440, 760, 640])
check('green_box', green, [572.4, 229.8, 795.1, 284.1], [1120, 440, 1720, 640])
check('cyan1', cyan, [254.9, 308.2, 493.3, 348.9], [470, 600, 1100, 742])
check('cyan2', cyan, [254.9, 362.5, 493.3, 403.2], [470, 748, 1100, 864])
check('cyan3', cyan, [254.9, 416.8, 493.3, 457.5], [470, 862, 1100, 980])
check('cyan4', cyan, [254.9, 474.2, 493.3, 514.9], [470, 985, 1100, 1105])
check('leaf_box', leaf, [565.1, 342.6, 801.4, 381.3], [1100, 690, 1730, 830])

# texts
check('title', redink, [340.2, 71.1, 568.2, 96.2], [600, 120, 1300, 230])
check('rootL1', redink, [384.0, 129.6, 526.6, 144.2], [730, 255, 1170, 310])
check('rootL2', redink, [446.4, 154.7, 464.1, 169.3], [880, 312, 1020, 360])
check('blueL1', white, [166.4, 239.2, 280.9, 252.8], [242, 487, 692, 532])
check('blueL2', white, [183.0, 264.3, 264.2, 282.1], [242, 545, 692, 592])
check('green_txt', white, [643.1, 250.7, 724.3, 268.5], [1210, 490, 1640, 585])
check('cyan1_txt', navy, [274.7, 320.7, 473.5, 335.3], [500, 648, 1080, 740])
check('cyan2_txt', navy, [260.1, 375.0, 488.0, 389.6], [500, 758, 1080, 858])  # re-measured full bbox
check('cyan3_txt', navy, [271.5, 429.3, 476.6, 449.1], [500, 870, 1080, 976])
check('cyan4_txt', navy, [275.7, 487.8, 472.4, 506.6], [500, 980, 1080, 1098])
check('leaf_txt', dkgreen, [577.6, 354.1, 788.9, 374.0], [1120, 700, 1700, 812])

# connectors (tight windows, clear of text/boxes)
check('drop_line', redink, [452.9, 180.0, 456.1, 211.0], [934, 376, 962, 436])
check('hbar', redink, [224.7, 211.7, 684.3, 215.7], [400, 438, 1500, 452])
check('spine', redink, [223.9, 297.6, 227.9, 318.9], [458, 620, 484, 664])  # x-band segment (window-matched)
check('right_shft', redink, [682.3, 284.1, 686.3, 326.5], [1412, 588, 1440, 676])
check('headL', redink, [220.0, 217.9, 229.4, 229.4], [440, 450, 500, 484])
check('headR', redink, [679.1, 217.9, 689.5, 228.9], [1385, 450, 1445, 484])
check('cyanHead1', redink, [246.0, 324.3, 253.9, 332.9], [508, 676, 536, 698])  # apex half
check('cyanHead4', redink, [246.0, 490.3, 253.9, 498.9], [508, 1012, 536, 1044])  # apex half
check('rightHead', redink, [679.6, 327.0, 689.0, 339.5], [1400, 682, 1450, 714])

print()
print('RESULT:', 'ALL OK' if not FAILS else 'FAILS: ' + ', '.join(FAILS))
