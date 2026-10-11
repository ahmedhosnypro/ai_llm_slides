#!/usr/bin/env python3
"""selfcheck attempt 1 (v2, fixed harness) — closed-loop PIL verification of the
150dpi render against unique_slides/slide_029.jpg (frame px * 150/72 = render px)."""
from PIL import Image
import numpy as np
import sys

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
R = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide029/render_2.png").convert("RGB"), dtype=np.int16)
F = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)
SC = 150 / 72.0
ok = True

def rp(x):
    return int(round(x * SC))

def bbox_img(img, x0, y0, x1, y1, pred):
    reg = img[y0:y1, x0:x1]
    m = pred(reg)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max()))

def near(a, b, tol):
    return a is not None and all(abs(x - y) <= tol for x, y in zip(a, b))

def check(name, cond, detail):
    global ok
    if cond:
        print("ok  :", name, detail)
    else:
        ok = False
        print("FAIL:", name, detail)

darkp = lambda reg: reg.sum(axis=2) < 330
redp = lambda reg: (reg[:, :, 0] > 130) & (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] - reg[:, :, 2] > 60)
bluep = lambda reg: (reg[:, :, 2] > 120) & (reg[:, :, 2] - reg[:, :, 0] > 50) & (reg[:, :, 2] - reg[:, :, 1] > 40)
magp = lambda reg: (reg[:, :, 0] > 120) & (reg[:, :, 0] < 225) & (reg[:, :, 1] < 150) & (reg[:, :, 2] > 130) & (reg[:, :, 2] - reg[:, :, 1] > 35)
yel = lambda reg: (reg[:, :, 0] > 215) & (reg[:, :, 1] > 205) & (reg[:, :, 2] < 190) & (reg[:, :, 0] - reg[:, :, 2] > 40)

# 1. TITLE L1 (clean region below the panel border, left of the badge numeral)
rb = bbox_img(R, rp(110), rp(50), rp(855), rp(79), darkp)
check("title L1 ink", near(rb, (rp(163), rp(58), rp(770), rp(76)), 22), f"{rb} vs {(rp(163), rp(58), rp(770), rp(76))}")
hb = bbox_img(R, rp(110), rp(48), rp(855), rp(80), yel)
check("title highlight", near(hb, (rp(411), rp(53), rp(773), rp(78)), 28), f"{hb} vs {(rp(411), rp(53), rp(773), rp(78))}")

# 2. SUBTITLE (clean region below title descenders, left of badge)
sb = bbox_img(R, rp(95), rp(78), rp(850), rp(104), darkp)
check("subtitle ink", near(sb, (rp(108), rp(79), rp(826), rp(101)), 30), f"{sb} vs {(rp(108), rp(79), rp(826), rp(101))}")
reg = R[rp(80):rp(103), rp(95):rp(850)]
rcols = np.nonzero(((reg[:, :, 0] > 110) & (reg[:, :, 0] - reg[:, :, 1] > 55) & (reg[:, :, 0] - reg[:, :, 2] > 45)).sum(axis=0) > 0)[0]
segs = []
if len(rcols):
    s = p = rcols[0]
    for c in rcols[1:]:
        if c - p > rp(8):
            segs.append((s + rp(95), p + rp(95)))
            s = c
        p = c
    segs.append((s + rp(95), p + rp(95)))
check("subtitle red x-runs n=4", len(segs) == 4, f"{segs}")

# 3. CALLOUTS
cyanfill = lambda reg: (reg[:, :, 2] > 230) & (reg[:, :, 1] > 230) & (reg[:, :, 2] - reg[:, :, 0] > 8) & (reg[:, :, 1] - reg[:, :, 0] > 8)
c1 = bbox_img(R, rp(290), rp(130), rp(510), rp(195), cyanfill)
check("callout1 fill", near(c1, (rp(315), rp(140), rp(490), rp(184)), 20), f"{c1}")
c2 = bbox_img(R, rp(610), rp(130), rp(870), rp(195), cyanfill)
check("callout2 fill", near(c2, (rp(634), rp(145), rp(846), rp(188)), 20), f"{c2}")
t1 = bbox_img(R, rp(316), rp(142), rp(489), rp(183), lambda reg: darkp(reg) | magp(reg))
check("callout1 text inside fill", t1 is not None and c1 is not None and t1[0] >= c1[0] - 4 and t1[1] >= c1[1] - 4 and t1[2] <= c1[2] + 4 and t1[3] <= c1[3] + 4, f"{t1} in {c1}")
t2 = bbox_img(R, rp(636), rp(147), rp(845), rp(186), lambda reg: darkp(reg) | magp(reg))
check("callout2 text inside fill", t2 is not None and c2 is not None and t2[0] >= c2[0] - 4 and t2[1] >= c2[1] - 4 and t2[2] <= c2[2] + 4 and t2[3] <= c2[3] + 4, f"{t2} in {c2}")
r1 = bbox_img(R, rp(330), rp(146), rp(470), rp(162), redp)
check("c1 KEYS red noun", near(r1, (rp(384), rp(149), rp(420), rp(159)), 24), f"{r1}")
r2 = bbox_img(R, rp(650), rp(151), rp(830), rp(166), redp)
check("c2 VALUES red noun", near(r2, (rp(741), rp(154), rp(794), rp(163)), 24), f"{r2}")

