#!/usr/bin/env python3
"""selfcheck_attempt_2 — closed-loop PIL ink check, clean windows (chrome border at
render x 1914-1915 excluded; window offsets added; expectations = frame bboxes via
the mapping). Tol 5 render px unless noted."""
import json
from PIL import Image
import numpy as np

REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/render_1.png"
K = 150.0 / 72.0
AX, SX, SY = 17.72, 0.961231, 0.955556
def RX(fx): return (fx - AX) / SX * K
def RY(fy): return fy / SY * K

img = Image.open(REND).convert("RGB")
A = np.asarray(img).astype(int)
R, Gc, B = A[..., 0], A[..., 1], A[..., 2]
res = {}
XLIM = 1905  # chrome panel right border sits at 1914-1915 — keep windows left of it

def bbox(mask, ox, oy):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [ox + int(xs.min()), oy + int(ys.min()), ox + int(xs.max()), oy + int(ys.max()), int(mask.sum())]

def check(name, got, exp, tol=5.0):
    if got is None:
        res[name] = "FAIL: no ink"
        return
    d = [abs(got[i] - exp[i]) for i in range(4)]
    res[name] = f"{'OK ' if max(d) <= tol else 'FAIL'} max|d|={max(d):.1f} got={got[:4]} exp={[round(e,1) for e in exp[:4]]}"

redm = (R > 100) & (R - Gc > 35) & (R - B > 30)
blum = (B - R > 45) & (B > 90)
dk = (A.sum(axis=2) < 430)

# 1. title (avoid chrome border column)
got = bbox(redm[120:185, 600:1900], 600, 120)
check("title", got, [RX(339), RY(59), RX(689), RY(78)])
res["title_w"] = got[2] - got[0] if got else None
res["title_w_exp"] = RX(689) - RX(339)

# 2. subtitle (window ends before badge ring x 1849)
got = bbox(blum[180:240, 600:1840], 600, 180)
check("subtitle", got, [RX(322), RY(85.5), RX(718), RY(105)])
res["sub_w"] = got[2] - got[0] if got else None
res["sub_w_exp"] = RX(718) - RX(322)

# 3. diagram panel border
db = (B - R > 25) & (A.sum(axis=2) < 500)
got = bbox(db[230:760, 90:1890], 90, 230)
check("dbox", got, [RX(64), RY(111), RX(893), RY(342)])

# 4. row1 lane sage fill
sage = (abs(R - Gc) < 12) & (abs(Gc - B) < 12) & (A.sum(axis=2) > 560) & (A.sum(axis=2) < 720)
got = bbox(sage[255:335, 380:1880], 380, 255)
check("lane1_fill", got, [RX(180), RY(121), RX(874), RY(154)])

# 5. row1 box borders: rose strokes — column profile of (R-G>18, R>150) in box band
r1b = (R - Gc > 18) & (R > 150) & (Gc > 95) & (R - B > 12)
sub = r1b[int(RY(127)):int(RY(147)), 300:1880]
colc = sub.sum(axis=0)
strokes = [300 + i for i in range(len(colc)) if colc[i] >= 14]
runs, s = [], None
for c in strokes:
    if runs and c - runs[-1][1] <= 2: runs[-1][1] = c
    else: runs.append([c, c])
res["r1_vstrokes_n"] = len(runs)
if len(runs) >= 2:
    expL, expR = RX(182), RX(877)
    res["r1_vstrokes_d"] = [round(runs[0][0] - expL, 1), round(runs[-1][1] - expR, 1)]

# 6. row1 text band
r1t = (R - Gc > 45) & (R < 190) & (R > 80)
got = bbox(r1t[int(RY(130)):int(RY(145)), 380:1880], 380, int(RY(130)))
check("r1_text_band", got, [RX(193), RY(131.5), RX(869), RY(142)])

# 7. row2 lane lavender
lav = (B - R > 35) & (R > 170) & (R < 225) & (B > 230)
got = bbox(lav[390:470, 380:1880], 380, 390)
check("lane2_fill", got, [RX(178), RY(189), RX(872), RY(223)])

