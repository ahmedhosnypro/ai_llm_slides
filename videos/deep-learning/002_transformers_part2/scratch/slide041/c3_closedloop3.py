#!/usr/bin/env python3
"""c3_closedloop3.py — attempt-3 closed loop: boxes/texts as c2 + color-aware connector checks."""
from PIL import Image
import numpy as np
import sys

K = sys.argv[1] if len(sys.argv) > 1 else '3'
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
# light-shaft mask: any pixel meaningfully darker than panel bg, not a box fill
lum = (R + G + B) / 3.0
shaft = (lum < 216) & (lum > 140)

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

# boxes + texts (same targets as attempt 2)
check('root_box', peach, [347.5, 124.4, 565.1, 176.6], [650, 220, 1250, 420])
check('blue_box', blue, [113.3, 231.9, 335.0, 286.2], [180, 440, 760, 640])
check('green_box', green, [572.4, 229.8, 795.1, 284.1], [1120, 440, 1720, 640])
check('cyan1', cyan, [254.9, 308.2, 493.3, 348.9], [470, 600, 1100, 742])
check('cyan2', cyan, [254.9, 362.5, 493.3, 403.2], [470, 748, 1100, 864])
check('cyan3', cyan, [254.9, 416.8, 493.3, 457.5], [470, 862, 1100, 980])
check('cyan4', cyan, [254.9, 474.2, 493.3, 514.9], [470, 985, 1100, 1105])
check('leaf_box', leaf, [565.1, 342.6, 801.4, 381.3], [1100, 690, 1730, 830])
check('title', redink, [340.2, 71.1, 568.2, 96.2], [600, 120, 1300, 230])
check('rootL1', redink, [384.0, 129.6, 526.6, 144.2], [730, 255, 1170, 310])
check('blueL1', white, [166.4, 239.2, 280.9, 252.8], [242, 487, 692, 532])
check('blueL2', white, [183.0, 264.3, 264.2, 282.1], [242, 545, 692, 592])
check('green_txt', white, [643.1, 250.7, 724.3, 268.5], [1210, 490, 1640, 585])
check('cyan1_txt', navy, [274.7, 320.7, 473.5, 335.3], [500, 648, 1080, 740])
check('cyan2_txt', navy, [260.1, 375.0, 488.0, 389.6], [500, 758, 1080, 858])
check('cyan3_txt', navy, [271.5, 429.3, 476.6, 449.1], [500, 870, 1080, 976])
check('cyan4_txt', navy, [275.7, 487.8, 472.4, 506.6], [500, 980, 1080, 1098])
check('leaf_txt', dkgreen, [577.6, 354.1, 788.9, 374.0], [1120, 700, 1700, 812])

# heads (shrunk ~12% for JPEG-halo compensation; targets = halo-shrunk frame ink)
check('headL', redink, [220.6, 218.2, 228.8, 228.0], [440, 450, 500, 484])
check('headR', redink, [679.8, 218.2, 688.8, 228.0], [1385, 450, 1445, 484])
check('rightHead', redink, [680.2, 327.6, 688.4, 338.8], [1400, 678, 1450, 714])

# shafts (color-aware; positions from draw params)
# drop x=454.2c y 176.6..213.7 -> px x [944.2..948.4] y [367.9..445.2]
bb = bbox(shaft, 938, 372, 956, 440)
print('drop_line  got', bb[:4] if bb else None, ' tgt x[944.2..948.4] y[367.9..445.2]')
# hbar y 213.7 -> 443.9..446.1 ; x 468.1..1425.6
bb = bbox(shaft, 400, 438, 1500, 452)
print('hbar       got', bb[:4] if bb else None, ' tgt y[443.9..446.1] x[468.1..1425.6]')
# spine x 225.9c -> 468.5..472.7 ; segment y 620..664 clear of shafts
bb = bbox(shaft, 458, 620, 484, 664)
print('spine      got', bb[:4] if bb else None, ' tgt x[468.5..472.7]')
# right shaft x 684.3c -> 1423.5..1427.7 ; y 591.9..680.2 (clear of head)
bb = bbox(shaft, 1412, 588, 1440, 672)
print('right_shft got', bb[:4] if bb else None, ' tgt x[1423.5..1427.7]')
# cyan shaft 1: y 328.6c -> 683.6..685.7 ; x from 472 to head base 504
bb = bbox(shaft, 476, 674, 502, 696)
print('cyanShft1  got', bb[:4] if bb else None, ' tgt y[683.6..685.7] x[472..504]')

# cyan/leaf border color sample (should be ~C0C0C0 now)
print('cyan1 top border row (y~641):', [tuple(im[641, x]) for x in (700, 800, 900)])
print('leaf top border row (y~711):', [tuple(im[711, x]) for x in (1250, 1400, 1550)])
print('spine px sample:', [tuple(im[y, 470]) for y in (640, 700, 900)])
print('hbar px sample:', [tuple(im[445, x]) for x in (600, 900, 1200)])
print('drop px sample:', [tuple(im[y, 946]) for y in (390, 410, 430)])

print()
print('RESULT:', 'ALL OK' if not FAILS else 'FAILS: ' + ', '.join(FAILS))
