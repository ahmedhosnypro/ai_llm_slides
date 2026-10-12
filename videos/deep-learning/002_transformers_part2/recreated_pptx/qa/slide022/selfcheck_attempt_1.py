#!/usr/bin/env python3
"""selfcheck_attempt_1 — closed-loop PIL ink check for slide 022 (render vs frame-measured).
Render: 150dpi PNG of a 13.333x7.5in slide (2001x1125). 1 render px = 1/200 in; 1 slide pt
= 200/72 px. Frame px -> slide pt: X=(fx-17.72)/0.961231, Y=fy/0.955556. Tol ~5 render px."""
import json
from PIL import Image
import numpy as np

REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/render_1.png"
K = 150.0 / 72.0  # render px per slide pt (150 dpi)
AX, SX, SY = 17.72, 0.961231, 0.955556
def RX(fx): return (fx - AX) / SX * K
def RY(fy): return fy / SY * K

img = Image.open(REND).convert("RGB")
A = np.asarray(img).astype(int)
R, Gc, B = A[..., 0], A[..., 1], A[..., 2]
res = {}

def bbox(mask, x0, y0):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(mask.sum())]

def check(name, got, exp, tol=5.0):
    if got is None:
        res[name] = "FAIL: no ink"
        return
    d = [abs(got[i] - exp[i]) for i in range(4)]
    ok = max(d) <= tol
    res[name] = f"{'OK ' if ok else 'FAIL'} max|d|={max(d):.1f} got={got[:4]} exp={[round(e,1) for e in exp[:4]]}"

# 1. title
redm = (R > 100) & (R - Gc > 35) & (R - B > 30)
got = bbox(redm[120:250, 800:2050], 800, 120)
check("title", got, [RX(339), RY(59), RX(689), RY(78)])

# 2. subtitle
blum = (B - R > 45) & (B > 90)
got = bbox(blum[220:320, 850:2050], 850, 220)
check("subtitle", got, [RX(322), RY(85.5), RX(718), RY(105)])

# 3. diagram panel border (dark blue-violet)
db = (B - R > 25) & (A.sum(axis=2) < 500)
got = bbox(db[290:980, 100:2520], 100, 290)
check("dbox", got, [RX(64), RY(111), RX(893), RY(342)])

# 4. row1 lane: sage fill band
sage = (abs(R - Gc) < 12) & (abs(Gc - B) < 12) & (A.sum(axis=2) > 560) & (A.sum(axis=2) < 720)
got = bbox(sage[300:470, 400:2480], 400, 300)
check("lane1_fill", got, [RX(180), RY(121), RX(874), RY(154)])

# 5. row1 boxes: cream fill runs in band
cream = (R - B > 10) & (R > 228) & (Gc > 220)
sub = cream[int(RY(128)):int(RY(146)), 400:2480]
colc = sub.sum(axis=0)
runs, s = [], None
for i, v in enumerate(colc >= 6):
    if v and s is None: s = i
    elif not v and s is not None:
        if i - s > 30: runs.append((400 + s, 400 + i - 1))
        s = None
res["r1_boxes_count"] = len(runs)
if runs:
    res["r1_boxes_first"] = runs[0]
    res["r1_boxes_last"] = runs[-1]
    exp_first = (RX(182), RX(241)); exp_last = (RX(813), RX(877))
    res["r1_boxes_first_d"] = [round(runs[0][0] - exp_first[0], 1), round(runs[0][1] - exp_first[1], 1)]
    res["r1_boxes_last_d"] = [round(runs[-1][0] - exp_last[0], 1), round(runs[-1][1] - exp_last[1], 1)]

# 6. row1 box text band (dark maroon)
r1t = (R - Gc > 45) & (R < 190) & (R > 80)
got = bbox(r1t[int(RY(129)):int(RY(146)), 450:2470], 450, int(RY(129)))
check("r1_text_band", got, [RX(193), RY(131.5), RX(869), RY(142)])