# 4. TAN LABEL BOXES (sample fill corners, text-free)
def avgc(x0, y0, x1, y1):
    return tuple(int(round(v)) for v in R[rp(y0):rp(y1), rp(x0):rp(x1)].reshape(-1, 3).mean(axis=0))
kf = avgc(66, 208, 78, 213)
vf = avgc(820, 196, 830, 202)
check("KEYs box fill tan", 195 < kf[0] < 250 and 165 < kf[1] < 225 and 110 < kf[2] < 190, f"{kf}")
check("Values box fill tan", 195 < vf[0] < 250 and 165 < vf[1] < 225 and 110 < vf[2] < 190, f"{vf}")
tanp = lambda reg: (reg[:, :, 0] > 200) & (reg[:, :, 0] < 252) & (reg[:, :, 1] > 170) & (reg[:, :, 1] < 228) & (reg[:, :, 2] > 110) & (reg[:, :, 2] < 200)
k = bbox_img(R, rp(56), rp(184), rp(146), rp(220), tanp)
check("KEYs box bbox", near(k, (rp(64), rp(190), rp(134), rp(214)), 16), f"{k}")
v = bbox_img(R, rp(752), rp(191), rp(844), rp(224), tanp)
check("Values box bbox", near(v, (rp(762), rp(193), rp(835), rp(218)), 16), f"{v}")

# 5. BADGES (regions clear of the flow row y328 => render 683)
for name, (cx, cy) in {"K": (163, 342), "V": (747.5, 342.5), "Q": (258.5, 439)}.items():
    bb = bbox_img(R, rp(cx - 15), rp(cy - 15), rp(cx + 15), rp(cy + 15), redp)
    check(f"badge {name}", near(bb, (rp(cx - 12), rp(cy - 12), rp(cx + 12), rp(cy + 12)), 12), f"{bb}")
    wl = bbox_img(R, rp(cx - 9), rp(cy - 9), rp(cx + 9), rp(cy + 9), lambda reg: (reg[:, :, 0] > 235) & (reg[:, :, 1] > 225) & (reg[:, :, 2] > 225))
    check(f"badge {name} white letter", wl is not None, f"{wl}")

# 6. QUERY BOX + text
of = lambda reg: (reg[:, :, 0] > 228) & (reg[:, :, 0] - reg[:, :, 2] > 42) & (reg[:, :, 1] - reg[:, :, 2] > 22) & (reg[:, :, 1] < 238)
q = bbox_img(R, rp(102), rp(413), rp(245), rp(466), of)
check("query box fill", near(q, (rp(111), rp(420), rp(240), rp(460)), 14), f"{q}")
qt = bbox_img(R, rp(112), rp(421), rp(239), rp(459), lambda reg: (reg[:, :, 0] > 100) & (reg[:, :, 0] - reg[:, :, 1] > 55) & (reg[:, :, 0] - reg[:, :, 2] > 45))
check("query text inside box", qt is not None and qt[0] >= rp(111) - 2 and qt[2] <= rp(240) + 2, f"{qt}")
reg = R[rp(421):rp(459), rp(112):rp(239)]
m = (reg[:, :, 0] > 100) & (reg[:, :, 0] - reg[:, :, 1] > 55) & (reg[:, :, 0] - reg[:, :, 2] > 45)
rows = m.sum(axis=1)
bands = []
inb = False
for i, n in enumerate(rows):
    if n > 2 and not inb:
        inb, b0 = True, i
    elif n <= 2 and inb:
        inb = False
        if i - b0 > 3:
            bands.append((rp(421) + b0, rp(421) + i - 1))
if inb:
    bands.append((rp(421) + b0, rp(421) + len(rows) - 1))
check("query text 2 bands", len(bands) == 2, f"{bands}")