# 8. row2 borders band
r2b = (B - R > 40) & (R < 170) & (B > 150)
got = bbox(r2b[int(RY(193)):int(RY(219)), 380:1880], 380, int(RY(193)))
check("r2_borders_band", got, [RX(179), RY(194.5), RX(873), RY(217)])

# 9. row2 text band
r2t = (B - R > 70) & (R < 110)
got = bbox(r2t[int(RY(197)):int(RY(214)), 380:1880], 380, int(RY(197)))
check("r2_text_band", got, [RX(191), RY(198.5), RX(866), RY(212)])

# 10. row3 lane pink
pink = (R - B > 4) & (R > 235) & (Gc > 215) & (Gc < 245)
got = bbox(pink[545:625, 380:1880], 380, 545)
check("lane3_fill", got, [RX(178), RY(265), RX(871), RY(299)])

# 11. row3 text band
r3t = (R - Gc > 55) & (R < 180)
got = bbox(r3t[int(RY(276)):int(RY(292)), 380:1880], 380, int(RY(276)))
check("r3_text_band", got, [RX(200), RY(278.5), RX(864), RY(290)])

# 12. dots1
grayd = (abs(R - Gc) < 18) & (abs(Gc - B) < 18) & (A.sum(axis=2) < 590) & (A.sum(axis=2) > 330)
x0w = int(RX(615))
sub = grayd[int(RY(132)):int(RY(145)), x0w:int(RX(725))]
colc = sub.sum(axis=0)
runs, s = [], None
for i, v in enumerate(colc >= 2):
    if v and s is None: s = i
    elif not v and s is not None: runs.append((x0w + s, x0w + i - 1)); s = None
res["dots1_n"] = len(runs)
if len(runs) == 5:
    exp = [RX(637), RX(655), RX(673), RX(691.5), RX(706.5)]
    res["dots1_d"] = [round((a + b) / 2 - e, 1) for (a, b), e in zip(runs, exp)]

# 13. arrows
orange = (R > 150) & (R - B > 70) & (Gc > 55) & (Gc < 200) & (B < 140)
sub = orange[int(RY(292)):int(RY(307)), 380:1880]
ys, xs = np.where(sub)
cl = []
if len(xs):
    pts = sorted(zip(xs, ys))
    cur = [pts[0][0], pts[0][0], pts[0][1], pts[0][1]]
    for x, y in pts[1:]:
        if x - cur[1] <= 14:
            cur[1] = max(cur[1], x); cur[2] = min(cur[2], y); cur[3] = max(cur[3], y)
        else:
            cl.append(cur); cur = [x, x, y, y]
    cl.append(cur)
res["arrows_n"] = len(cl)
if len(cl) == 6:
    expx = [(271, 285), (346, 356), (418, 430), (494, 502), (567, 575), (832, 841)]
    res["arrows_dx0"] = [round(cl[i][0] + 380 - RX(expx[i][0]), 1) for i in range(6)]
    res["arrows_dy"] = [round(cl[0][2] + int(RY(292)) - RY(294), 1), round(cl[0][3] + int(RY(292)) - RY(304.5), 1)]

# 14. deltas
delt = (R - B > 55) & (R > 110) & (R < 200) & (Gc < 110)
y0w = int(RY(313))
sub = delt[y0w:int(RY(331)), 380:1880]
ys, xs = np.where(sub)
cl = []
if len(xs):
    pts = sorted(zip(xs, ys))
    cur = [pts[0][0], pts[0][0], pts[0][1], pts[0][1]]
    for x, y in pts[1:]:
        if x - cur[1] <= 14:
            cur[1] = max(cur[1], x); cur[2] = min(cur[2], y); cur[3] = max(cur[3], y)
        else:
            cl.append(cur); cur = [x, x, y, y]
    cl.append(cur)
res["deltas_n"] = len(cl)
if len(cl) == 6:
    expx = [226.5, 296, 378, 453, 525, 793.5]
    res["deltas_dc"] = [round((cl[i][0] + cl[i][1]) / 2 + 380 - RX(expx[i]), 1) for i in range(6)]
    res["deltas_yd"] = [round(cl[0][2] + y0w - RY(316), 1), round(cl[0][3] + y0w - RY(327), 1)]

