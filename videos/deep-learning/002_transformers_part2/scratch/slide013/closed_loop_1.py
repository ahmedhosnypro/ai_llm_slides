#!/usr/bin/env python3
"""Closed-loop ink check: render_1.png (150dpi, 2000x1125) vs frame-measured targets.
render_px = slide_pt * 2.0833 ; slide_pt from frame via the fitted mapping."""
from PIL import Image

R = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide013/render_1.png').convert('RGB')
W, H = R.size
rp = R.load()
print('render size', W, H)

AX, SX, SY = 17.628, 0.961232, 0.955556
K = 2.0833  # render px per slide pt
def tx(fx): return (fx - AX) / SX * K
def ty(fy): return fy / SY * K

def bbox_in(x0, x1, y0, y1, fn):
    xs, ys = [], []
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            if fn(*rp[x, y]):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return (min(xs), max(xs), min(ys), max(ys), len(xs))

def check(name, bb, tx0, tx1, ty0, ty1, tol=4.0):
    if bb is None:
        print('%-28s EMPTY  (target x %.0f..%.0f y %.0f..%.0f)' % (name, tx0, tx1, ty0, ty1))
        return False
    gx0, gx1, gy0, gy1 = tx(tx0), tx(tx1), ty(ty0), ty(ty1)
    dx0 = bb[0] - gx0; dx1 = bb[1] - gx1; dy0 = bb[2] - gy0; dy1 = bb[3] - gy1
    ok = max(abs(dx0), abs(dx1), abs(dy0), abs(dy1)) <= tol
    print('%-28s %s render x %4d..%4d y %4d..%4d | target x %6.1f..%6.1f y %6.1f..%6.1f | d %+5.1f %+5.1f %+5.1f %+5.1f' % (
        name, 'OK  ' if ok else 'FAIL', bb[0], bb[1], bb[2], bb[3], gx0, gx1, gy0, gy1, dx0, dx1, dy0, dy1))
    return ok

# color tests (render colors are exact; JPEG noise absent)
def near(c, tol=14):
    return lambda r, g, b: abs(r - c[0]) <= tol and abs(g - c[1]) <= tol and abs(b - c[2]) <= tol

all_ok = True
# 1 peach panel
all_ok &= check('peach panel', bbox_in(60, 1990, 120, 1110, near((247, 226, 205), 10)), 72, 849, 107, 500)
# 2 mint ellipse
all_ok &= check('mint ellipse', bbox_in(350, 600, 330, 960, near((133, 255, 167), 16)), 213, 262, 172, 421)
# 3 input ellipse (drawn at transparency 45 over white -> ~ (215,219,226)?) sample
all_ok &= check('input ellipse', bbox_in(60, 470, 320, 960, near((214, 218, 225), 12)), 66, 212, 169, 423)
# 4 DP box
all_ok &= check('DP box', bbox_in(480, 790, 380, 880, near((219, 203, 187), 10)), 264, 349, 187, 387)
# 5 softmax
all_ok &= check('softmax', bbox_in(900, 1070, 390, 870, near((248, 222, 251), 10)), 458, 489, 190, 386)
# 6 sigma box
all_ok &= check('sigma box', bbox_in(1030, 1390, 390, 480, near((234, 254, 252), 10)), 515, 642, 188, 210)
# 7 Wv band
all_ok &= check('Wv band', bbox_in(1400, 1610, 460, 850, near((248, 250, 104), 14)), 689, 737, 222, 379)
# 8 right container fill
all_ok &= check('right container', bbox_in(1540, 1800, 440, 860, near((232, 245, 231), 8)), 750, 827, 217, 381)
# 9 sentence container fill
all_ok &= check('sentence container', bbox_in(350, 1030, 950, 1100, near((232, 245, 231), 8)), 196, 472, 452, 498)
# 10 Wq box (white w/ red border on peach)
all_ok &= check('Wq box', bbox_in(560, 700, 850, 950, lambda r, g, b: r > 246 and g > 246 and b > 246), 292, 329, 419, 442)
# 11 dots (navy cores)
dots_t = [(339, 238.5), (324, 277.5), (309, 315.5), (286.5, 357.5)]
for i, (fx, fy) in enumerate(dots_t):
    cx, cy = tx(fx), ty(fy)
    bb = bbox_in(cx - 22, cx + 22, cy - 22, cy + 22, near((7, 7, 168), 60))
    if bb:
        cxb = (bb[0] + bb[1]) / 2; cyb = (bb[2] + bb[3]) / 2
        d = max(abs(cxb - cx), abs(cyb - cy))
        print('dot%d core center render (%.1f, %.1f) target (%.1f, %.1f) d=%.1f %s' % (
            i + 1, cxb, cyb, cx, cy, d, 'OK' if d <= 6 else 'FAIL'))
        all_ok &= d <= 6
    else:
        print('dot%d core EMPTY' % (i + 1)); all_ok = False
# 12 multiply circles (red rings) centers
circ_t = [(536, 238), (564, 277), (581, 316), (608, 358)]
for i, (fx, fy) in enumerate(circ_t):
    cx, cy = tx(fx), ty(fy)
    bb = bbox_in(cx - 25, cx + 25, cy - 25, cy + 25, lambda r, g, b: 150 <= r <= 210 and g <= 80 and b <= 80)
    if bb:
        cxb = (bb[0] + bb[1]) / 2; cyb = (bb[2] + bb[3]) / 2
        d = max(abs(cxb - cx), abs(cyb - cy))
        print('circ%d ring center render (%.1f, %.1f) target (%.1f, %.1f) d=%.1f %s' % (
            i + 1, cxb, cyb, cx, cy, d, 'OK' if d <= 8 else 'FAIL'))
        all_ok &= d <= 8
    else:
        print('circ%d ring EMPTY' % (i + 1)); all_ok = False
# 13 title L1 ink
all_ok &= check('title L1 ink', bbox_in(400, 1700, 100, 180, lambda r, g, b: r < 120 and g < 120 and b < 200), 234, 770, 58, 74)
# 14 title L2 ink
all_ok &= check('title L2 ink', bbox_in(380, 1720, 175, 230, lambda r, g, b: (r < 120 and g < 120) or (r > 130 and g < 90 and b < 90)), 199, 805, 79, 97)
# 15 pills
all_ok &= check('Similarity pill', bbox_in(540, 750, 330, 400, near((255, 255, 227), 10)), 280, 343, 159, 178)
all_ok &= check('Probabilities pill', bbox_in(860, 1090, 320, 395, near((255, 255, 227), 10)), 432, 512, 157, 177)
all_ok &= check('WeightedSUM pill', bbox_in(1190, 1450, 320, 400, near((255, 255, 227), 10)), 591, 680, 157, 178)
# 16 output box (dashed green border + cells)
all_ok &= check('output box green', bbox_in(1100, 1310, 230, 320, lambda r, g, b: g > 110 and r < 110 and b < 110), 545, 615, 117, 142)
print()
print('CLOSED-LOOP:', 'ALL OK' if all_ok else 'FAILURES PRESENT')