# 7. row2 lane lavender band
lav = (B - R > 35) & (R > 170) & (R < 225) & (B > 230)
got = bbox(lav[int(RY(188)):int(RY(224)), 400:2480], 400, int(RY(188)))
check("lane2_fill", got, [RX(178), RY(189), RX(872), RY(223)])

# 8. row2 box borders (medium blue) row band
r2b = (B - R > 40) & (R < 170) & (B > 150)
sub = r2b[int(RY(196)):int(RY(216)), 400:2480]
colc = sub.sum(axis=0)
runs, s = [], None
for i, v in enumerate(colc >= 8):
    if v and s is None: s = i
    elif not v and s is not None:
        if i - s >= 1: runs.append((400 + s, 400 + i - 1))
        s = None
res["r2_vstrokes_n"] = len(runs)
if runs:
    res["r2_vstrokes_first_last"] = [runs[0], runs[-1]]
    res["r2_vstroke_d"] = [round(runs[0][0] - RX(179), 1), round(runs[-1][1] - RX(873), 1)]
got = bbox(r2b[int(RY(193)):int(RY(219)), 400:2480], 400, int(RY(193)))
check("r2_borders_band", got, [RX(179), RY(194.5), RX(873), RY(217)])

# 9. row2 text band
r2t = (B - R > 70) & (R < 110)
got = bbox(r2t[int(RY(197)):int(RY(214)), 450:2470], 450, int(RY(197)))
check("r2_text_band", got, [RX(191), RY(198.5), RX(866), RY(212)])

# 10. row3 lane pink band
pink = (R - B > 4) & (R > 235) & (Gc > 215) & (Gc < 245)
got = bbox(pink[int(RY(264)):int(RY(299)), 400:2480], 400, int(RY(264)))
check("lane3_fill", got, [RX(178), RY(265), RX(871), RY(299)])

# 11. row3 box fill + text
r3t = (R - Gc > 55) & (R < 180)
got = bbox(r3t[int(RY(277)):int(RY(293)), 450:2470], 450, int(RY(277)))
check("r3_text_band", got, [RX(200), RY(278.5), RX(864), RY(290)])

# 12. dots row1: gray clusters
grayd = (abs(R - Gc) < 18) & (abs(Gc - B) < 18) & (A.sum(axis=2) < 590) & (A.sum(axis=2) > 330)
sub = grayd[int(RY(132)):int(RY(145)), int(RX(615)):int(RX(725))]
colc = sub.sum(axis=0)
runs, s = [], None
for i, v in enumerate(colc >= 2):
    if v and s is None: s = i
    elif not v and s is not None: runs.append((int(RX(615)) + s, int(RX(615)) + i - 1)); s = None
res["dots1_n"] = len(runs)
if len(runs) == 5:
    exp = [RX(637), RX(655), RX(673), RX(691.5), RX(706.5)]
    got_c = [round((a + b) / 2, 1) for a, b in runs]
    res["dots1_d"] = [round(g - e, 1) for g, e in zip(got_c, exp)]

# 13. arrows: orange clusters
orange = (R > 150) & (R - B > 70) & (Gc > 55) & (Gc < 200) & (B < 140)
sub = orange[int(RY(292)):int(RY(307)), 400:2480]
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
    res["arrows_d"] = [round(cl[i][0] - RX(expx[i][0]), 1) for i in range(6)]
    res["arrows_dy"] = round(cl[0][2] + int(RY(292)) - RY(294), 1)

# 14. deltas: dark red clusters below
delt = (R - B > 55) & (R > 110) & (R < 200) & (Gc < 110)
sub = delt[int(RY(313)):int(RY(331)), 400:2480]
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
    res["deltas_dc"] = [round((cl[i][0] + cl[i][1]) / 2 - RX(expx[i]), 1) for i in range(6)]
    res["deltas_y"] = [round(cl[0][2] + int(RY(313)) - RY(316), 1), round(cl[0][3] + int(RY(313)) - RY(327), 1)]