# 15. cyan panel
cyan = (B - R > 6) & (Gc > 230) & (B > 235) & (R > 200)
got = bbox(cyan[755:1095, 100:1890], 100, 755)
check("panel_fill", got, [RX(68), RY(352), RX(889), RY(500)])

# 16. line1 segments
got = bbox(dk[int(RY(364)):int(RY(384)), 110:480], 110, int(RY(364)))
check("line1a", got, [RX(80), RY(366), RX(146), RY(382)])
res["line1a_w"] = got[2] - got[0] if got else None
got = bbox(dk[int(RY(364)):int(RY(384)), 480:1900], 480, int(RY(364)))
check("line1b", got, [RX(187), RY(366), RX(825), RY(382)])
res["line1b_w"] = got[2] - got[0] if got else None
res["line1b_w_exp"] = RX(825) - RX(187)

# 17. problems
pred = (R - Gc > 55) & (R - B > 55) & (R > 100)
got = bbox(pred[int(RY(387)):int(RY(404)), 110:600], 110, int(RY(387)))
check("problems", got, [RX(80), RY(389.5), RX(155), RY(401.5)])
res["problems_w"] = got[2] - got[0] if got else None
res["problems_w_exp"] = RX(155) - RX(80)

# 18. bullets
got = bbox(dk[int(RY(409)):int(RY(428)), 110:1900], 110, int(RY(409)))
check("b1a", got, [RX(98), RY(410.5), RX(887), RY(426.5)])
res["b1a_w"] = got[2] - got[0] if got else None
res["b1a_w_exp"] = RX(887) - RX(98)
got = bbox(dk[int(RY(431)):int(RY(450)), 110:1000], 110, int(RY(431)))
check("b1b", got, [RX(98), RY(432.5), RX(336), RY(448.5)])
res["b1b_w"] = got[2] - got[0] if got else None
res["b1b_w_exp"] = RX(336) - RX(98)
got = bbox(dk[int(RY(453)):int(RY(471)), 110:1900], 110, int(RY(453)))
check("b2", got, [RX(97), RY(454.5), RX(879), RY(470)])
res["b2_w"] = got[2] - got[0] if got else None
res["b2_w_exp"] = RX(879) - RX(97)
got = bbox(dk[int(RY(474)):int(RY(493)), 110:1700], 110, int(RY(474)))
check("b3", got, [RX(97), RY(475.5), RX(743), RY(491.5)])
res["b3_w"] = got[2] - got[0] if got else None
res["b3_w_exp"] = RX(743) - RX(97)

# 19. labels (windows stop at x 470 — the lanes start ~x 349/352)
gm = (abs(R - Gc) < 20) & (abs(Gc - B) < 20) & (A.sum(axis=2) < 480)
got = bbox(gm[int(RY(112)):int(RY(128)), 130:330], 130, int(RY(112)))
check("lab1_line1", got, [RX(79), RY(114.5), RX(159), RY(126)])
got = bbox(gm[int(RY(128)):int(RY(142)), 130:330], 130, int(RY(128)))
check("lab1_line2", got, [RX(79), RY(129.5), RX(148), RY(140)])
got = bbox(gm[int(RY(142)):int(RY(160)), 130:330], 130, int(RY(142)))
check("lab1_line3", got, [RX(79), RY(145.5), RX(137), RY(157.5)])
got = bbox(blum[int(RY(190)):int(RY(206)), 130:330], 130, int(RY(190)))
check("lab2_line1", got, [RX(78), RY(193), RX(131), RY(202)])
got = bbox(blum[int(RY(206)):int(RY(226)), 130:330], 130, int(RY(206)))
check("lab2_line2", got, [RX(78), RY(207.5), RX(158), RY(220)])
got = bbox(pred[int(RY(261)):int(RY(277)), 130:330], 130, int(RY(261)))
check("lab3_line1", got, [RX(76), RY(263.5), RX(157), RY(275.5)])
got = bbox(pred[int(RY(278)):int(RY(297)), 130:330], 130, int(RY(278)))
check("lab3_line2", got, [RX(79), RY(279.5), RX(112), RY(289)])

print(json.dumps(res, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/selfcheck_attempt_2_output.txt", "w") as f:
    f.write(json.dumps(res, indent=1, default=str))
