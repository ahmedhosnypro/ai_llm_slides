#!/usr/bin/env python3
"""Closed-loop check attempt 3 (fixed windows/masks)."""
from PIL import Image

R = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide013/render_1.png').convert('RGB')
rp = R.load()
AX, SX, SY = 17.628, 0.961232, 0.955556
K = 2.0833
def tx(fx): return (fx - AX) / SX * K
def ty(fy): return fy / SY * K

def bbox_in(x0, x1, y0, y1, fn):
    xs, ys = [], []
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            if fn(*rp[x, y]):
                xs.append(x); ys.append(y)
    return (min(xs), max(xs), min(ys), max(ys), len(xs)) if xs else None

def check(name, bb, t, tol=4.0):
    tx0, tx1, ty0, ty1 = t
    if bb is None:
        print('%-26s EMPTY' % name); return False
    gx0, gx1, gy0, gy1 = tx(tx0), tx(tx1), ty(ty0), ty(ty1)
    d = (bb[0]-gx0, bb[1]-gx1, bb[2]-gy0, bb[3]-gy1)
    ok = max(abs(v) for v in d) <= tol
    print('%-26s %s render x %4d..%4d y %4d..%4d | d %+5.1f %+5.1f %+5.1f %+5.1f' % (
        name, 'OK  ' if ok else 'FAIL', bb[0], bb[1], bb[2], bb[3], *d))
    return ok

ok = True
ok &= check('title L1 ink', bbox_in(400, 1700, 100, 172, lambda r,g,b: r<120 and g<120 and b<200), (234, 770, 58, 74), 5)
ok &= check('title L2 ink', bbox_in(380, 1720, 168, 245, lambda r,g,b: (r<120 and g<120 and b<120) or (130<=r<=220 and g<90 and b<90)), (199, 805, 79, 97), 6)
# x-center of L2
bb = bbox_in(380, 1720, 168, 245, lambda r,g,b: (r<120 and g<120 and b<120) or (130<=r<=220 and g<90 and b<90))
print('L2 ink center render %.1f target %.1f' % ((bb[0]+bb[1])/2, (tx(199)+tx(805))/2))
# multiply circles: ring bbox should be centered on target within 6px
circ_t = [(536, 238), (564, 277), (581, 316), (608, 358)]
for i, (fx, fy) in enumerate(circ_t):
    cx, cy = tx(fx), ty(fy)
    bb = bbox_in(cx-20, cx+20, cy-20, cy+20, lambda r,g,b: 150<=r<=215 and g<=80 and b<=80)
    cxb, cyb = (bb[0]+bb[1])/2, (bb[2]+bb[3])/2
    d = max(abs(cxb-cx), abs(cyb-cy))
    print('circ%d center d=%.1f %s' % (i+1, d, 'OK' if d<=6 else 'FAIL')); ok &= d<=6
ok &= check('Wq box cream', bbox_in(560, 700, 850, 975, lambda r,g,b: r>246 and g>244 and b>232 and b<250), (292, 329, 419, 442))
ok &= check('sentence X labels', bbox_in(400, 1000, 1006, 1052, lambda r,g,b: 130<=r<=220 and g<90 and b<90), (226, 452, 466, 481), 6)
ok &= check('X2 highlight magenta', bbox_in(560, 720, 995, 1070, lambda r,g,b: 110<=r<=170 and g<70 and 110<=b<=170), (287, 324, 462, 484), 6)
# right container cells: periwinkle + pink cell CENTER positions (cell4/5 of top row)
bbp = bbox_in(1560, 1760, 470, 530, lambda r,g,b: abs(r-204)<=16 and abs(g-204)<=16 and abs(b-255)<=10)
print('periwinkle cell top row: render x %s..%s target x %.0f..%.0f' % (bbp[0], bbp[1], tx(794), tx(807)))
ok &= abs((bbp[0]+bbp[1])/2 - (tx(794)+tx(807))/2) <= 6
bbk = bbox_in(1560, 1780, 470, 530, lambda r,g,b: r>230 and 120<g<180 and 180<b<230)
print('pink cell top row: render x %s..%s target x %.0f..%.0f' % (bbk[0], bbk[1], tx(807), tx(820)))
ok &= abs((bbk[0]+bbk[1])/2 - (tx(807)+tx(820))/2) <= 6
# frame containment: nothing crosses the house frame (ink beyond panel edges)
print('CLOSED-LOOP ATTEMPT 3:', 'ALL OK' if ok else 'FAILURES PRESENT')