# 7. RESULT BOX
wf = lambda reg: (reg[:, :, 0] > 240) & (reg[:, :, 1] > 240) & (reg[:, :, 2] > 240)
w = bbox_img(R, rp(548), rp(428), rp(836), rp(508), wf)
check("result box white", near(w, (rp(560), rp(437), rp(824), rp(499)), 16), f"{w}")
bl = bbox_img(R, rp(550), rp(428), rp(835), rp(508), bluep)
check("result box blue ink", bl is not None, f"{bl}")
reg = R[rp(436):rp(500), rp(562):rp(822)]
rows = (darkp(reg) | bluep(reg) | redp(reg)).sum(axis=1)
bands = []
inb = False
for i, n in enumerate(rows):
    if n > 3 and not inb:
        inb, b0 = True, i
    elif n <= 3 and inb:
        inb = False
        if i - b0 > 4:
            bands.append((rp(436) + b0, rp(436) + i - 1))
if inb:
    bands.append((rp(436) + b0, rp(436) + len(rows) - 1))
check("result text 3 line bands", len(bands) == 3, f"{bands}")
rr = bbox_img(R, rp(565), rp(440), rp(820), rp(458), redp)
check("result L1 red nouns (Values..Keys)", rr is not None and rr[0] <= rp(650) and rr[2] >= rp(740), f"{rr}")
rr3 = bbox_img(R, rp(565), rp(478), rp(820), rp(496), redp)
check("result L3 red Query", rr3 is not None and rr3[0] >= rp(700), f"{rr3}")

# 8. CURVES / ARROWS
lc = bbox_img(R, rp(96), rp(400), rp(180), rp(475), redp)
check("left red curve present", lc is not None, f"{lc}")
reg = R[rp(397):rp(413), rp(790):rp(815)]
grn = ((reg[:, :, 1] > 100) & (reg[:, :, 1] - reg[:, :, 0] > 30) & (reg[:, :, 1] - reg[:, :, 2] > 20)) | redp(reg)
check("right curve/head absent", int(grn.sum()) < 10, f"ink px={int(grn.sum())}")
reg = R[rp(404):rp(470), rp(272):rp(500)]
check("thin x298 arrow absent", int(redp(reg).sum()) < 10, f"ink px={int(redp(reg).sum())}")
ca = bbox_img(R, rp(258), rp(505), rp(295), rp(532), redp)
check("chunky diagonal present", ca is not None and near(ca, (rp(262), rp(508), rp(290), rp(528)), 12), f"{ca}")

# 8b. DOT-FEED ARROWHEADS below the four Dot-Product dots (attempt-2 fix)
for name, (ax, ay, aw, ah) in {
    "A1": (329.5, 255, 8, 10), "A2": (308, 297, 9.5, 10),
    "A3": (290.5, 337, 7.5, 10), "A4": (276.5, 381, 8, 8),
}.items():
    ab = bbox_img(R, rp(ax - 5), rp(ay - 3), rp(ax + aw + 5), rp(ay + ah + 3), redp)
    check(f"dot-feed arrowhead {name}", ab is not None, f"{ab} (drawn at frame {ax},{ay} {aw}x{ah})")

# 9. INHERITED fills (component => compare to certified parent render, not the JPEG)
P = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide026/render_1.png").convert("RGB"), dtype=np.int16)
for name, (x0, y0, x1, y1) in {
    "sigma fill": (560, 200, 600, 213),
    "softmax fill": (465, 250, 480, 270),
    "left stack fill": (80, 260, 120, 280),
    "strip fill": (200, 480, 240, 500),
    "dotproduct fill": (270, 220, 300, 240),
}.items():
    a = np.asarray(R[rp(y0):rp(y1), rp(x0):rp(x1)].reshape(-1, 3).mean(axis=0), dtype=int)
    b = np.asarray(P[rp(y0):rp(y1), rp(x0):rp(x1)].reshape(-1, 3).mean(axis=0), dtype=int)
    d = int(np.abs(a - b).max())
    check(f"inherited {name} == certified parent render", d <= 14, f"render {a} vs parent {b} (maxch {d})")

# 10. HOUSE CONTAINMENT: no content ink in the white margin beyond the border's
# anti-aliased edge (margin is ~84px wide; border stroke + AA ends ~x95/x1907/y102)
band = 6
top = R[: 96 - band, :, :]
bot = R[1118 + band:, :, :]
lef = R[:, : 89 - band, :]
rig = R[:, 1912 + band:, :]
def ink_px(reg):
    dark = reg.sum(axis=2) < 700
    redish = (reg[:, :, 0] > 150) & (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] - reg[:, :, 2] > 60)
    return int((dark & ~redish).sum())
tot = ink_px(top) + ink_px(bot) + ink_px(lef) + ink_px(rig)
check("no content ink in white margin beyond border AA", tot < 50, f"px={tot}")

print("\nSELF-CHECK", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