# 15. cyan panel
cyan = (B - R > 6) & (Gc > 230) & (B > 235) & (R > 200)
got = bbox(cyan[int(RY(350)):int(RY(500)), 100:2520], 100, int(RY(350)))
check("panel_fill", got, [RX(68), RY(352), RX(889), RY(500)])

# 16. line1: two segments
dk = (A.sum(axis=2) < 430)
got = bbox(dk[int(RY(365)):int(RY(384)), 180:600], 180, int(RY(365)))
check("line1a", got, [RX(80), RY(366), RX(146), RY(382)])
got = bbox(dk[int(RY(365)):int(RY(384)), 480:2330], 480, int(RY(365)))
check("line1b", got, [RX(187), RY(366), RX(825), RY(382)])

# 17. problems
pred = (R - Gc > 55) & (R - B > 55) & (R > 100)
got = bbox(pred[int(RY(388)):int(RY(404)), 180:600], 180, int(RY(388)))
check("problems", got, [RX(80), RY(389.5), RX(155), RY(401.5)])

# 18. bullets
got = bbox(dk[int(RY(409)):int(RY(428)), 250:2480], 250, int(RY(409)))
check("b1a", got, [RX(98), RY(410.5), RX(887), RY(426.5)])
got = bbox(dk[int(RY(431)):int(RY(450)), 250:1000], 250, int(RY(431)))
check("b1b", got, [RX(98), RY(432.5), RX(336), RY(448.5)])
got = bbox(dk[int(RY(453)):int(RY(471)), 250:2480], 250, int(RY(453)))
check("b2", got, [RX(97), RY(454.5), RX(879), RY(470)])
got = bbox(dk[int(RY(474)):int(RY(493)), 250:2100], 250, int(RY(474)))
check("b3", got, [RX(97), RY(475.5), RX(743), RY(491.5)])

# 19. labels
gm = (abs(R - Gc) < 20) & (abs(Gc - B) < 20) & (A.sum(axis=2) < 480)
got = bbox(gm[int(RY(112)):int(RY(142)), 180:480], 180, int(RY(112)))
check("lab1_line1", got, [RX(79), RY(114.5), RX(159), RY(126)])
got = bbox(gm[int(RY(127)):int(RY(142)), 180:480], 180, int(RY(127)))
check("lab1_line2", got, [RX(79), RY(129.5), RX(148), RY(140)])
got = bbox(gm[int(RY(142)):int(RY(160)), 180:480], 180, int(RY(142)))
check("lab1_line3", got, [RX(79), RY(145.5), RX(137), RY(157.5)])
got = bbox(blum[int(RY(190)):int(RY(206)), 180:480], 180, int(RY(190)))
check("lab2_line1", got, [RX(78), RY(193), RX(131), RY(202)])
got = bbox(blum[int(RY(206)):int(RY(224)), 180:480], 180, int(RY(206)))
check("lab2_line2", got, [RX(78), RY(207.5), RX(158), RY(220)])
got = bbox(pred[int(RY(261)):int(RY(277)), 180:480], 180, int(RY(261)))
check("lab3_line1", got, [RX(76), RY(263.5), RX(157), RY(275.5)])
got = bbox(pred[int(RY(278)):int(RY(296)), 180:480], 180, int(RY(278)))
check("lab3_line2", got, [RX(79), RY(279.5), RX(112), RY(289)])

# 20. containment: no content ink outside the house panel (x 42..919, y 45..540 slide pt)
out_in = A[int(RY(45)) - 6:int(RY(540)) + 6, int(RX(42)) - 6:int(RX(919)) + 6]
res["render_size"] = list(A.shape[:2])

print(json.dumps(res, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/selfcheck_attempt_1_output.txt", "w") as f:
    f.write(json.dumps(res, indent=1, default=str))
